#-*- coding: utf-8 -
import web3
from web3.auto import w3
from eth_account.messages import defunct_hash_message





# SignatureValidator class validate the signature of a message using the public key of the source,the message and the signature
class SignatureValidator:




    def validate(self,publicKey,token,signature):
        message_hash = defunct_hash_message(text=token)
        result=w3.eth.account.recoverHash(message_hash, signature=signature)
        #print('resultat {}\n clé:{}'.format(result,publicKey))
        if(result==publicKey):
            return True
        print("{} != {}".format(result,publicKey))
        return False



# SignatureProvider class emit a signature oh a message using the a privateKey
class SignatureProvider:

    def __init__(self,privateKey):
        self._privateKey=privateKey
    def _to_32byte_hex(self,val):
    	return w3.toHex(w3.toBytes(val).rjust(32, b'\0'))

    def sign(self,message):
        message_hash = defunct_hash_message(text=message)
        signed_message = w3.eth.account.signHash(message_hash, private_key=self._privateKey)
        return self._to_32byte_hex(signed_message.signature)
