from .Validator import SignatureValidator,SignatureProvider
from .AppContext import AppContext
from .TokenGenerator import TokenGenerator
import sys


from DataLayer.BCKRepository import KeyContractRepository as AuthRepo




#class that handles the different step of the authentication procedure
class AuthenticationHandler:

    def __init__(self,privateKey,signatureValidator=SignatureValidator,tokenGenerator=TokenGenerator,authRepo=AuthRepo,signatureProvider=SignatureProvider):

        self.signatureValidator=signatureValidator()
        self.signatureProvider=signatureProvider(privateKey)
        self.tokenGen=tokenGenerator()
        self.authRepo=authRepo()
        pass


    def generateChallenge(self,publicKey):
        token=self.tokenGen.generateChallengeToken(publicKey)
        return token


    def sign(self,message):
        return self.signatureProvider.sign(message)

    def validateSignature(self,message,signature,publicKey):
        return self.signatureValidator.validate(publicKey=publicKey,token=message,signature=signature)



    def generateAuthentificateToken(self,contract):
        token=self.tokenGen.generateAuthentificateToken(contact)
