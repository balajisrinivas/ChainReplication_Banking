
import da
import sys
import server

class ServerManager(object):

    def createServerChain(self, n, bankInfoMap):
        da.api.config(channel='fifo', clock='Lamport')
        psSet = da.api.new(server.Server, num=n)
        ps = list(psSet)
        print(ps)
        crashTypeList = bankInfoMap['crashTypeList']
        for i in range(len(ps)):
            if (i == 0):
                serverType = 'head'
                pred = None
                if (i == (len(ps) - 1)):
                    succ = None
                else:
                    succ = ps[(i + 1)]
            elif (i == (len(ps) - 1)):
                serverType = 'tail'
                pred = ps[(i - 1)]
                succ = None
            else:
                serverType = 'mid'
                pred = ps[(i - 1)]
                succ = ps[(i + 1)]
            bankInfoMap.update({'pred': pred, 'succ': succ, 'serverType': serverType, 'register': True})
            bankInfoMap['crashType'] = crashTypeList[i]
            da.api.setup(ps[i], ({}, bankInfoMap))
        da.api.start(psSet)
        return ps

def main():
    pass
