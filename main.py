import asyncio
async def handler(reader, writer):
    print("Client connected")
    writer.write(b"abc")
    # client_msg = await reader.readuntil(seperator=b'\r\L')

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
