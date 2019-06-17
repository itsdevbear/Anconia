import sys
import socket
import struct
import binascii
from threading import Thread
import logging
from concurrent.futures import ThreadPoolExecutor
import socketserver
import traceback
from japronto import Application
from proto import messages_pb2
from message_client import MessageClient
from common import exponential_backoff, simulate_network_latency


class MessageServer:
    def __init__(self, message_client, host=None, port=None):
        self.message_client = message_client
        self.sock = None
        self.logger = logging.getLogger('main')
        self.peers = set([])
        self.address = host
        self.port = port
        self.listener_thread = None
        # self.thread_executor = ThreadPoolExecutor(max_workers=8)

    def bind_to_open_port(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect_to = ('', 0)
        if self.address and self.port:
            connect_to = (self.address, self.port)

        sock.bind(connect_to)
        sock.listen(16)
        address, port = sock.getsockname()

        self.sock = sock
        self.address = address
        self.port = port
        return address, port

    def start(self):
        app = Application()
        app.router.add_route('/', self.handle_message, methods=['POST'])
        app.run(host=self.address, port=self.port)
        return self.address, self.port

        # try:
        #     address, port = self.bind_to_open_port()
        #     self.listen_to_messages(self.sock)
        # except (KeyboardInterrupt, SystemExit):
        #     self.thread_executor.shutdown(wait=False)
        #     sys.exit()

    def start_connection_thread(self, conn):
        try:
            # raw_msg = exponential_backoff(
            #     self.logger, conn.recv,
            #     (1024,), timeout=0.01, max_retry=5)
            raw_msg = conn.recv(1024)
            if raw_msg:
                response = self.handle_message(raw_msg)
                if response:
                    # exponential_backoff(
                    #     self.logger, conn.sendall,
                    #     (response,), timeout=0.01, max_retry=5)
                    conn.sendall(response)
                    simulate_network_latency()
            conn.close()
        except socket.error:
            # self.logger.error(e)
            # traceback.print_exc()
            pass

    def listen_to_messages(self, sock):
        address, port = sock.getsockname()
        self.logger.info(f'Listening to messages on {address}:{port}')
        while True:
            conn, _ = sock.accept()
            self.thread_executor.submit(self.start_connection_thread, conn)
        sock.close()

    def handle_message(self, request):
        raw_msg = request.body
        try:
            common_msg = messages_pb2.CommonMessage()
            common_msg.ParseFromString(raw_msg)

            message_handlers = {
                messages_pb2.JOIN_MESSAGE: ('Join', 'join', self.add_peer),
                messages_pb2.TRANSACTION_MESSAGE: ('Transaction', 'transaction', self.handle_transaction),
                messages_pb2.NODE_QUERY_MESSAGE: (
                    'NodeQuery', 'node_query', self.handle_node_query),
                messages_pb2.REQUEST_SYNC_GRAPH_MESSAGE: (
                    'RequestSyncGraph', 'request_sync_graph', self.handle_sync_graph),
            }

            handler = message_handlers.get(common_msg.message_type)
            if not handler:
                raise ValueError(
                    f"There is no message type {common_msg.message_type} or handler not created yet")

            message_classname, attr_name, handler_function = handler
            sub_msg = getattr(messages_pb2, message_classname)()
            sub_msg.CopyFrom(getattr(common_msg, attr_name))
            return handler_function(request, sub_msg)
        except Exception:
            traceback.print_exc()
            return request.Response(code=500)

    def handle_transaction(self, request, txn_msg):
        self.message_client.receive_transaction(txn_msg)
        return request.Response(body=b'')

    def handle_node_query(self, request, query_msg):
        """
        If we have not encountered the transaction yet,
        Respond the query with the query's is_strongly_preferred field
        And store the transaction into our own DAG.

        If encountered before, respond with own preference.
        """
        txn_hash = query_msg.txn_hash
        is_strongly_preferred = False

        with self.message_client.lock:
            if not self.message_client.dag.transactions.get(txn_hash):
                # if transaction doesn't exist locally,
                # request from the querying node to patch the transaction
                # make own decision from received transaction
                # txn = self.message_client.request_transaction(
                #     txn_hash, query_msg.from_address, query_msg.from_port)
                # if txn:
                #     self.message_client.receive_transaction(txn)
                #     is_strongly_preferred = self.message_client.dag.is_strongly_preferred(
                #         txn)
                # else:
                #     is_strongly_preferred = query_msg.is_strongly_preferred
                is_strongly_preferred = query_msg.is_strongly_preferred
            else:
                txn = self.message_client.dag.transactions[txn_hash]
                is_strongly_preferred = self.message_client.dag.is_strongly_preferred(
                    txn)
                # print(
                #     f'Default: {query_msg.is_strongly_preferred}, Response: {is_strongly_preferred}')

        response_query = messages_pb2.NodeQuery()
        response_query.txn_hash = txn_hash
        response_query.is_strongly_preferred = is_strongly_preferred
        response_query.from_address = self.address
        response_query.from_port = self.port
        msg = MessageClient.create_message(
            messages_pb2.NODE_QUERY_MESSAGE, response_query)
        return request.Response(body=msg)

    def handle_sync_graph(self, request, request_sync_graph_msg):
        if request_sync_graph_msg.target_txn_hash:
            sync_msg = messages_pb2.SyncGraph()
            txn = self.message_client.dag.transactions.get(
                request_sync_graph_msg.target_txn_hash)

            if txn:
                sync_msg.transactions.append(txn)
                msg = MessageClient.create_message(
                    messages_pb2.SYNC_GRAPH_MESSAGE, sync_msg)
                return request.Response(text=msg.decode('utf-8'))
            return request.Response(body=b'')

        sync_msg = messages_pb2.SyncGraph()
        transactions = self.message_client.dag.transactions.values()
        sync_msg.transactions.extend(transactions)
        conflict_sets = self.message_client.dag.conflicts.conflicts

        for conflict_set in conflict_sets:
            conflict_msg = messages_pb2.ConflictSet()
            conflict_msg.hashes.extend(conflict_set)
            sync_msg.conflicts.append(conflict_msg)

        msg = MessageClient.create_message(
            messages_pb2.SYNC_GRAPH_MESSAGE, sync_msg
        )
        return request.Response(body=msg)

    def add_peer(self, request, join_msg):
        new_peer = (join_msg.address, join_msg.port)
        with self.message_client.lock:
            self.message_client.add_peer(new_peer)
        return request.Response(body=b'')
