import sys
import time
import random
import params
from message_client import MessageClient
from threading import Thread


def _create_random_transactions(message_client):
    while True:
        recipient_addr = random.choice(
            message_client.state.get_all_addresses())
        msg = message_client.generate_transaction(recipient_addr, 100)
        message_client.broadcast_message(msg)
        time.sleep(params.RANDOM_TX_GENERATION)
        message_client.broadcast_message(msg)


def create_random_transactions(message_client):
    thread = Thread(target=_create_random_transactions, args=(message_client,))
    thread.setDaemon(True)
    thread.start()
