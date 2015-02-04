
import da
import sys
import serverManager
import client
import master
import io
import json
import time
from pprint import pprint

class TestApp(object):

    def __init__(self):
        pass

    def trigger(self):
        da.api.config(channel='fifo', clock='Lamport')
        sm = serverManager.ServerManager()
        configPath = ('C://Users//PearlWin//pythonspace//ChainReplicationP3//config//' + sys.argv[1])
        json_data = open(configPath)
        data = json.load(json_data)
        numBanks = len(data['banks'])
        clientReqDelay = data['clientWaitTime']
        simulateMessageLoss = data['simulate_msg_loss']
        extTailFailure = data['ext_tail_failure']
        masterSet = da.api.new(master.Master, num=1)
        masterList = list(masterSet)
        da.api.setup(masterList[0], ({}, {'extTailFailure': extTailFailure}))
        da.api.start(masterSet)
        for i in range(numBanks):
            numServers = data['banks'][i]['numServers']
            bankName = data['banks'][i]['bankName']
            numClients = data['banks'][i]['numClients']
            crashTypeList = data['banks'][i]['crashTypeList']
            serverChain = sm.createServerChain(numServers, {'bankname': bankName, 'crashTypeList': crashTypeList, 'master': masterList[0], 'simulate_msg_loss': simulateMessageLoss})
            head = serverChain[0]
            tail = serverChain[(len(serverChain) - 1)]
            print('ServerManager : Server Chain for bank', bankName, ' : ', serverChain)
            cSet = da.api.new(client.Client, num=numClients)
            cList = list(cSet)
            for j in range(len(cList)):
                da.api.setup(cList[j], ({}, {'bankname': bankName, 'id': str(j), 'head': head, 'tail': tail, 'configPath': configPath, 'delay': clientReqDelay, 'master': masterList[0]}))
            da.api.start(cSet)
        json_data.close()

def main():
    t = TestApp()
    t.trigger()
