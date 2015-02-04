
import da
PatternExpr_0 = da.pat.TuplePattern([da.pat.ConstantPattern('setPred'), da.pat.FreePattern('pred')])
PatternExpr_1 = da.pat.FreePattern('source')
PatternExpr_2 = da.pat.TuplePattern([da.pat.ConstantPattern('setSucc'), da.pat.FreePattern('succ')])
PatternExpr_3 = da.pat.FreePattern('source')
PatternExpr_4 = da.pat.TuplePattern([da.pat.ConstantPattern('getBalance'), da.pat.FreePattern('reqId'), da.pat.FreePattern('accountNum')])
PatternExpr_5 = da.pat.FreePattern('client')
PatternExpr_6 = da.pat.TuplePattern([da.pat.ConstantPattern('deposit'), da.pat.FreePattern('reqId'), da.pat.FreePattern('accountNum'), da.pat.FreePattern('amount')])
PatternExpr_7 = da.pat.FreePattern('client')
PatternExpr_8 = da.pat.TuplePattern([da.pat.ConstantPattern('withdraw'), da.pat.FreePattern('reqId'), da.pat.FreePattern('accountNum'), da.pat.FreePattern('amount')])
PatternExpr_9 = da.pat.FreePattern('client')
PatternExpr_10 = da.pat.TuplePattern([da.pat.ConstantPattern('sync'), da.pat.FreePattern('result'), da.pat.FreePattern('clientPid'), da.pat.FreePattern('accountNum'), da.pat.FreePattern('pTransObj')])
PatternExpr_11 = da.pat.FreePattern('server')
PatternExpr_12 = da.pat.TuplePattern([da.pat.ConstantPattern('sentRequestsAck'), da.pat.FreePattern('result'), da.pat.FreePattern('clientPid'), da.pat.FreePattern('accountNum'), da.pat.FreePattern('pTransObj')])
PatternExpr_13 = da.pat.FreePattern('successor')
PatternExpr_14 = da.pat.ConstantPattern('takeNewTailAction')
PatternExpr_15 = da.pat.FreePattern('master')
PatternExpr_16 = da.pat.TuplePattern([da.pat.ConstantPattern('takeOldTailAction'), da.pat.FreePattern('bankName'), da.pat.FreePattern('currTail'), da.pat.FreePattern('newTail')])
PatternExpr_17 = da.pat.FreePattern('master')
PatternExpr_18 = da.pat.TuplePattern([da.pat.ConstantPattern('setBalanceAndTransMap'), da.pat.FreePattern('inBalanceMap'), da.pat.FreePattern('inProcessedTransMap'), da.pat.TuplePattern([da.pat.FreePattern('bankName'), da.pat.FreePattern('currTail'), da.pat.FreePattern('newTail'), da.pat.FreePattern('master')])])
PatternExpr_19 = da.pat.FreePattern('server')
PatternExpr_20 = da.pat.TuplePattern([da.pat.ConstantPattern('handlePredCrash'), da.pat.FreePattern('myNewPred')])
PatternExpr_21 = da.pat.FreePattern('master')
PatternExpr_22 = da.pat.TuplePattern([da.pat.ConstantPattern('handleSuccCrash'), da.pat.FreePattern('sentRequestsLen'), da.pat.FreePattern('newSucc')])
PatternExpr_23 = da.pat.FreePattern('master')
PatternExpr_24 = da.pat.TuplePattern([da.pat.ConstantPattern('processNoAckRequests'), da.pat.FreePattern('sentRequestsSuffix')])
PatternExpr_25 = da.pat.FreePattern('pred')
import sys
import actionprocess
import time
import random
import math

class Server(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_0', PatternExpr_0, sources=[PatternExpr_1], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_0]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_1', PatternExpr_2, sources=[PatternExpr_3], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_1]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_2', PatternExpr_4, sources=[PatternExpr_5], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_2]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_3', PatternExpr_6, sources=[PatternExpr_7], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_3]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_4', PatternExpr_8, sources=[PatternExpr_9], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_4]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_5', PatternExpr_10, sources=[PatternExpr_11], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_5]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_6', PatternExpr_12, sources=[PatternExpr_13], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_6]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_7', PatternExpr_14, sources=[PatternExpr_15], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_7]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_8', PatternExpr_16, sources=[PatternExpr_17], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_8]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_9', PatternExpr_18, sources=[PatternExpr_19], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_9]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_10', PatternExpr_20, sources=[PatternExpr_21], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_10]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_11', PatternExpr_22, sources=[PatternExpr_23], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_11]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ServerReceivedEvent_12', PatternExpr_24, sources=[PatternExpr_25], destinations=None, timestamps=None, record_history=None, handlers=[self._Server_handler_12])])

    def setup(self, ps, argsMap):
        self.ps = ps
        self.argsMap = argsMap
        self.myName = self.argsMap['bankname']
        self.crashType = self.argsMap['crashType']
        self.serverType = self.argsMap['serverType']
        self.register = self.argsMap['register']
        self.simulateMsgLoss = self.argsMap['simulate_msg_loss']
        self.balanceMap = {}
        self.processedTransMap = {}
        self.sentRequests = []
        self.pred = self.argsMap['pred']
        self.succ = self.argsMap['succ']
        self.master = self.argsMap['master']
        self.processed = 'processed'
        self.inconsistent = 'inconsistentWithHistory'
        self.insufficient = 'insufficientBalance'
        self.deposit = 'deposit'
        self.withdraw = 'withdraw'
        self.crashCounter = 1

    def main(self):
        if self.register:
            self._send(('registerServer', self.myName, self.serverType), self.master)
            self._send(('registerPredSucc', self.myName, self.pred, self.succ), self.master)
        actionSet = da.api.new(actionprocess.ActionProcess, num=1)
        actionList = list(actionSet)
        da.api.setup(actionList[0], ({}, {'delay': 1, 'action': 'pingMaster', 'srcPid': self.id, 'destPid': self.master, 'bankName': self.myName}))
        da.api.start(actionSet)
        self.output('Server awaited : ', self.id, '\n')
        [crashT, n] = self.crashType
        _st_label_165 = 0
        self._timer_start()
        while (_st_label_165 == 0):
            _st_label_165 += 1
            if (n == self.crashCounter):
                self._send('kill', actionList[0])
                self.output('Server', self.myName, 'terminating due to the constraint : ', self.crashType, '\n')
                _st_label_165 += 1
            elif self._timer_expired:
                self.output('Server', self.myName, 'terminating due to timeout : ', self.id, '\n')
                _st_label_165 += 1
            else:
                super()._label('_st_label_165', block=True, timeout=100)
                _st_label_165 -= 1

    def sync(self, result, clientPid, accountNum, pTransObj):
        if (not (self.succ is None)):
            self._send(('sync', result, clientPid, accountNum, pTransObj), self.succ)
            if (not ((result, clientPid, accountNum, pTransObj) in self.sentRequests)):
                self.sentRequests.append((result, clientPid, accountNum, pTransObj))
        else:
            if self.shallDropRequest(self.simulateMsgLoss):
                self.output('RESEND Dropping result to client to simulate message loss : ', result, '\n')
            else:
                self.output('Sending result to client ', clientPid, ' by ', self.id, ' : ', result, '\n')
                self._send(('result', result), clientPid)
            if (not (self.pred == None)):
                self._send(('sentRequestsAck', result, clientPid, accountNum, pTransObj), self.pred)
        self.updateCrashCounter('send')

    def shallDropRequest(self, simulateMsgLoss):
        if (simulateMsgLoss == 'true'):
            random.seed(round(time.time()))
            r = random.random()
            if (r < 0.5):
                return True
            else:
                return False
        else:
            return False

    def updateBalanceAndTransactionMaps(self, accountNum, result, pTransObj):
        if ((result[1] == self.processed) and (not (pTransObj == ()))):
            self.balanceMap[accountNum] = result[3]
        if (not (pTransObj == ())):
            self.processedTransMap[result[0]] = pTransObj

    def updateCrashCounter(self, event):
        [crashT, n] = self.crashType
        if (event == crashT):
            self.crashCounter += 1
            self.output('CrashCounter Status for bank : ', self.myName, ' : ', self.crashCounter)

    def currBalance(self, accountNum):
        if (accountNum in self.balanceMap):
            balance = self.balanceMap[accountNum]
        else:
            self.balanceMap[accountNum] = 0
            balance = 0
        return balance

    def getBalance(self, reqId, accountNum):
        return (reqId, self.processed, accountNum, self.currBalance(accountNum))

    def depositAmount(self, reqId, accountNum, amount):
        balance = self.currBalance(accountNum)
        if (not (reqId in self.processedTransMap)):
            self.balanceMap[accountNum] = (balance + amount)
            transObj = (reqId, accountNum, (amount, (balance + amount), self.processed), self.deposit)
            self.processedTransMap[reqId] = transObj
            return ((reqId, self.processed, accountNum, (balance + amount)), transObj)
        else:
            (pReqId, pAccountNum, (pAmount, pRepliedBalance, pRepliedType), transType) = self.processedTransMap[reqId]
            if ((pAccountNum, pAmount, transType) == (accountNum, amount, self.deposit)):
                return ((reqId, pRepliedType, accountNum, pRepliedBalance), ())
            else:
                return ((reqId, self.inconsistent, accountNum, balance), ())

    def withdrawAmount(self, reqId, accountNum, amount):
        balance = self.currBalance(accountNum)
        if (not (reqId in self.processedTransMap)):
            if (balance >= amount):
                self.balanceMap[accountNum] = (balance - amount)
                transObj = (reqId, accountNum, (amount, (balance - amount), self.processed), self.withdraw)
                self.processedTransMap[reqId] = transObj
                return ((reqId, self.processed, accountNum, (balance - amount)), transObj)
            else:
                transObj = (reqId, accountNum, (amount, balance, self.insufficient), self.withdraw)
                self.processedTransMap[reqId] = transObj
                return ((reqId, self.insufficient, accountNum, balance), transObj)
        else:
            (pReqId, pAccountNum, (pAmount, pRepliedBalance, pRepliedType), transType) = self.processedTransMap[reqId]
            if ((pAccountNum, pAmount, transType) == (accountNum, amount, self.withdraw)):
                return ((reqId, pRepliedType, accountNum, pRepliedBalance), ())
            else:
                return ((reqId, self.inconsistent, accountNum, balance), ())

    def _Server_handler_0(self, pred, source):
        self.output('Setting Predecessor for ', self.id, ' as ', pred, '\n')
        self.pred = pred
    _Server_handler_0._labels = None
    _Server_handler_0._notlabels = None

    def _Server_handler_1(self, source, succ):
        self.output('Setting Successor for ', self.id, ' as ', succ, '\n')
        self.succ = succ
    _Server_handler_1._labels = None
    _Server_handler_1._notlabels = None

    def _Server_handler_2(self, accountNum, reqId, client):
        self.output('Received getBalance request ', str(reqId), ' from client ', client, ' by ', self.id, '\n')
        result = self.getBalance(reqId, accountNum)
        self._send(('result', result), client)
        self.updateCrashCounter('receive')
    _Server_handler_2._labels = None
    _Server_handler_2._notlabels = None

    def _Server_handler_3(self, amount, accountNum, client, reqId):
        self.output('Received deposit request ', str(reqId), ' from client ', client, ' by ', self.id, '\n')
        (result, pTransObj) = self.depositAmount(reqId, accountNum, amount)
        self.sync(result, client, accountNum, pTransObj)
        self.updateCrashCounter('receive')
    _Server_handler_3._labels = None
    _Server_handler_3._notlabels = None

    def _Server_handler_4(self, client, reqId, amount, accountNum):
        self.output('Received withdraw request ', str(reqId), ' from client ', client, ' by ', self.id, '\n')
        (result, pTransObj) = self.withdrawAmount(reqId, accountNum, amount)
        self.sync(result, client, accountNum, pTransObj)
        self.updateCrashCounter('receive')
    _Server_handler_4._labels = None
    _Server_handler_4._notlabels = None

    def _Server_handler_5(self, clientPid, pTransObj, result, accountNum, server):
        self.output('Received sync request ', result[0], ' from ', server, ' by ', self.id, '\n')
        if (server == self.pred):
            self.updateBalanceAndTransactionMaps(accountNum, result, pTransObj)
            self.sync(result, clientPid, accountNum, pTransObj)
        else:
            self.output('Chain corrupted ! :) Time to grab some coffee!!', '\n')
        self.updateCrashCounter('receive')
    _Server_handler_5._labels = None
    _Server_handler_5._notlabels = None

    def _Server_handler_6(self, pTransObj, result, accountNum, successor, clientPid):
        self.sentRequests.remove((result, clientPid, accountNum, pTransObj))
        if (not (self.pred == None)):
            self._send(('sentRequestsAck', result, clientPid, accountNum, pTransObj), self.pred)
    _Server_handler_6._labels = None
    _Server_handler_6._notlabels = None

    def _Server_handler_7(self, master):
        self.output('Taking new tail action. Current SentRequests : ', self.sentRequests, '\n')
        for (result, clientPid, accountNum, pTransObj) in self.sentRequests:
            self._send(('result', result), clientPid)
            if (not (self.pred == None)):
                self._send(('sentRequestsAck', result, clientPid, accountNum, pTransObj), self.pred)
    _Server_handler_7._labels = None
    _Server_handler_7._notlabels = None

    def _Server_handler_8(self, newTail, currTail, master, bankName):
        self.output(' EXTENDCHAIN To be old tail sending BalanceMap and TransMap to New Tail : ', newTail)
        self._send(('setBalanceAndTransMap', self.balanceMap, self.processedTransMap, (bankName, currTail, newTail, master)), newTail)
        self.updateCrashCounter('receive_ext')
    _Server_handler_8._labels = None
    _Server_handler_8._notlabels = None

    def _Server_handler_9(self, master, inBalanceMap, inProcessedTransMap, server, bankName, currTail, newTail):
        self.output('EXTENDCHAIN Receiving BalanceMap and TransMap from Old Tail : ', currTail, ' BalanceMap : ', inBalanceMap, ' TransMap : ', inProcessedTransMap)
        self.balanceMap = inBalanceMap
        self.processedTransMap = inProcessedTransMap
        self._send(('ackSetBalanceAndTransMap', (bankName, currTail, newTail, master)), master)
        self.updateCrashCounter('receive')
    _Server_handler_9._labels = None
    _Server_handler_9._notlabels = None

    def _Server_handler_10(self, master, myNewPred):
        self.output('MIDCRASHHANDLING Received handlePredCrash from master for my new pred : ', myNewPred, '\n')
        sentRequestsLen = len(self.sentRequests)
        self._send(('respHandlePredCrash', sentRequestsLen, myNewPred), master)
        self.updateCrashCounter('receive_fail')
    _Server_handler_10._labels = None
    _Server_handler_10._notlabels = None

    def _Server_handler_11(self, sentRequestsLen, master, newSucc):
        if (len(self.sentRequests) > sentRequestsLen):
            sentRequestsSuffix = self.sentRequests[(sentRequestsLen - len(self.sentRequests)):]
            self.output('MIDCRASHHANDLING Sending SentrequestsSuffixList to my new successor : ', newSucc, ' : ', sentRequestsSuffix, '\n')
            self._send(('processNoAckRequests', sentRequestsSuffix), newSucc)
        else:
            self.output('MIDCRASHHANDLING No SentrequestsSuffixList to be sent to my new successor : ', newSucc, '\n')
        self.updateCrashCounter('receive_fail')
    _Server_handler_11._labels = None
    _Server_handler_11._notlabels = None

    def _Server_handler_12(self, pred, sentRequestsSuffix):
        self.output('MIDCRASHHANDLING Received SentrequestsSuffixList from my new predecessor : ', pred, ' : ', sentRequestsSuffix, '\n')
        for (result, clientPid, accountNum, pTransObj) in sentRequestsSuffix:
            self.updateBalanceAndTransactionMaps(accountNum, result, pTransObj)
            self.sync(result, clientPid, accountNum, pTransObj)
    _Server_handler_12._labels = None
    _Server_handler_12._notlabels = None

def main():
    pass
