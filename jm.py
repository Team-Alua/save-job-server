import job
import os
import random
import string

def generateNewDirectory():
    dirName = ''.join(random.choices(string.ascii_uppercase, k=10))
    os.makedirs('./' + dirName)
    return dirName

class JobManager:
    def __init__(self):
        self.handlers = {}
        self.jobs = {}
        self.listeners = []
        self.initHandlers()

    def initHandlers(self):
        self.addHandler('/add', self, self.addJob)
        self.addHandler('/remove', self, self.removeJob)
        self.addHandler('/job', self, self.processJob)
    
    def addHandler(self, handlerPath, handleObj, handleFunc):
        self.handlers[handlerPath] = (handleObj, handleFunc)

    def addJobListener(self, keyset, listener):
        self.listeners.append((keyset, listener))

    async def process(self, path, data, writer):
        for handlerPath, handEntry in self.handlers:
            (handleObj, handleFunc) = handEntry
            if path.startswith(handlerPath):
                subPath = path[len(handlerPath) + 1:]
                if inspect.iscoroutinefunction(handleFunc):
                    await handleFunc(handleObj, subPath, data, writer)
                else:
                    handleFunc(handleObj, subPath, data, writer)
                return

        raise ValueError('Handler does not exist')


    async def addJob(self, path, data, writer):
        jName = data.get('name', None)
        # Job already exists
        if jName in self.jobs:
            return

        jKeyset = int(path)

        # keyset is not valid
        if keyset == 0:
            return

        capableListeners = []
        for (lKeyset, listener) in self.listeners:
            if jKeyset <= lKeyset:
                capableListeners.append(listener)

        if len(capableListeners) == 0:
            return
        # Add the job
        job = Job()
        job.addSource(data.get('source', ''))
        job.addTarget(generateNewDirectory())
        self.jobs[jName] = job
        # Notify listeners
        for listener in capableListeners:
            await listener(jName)

    def removeJob(self, jobName, data, writer):
        if jobName in self.jobs:
            del self.jobs[jobName]

    def findJob(self, jobName):
        return self.jobs.get(jobName, None)

    async def processJob(self, path, data, writer): 
        pathPieces = path.split('/')
        jobName = pathPieces[0]
        jobCmd = pathPieces[1] or ""

        job = self.findJob(jobName)
        if job == None:
            # Job doesn't exist
            return
        # Remove the job then process the command
        if jobCmd == "complete":
            self.removeJob(jobName)

        await job.process(jobCmd, data, writer)

