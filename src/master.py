
import da
PatternExpr_0 = da.pat.TuplePattern([da.pat.ConstantPattern('registerServer'), da.pat.FreePattern('bankName'), da.pat.FreePattern('serverType')])
PatternExpr_1 = da.pat.FreePattern('server')
PatternExpr_2 = da.pat.TuplePattern([da.pat.ConstantPattern('registerClient'), da.pat.FreePattern('bankName')])
PatternExpr_3 = da.pat.FreePattern('client')
PatternExpr_4 = da.pat.TuplePattern([da.pat.ConstantPattern('registerPredSucc'), da.pat.FreePattern('bankName'), da.pat.FreePattern('pred'), da.pat.FreePattern('succ')])
PatternExpr_5 = da.pat.FreePattern('server')
PatternExpr_6 = da.pat.TuplePattern([da.pat.ConstantPattern('pingMaster'), da.pat.FreePattern('bankName'), da.pat.FreePattern('server')])
PatternExpr_7 = da.pat.FreePattern('serverWorker')
PatternExpr_8 = da.pat.ConstantPattern('checkForFailedServers')
PatternExpr_9 = da.pat.FreePattern('masterWorker')
PatternExpr_10 = da.pat.ConstantPattern('checkForChainLength')
PatternExpr_11 = da.pat.FreePattern('worker')
PatternExpr_12 = da.pat.TuplePattern([da.pat.ConstantPattern('respHandlePredCrash'), da.pat.FreePattern('sentRequestsLen'), da.pat.FreePattern('newPred')])
PatternExpr_13 = da.pat.FreePattern('newSucc')
PatternExpr_14 = da.pat.TuplePattern([da.pat.ConstantPattern('ackSetBalanceAndTransMap'), da.pat.TuplePattern([da.pat.FreePattern('bankName'), da.pat.FreePattern('currTail'), da.pat.FreePattern('newTail'), da.pat.FreePattern('master')])])
PatternExpr_15 = da.pat.FreePattern('inNewTail')
import sys
import time
import server
import actionprocess

class Master(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_MasterReceivedEvent_0', PatternExpr_0, sources=[PatternExpr_1], destinations=None, timestamps=None, record_history=None, handlers=[self._Master_handler_0]), da.pat.EventPattern(da.pat.ReceivedEvent, '_MasterReceivedEvent_1', PatternExpr_2, sources=[PatternExpr_3], destinations=None, timestamps=None, record_history=None, handlers=[self._Master_handler_1]), da.pat.EventPattern(da.pat.ReceivedEvent, '_MasterReceivedEvent_2', PatternExpr_4, sources=[PatternExpr_5], destinations=None, timestamps=None, record_history=None, handlers=[self._Master_handler_2]), da.pat.EventPattern(da.pat.ReceivedEvent, '_MasterReceivedEvent_3', PatternExpr_6, sources=[PatternExpr_7], destinations=None, timestamps=None, record_history=None, handlers=[self._Master_handler_3]), da.pat.EventPattern(da.pat.ReceivedEvent, '_MasterReceivedEvent_4', PatternExpr_8, sources=[PatternExpr_9], destinations=None, timestamps=None, record_history=None, handlers=[self._Master_handler_4]), da.pat.EventPattern(da.pat.ReceivedEvent, '_MasterReceivedEvent_5', PatternExpr_10, sources=[PatternExpr_11], destinations=None, timestamps=None, record_history=None, handlers=[self._Master_handler_5]), da.pat.EventPattern(da.pat.ReceivedEvent, '_MasterReceivedEvent_6', PatternExpr_12, sources=[PatternExpr_13], destinations=None, timestamps=None, record_history=None, handlers=[self._Master_handler_6]), da.pat.EventPattern(da.pat.ReceivedEvent, '_MasterReceivedEvent_7', PatternExpr_14, sources=[PatternExpr_15], destinations=None, timestamps=None, record_history=None, handlers=[self._Master_handler_7])])

    def setup(self, ps, argsMap):
        self.ps = ps
        self.argsMap = argsMap
        self.bankServersPingMap = {}
        self.bankHeadTailMap = {}
        self.bankClientsMap = {}
        self.bankPredSuccMap = {}
        self.extTailFailure = self.argsMap['extTailFailure']
        self.chainThreshold = 3

    def main(self):
        actionSet = da.api.new(actionprocess.ActionProcess, num=2)
        actionList = list(actionSet)
        da.api.setup(actionList[0], ({}, {'delay': 15, 'action': 'checkForFailedServers', 'srcPid': self.id, 'destPid': self.id}))
        da.api.setup(actionList[1], ({}, {'delay': 15, 'action': 'checkForChainLength', 'srcPid': self.id, 'destPid': self.id}))
        da.api.start(actionSet)
        self.output('Master awaited : ', self.id, '\n')
        _st_label_149 = 0
        self._timer_start()
        while (_st_label_149 == 0):
            _st_label_149 += 1
            if False:
                pass
                _st_label_149 += 1
            elif self._timer_expired:
                self.output('Master terminating : ', self.id, '\n')
                _st_label_149 += 1
            else:
                super()._label('_st_label_149', block=True, timeout=100)
                _st_label_149 -= 1

    def updateBankHeadTailMap(self, bankName, serverPid, serverType):
        if (serverType == 'head'):
            if (bankName in self.bankHeadTailMap):
                (oldHead, oldTail) = self.bankHeadTailMap[bankName]
                self.bankHeadTailMap[bankName] = (serverPid, oldTail)
            else:
                self.bankHeadTailMap[bankName] = (serverPid, None)
        elif (serverType == 'tail'):
            if (bankName in self.bankHeadTailMap):
                (oldHead, oldTail) = self.bankHeadTailMap[bankName]
                self.bankHeadTailMap[bankName] = (oldHead, serverPid)
            else:
                self.bankHeadTailMap[bankName] = (None, serverPid)
        else:
            pass

    def updateBankServersPingMap(self, bankName, serverPid):
        self.bankServersPingMap[(bankName, serverPid)] = round(time.time())

    def takeServerFailureAction(self, bankName, failedServerPid):
        if (bankName in self.bankHeadTailMap):
            (bankHeadPid, bankTailPid) = self.bankHeadTailMap[bankName]
            if (bankHeadPid == failedServerPid):
                self.output('Head Crash Detected for the bank: ', bankName, ' Crashed Head : ', failedServerPid, '\n')
                self.printEssentialState(('State Before Head Crash handling for bank : ' + bankName))
                del self.bankServersPingMap[(bankName, failedServerPid)]
                (ignore, newHeadPid) = self.bankPredSuccMap[(bankName, failedServerPid)]
                del self.bankPredSuccMap[(bankName, failedServerPid)]
                (ignore, nHeadSucc) = self.bankPredSuccMap[(bankName, newHeadPid)]
                self.bankPredSuccMap[(bankName, newHeadPid)] = (None, nHeadSucc)
                self._send(('setPred', None), newHeadPid)
                self.bankHeadTailMap[bankName] = (newHeadPid, bankTailPid)
                if (bankName in self.bankClientsMap):
                    clientList = self.bankClientsMap[bankName]
                    for clientPid in clientList:
                        self._send(('head', newHeadPid), clientPid)
                self.printEssentialState(('State After Head Crash handling for bank :' + bankName))
            elif (bankTailPid == failedServerPid):
                self.output('Tail Crash Detected for the bank: ', bankName, ' Crashed Tail : ', failedServerPid, '\n')
                self.printEssentialState(('State Before Tail Crash handling for bank : ' + bankName))
                del self.bankServersPingMap[(bankName, failedServerPid)]
                (newTailPid, ignore) = self.bankPredSuccMap[(bankName, failedServerPid)]
                del self.bankPredSuccMap[(bankName, failedServerPid)]
                (nTailPred, ignore) = self.bankPredSuccMap[(bankName, newTailPid)]
                self.bankPredSuccMap[(bankName, newTailPid)] = (nTailPred, None)
                self._send(('setSucc', None), newTailPid)
                self.bankHeadTailMap[bankName] = (bankHeadPid, newTailPid)
                if (bankName in self.bankClientsMap):
                    clientList = self.bankClientsMap[bankName]
                    for clientPid in clientList:
                        self._send(('tail', newTailPid), clientPid)
                (da.api.send('takeNewTailAction', to=newTailPid),)
                self.printEssentialState(('State After Tail Crash handling for bank :' + bankName))
            else:
                self.output(' MIDCRASHHANDLING Mid Server Crash Detected for the bank: ', bankName, ' Crashed Server : ', failedServerPid, '\n')
                self.printEssentialState((' MIDCRASHHANDLING State Before Mid Server Crash handling for bank : ' + bankName))
                del self.bankServersPingMap[(bankName, failedServerPid)]
                (failedSerPred, failedServerSucc) = self.bankPredSuccMap[(bankName, failedServerPid)]
                del self.bankPredSuccMap[(bankName, failedServerPid)]
                (fPP, ignore) = self.bankPredSuccMap[(bankName, failedSerPred)]
                (ignore, fSS) = self.bankPredSuccMap[(bankName, failedServerSucc)]
                self.bankPredSuccMap[(bankName, failedSerPred)] = (fPP, failedServerSucc)
                self.bankPredSuccMap[(bankName, failedServerSucc)] = (failedSerPred, fSS)
                self._send(('setSucc', failedServerSucc), failedSerPred)
                self._send(('setPred', failedSerPred), failedServerSucc)
                self._send(('handlePredCrash', failedSerPred), failedServerSucc)
                self.printEssentialState((' MIDCRASHHANDLING State After Mid Server Crash handling for bank :' + bankName))

    def getBankChainLength(self, bankName):
        chainLength = 0
        for (bName, server) in self.bankServersPingMap:
            if (bName == bankName):
                chainLength += 1
        return chainLength

    def extendServerChain(self, bankName):
        self.output(' EXTENDCHAIN Extending chain for the bank : ', bankName, '\n')
        (ignore, currTail) = self.bankHeadTailMap[bankName]
        psSet = da.api.new(server.Server, num=1)
        psList = list(psSet)
        if (self.extTailFailure == 'true'):
            crashType = ['receive', 2]
        else:
            crashType = ['unbounded', 0]
        da.api.setup(psList[0], ({}, {'pred': currTail, 'succ': None, 'serverType': 'tail', 'bankname': bankName, 'crashType': crashType, 'master': self.id, 'register': False, 'simulate_msg_loss': 'false'}))
        da.api.start(psSet)
        newTail = psList[0]
        self._send(('takeOldTailAction', bankName, currTail, newTail), currTail)

    def printEssentialState(self, msg):
        self.output(msg, '\n')
        self.output('Master : BankHeadTailMap : ', self.bankHeadTailMap, '\n')
        self.output('Master : BankServersPingMap : ', self.bankServersPingMap, '\n')
        self.output('Master : BankPredSuccMap : ', self.bankPredSuccMap, '\n')

    def _Master_handler_0(self, server, serverType, bankName):
        self.updateBankHeadTailMap(bankName, server, serverType)
        self.updateBankServersPingMap(bankName, server)
    _Master_handler_0._labels = None
    _Master_handler_0._notlabels = None

    def _Master_handler_1(self, bankName, client):
        if (bankName in self.bankClientsMap):
            clientList = self.bankClientsMap[bankName]
            clientList.append(client)
            self.bankClientsMap[bankName] = clientList
        else:
            self.bankClientsMap[bankName] = [client]
    _Master_handler_1._labels = None
    _Master_handler_1._notlabels = None

    def _Master_handler_2(self, succ, pred, server, bankName):
        self.bankPredSuccMap[(bankName, server)] = (pred, succ)
    _Master_handler_2._labels = None
    _Master_handler_2._notlabels = None

    def _Master_handler_3(self, bankName, serverWorker, server):
        self.updateBankServersPingMap(bankName, server)
        self.output('Master :  Received ping from server : ', server, ' of bank : ', bankName)
    _Master_handler_3._labels = None
    _Master_handler_3._notlabels = None

    def _Master_handler_4(self, masterWorker):
        self.output('Master checking for failed servers')
        currTs = round(time.time())
        itbankServersPingMap = self.bankServersPingMap.copy()
        for (bankName, serverPid) in itbankServersPingMap:
            ts = itbankServersPingMap[(bankName, serverPid)]
            if ((currTs - ts) >= 5):
                self.output('Master found a failed server : ', bankName, serverPid)
                self.takeServerFailureAction(bankName, serverPid)
    _Master_handler_4._labels = None
    _Master_handler_4._notlabels = None

    def _Master_handler_5(self, worker):
        self.output('Master checking for chain length')
        for bankName in self.bankHeadTailMap:
            chainCount = self.getBankChainLength(bankName)
            if (chainCount <= self.chainThreshold):
                self.extendServerChain(bankName)
    _Master_handler_5._labels = None
    _Master_handler_5._notlabels = None

    def _Master_handler_6(self, sentRequestsLen, newSucc, newPred):
        self._send(('handleSuccCrash', sentRequestsLen, newSucc), newPred)
    _Master_handler_6._labels = None
    _Master_handler_6._notlabels = None

    def _Master_handler_7(self, currTail, master, inNewTail, bankName, newTail):
        self.output('EXTENDCHAIN Chain extension successful. Reconfiguring Server Chain and Updating master maps for ', bankName)
        self._send(('setSucc', newTail), currTail)
        self.updateBankServersPingMap(bankName, newTail)
        self.updateBankHeadTailMap(bankName, newTail, 'tail')
        (currTailPred, ignore) = self.bankPredSuccMap[(bankName, currTail)]
        self.bankPredSuccMap[(bankName, currTail)] = (currTailPred, newTail)
        self.bankPredSuccMap[(bankName, newTail)] = (currTail, None)
        self.output('EXTENDCHAIN Chain extension successful. Updated Master Maps BHTM : ', self.bankHeadTailMap, ' BPSM : ', self.bankPredSuccMap)
        if (bankName in self.bankClientsMap):
            clientList = self.bankClientsMap[bankName]
            for client in clientList:
                self._send(('tail', newTail), client)
    _Master_handler_7._labels = None
    _Master_handler_7._notlabels = None

def main():
    pass
