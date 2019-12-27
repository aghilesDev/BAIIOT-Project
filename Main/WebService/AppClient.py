from WebService.AppContext import AppContextFactory
from WebService.IOTAuthentificator import ToGatewayAuthentificator,ToIOTAuthentificator
from CustomException import BAIIOTException,RequestException
from WebService.RequestManager import RequestManager,RequestStreamManager
from WebService.Constante import CameraCommand
import socket,ssl
import time,cv2,base64
import zlib
import sys
from threading import Thread



class ClientOrderIterator:
    def __init__(self,appContext):
        self.appContext=appContext

    def _executeAuthentication(self,sock,managementContractAdress,addressBCkNode,password):
        authentificator=ToIOTAuthentificator(appContext=self.appContext,socket=sock,ssl_version=ssl.PROTOCOL_TLSv1_2,addressBCkNode=addressBCkNode,password=password)
        try:
            bckContrat=authentificator.executeAuthentification(managementContractAdress);
        except BAIIOTException as exception:
            print('error')
            authentificator.sendErrorMessage()
        except RequestException as exception:
            print("authentication failed")
        else:
            return authentificator



    def execute(self,address,managementContractAdress,command,addressBCkNode,password):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(address)
        authentificator=self._executeAuthentication(s,managementContractAdress,addressBCkNode=addressBCkNode,password=password)
        s=authentificator.ssl_socket
        requestManager=RequestManager(s)
        requestManager.sendMessage(command)
        requestManager.receiveMessage()
        return True









class CilentStreamIterator:
    def __init__(self,appContext,view_CallBack):
        self.appContext=appContext
        self.view_CallBack=view_CallBack

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
        requestManager.sendMessage({'iotContrat':iotContract})
        rfile=s.makefile('rb')
        wfile=s.makefile('wb')
        streamManager=RequestStreamManager(socket=s,rfile=rfile,wfile=wfile)
        while True:
            data= streamManager.receiveMessage()
            data = data['data']
            self.view_CallBack.setStreamView(frame=data)




class ClientStreamView:
    def __init__(self):
        clientCtx=AppContextFactory.getinstance("DataClient/self/config.json")
        self.ip=sys.argv[1]
        self.port=int(sys.argv[2])
        self.password=sys.argv[3]
        self.iterator=CilentStreamIterator(appContext=clientCtx,view_CallBack=self)


    def setStreamView(self,frame):
        cv2.imshow('Client',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass
    def onAction(self):
        addressBCkNode=("192.168.43.208",8545)
        print("visio")
        self.iterator.execute(address=(self.ip,self.port),managementContractAdress='0xA371D157fB34b21F98E48407d2f8D6DC6E0e43a9',iotContract="0x058eEf27243B26aAa247862daAB4cfc8f0EC34e9",addressBCkNode=addressBCkNode,password=self.password)


view=ClientStreamView()
t=Thread(target=view.onAction)
t.start()

#clientCtx=AppContextFactory.getinstance("DataClient/self/config.json")
#ip=sys.argv[1]
#port=int(sys.argv[2])
#password=sys.argv[3]
#iterator=ClientOrderIterator(appContext=clientCtx)
#addressBCkNode=("127.0.0.1",8545)
#command={'command': CameraCommand._START_RECORD}
#command={'command': CameraCommand._STOP_RECORD}

#iterator.execute(address=(ip,port),command=command,managementContractAdress='0xA371D157fB34b21F98E48407d2f8D6DC6E0e43a9',   addressBCkNode=addressBCkNode,password=password)
