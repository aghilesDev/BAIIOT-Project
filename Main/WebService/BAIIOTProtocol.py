import socket,ssl
import os
from DataLayer.BCKContext import BCKContext
from web3.auto import w3
import WebService.Validator as Validator
from WebService.AuthenticationHandler import AuthenticationHandler,TokenGenerator
import json
from WebService.AppContext import AppContextFactory
from DataLayer.BCKRepository import ManagementKeyContractRepository,KeyContractRepository
from WebService.Constante import EntityType
from CustomException import InvalideSignatureException,ContractNotInMangementContractException
from WebService.RequestManager import RequestManager
import collections


class BAIIOTBaseAuthentificator:
    def __init__(self,appContext,socket,ssl_version,addressBCkNode,password):
        if password is None:
            password=appContext.config['bck_password']
        else:
            appContext.config['bck_password']=password
        (ip,port)=addressBCkNode
        bckContext=BCKContext.getRawinstance(newAccount=appContext.config['bck_publicKey'],password=password,address="{}:{}".format(ip,port))
        self.appContext=appContext
        self.socket=socket
        self.type=appContext.config['type']
        self.bckContext=bckContext
        self.ssl_version=ssl_version
        self.requestManager=RequestManager(socket)

        self.ssl_socket=None

    def executeAuthentification(self):
        pass


    def makeSslTunnel(self,newsocket,serverSide,bckContrat):
        connstream = ssl.wrap_socket(newsocket,
                                 server_side=serverSide,

                                 ca_certs="{}/{}.pem".format(self.appContext.config['certificat_storage'],bckContrat),
                                 certfile = self.appContext.config['certificat_path'],
                                 keyfile = self.appContext.config['certificat_key_path'],
                                 ssl_version = self.ssl_version,
                                 cert_reqs=ssl.CERT_OPTIONAL)

        self.ssl_socket=connstream
        return connstream

    def readSocket(self):
        data=self.requestManager.receiveMessage()
        return data

    def sendMessage(self,data):
        self.requestManager.sendMessage(data)

    def sendEndMessage(self):
        self.requestManager.sendEndMessage()


    def sendErrorMessage(self):
        self.requestManager.sendErrorMessage(error=RequestManager.AUTHENTICATION_ERROR)

    def readSocket2(self):
        data=""
        while data.endswith("}")==False:
            data =data+ self.socket.recv(1024).strip().decode()
        return data







class BAIIOTClienAuthentificator(BAIIOTBaseAuthentificator):
    def __init__(self,appContext,socket,ssl_version,addressBCkNode,password):
        BAIIOTBaseAuthentificator.__init__(self,appContext=appContext,socket=socket,ssl_version=ssl_version,addressBCkNode=addressBCkNode,password=password)
        #self.appContext=appContext
        #self.socket=socket
        #self.bckContext=bckContext
        self.authHandler=AuthenticationHandler(privateKey=self.appContext.getBCKPrivateKey())
        self.managementRepo=ManagementKeyContractRepository()
        self.keyRepo=KeyContractRepository()
        #self.ssl_version=ssl_version
        self.otherPbkey=None
        self.otherContract=None
        self.otherManagmentContract=None

    def executeAuthentification(self,managementContract):
        self.initiation(managementContract)

        myChallenge=self.second(managementContract)

        self.third(myChallenge)
        self.makeSslTunnel(self.socket,serverSide=False,bckContrat=self.otherContract)
        return self.otherContract

    def initiation(self,managementContractAdress):
        myContrat=self.appContext.config['bck_keyContract']
        instance=BCKContext.getinstance(0)
        #managementContractAdress='0x8A5d5dB78A3dfCBa5FbC9B962Db57a8F09a2DF27'
        myData={'contrat':myContrat,'managementContract':managementContractAdress,'type':self.appContext.config['type']}
        self.sendMessage(myData)
        #myData=json.dumps(myData)
        #self.socket.send(myData.encode())




    def second(self,managementContractAdress):

        data=self.readSocket()
        data=data['data']
        print(data)
        #data=json.loads(data)
        contract=data['contrat']
        challenge=data['challenge']
        myCertificate=self.appContext.getCertificate()
        #verifie la presence du server/gateway
        #val=self.managementRepo.gatewayIsPermited(publicKey=contract,contract_address=managementContractAdress)
        val=self.entityIspermited(publicKey=contract,contract_address=managementContractAdress)
        if val ==False:
            raise ContractNotInMangementContractException()
        self.otherPbkey=self.keyRepo.getPublicKeyUser(contract)
        myChallenge=self.authHandler.generateChallenge(self.otherPbkey)
        #sign le challenge de server/gateway
        message=collections.OrderedDict([('certificat',myCertificate),('challenge',challenge)])
        message=json.dumps(message)
        mySignature=self.authHandler.sign(message)
        myData={'signature':mySignature,'certificat':myCertificate,'challenge':myChallenge}
        self.sendMessage(myData)
        #myData=json.dumps(myData)
        #elf.socket.send(myData.encode())
        self.otherContract=contract
        return myChallenge

    def third(self,myChallenge):
        data=self.readSocket()
        data=data['data']
        print(data)
        signature=data['signature']
        certificate=data['certificat']
        message=collections.OrderedDict([('certificat',certificate),('challenge',myChallenge)])
        message=json.dumps(message)
        val=self.authHandler.validateSignature(message=message,signature=signature,publicKey=self.otherPbkey)
        #val=False
        if val ==False:
            raise InvalideSignatureException()

        self.sendEndMessage()
        certifRepo=self.appContext.getCertificateRepo()
        certifRepo.save(fileName="{}.pem".format(self.otherContract),content=certificate)

    def entityIspermited(publicKey,contract_address):
        pass





class BAIIOTSevertAuthentificator(BAIIOTBaseAuthentificator):
    def __init__(self,appContext,socket,ssl_version,addressBCkNode,password):
        BAIIOTBaseAuthentificator.__init__(self,appContext=appContext,socket=socket,ssl_version=ssl_version,addressBCkNode=addressBCkNode,password=password)

        self.authHandler=AuthenticationHandler(privateKey=self.appContext.getBCKPrivateKey())
        self.managementRepo=ManagementKeyContractRepository()
        self.keyRepo=KeyContractRepository()

        self.otherPbkey=None
        self.otherContract=None
        self.otherCertificate=None
        self.otherManagmentContract=None
        self.otherType=None

    def executeAuthentification(self):
        managementContract=self.initiation()

        myChallenge=self.second(managementContract)
        self.third()
        self.makeSslTunnel(self.socket,serverSide=True,bckContrat=self.otherContract)
        return self.otherContract


    def initiation(self):
        #identifier le type de l'entrant iot ou client
        data=self.readSocket()
        data=data['data']
        contract=data['contrat']

        managementContractAdress=data['managementContract']
        self.otherType=int(data['type'])
        val=self.entityIspermited(publicKey=contract,contract_address=managementContractAdress)
        if val ==False:
            raise ContractNotInMangementContractException()
        pbkey=self.keyRepo.getPublicKeyUser(contract)
        print("entité éxiste")
        myChallenge=self.authHandler.generateChallenge(pbkey)



        myContrat=self.appContext.config['bck_keyContract']

        myData={'contrat':myContrat,'challenge':myChallenge}
        self.sendMessage(myData)
        #myData=json.dumps(myData)
        #self.socket.send(myData.encode())
        self.otherPbkey=pbkey
        self.otherContract=contract
        return myChallenge


    def second(self,myChallenge):
        data=self.readSocket()
        data=data['data']
        print(data)
        certificate=data['certificat']
        signature=data['signature']
        message=collections.OrderedDict([('certificat',certificate),('challenge',myChallenge)])
        message=json.dumps(message)
        challenge=data['challenge']
        #vérifie signature de iot/client
        print("verification de la signature")
        val=self.authHandler.validateSignature(message=message,signature=signature,publicKey=self.otherPbkey)
        print("message:{}".format(message))
        print("pb:{}".format(self.otherPbkey))
        print("sign:{}".format(signature))
        if val ==False:
            raise InvalideSignatureException()

        #signe le challenge de iot/client
        myCertificate=self.appContext.getCertificate()
        message=collections.OrderedDict([('certificat',myCertificate),('challenge',challenge)])
        message=json.dumps(message)
        mySignature=self.authHandler.sign(message)
        myData={'signature':mySignature,'certificat':myCertificate}
        self.sendMessage(myData)
        self.otherCertificate=certificate


    def third(self):
        self.readSocket()
        certifRepo=self.appContext.getCertificateRepo()
        certifRepo.save(fileName="{}.pem".format(self.otherContract),content=self.otherCertificate)

    def entityIspermited(self,publicKey,contract_address):
        pass
