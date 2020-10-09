from flask import Flask, request
from paxos import *

app = Flask(__name__)

proposer:Proposer = None
acceptor_ports = []

# localhost:PORT/?pid=0&qsize=3&val=10
@app.route('/')
def index():
    pid:int = request.args.get('pid')
    qsize:int = request.args.get('qsize')
    val:int = request.args.get('val')
    print(pid, qsize, val)
    proposer = Proposer(pid, qsize, val)

    return "Created proposer: " + str(proposer.proposer_id) + ", " + str(proposer.quorum_size) + ", " + str(proposer.val)

@app.route('/propose')
def propose():
    proposer.propose()

@app.route('/receive_promise')
def receive_promise():
    proposer.receive_promise()