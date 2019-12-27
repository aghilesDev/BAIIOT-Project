import json
from DataLayer.FileRepository import FileRepository
from web3.auto import w3

class AppContextFactory:
    _instance=None

    def __init__(self):
        raise Exception("it's A factory for an instance call AppContextFactory.getinstance()");


    @classmethod
    def getinstance(cls,configFile=""):
        if cls._instance is None:
            cls._instance=AppContext(configFile)
        return cls._instance


class AppContext:
    """docstring for AppContext."""


    def __init__(self,configFile):
        with open(configFile) as json_file:
            self.config=json_file.read()
            self.config=json.loads(self.config)
            self.certificateRepo=FileRepository(self.config['certificat_storage'])


    def getCertificateRepo(self):
        return self.certificateRepo


    def getCertificate(self):
        file=open(self.config['certificat_path'],"r")
        content=file.read()
        return content





    def getBCKPrivateKey(self):
        privateKey=None
        with open(self.config['bck_privateKey_path']) as keyfile:#change le chemin vers le dossier de ta clé privée
        	encrypted_key = keyfile.read()
        try:
        	privateKey = w3.eth.account.decrypt(encrypted_key, self.config['bck_password'])
        except ValueError:
        	print("mot de passe invalide")
        return privateKey
