#! python3

from flask import Flask, request, jsonify
from Blockchain import Blockchain
import json

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return jsonify({"length": len(chain_data),"chain": chain_data}), 200

@app.route('/mine', methods=['GET'])
def mine():
    new_block = blockchain.mine()
    if new_block == None:
        return "Not found transactions to verify", 200
    response = {
        'message' : 'Forged new block',
        'index' : new_block.index,
        'transactions' : new_block.transactions,
        'nonce' : new_block.nonce,
        'previous_hash' : new_block.previous_hash
    }
    return jsonify(response), 200

@app.route('/transaction/new', methods=['GET'])
def new_transaction():
    required = ['sender', 'receiver', 'amount']
    if not all(k in request.args for k in required):
        return 'Missing values.', 400
    sender = request.args.get('sender')
    receiver = request.args.get('receiver')
    amount = request.args.get('amount')
    index = blockchain.add_new_transaction(sender, receiver, amount)
    response = {
        'message' : f"Transaction will be added to block {index}",
        'sender' : sender,
        'receiver' : receiver,
        'amount' : amount
    }
    return jsonify(response), 200

app.run(debug=True, port=5000)