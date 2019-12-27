class ConnectionContextFactory:
    _instance=None

    def __init__(self):
        raise Exception("it's A factory for an instance call ConnectionContextFactory.getinstance()");


    @classmethod
    def getinstance(cls,configFile=""):
        if cls._instance is None:
            cls._instance=ConnectionContext()
        return cls._instance




class ConnectionContext:
    def __init__(self):
        self.info={}
        self.contracts={}

    def addSocket(self,addr,port,contract,type):
        socket='{}:{}'.format(addr,port)
        data={'type':type,'contract':contract,'viewers':{},'streamers':[]}
        self.info[socket]=data
        self.contracts[contract]=(addr,port)


    def socketExist(self,addr,port):
        socket='{}:{}'.format(addr,port)
        return socket in self.info.keys()

    def removeSocket(self,addr,port):
        info=self.info.pop('{}:{}'.format(addr,port))
        self.contracts.pop(info['contract'])

    def getaddress(self,contrat):
        address=self.contracts[contrat]
        return address

    def getType(self,addr,port):
        type=self.info['{}:{}'.format(addr,port)]['type']

        return type

    def getContract(self,addr,port):
        contract=self.info['{}:{}'.format(addr,port)]['contract']
        return contract

    def getViwers(self,addr,port):
        viewers=self.info['{}:{}'.format(addr,port)]['viewers']
        return viewers

    def addToViwers(self,requestHandler,addr,port):
        (addrViewer,portViewer)=requestHandler.request.getpeername()
        self.info['{}:{}'.format(addr,port)]['viewers']['{}:{}'.format(addrViewer,portViewer)]=requestHandler
        self.info['{}:{}'.format(addrViewer,portViewer)]['streamers'].append('{}:{}'.format(addr,port))



    def removeFromViewers(self,requestHandler,addr,port):
        (addrViewer,portViewer)=requestHandler.request.getpeername()
        streamers=self.info['{}:{}'.format(addrViewer,portViewer)]['streamers']
        for streamer in streamers:
            self.info[streamer]['viewers'].pop('{}:{}'.format(addrViewer,portViewer))
