from CustomException import RequestException,RequestAuthException,RequestAccessException
import json
import struct
import pickle


class RequestManager(object):

    AUTHENTICATION_ERROR=1
    ACCESS_ERROR=2
    REQUEST_OK=200
    REQUEST_END=250
    REQUEST_AUTH_ERROR=401
    REQUEST_ACCESS_ERROR=403

    """docstring for RequestManager."""
    def __init__(self,socket):
        self.socket=socket
        self.data=""

    def send(self,data):
        data=json.dumps(data)
        self.socket.send(data.encode())


    def receive(self):
        end=self._findEndRequest()
        while end==-1:
            self.data =self.data+ self.socket.recv(1024).strip().decode()
            end=self._findEndRequest()
        end=end+1
        data=self.data[:end]
        self.data=self.data[end:]
        data=json.loads(data)
        return data

    def sendMessage(self,data):
        data={'code':RequestManager.REQUEST_OK,'data':data}
        self.send(data)

    def sendErrorMessage(self,error):
        if error==RequestManager.AUTHENTICATION_ERROR:
            data={'code':RequestManager.REQUEST_AUTH_ERROR}
        elif error==RequestManager.ACCESS_ERROR:
            data={'code':RequestManager.REQUEST_ACCESS_ERROR}
        else:
            print('request not send')
            return
        self.send(data)


    def sendEndMessage(self):
        data={'code':RequestManager.REQUEST_END,'data':None}
        self.send(data)


    def _findEndRequest(self):
        begin=0
        end=0
        for i in range(len(self.data)):
            char=self.data[i]
            if char=="{":
                begin=begin+1
            elif char=="}":
                end=end+1

            if begin==end and begin !=0:
                return i
        return -1


    def receiveMessage(self):
        data=self.receive()
        code=data['code']
        if code== RequestManager.REQUEST_OK or code== RequestManager.REQUEST_END:
            return data
        elif code==RequestManager.REQUEST_AUTH_ERROR:
            raise RequestAuthException()
        elif  code==RequestManager.REQUEST_ACCESS_ERROR:
            raise RequestAccessException()
        raise RequestException()


class RequestStreamManager(RequestManager):

    def __init__(self,socket,rfile,wfile):
        RequestManager.__init__(self,socket)
        self.data=b""
        self.rfile=rfile
        self.wfile=wfile

    def send(self,data):
        code=data['code']
        data=data['data']
        data = pickle.dumps(data, 0)
        size = len(data)
        self.socket.sendall(struct.pack(">L", code)+struct.pack(">L", size) + data)


    def receive(self):
        payload_size = struct.calcsize(">L")
        payload_size=payload_size
        while len(self.data)<(payload_size*2):
            self.data+= self.socket.recv(30000)

        code=self.data[:payload_size]
        self.data=self.data[payload_size:]

        data_size=self.data[:payload_size]
        self.data=self.data[payload_size:]

        data_size=struct.unpack(">L",data_size)[0]
        code=struct.unpack(">L",code)[0]


        while len(self.data)<data_size:
            self.data+= self.socket.recv(30000)
        data=self.data[:data_size]
        self.data=self.data[data_size:]
        data=pickle.loads(data, fix_imports=True, encoding="bytes")
        data={'code':code,'data':data}

        return data



class RequestRawStreamManager(RequestManager):

    def __init__(self,socket,rfile,wfile):
        RequestManager.__init__(self,socket)
        self.data=b""
        self.rfile=rfile
        self.wfile=wfile

    def send(self,data):
        code=data['code']
        data=data['data']
        #data = pickle.dumps(data, 0)
        size = len(data)
        self.socket.sendall(struct.pack(">L", code)+struct.pack(">L", size) + data)


    def receive(self):
        payload_size = struct.calcsize(">L")
        payload_size=payload_size
        while len(self.data)<(payload_size*2):
            self.data+= self.socket.recv(30000)

        code=self.data[:payload_size]
        self.data=self.data[payload_size:]

        data_size=self.data[:payload_size]
        self.data=self.data[payload_size:]

        data_size=struct.unpack(">L",data_size)[0]
        code=struct.unpack(">L",code)[0]


        while len(self.data)<data_size:
            self.data+= self.socket.recv(30000)
        data=self.data[:data_size]
        self.data=self.data[data_size:]
        #data=pickle.loads(data, fix_imports=True, encoding="bytes")
        data={'code':code,'data':data}

        return data
