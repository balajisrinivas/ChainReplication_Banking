
import da
PatternExpr_0 = da.pat.ConstantPattern('kill')
PatternExpr_1 = da.pat.FreePattern('myspawner')
import sys
import time

class ActionProcess(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ActionProcessReceivedEvent_0', PatternExpr_0, sources=[PatternExpr_1], destinations=None, timestamps=None, record_history=None, handlers=[self._ActionProcess_handler_0])])

    def setup(self, ps, argsMap):
        self.argsMap = argsMap
        self.ps = ps
        self.delay = self.argsMap['delay']
        self.action = self.argsMap['action']
        self.srcPid = self.argsMap['srcPid']
        self.destPid = self.argsMap['destPid']
        self.kill = False
        if ('bankName' in self.argsMap):
            self.bankName = self.argsMap['bankName']
        else:
            self.bankName = ''

    def main(self):
        if (self.action == 'pingMaster'):
            self.pingMaster()
        elif (self.action == 'checkForFailedServers'):
            self.checkForFailedServers(self.delay)
        elif (self.action == 'checkForChainLength'):
            self.checkForChainLength(self.delay)
        elif (self.action == 'checkLostMsg'):
            self.checkLostMsg(self.delay)
        if (self.kill == True):
            self.output('Action process terminating due to parent kill')

    def pingMaster(self):
        _st_label_18 = 0
        self._timer_start()
        while (_st_label_18 == 0):
            _st_label_18 += 1
            if (self.kill == True):
                pass
                _st_label_18 += 1
            elif self._timer_expired:
                self._send(('pingMaster', self.bankName, self.srcPid), self.destPid)
                self.pingMaster()
                _st_label_18 += 1
            else:
                super()._label('_st_label_18', block=True, timeout=1)
                _st_label_18 -= 1

    def checkForFailedServers(self, Delay):
        time.sleep(Delay)
        self._send('checkForFailedServers', self.destPid)
        self.checkForFailedServers(10)

    def checkForChainLength(self, delay):
        time.sleep(delay)
        self._send('checkForChainLength', self.destPid)
        self.checkForChainLength(10)

    def checkLostMsg(self, delay):
        time.sleep(delay)
        self._send('checkLostMsg', self.destPid)
        self.checkLostMsg(delay)

    def _ActionProcess_handler_0(self, myspawner):
        self.output('Action process received kill')
        self.kill = True
    _ActionProcess_handler_0._labels = None
    _ActionProcess_handler_0._notlabels = None

def main():
    pass
