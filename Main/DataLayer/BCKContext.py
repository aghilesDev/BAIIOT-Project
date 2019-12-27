from web3 import Web3,eth,personal


#Module that contains the BCKContext class which contains the context of the connection with the BlockChaine
#It's Implemented with Factory pattern to avoid creating multiple-connections with the Blockchain
class BCKContext :
    _instance=None

    def __init__(self):
        raise Exception("it's A factory for an instance call DBContext.getinstance()");


    @classmethod
    def getinstance(cls,indice=0,password='prg2014',address="127.0.0.1:8545"):

        if cls._instance is None:
            #connect the web3 instance to a Node of the blockchaine
            cls._instance = Web3(Web3.HTTPProvider("http://{}".format(address)))
            #unlock the account
            if cls._instance.personal.unlockAccount(cls._instance.eth.accounts[indice], password):
                #the server use the account of index 0 which have been unlocked
                cls._instance.eth.defaultAccount=cls._instance.eth.accounts[indice]

        return cls._instance

    @classmethod
    def getRawinstance(cls,newAccount,password='prg2014',address="127.0.0.1:8545"):

        if cls._instance is None:
            #connect the web3 instance to a Node of the blockchaine
            cls._instance = Web3(Web3.HTTPProvider("http://{}".format(address)))
            #unlock the account
            if cls._instance.personal.unlockAccount(newAccount, password):
                #the server use the account of index 0 which have been unlocked
                #cls._instance.personal.lockAccount(cls._instance.eth.defaultAccount)
                cls._instance.eth.defaultAccount=newAccount

        return cls._instance

    @classmethod
    def  setAccount(cls,indice,password='prg2014'):
        if cls._instance is None:
            return
        account=cls._instance.eth.defaultAccount
        if cls._instance.personal.unlockAccount(cls._instance.eth.accounts[indice], password):
            #the server use the account of index 0 which have been unlocked
            cls._instance.personal.lockAccount(account)
            cls._instance.eth.defaultAccount=cls._instance.eth.accounts[indice]


    @classmethod
    def  setRawAccount(cls,newAccount,password='prg2014'):
        if cls._instance is None:
            return
        account=cls._instance.eth.defaultAccount
        cls._instance.eth.defaultAccount=newAccount
        if cls._instance.personal.unlockAccount(cls._instance.eth.accounts[indice],password):
            #the server use the account of index 0 which have been unlocked
            cls._instance.personal.lockAccount(account)
            cls._instance.eth.defaultAccount=cls._instance.eth.accounts[indice]
