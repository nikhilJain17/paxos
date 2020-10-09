import requests
from enum import Enum

PROPOSAL_ID = 0                                     # global proposal id to be used / incremented by proposers

class Messenger():
    acceptor_endpoints = []
    proposer_endpoints = {}
    
    def set_acceptor_endpoints(self, endpoints):
        self.acceptor_endpoints = endpoints

    def set_proposer_endpoints(self, endpoints):
        self.proposer_endpoints = endpoints

    def send_prepare(self, uid, proposal_id):
        '''
        Broadcasts a Prepare message to all Acceptors
        '''
        for a in acceptor_endpoints:
            url = "http://localhost:" + a + "/receive_prepare"
            params = {"uid" : uid, "proposal_id" : proposal_id}
            requests.get(url=url, params=params)

    def send_promise(self, proposer_uid, proposal_id, previous_id, accepted_value):
        '''
        Sends a Promise message to the specified Proposer
        '''
        p = proposer_endpoints[proposer_uid]
        p += "/receive_promise"
        requests.get(url=p)

    def send_accept(self, uid, proposal_id, proposal_value):
        '''
        Broadcasts an Accept! message to all Acceptors
        '''
        for a in acceptor_endpoints:
            url = "http://localhost:" + a + "/receive_accept"
            params = {"uid" : uid, "proposal_id" : proposal_id, "proposal_value" : proposal_value}
            requests.get(url=url, params=params)

    def send_accepted(self, proposal_id, accepted_value):
        '''
        Broadcasts an Accepted message to all Learners
        '''

    def on_resolution(self, proposal_id, value):
        '''
        Called when a resolution is reached
        '''

class Proposer():    
    def __init__(self, proposer_id:int, quorum_size:int, val:int): 
        
        self.messenger:Messenger = Messenger()
        
        self.proposer_id:int = proposer_id          # id for specific proposer
        self.proposal_id:int = 0                    # id for current proposal
        self.quorum_size = quorum_size              # how many acceptors are in a quorom

        self.val = val                              # the value we are trying to send out

        self.promise_responses = 0
        self.highest_acceptedid_received = -1       # (phase 2) keep track of highest accepted id that an acceptor responds with
        self.highest_acceptedval_received = -1      # ^

    ### Phase 1 #########################################################
    def prepare(self):
        '''
        [Phase 1] Prepare acceptors to receive a value and attempt to secure a quorom
        '''
        self.messenger.send_prepare((self.proposal_id, self.proposer_id))
        PROPOSAL_ID += 1
        print("[PROPOSER] send prepare for ", str((self.proposal_id)))

    ### Phase 2 #########################################################
    def receive_promise(self, accepted_id:int, accepted_val:int = None):
        '''
        [Phase 2] Handle receiving responses

        Returns bool indicating to network to blast value or not
        '''
        self.promise_responses += 1

        if self.promise_responses >= quorum_size:
            # did the response contain accepted value from other proposers?
            if (accepted_val != None):
                # if so, we have to consider that the accepted value and blast it,
                # since it might have been a previously accepted value we don't know about.
                self.val = accepted_val
            
            # blast that shite
            self.messenger.send_accept(self.proposal_id, self.val)
            print("[PROPOSER] have quorum, sending accept for ", str((self.proposal_id, self.val)))

class Acceptor():
    def __init__(self):
        self.proposal_accepted = False
        self.max_id = -1
        self.max_proposer_id = -1

        self.accepted_val = None
        self.accepted_id = None

        self.messenger:Messenger = Messenger()
    
    ### Phase 1 #########################################################
    def promise(self, uid:int, proposal_id:int):
        if self.max_id < proposal_id:
            # have to accept new one
            self.max_id = proposal_id
            if self.proposal_accepted == True:
                # if we already accepted something, blast that back
                self.messenger.send_promise(uid, self.max_id, self.accepted_val)
                print("[ACCEPTOR] promised ", str((self.max_id, self.accepted_val)))
            else:
                # otherwise just accept this proposal
                self.messenger.send_promise(uid, self.max_id, None)
                print("[ACCEPTOR] promised ", str(self.max_id))

    ### Phase 2 #########################################################
    def receive_accept(self, uid, proposal_id, value):
        if (proposal_id == self.max_id):         # is the ID the largest I have seen so far?
            self.proposal_accepted = True       # note that we accepted a proposal
            self.accepted_id = proposal_id          # save the accepted proposal number
            self.accepted_val = val             # save the accepted proposal data
            self.messenger.send_accepted(proposal_id, self.accepted_val)
            print("[ACCEPTOR] accepted ", str((self.accepted_id, self.accepted_val)))
class Learner():
    pass