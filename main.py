import asyncio
import pathlib
import inspect
import jm
jobManager = jm.JobManager()

async def handler(reader, writer):
    client_request = await reader.readuntil(seperator=b'\r\L')
    client_request = json.loads(client_request.decode('utf8')) 
    path = client_request.get("path", "/DNE")
    await jobManager.process(path, client_request, writer)
    writer.close()
    await writer.wait_closed()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

server = asyncio.start_server(handler, '0.0.0.0', 1234)
loop.run_until_complete(server)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
