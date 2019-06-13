import pdb
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
service_key = os.path.join(root_dir, 'service-key.json')

cred = credentials.Certificate(service_key)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://anconia-4008c.firebaseio.com'
})

db = firestore.client()
nodes_ref = db.collection('nodes')
transactions_ref = db.collection('transactions')


def to_peers_string(peers):
    return [host+':'+str(port)for host, port in list(peers)]


def set_nodes(peers):
    peers = to_peers_string(peers)
    node_ref = nodes_ref.document()
    node_ref.set({
        'created_at': firestore.SERVER_TIMESTAMP,
        'peers': peers
    })
    return node_ref.get().id


def update_nodes(document_id, peers):
    peers = to_peers_string(peers)
    node_ref = nodes_ref.document(document_id)
    node_ref.update({
        'peers': peers
    })


@firestore.transactional
def update_children(transaction, txn_ref, child):
    snapshot = txn_ref.get(transaction=transaction)
    children_snapshot = snapshot.get('children')
    children_snapshot.append(child)

    transaction.update(txn_ref, {
        'children': children_snapshot
    })


def set_transaction(txn_msg, conflicts, is_preferred):
    txn_ref = transactions_ref.document(txn_msg.hash)
    txn_ref.set({
        'children': [child for child in txn_msg.children],
        'conflicts': conflicts,
        'is_preferred': is_preferred,
        'chit': txn_msg.chit,
    }, merge=True)

    for parent in txn_msg.parents:
        db_transaction = db.transaction()
        update_children(db_transaction, txn_ref, parent)