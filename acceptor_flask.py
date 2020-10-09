from flask import Flask, request
from paxos import *

app = Flask(__name__)

acceptor:Acceptor = Acceptor()


# localhost:PORT/?pid=0&qsize=3&val=10
@app.route('/')
def index():
    return "dont look at this"

### Phase 1 #########################################################
@app.route('/receive_prepare')
def propose():
    '''
    When the proposer sends a prepare, it will send it to this endpoint.
    '''
    uid = int(request.args["uid"])
    proposal_id = int(request.args["proposal_id"])

    acceptor.promise(uid, proposal_id)

### Phase 2 #########################################################
@app.route('/receive_accept')
def receive_accept():
    '''
    When the proposer sends an accept, it will send to this endpoint.
    '''
    uid = int(request.args["uid"])
    proposal_id = int(request.args["proposal_id"])
    value = int(request.args["value"])

    acceptor.receive_accept(uid, proposal_id, value)
