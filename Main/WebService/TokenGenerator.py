from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .AppContext import AppContextFactory


#TokenGenerator is a class wich handle the generation,validation and decryptage of challange tokens and authentication tokens
class TokenGenerator:
    def generateChallengeToken(self,publicKey,expiration=3600):
        s = Serializer(AppContextFactory.getinstance().config['secret_key'], expiration)
        return s.dumps({'publicKey': publicKey,'authentified':False}).decode('utf-8')

    def generateAuthentificationToken(self,contrat,expiration=3600):
        s = Serializer(AppContextFactory.getinstance.config['secret_key'], expiration)
        return s.dumps({'Contrat': contrat  ,'authentified':True}).decode('utf-8')


    def decryptToken(self,token):
        token=token.encode('utf-8')
        s = Serializer(AppContextFactory.getinstance.config['secret_key'])
        try:
            data = s.loads(token)
        except:
            return None
        return data

    def verifyChallengeToken(self,token):
        data=self.decryptToken(token=token)
        if data == None:
            return False
        if data.get('authentified') == True:
            return False
        return True

    def verifyAuthentificationToken(self,token):
        data=self.decryptToken(token=token)
        if data == None:
            return False
        if data.get('authentified') == False:
            return False
        return True
