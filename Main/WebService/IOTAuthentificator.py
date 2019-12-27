from WebService.BAIIOTProtocol import BAIIOTClienAuthentificator,BAIIOTSevertAuthentificator
from CustomException import BAIIOTException
from WebService.Constante import EntityType

from DataLayer.BCKContext import BCKContext



class ToGatewayAuthentificator(BAIIOTClienAuthentificator):

    def __init__(self,appContext,socket,ssl_version,addressBCkNode,password=None):
        BAIIOTClienAuthentificator.__init__(self,appContext=appContext,socket=socket,ssl_version=ssl_version,addressBCkNode=addressBCkNode ,password=password)

    def entityIspermited(self,publicKey,contract_address):
        return self.managementRepo.gatewayIsPermited(publicKey=publicKey,contract_address= contract_address)

class ToServerAuthentificator(BAIIOTClienAuthentificator):

        def __init__(self,appContext,socket,ssl_version,addressBCkNode,password=None):
            BAIIOTClienAuthentificator.__init__(self,appContext=appContext,socket=socket,ssl_version=ssl_version,addressBCkNode=addressBCkNode,password=password)

        def entityIspermited(self,publicKey,contract_address):
            return self.managementRepo.serverIsPermited(publicKey=publicKey,contract_address= contract_address)



class ToIOTAuthentificator(BAIIOTClienAuthentificator):

        def __init__(self,appContext,socket,ssl_version,addressBCkNode,password=None):
            BAIIOTClienAuthentificator.__init__(self,appContext=appContext,socket=socket,ssl_version=ssl_version,addressBCkNode=addressBCkNode,password=password)

        def entityIspermited(self,publicKey,contract_address):
            return self.managementRepo.iotIsPermited(publicKey=publicKey,contract_address= contract_address)



class GatewayAuthentificator(BAIIOTSevertAuthentificator):

    def __init__(self,appContext,socket,ssl_version,addressBCkNode,password=None):
        BAIIOTSevertAuthentificator.__init__(self,appContext=appContext,socket=socket,ssl_version=ssl_version,addressBCkNode=addressBCkNode,password=password)

    def entityIspermited(self,publicKey,contract_address):
        if self.otherType== EntityType._IOT:
            return self.managementRepo.iotIsPermited(publicKey=publicKey,contract_address= contract_address)
        if self.otherType== EntityType._CLIENT:
            return self.managementRepo.userIsPermited(publicKey=publicKey,contract_address= contract_address)
        raise BAIIOTException()



class ServerAuthentificator(BAIIOTSevertAuthentificator):

    def __init__(self,appContext,socket,ssl_version,addressBCkNode,password=None):
        BAIIOTSevertAuthentificator.__init__(self,appContext=appContext,socket=socket,ssl_version=ssl_version,addressBCkNode=addressBCkNode,password=password)

    def entityIspermited(self,publicKey,contract_address):
        if self.otherType== EntityType._GATEWAY:
            return self.managementRepo.gatewayIsPermited(publicKey=publicKey,contract_address= contract_address)
        if self.otherType== EntityType._CLIENT:
            return self.managementRepo.userIsPermited(publicKey=publicKey,contract_address= contract_address)
        raise BAIIOTException()

class IOTAuthentificator(BAIIOTSevertAuthentificator):

    def __init__(self,appContext,socket,ssl_version,addressBCkNode,password=None):
        BAIIOTSevertAuthentificator.__init__(self,appContext=appContext,socket=socket,ssl_version=ssl_version,addressBCkNode=addressBCkNode,password=password)

    def entityIspermited(self,publicKey,contract_address):
        if self.appContext.config['bck_managementKeyContract']!=contract_address:
            return False
        pbkey=self.keyRepo.getPublicKeyUser(publicKey)
        ownerPbKey=self.managementRepo.getOwner(contract_address= contract_address)
        if(ownerPbKey==pbkey):
            return True
        else:
            return False
