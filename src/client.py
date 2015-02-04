
import da
PatternExpr_0 = da.pat.TuplePattern([da.pat.ConstantPattern('result'), da.pat.FreePattern('result')])
PatternExpr_1 = da.pat.FreePattern('server')
PatternExpr_2 = da.pat.TuplePattern([da.pat.ConstantPattern('head'), da.pat.FreePattern('headPid')])
PatternExpr_3 = da.pat.FreePattern('sender')
PatternExpr_4 = da.pat.TuplePattern([da.pat.ConstantPattern('tail'), da.pat.FreePattern('tailPid')])
PatternExpr_5 = da.pat.FreePattern('sender')
PatternExpr_6 = da.pat.ConstantPattern('checkLostMsg')
PatternExpr_7 = da.pat.FreePattern('worker')
import sys
import time
import io
import json
import math
import random
from _ast import Num
import time
import actionprocess

class Client(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_0', PatternExpr_0, sources=[PatternExpr_1], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_0]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_1', PatternExpr_2, sources=[PatternExpr_3], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_1]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_2', PatternExpr_4, sources=[PatternExpr_5], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_2]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_3', PatternExpr_6, sources=[PatternExpr_7], destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_3])])

    def setup(self, ps, argsMap):
        self.argsMap = argsMap
        self.ps = ps
        self.myId = self.argsMap['id']
        self.bankName = self.argsMap['bankname']
        self.head = self.argsMap['head']
        self.tail = self.argsMap['tail']
        self.timeDelay = self.argsMap['delay']
        self.configPath = self.argsMap['configPath']
        self.masterPid = self.argsMap['master']
        self.seqNumber = 0
        self.msgTracker = {}

    def main(self):
        actionSet = da.api.new(actionprocess.ActionProcess, num=1)
        actionList = list(actionSet)
        da.api.setup(actionList[0], ({}, {'delay': 15, 'action': 'checkLostMsg', 'srcPid': self.id, 'destPid': self.id}))
        da.api.start(actionSet)
        self._send(('registerClient', self.bankName), self.masterPid)
        self.generateRequests()
        super()._label('yield1', block=False)
        _st_label_176 = 0
        self._timer_start()
        while (_st_label_176 == 0):
            _st_label_176 += 1
            if False:
                pass
                _st_label_176 += 1
            elif self._timer_expired:
                self.output('Client terminating : ', ((self.bankName + '.') + self.myId), '\n')
                _st_label_176 += 1
            else:
                super()._label('yield1', block=True, timeout=90)
                _st_label_176 -= 1

    def generateRequests(self):
        json_data = open(self.configPath)
        data = json.load(json_data)
        requestGenerationType = data['requestGenerationType']
        boolClientResendsRequests = data['ifClientResendsRequests']
        time.sleep(5)
        if (requestGenerationType == 'randomizedRequests'):
            self.generateRandomRequests(boolClientResendsRequests)
        elif (requestGenerationType == 'itemizedRequests'):
            self.generateItemizedRequests(boolClientResendsRequests)

    def getSequenceNumber(self):
        self.seqNumber += 1
        return self.seqNumber

    def generateAccountNumber(self):
        return ((('acc' + self.bankName) + self.myId) + str(self.getSequenceNumber()))

    def generateReqID(self, number):
        return ((((self.bankName + '.') + self.myId) + '.') + str(number))

    def generateRandomRequests(self, boolClientResendsRequests):
        json_data = open(self.configPath)
        data = json.load(json_data)
        requestParametersList = []
        randomizedRequestsList = []
        randomizedRequestsList = data['randomizedRequests']
        requestParametersList = randomizedRequestsList[((self.bankName + '.') + self.myId)]
        seed = requestParametersList[0]
        numRequests = requestParametersList[1]
        probBalance = requestParametersList[2]
        probDeposit = requestParametersList[3]
        probWithdraw = requestParametersList[4]
        numBalanceRequests = round((numRequests * probBalance))
        numDepositRequests = round((numRequests * probDeposit))
        numWithdrawRequests = (numRequests - (numBalanceRequests + numDepositRequests))
        accNum = self.generateAccountNumber()
        random.seed(seed)
        lcm = ((numBalanceRequests * numDepositRequests) * numWithdrawRequests)
        balanceCounter = (lcm / numBalanceRequests)
        depositCounter = (lcm / numDepositRequests)
        withdrawCounter = (lcm / numWithdrawRequests)
        origBalanceCounter = balanceCounter
        origDepositCounter = depositCounter
        origWithdrawCounter = withdrawCounter
        for j in range(lcm):
            super()._label('yield2', block=False)
            if (balanceCounter == 0.0):
                balanceCounter = origBalanceCounter
                reqID = self.generateReqID(self.getSequenceNumber())
                self._send(('getBalance', reqID, accNum), self.tail)
                self.msgTracker[reqID] = (('getBalance', reqID, accNum), 'tail', round(time.time()))
                self.awaitSleep(self.timeDelay)
                if (boolClientResendsRequests == 'true'):
                    if (random.random() < 0.2):
                        self._send(('getBalance', reqID, accNum), self.tail)
                        self.awaitSleep(self.timeDelay)
                    else:
                        pass
            if (depositCounter == 0.0):
                depositCounter = origDepositCounter
                reqID = self.generateReqID(self.getSequenceNumber())
                randAmount = random.randint(0, 10000)
                self._send(('deposit', reqID, accNum, randAmount), self.head)
                self.msgTracker[reqID] = (('deposit', reqID, accNum, randAmount), 'head', round(time.time()))
                self.awaitSleep(self.timeDelay)
                if (boolClientResendsRequests == 'true'):
                    if (random.random() < 0.2):
                        self._send(('deposit', reqID, accNum, randAmount), self.head)
                        self.awaitSleep(self.timeDelay)
                    else:
                        pass
            if (withdrawCounter == 0.0):
                withdrawCounter = origWithdrawCounter
                reqID = self.generateReqID(self.getSequenceNumber())
                randAmount = random.randint(0, 10000)
                self._send(('withdraw', reqID, accNum, randAmount), self.head)
                self.msgTracker[reqID] = (('withdraw', reqID, accNum, randAmount), 'head', round(time.time()))
                self.awaitSleep(self.timeDelay)
                if (boolClientResendsRequests == 'true'):
                    if (random.random() < 0.2):
                        self._send(('withdraw', reqID, accNum, randAmount), self.head)
                        self.awaitSleep(self.timeDelay)
                    else:
                        pass
            balanceCounter -= 1
            depositCounter -= 1
            withdrawCounter -= 1

    def generateItemizedRequests(self, boolClientResendsRequests):
        json_data = open(self.configPath)
        data = json.load(json_data)
        itemizedRequestsDict = {}
        itemizedRequestsDict = data['itemizedRequests']
        partreqID = ((self.bankName + '.') + self.myId)
        reqTupleList = []
        reqTupleList = itemizedRequestsDict[partreqID]
        for p in reqTupleList:
            reqTuple = []
            reqTuple = p
            reqID = ((partreqID + '.') + str(reqTuple[0]))
            reqType = reqTuple[1]
            accNum = reqTuple[2]
            amount = reqTuple[3]
            if (reqType == 'balance'):
                self._send(('getBalance', reqID, accNum), self.tail)
                self.msgTracker[reqID] = (('getBalance', reqID, accNum), 'tail', round(time.time()))
                self.awaitSleep(self.timeDelay)
                if (boolClientResendsRequests == 'true'):
                    if (random.random() < 0.2):
                        self._send(('getBalance', reqID, accNum), self.tail)
                        self.awaitSleep(self.timeDelay)
                    else:
                        pass
            elif (reqType == 'deposit'):
                self._send(('deposit', reqID, accNum, amount), self.head)
                self.msgTracker[reqID] = (('deposit', reqID, accNum, amount), 'head', round(time.time()))
                self.awaitSleep(self.timeDelay)
                if (boolClientResendsRequests == 'true'):
                    if (random.random() < 0.2):
                        self._send(('deposit', reqID, accNum, amount), self.head)
                        self.awaitSleep(self.timeDelay)
                    else:
                        pass
            elif (reqType == 'withdraw'):
                self._send(('withdraw', reqID, accNum, amount), self.head)
                self.msgTracker[reqID] = (('withdraw', reqID, accNum, amount), 'head', round(time.time()))
                self.awaitSleep(self.timeDelay)
                if (boolClientResendsRequests == 'true'):
                    if (random.random() < 0.2):
                        self._send(('withdraw', reqID, accNum, amount), self.head)
                        self.awaitSleep(self.timeDelay)
                    else:
                        pass

    def awaitSleep(self, Delay):
        _st_label_166 = 0
        self._timer_start()
        while (_st_label_166 == 0):
            _st_label_166 += 1
            if False:
                pass
                _st_label_166 += 1
            elif self._timer_expired:
                pass
                _st_label_166 += 1
            else:
                super()._label('_st_label_166', block=True, timeout=Delay)
                _st_label_166 -= 1

    def _Client_handler_0(self, server, result):
        (reqId, i1, i2, i3) = result
        if (reqId in self.msgTracker):
            del self.msgTracker[reqId]
            self.output('Received response', result, ' from server : ', len(self.msgTracker), '\n')
    _Client_handler_0._labels = None
    _Client_handler_0._notlabels = None

    def _Client_handler_1(self, sender, headPid):
        self.output('Received new head for bank ', self.bankName, ' : ', headPid, '\n')
        self.head = headPid
    _Client_handler_1._labels = None
    _Client_handler_1._notlabels = None

    def _Client_handler_2(self, tailPid, sender):
        self.output('Received new tail for bank ', self.bankName, ' : ', tailPid, '\n')
        self.tail = tailPid
    _Client_handler_2._labels = None
    _Client_handler_2._notlabels = None

    def _Client_handler_3(self, worker):
        currTime = round(time.time())
        for reqId in self.msgTracker:
            (request, type, ts) = self.msgTracker[reqId]
            if ((currTime - ts) >= 15):
                if (type == 'head'):
                    sPid = self.head
                else:
                    sPid = self.tail
                self.output('RESEND Sending lost message :  ', request, '\n')
                self._send(request, sPid)
    _Client_handler_3._labels = None
    _Client_handler_3._notlabels = None

def main():
    pass
