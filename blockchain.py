import hashlib
import time


class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash


class Blockchain:
    def __init__(self):
        self.chain = [self.get_genesis_block()]

    @staticmethod
    def get_genesis_block():
        return Block(0, "0", int(time.time()), "Genesis Block", "0")

    def add_block(self, new_block):
        self.chain.append(new_block)

    def get_latest_block(self):
        return self.chain[-1]

    def calculate_hash(self, index, previous_hash, timestamp, data):
        return hashlib.sha256(f'{index}{previous_hash}{timestamp}{data}'.encode('utf-8')).hexdigest()
    
    def print_blockchain(self):
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Hash: {block.hash}")
            print("----------------------------")