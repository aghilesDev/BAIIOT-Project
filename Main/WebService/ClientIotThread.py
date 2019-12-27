from threading import Thread

class ClientThread(Thread):
    pass

class IotThread(Thread):
    def __init__(self,iterator,**kwargs):
        slef.iterator=iterator
        self.kwargs=kwargs
    def run(self):
        self.iterator.execute()
