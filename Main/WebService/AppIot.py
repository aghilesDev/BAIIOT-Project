from WebService.AppContext import AppContextFactory
from WebService.IOTAuthentificator import ToGatewayAuthentificator,IOTAuthentificator
from CustomException import BAIIOTException,RequestException
from WebService.RequestManager import RequestManager,RequestStreamManager
from WebService.Constante import CameraCommand
import socket,ssl
import time,cv2,base64
import zlib
import sys
from threading import Thread




class IOTOrderIterator:
    def __init__(self,appContext):
        self.appContext=appContext
        self.iterator=None

    def _executeAuthentication(self,sock,managementContractAdress,addressBCkNode,password):
        authentificator=IOTAuthentificator(appContext=self.appContext,socket=sock,ssl_version=ssl.PROTOCOL_TLSv1_2,addressBCkNode=addressBCkNode,password=password)
        try:
            bckContrat=authentificator.executeAuthentification();
        except BAIIOTException as exception:
            print('error')
            authentificator.sendErrorMessage()
        except RequestException as exception:
            print("authentication failed")
        else:
            return authentificator



    def execute(self,s,managementContractAdress,addressBCkNode,password):
        #s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.connect(address)
        authentificator=self._executeAuthentication(s,managementContractAdress,addressBCkNode=addressBCkNode,password=password)
        s=authentificator.ssl_socket
        requestManager=RequestManager(s)
        data=requestManager.receiveMessage()
        print("data received")
        data=data['data']
        command=data['command']
        if command == CameraCommand._START_RECORD:
            if self.iterator == None:
                self.startRecord()
        elif command == CameraCommand._STOP_RECORD:
            if self.iterator !=None:
                self.stopRecord()
        elif command == CameraCommand._START_SAVE:
            adress=data['address']
            (ip,port)=address
            self.startSave(ip,port)
        elif command == CameraCommand._STOP_SAVE:
            pass
        else:
            return True

    def startRecord(self):
        gatewayAdress=str.split(self.appContext.config["gateway_address"],":")
        gatewayAdress=(gatewayAdress[0],int(gatewayAdress[1]))
        print("je commence enregistremant")
        addressBCkNode=str.split(self.appContext.config["bck_node_address"],":")
        addressBCkNode=(addressBCkNode[0],int(addressBCkNode[1]))
        self.iterator=IOTStreamIterator(appContext=clientCtx,address=gatewayAdress,managementContractAdress=self.appContext.config["bck_managementKeyContract"],iotContract="0x058eEf27243B26aAa247862daAB4cfc8f0EC34e9",addressBCkNode=addressBCkNode,password=None)
        self.iterator.start()

    def stopRecord(self):
        self.iterator.stop()
        self.iterator=None


    def startSave(self,ip,port):
        pass







class IOTStreamIterator(Thread):
    def __init__(self,appContext,address,managementContractAdress,iotContract,addressBCkNode,password):
        Thread.__init__(self)
        self.appContext=appContext
        self.running=True
        self.finish=False
        self.appContext=appContext
        self.address=address
        self.managementContractAdress=managementContractAdress
        self.iotContract=iotContract
        self.addressBCkNode=addressBCkNode
        self.password=password

    def _executeAuthentication(self,sock,managementContractAdress,addressBCkNode,password):
        authentificator=ToGatewayAuthentificator(appContext=self.appContext,socket=sock,ssl_version=ssl.PROTOCOL_TLSv1_2,addressBCkNode=addressBCkNode,password=password)
        try:
            bckContrat=authentificator.executeAuthentification(managementContractAdress);
        except BAIIOTException as exception:
            print('error')
            authentificator.sendErrorMessage()
        except RequestException as exception:
            print("authentication failed")
        else:
            return authentificator



    def execute(self,address,managementContractAdress,iotContract,addressBCkNode,password):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(address)
        authentificator=self._executeAuthentication(s,managementContractAdress,addressBCkNode=addressBCkNode,password=password)
        s=authentificator.ssl_socket
        requestManager=RequestManager(s)
        rfile=s.makefile('rb')
        wfile=s.makefile('wb')
        self.streamManager=RequestStreamManager(socket=s,rfile=rfile,wfile=wfile)


        cam = cv2.VideoCapture(0)

        cam.set(3, 640);
        cam.set(4, 480);


        while self.running:

            ret, frame = cam.read()

            self.streamManager.sendMessage(frame)
            time.sleep(0.2)

        self.finish=True


    def run(self):
        self.execute(address=self.address,managementContractAdress=self.managementContractAdress,iotContract=self.iotContract,addressBCkNode=self.addressBCkNode,password=self.password)

    def stop(self):
        self.running=False
        while self.finish==False:
            time.sleep(0.2)
        self.streamManager.sendEndMessage()
        return True






#clientCtx=AppContextFactory.getinstance("DataIot/self/config.json")
#ip=sys.argv[1]
#port=int(sys.argv[2])
#iterator=IOTStreamIterator(appContext=clientCtx)
#addressBCkNode=("127.0.0.1",8545)
#iterator.execute(address=(ip,port),managementContractAdress='0xA371D157fB34b21F98E48407d2f8D6DC6E0e43a9',iotContract="0x058eEf27243B26aAa247862daAB4cfc8f0EC34e9",addressBCkNode=addressBCkNode,password=None)


clientCtx=AppContextFactory.getinstance("DataIot/self/config.json")
#ip=sys.argv[1]
#port=int(sys.argv[2])
iterator=IOTOrderIterator(appContext=clientCtx)
addressBCkNode=str.split(clientCtx.config["bck_node_address"],":")#("127.0.0.1",8545)
addressBCkNode=(addressBCkNode[0],int(addressBCkNode[1]))
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(("",4142))
s.listen(0)
while True:


    (sock,address)=s.accept()
    iterator.execute(s=sock,managementContractAdress=clientCtx.config["bck_managementKeyContract"],addressBCkNode=addressBCkNode,password=None)
    sock.close()
print("faire autre chose#######################################################")
