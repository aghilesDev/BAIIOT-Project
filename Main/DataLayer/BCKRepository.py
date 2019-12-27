from .BCKContext import BCKContext
from solc import compile_source
from web3.contract import ConciseContract
import json
import web3




class ContractRepository:
    def __init__(self):
        #We get an instance of the connection context with the blockchaine
        self.context=BCKContext.getinstance()


#class that handles the communication with the contracts
class ManagementKeyContractRepository(ContractRepository):
    def __init__(self):
        #We get an instance of the connection context with the blockchaine
        ContractRepository.__init__(self)
        #Compiling the code of the contract to have his ABI of
        contract_source_code = '''
        pragma solidity 0.4.25;
        contract ManagementKeyContract {

        address owner;
        mapping (address => bool) public users;
        mapping (address => bool) public iots;
        mapping (address => bool) public servers;
        mapping (address => bool) public gateways;




        constructor () public{
            owner=msg.sender;
            }




            function addUser(address user) public returns(bool){
            if(msg.sender != owner) return false;
            users[user]=true;
            return true;
            }

            function addIot(address iotAddress) public returns(bool){
            if(msg.sender != owner) return false;
            iots[iotAddress]=true;
            return true;
            }

            function addServer(address server) public returns(bool){
            if(msg.sender != owner) return false;
            servers[server]=true;
            return true;
            }

            function addGateway(address gateway) public returns(bool){
            if(msg.sender != owner) return false;
            gateways[gateway]=true;
            return true;
            }



            function removeUser(address user) public returns(bool){
            if(msg.sender != owner) return false;
            users[user]=false;
            return true;
            }

            function removeIot(address iotAddress) public returns(bool){
            if(msg.sender != owner) return false;
            iots[iotAddress]=false;
            return true;
            }

    function removeServer(address server) public returns(bool){
        if(msg.sender != owner) return false;
        servers[server]=false;
        return true;
    }

     function removeGateway(address gateway) public returns(bool){
        if(msg.sender != owner) return false;
        gateways[gateway]=false;
        return true;
    }


        function userIsPermited(address user) view public returns(bool){

            return users[user];
        }



        function ServerIsPermited(address server) view public returns(bool){
            return servers[server];
        }



        function iotIsPermited(address iotAddress) view public returns(bool){
            if(iots[iotAddress]==true)
                return (true);
            else
                return false;
        }

        function gatewayIsPermited(address gateway) view public returns(bool){
            if(gateways[gateway]==true)
                return true;
            else
                return false;
        }



        function setOwner(address newOwner) public returns(bool){
            if(msg.sender != owner) return true;
            owner=newOwner;
            return false;
            }

        function getPublicKeyUser() view public returns(address){
            return(owner);
        }

    }


        '''
        compiled_sol = compile_source(contract_source_code)
        self.contract_interface = compiled_sol['<stdin>:ManagementKeyContract']


    def userIsPermited(self,publicKey,contract_address=None):
        #make a a contract instance which is an interface to communicate with the contract using the address of the contract and his ABI
        contract_instance = self.context.eth.contract(abi=self.contract_interface['abi'], address=contract_address)
        message=contract_instance.functions.userIsPermited(publicKey).call()
        return message

    def serverIsPermited(self,publicKey,contract_address=None):
        #make a a contract instance which is an interface to communicate with the contract using the address of the contract and his ABI
        contract_instance = self.context.eth.contract(abi=self.contract_interface['abi'], address=contract_address)
        message=contract_instance.functions.ServerIsPermited(publicKey).call()
        return message

    def iotIsPermited(self,publicKey,contract_address=None):
        #make a a contract instance which is an interface to communicate with the contract using the address of the contract and his ABI
        contract_instance = self.context.eth.contract(abi=self.contract_interface['abi'], address=contract_address)
        message=contract_instance.functions.iotIsPermited(publicKey).call()
        return message


    def gatewayIsPermited(self,publicKey,contract_address=None):
        #make a a contract instance which is an interface to communicate with the contract using the address of the contract and his ABI
        contract_instance = self.context.eth.contract(abi=self.contract_interface['abi'], address=contract_address)
        message=contract_instance.functions.gatewayIsPermited(publicKey).call()
        return message


    def addServer(self,publicKey,contract_address=None):
        #make a a contract instance which is an interface to communicate with the contract using the address of the contract and his ABI
        contract_instance = self.context.eth.contract(abi=self.contract_interface['abi'], address=contract_address)
        message=contract_instance.functions.addServer(publicKey).call()
        tx_hash=contract_instance.functions.addServer(publicKey).transact()
        tx_receipt = self.context.eth.waitForTransactionReceipt(tx_hash)
        return message

    def addUser(self,publicKey,contract_address=None):
        #make a a contract instance which is an interface to communicate with the contract using the address of the contract and his ABI
        contract_instance = self.context.eth.contract(abi=self.contract_interface['abi'], address=contract_address)
        message=contract_instance.functions.addUser(publicKey).call()
        tx_hash=contract_instance.functions.addUser(publicKey).transact()
        tx_receipt = self.context.eth.waitForTransactionReceipt(tx_hash)
        return message

    def addIot(self,publicKey,contract_address=None):
        #make a a contract instance which is an interface to communicate with the contract using the address of the contract and his ABI
        contract_instance = self.context.eth.contract(abi=self.contract_interface['abi'], address=contract_address)
        message=contract_instance.functions.addIot(publicKey).call()
        tx_hash=contract_instance.functions.addIot(publicKey).transact()
        tx_receipt = self.context.eth.waitForTransactionReceipt(tx_hash)
        return message


    def addGateway(self,publicKey,contract_address=None):
        #make a a contract instance which is an interface to communicate with the contract using the address of the contract and his ABI
        contract_instance = self.context.eth.contract(abi=self.contract_interface['abi'], address=contract_address)
        message=contract_instance.functions.addGateway(publicKey).call()
        tx_hash=contract_instance.functions.addGateway(publicKey).transact()
        tx_receipt = self.context.eth.waitForTransactionReceipt(tx_hash)
        return message


    def removeServer(self,publicKey,contract_address=None):
        #make a a contract instance which is an interface to communicate with the contract using the address of the contract and his ABI
        contract_instance = self.context.eth.contract(abi=self.contract_interface['abi'], address=contract_address)
        message=contract_instance.functions.removeServer(publicKey).call()
        tx_hash=contract_instance.functions.removeServer(publicKey).transact()
        tx_receipt = self.context.eth.waitForTransactionReceipt(tx_hash)
        return message

    def removeUser(self,publicKey,contract_address=None):
        #make a a contract instance which is an interface to communicate with the contract using the address of the contract and his ABI
        contract_instance = self.context.eth.contract(abi=self.contract_interface['abi'], address=contract_address)
        message=contract_instance.functions.removeUser(publicKey).call()
        tx_hash=contract_instance.functions.removeUser(publicKey).transact()
        tx_receipt = self.context.eth.waitForTransactionReceipt(tx_hash)
        return message

    def removeIot(self,publicKey,contract_address=None):
        #make a a contract instance which is an interface to communicate with the contract using the address of the contract and his ABI
        contract_instance = self.context.eth.contract(abi=self.contract_interface['abi'], address=contract_address)
        message=contract_instance.functions.removeIot(publicKey).call()
        tx_hash=contract_instance.functions.removeIot(publicKey).transact()
        tx_receipt = self.context.eth.waitForTransactionReceipt(tx_hash)
        return message


    def removeGateway(self,publicKey,contract_address=None):
        #make a a contract instance which is an interface to communicate with the contract using the address of the contract and his ABI
        contract_instance = self.context.eth.contract(abi=self.contract_interface['abi'], address=contract_address)
        message=contract_instance.functions.removeGateway(publicKey).call()
        tx_hash=contract_instance.functions.removeGateway(publicKey).transact()
        tx_receipt = self.context.eth.waitForTransactionReceipt(tx_hash)
        return message

    def deployContract(self):
        contract = self.context.eth.contract(abi=self.contract_interface['abi'], bytecode=self.contract_interface['bin'])
        tx_hash=contract.constructor().transact()
        tx_receipt = self.context.eth.waitForTransactionReceipt(tx_hash)
        contract_address = tx_receipt['contractAddress']
        print("adresse contrat : {}".format(contract_address))
        return {contract_address:'ManagementKeyContract'}


    def getOwner(self,contract_address=None):
        #make a a contract instance which is an interface to communicate with the contract using the address of the contract and his ABI
        contract_instance = self.context.eth.contract(abi=self.contract_interface['abi'], address=contract_address)
        message=contract_instance.functions.getPublicKeyUser().call()
        return message






class KeyContractRepository(ContractRepository):
    def __init__(self):
        #We get an instance of the connection context with the blockchaine
        ContractRepository.__init__(self)
        #Compiling the code of the contract to have his ABI of
        contract_source_code = '''
        pragma solidity 0.4.25;
        contract KeyContract {
        address owner;

        constructor () public{
            owner=msg.sender;
        }

        function getPublicKeyUser() view public returns(address){
            return(owner);
        }



        function setOwner(address newOwner) public returns(bool){
            if(msg.sender != owner) return false;
            owner=newOwner;
            return true;
        }


        }
        '''
        compiled_sol = compile_source(contract_source_code)
        self.contract_interface = compiled_sol['<stdin>:KeyContract']



    def getPublicKeyUser(self,contract_address):
        #make a a contract instance which is an interface to communicate with the contract using the address of the contract and his ABI
        contract_instance = self.context.eth.contract(abi=self.contract_interface['abi'], address=contract_address)
        message=contract_instance.functions.getPublicKeyUser().call()
        return message

    def setOwner(self,contract_address,publicKey):
        contract_instance = self.context.eth.contract(abi=self.contract_interface['abi'], address=contract_address)
        message=contract_instance.functions.setOwner(publicKey).call()
        tx_hash=contract_instance.functions.setOwner(publicKey).transact()
        tx_receipt = self.context.eth.waitForTransactionReceipt(tx_hash)
        return message

    def deployContract(self):
        contract = self.context.eth.contract(abi=self.contract_interface['abi'], bytecode=self.contract_interface['bin'])
        tx_hash=contract.constructor().transact()
        tx_receipt = self.context.eth.waitForTransactionReceipt(tx_hash)
        contract_address = tx_receipt['contractAddress']
        print("adresse contrat : {}".format(contract_address))
        return {contract_address:'KeyContract'}
