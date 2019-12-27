from WebService.AppContext import AppContextFactory
from WebService.IOTAuthentificator import GatewayAuthentificator
from WebService.AppContext import AppContextFactory
from WebService.ConnectionContext import ConnectionContextFactory
from WebService.RequestManager import RequestManager,RequestStreamManager,RequestRawStreamManager
from WebService.Constante import EntityType
from CustomException import BAIIOTException,RequestException
import socketserver
import json
from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler
import ssl,sys
import numpy as np
import cv2
import socket
import sys
import pickle
import struct ## new
import zlib
import os,sys
from threading import Thread

serverCtx=AppContextFactory.getinstance("DataServer/self/config.json")



class CustomServer(socketserver.StreamRequestHandler):


    def handle(self):



        print('Socket created')

        print('Socket bind complete')

        print('Socket now listening')

        (addr,port)=self.request.getpeername()
        type=self.server.connectionContext.getType(addr,port)
        self.frames=[]
        if type==EntityType._CLIENT:
            self.handelClientRequest()
        elif type==EntityType._IOT:
            self.handelIotRequest()



        return

    def finish(self):
        print('finish')
        (addr,port)=self.request.getpeername()
        self.server.connectionContext.removeSocket(addr,port)






    def handelClientRequest(self):
        self.requestManager=RequestManager(self.request)
        self.streamManager=RequestRawStreamManager(socket=self.request,rfile=self.rfile,wfile=self.wfile)
        data=self.requestManager.receiveMessage()
        data=data['data']
        iotContrat=data['iotContrat']
        (addr,port)=self.server.connectionContext.getaddress(contrat=iotContrat)
        self.server.connectionContext.addToViwers(requestHandler=self,addr=addr,port=port)
        while True:
            if len(self.frames)>0:
                frame=self.frames[len(self.frames)-1]
                self.frames=[]
                self.streamManager.sendMessage(frame)

    def addFrame(self,frame):
        self.frames.append(frame)

    def SendMessage(self,data):
        self.streamManager.sendMessage(data)

    def handelIotRequest(self):
        self.requestManager=RequestManager(self.request)
        self.streamManager=RequestRawStreamManager(socket=self.request,rfile=self.rfile,wfile=self.wfile)
        (addr,port)=self.request.getpeername()
        while True:
            data=self.streamManager.receiveMessage()
            code=data['code']
            data=data['data']



            viewers=self.server.connectionContext.getViwers(addr=addr,port=port)
            for keys in viewers.keys():
                handler=viewers[keys]
                handler.addFrame(data)



        #enregistrer le certificat de l'entité dans serverCtx.config['certificat_storage'] sous le nom de contrat
        #créer un authentification token avec durée en utilisant contrat et managementContractAdress pour le contre d'accés
        return

class My_TCPServer(TCPServer):

    def __init__(self,server_address,RequestHandlerClass,ssl_version=ssl.PROTOCOL_TLSv1_2,bind_and_activate=True,appContext=AppContextFactory.getinstance("DataServer/self/config.json"),connectionContext=ConnectionContextFactory.getinstance()):
        TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.ssl_version = ssl_version
        self.appContext=appContext
        self.connectionContext=connectionContext





    def get_request(self):
        newsocket, fromaddr = self.socket.accept()
        addressBCkNode=("127.0.0.1",8545)
        authentificator=GatewayAuthentificator  (appContext=self.appContext,socket=newsocket,ssl_version=self.ssl_version,addressBCkNode=addressBCkNode)
        try:
            bckContrat=authentificator.executeAuthentification();
        except BAIIOTException as exception:
            authentificator.sendErrorMessage()
        except RequestException as exception:
            print("authentication failed")
        else:

            newsocket = authentificator.ssl_socket


            print("{}/{}.pem".format(self.appContext.config['certificat_storage'],bckContrat))
            (addr,port)=newsocket.getpeername()
            self.connectionContext.addSocket(addr,port,authentificator.otherContract,authentificator.otherType)
        return newsocket, fromaddr

    def verify_request(self,request, client_address):
        print("list of sockets:\n{}".format(self.connectionContext.info))
        (addr,port)=client_address
        exist=self.connectionContext.socketExist(addr,port)
        print(exist)
        return exist

    def handle_error(self,request, client_address):
        TCPServer.handle_error(self,request, client_address)
        (addr,port)=client_address
        self.connectionContext.removeSocket(addr,port)
        print("Nope")




class ThreadedCustomServer(socketserver.ThreadingMixIn,My_TCPServer):
    pass

ThreadedCustomServer((sys.argv[1], int(sys.argv[2])), CustomServer).serve_forever()


#NEW



class MySSL_TCPServer(TCPServer):
    def __init__(self,server_address,RequestHandlerClass,certfile,keyfile,ssl_version=ssl.PROTOCOL_TLSv1,bind_and_activate=True):
        TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version

    def get_request(self):
        newsocket, fromaddr = self.socket.accept()
        connstream = ssl.wrap_socket(newsocket,
                                 server_side=True,

                                 ca_certs='client.pem',
                                 certfile = self.certfile,
                                 keyfile = self.keyfile,
                                 ssl_version = self.ssl_version,
                                 cert_reqs=ssl.CERT_OPTIONAL)
        return connstream, fromaddr




class MySSL_ThreadingTCPServer(ThreadingMixIn, MySSL_TCPServer): pass

class testHandler(StreamRequestHandler):
    def handle(self):
        data = self.connection.recv(4096)
        print("client certificate:\n {}".format(ssl.DER_cert_to_PEM_cert(self.request.getpeercert(binary_form=True))))
        self.wfile.write(data)
