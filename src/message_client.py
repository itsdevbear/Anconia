import socket
import time
import threading
import logging
from proto import messages_pb2


# TO BE UPDATED PERIODICALLY
ATTR_NAMES = {
    messages_pb2.NODE_QUERY_MESSAGE: 'node_query',
    messages_pb2.JOIN_MESSAGE: 'join',
    messages_pb2.TRANSACTION_MESSAGE: 'transaction',
}


class MessageClient:
    def __init__(self, consensus_algorithm):
        self.peers = set([])
        self.color = messages_pb2.NONE_COLOR
        self.consensus_algorithm = consensus_algorithm
        self.logger = logging.getLogger('main')

    @staticmethod
    def get_sub_message(message_type, message):
        attr_name = ATTR_NAMES.get(message_type)
        if not attr_name:
            raise ValueError(
                f'Invalid message_type {message_type}, or ATTR_NAMES not updated')

        common_msg = messages_pb2.CommonMessage()
        common_msg.ParseFromString(message)
        sub_msg = getattr(common_msg, attr_name)
        return sub_msg

    @staticmethod
    def create_message(message_type, sub_msg):
        common_msg = messages_pb2.CommonMessage()
        common_msg.message_type = message_type

        attr_name = ATTR_NAMES.get(message_type)
        if not attr_name:
            raise ValueError(
                f'Invalid message_type {message_type}, or ATTR_NAMES not updated')

        getattr(common_msg, attr_name).CopyFrom(sub_msg)
        msg = common_msg.SerializeToString()
        return msg

    def run_consensus(self, txn_msg):
        self.consensus_algorithm(self, txn_msg)

    def add_peer(self, new_peer):
        addr, port = new_peer
        self.peers.add(new_peer)
        self.logger.info(f'Added new peer {addr}:{port}')

    def send_message(self, node, msg):
        addr, port = node
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.logger.debug(f'Connecting to {addr}:{port}')
            s.connect((addr, port))
            s.sendall(msg)
            data = s.recv(1024)
            return data

    def broadcast_message(self, msg):
        responses = []
        for addr, port in self.peers:
            node = (addr, port)
            self.send_message(node, msg)
        if self.peers:
            self.logger.info('Broadcasted transaction')
        else:
            self.logger.info('No peers, did not broadcast transaction')
        return responses

    def generate_transaction(self, color, amount):
        common_msg = messages_pb2.CommonMessage()
        txn_msg = messages_pb2.Transaction()
        txn_msg.color = color
        txn_msg.amount = amount
        msg = MessageClient.create_message(
            messages_pb2.TRANSACTION_MESSAGE, txn_msg)
        return msg
