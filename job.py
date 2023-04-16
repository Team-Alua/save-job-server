import inspect
import os
import hashlib

class Job:
    def __init__(self):
        self.sourceZip = ""
        self.targetDirectory = ""
        self.listeners = []

    async def process(self, path, data, writer):
        func = getattr(self, path, None)
        if func == None:
            # not found
            pass
        if inspect.isasyncgenfunction(func):
            await func(data, writer)
        else:
            func(data, writer)
    
    def addSource(self, zipName):
        self.sourceZip = zipName

    def addTarget(self, targetDirectory):
        self.targetDirectory = targetDirectory

    def getSource(self):
        return self.sourceZip

    def getFile(self, relativePath, mode):
        targetFilePath = os.path.join(self.targetDirectory, relativePath)
        return open(targetFilePath, mode)

    def addNotifyListener(self, listener):
        self.listeners.append(listener)
    
    async def notifyListeners(self, data):
        for listener in listeners:
            try:
                if inspect.isasyncgenfunction(listener):
                    await listener(data)
                else:
                    listener(data)
            except Exception:
                pass

    async def upload(self, data, writer): 
        pass
    
    async def verify(self, data, writer):
        referenceHash = data.get("hash", "")
        if referenceHash == "":
            # Bad hash
            return
        m = hashlib.md5()
        fh = self.getFile(data.get("file"), "rb")
        while True:
            data = fh.read(65536)
            if not data:
                break
            m.update(data)
        foundHash = m.hexdigest().decode('ascii')
        if referenceHash != foundHash:
            # File hash do not match
            return

    async def notify(self, data, writer):
        await notifyListeners(self, {
            "type": "NOTIFY",
            "message": data.get("msg", "")
        })

    async def complete(self, data, writer):
        await notifyListeners(self, {
            "type": "COMPLETE",
            "path": self.targetDirectory
            "error": data.get("error", "")
        })

    
