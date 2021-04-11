#! python3

from Block import Block
import time

class Blockchain:

    difficulty = 4

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), '0')
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash
    

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash())

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        # Se l'hash dell'ultimo blocco che ho nella blockchain è diverso dal previous_hash del blocco che mi arriva 
        # vuol dire che il blocco non è valido
        if previous_hash != block.previous_hash: 
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)

    def add_new_transaction(self, sender, receiver, amount):
        self.unconfirmed_transactions.append({
                                "sender":sender,
                                "receiver":receiver,
                                "amount":amount,})
        return self.last_block.index + 1

    def mine(self):
        # Non ci sono transazioni da confermare
        if not self.unconfirmed_transactions: 
            return None
        last_block = self.last_block
        new_block = Block(index = last_block.index + 1, 
                        transactions = self.unconfirmed_transactions,
                        timestamp = time.time(),
                        previous_hash = last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return self.last_block