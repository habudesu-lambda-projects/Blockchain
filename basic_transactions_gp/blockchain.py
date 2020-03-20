import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            "index": len(self.chain) + 1,
            "proof": proof,
            "timestamp": time(),
            "previous_hash": previous_hash,
            "transactions": self.current_transactions,
        }

        # Reset the current list of transactions
        self.current_transactions = []

        # Append the chain to the block
        self.chain.append(block)
        
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        block_string = json.dumps(block).encode()


        # TODO: Hash this string using sha256
        hashed_block = hashlib.sha256(block_string).hexdigest()

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hashed_block

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # TODO
        block_string = f'{block_string}{proof}'.encode()
        hashed_block = hashlib.sha256(block_string).hexdigest()

        return hashed_block[:6] == "000000"

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "index": len(blockchain.chain) + 1,
            "timestamp": time()
        }

        blockchain.current_transactions.append(transaction)

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()

    required = ['proof', 'id']

    if not all(k in data for k in required):
        response = {'message': "missing values"}
        return jsonify(response), 400

    block = blockchain.last_block
    block_string = json.dumps(block, sort_keys=True)
    proof = data['proof']
    id = data['id']

    if blockchain.valid_proof(block_string, proof):
        new_block = blockchain.new_block(proof, blockchain.hash(block))

        blockchain.new_transaction("0", id, 1)

        response = {
            "message": "New Block Forged",
            "new_block": new_block
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Invalid Proof"
        }
        return jsonify(response), 400

    


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "chain_length": len(blockchain.chain)
    }
    return jsonify(response), 200, {"Access-Control-Allow-Origin": "*"}

@app.route('/last_block', methods=['GET'])
def get_last_block():
    res = {
        "last_block": blockchain.last_block
    }
    return jsonify(res), 200

@app.route('/transactions/new', methods=['POST'])
def add_transaction():
    data = request.get_json()
    required = ['sender', 'recipient', 'amount']

    if not all(k in data for k in required):
        response = {'message': "missing values"}
        return jsonify(response), 400
    else:
        response = {'messaage': blockchain.last_block() + 1}
        return jsonify(response), 201

# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
