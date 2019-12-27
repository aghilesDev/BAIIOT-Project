class FileRepository:
    def __init__(self,filePath="."):
        self.path=filePath

    def save(self,fileName,content):
        with open("{}/{}".format(self.path,fileName),"w") as file:
            file.write(content)

    def read(self,fileName):
        content=None
        with open("{}/{}".format(self.path,fileName),"w") as file:
            content=file.read()
        return content
