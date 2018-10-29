import asyncio


# Utils subprocess
async def _read_stream(stream, cb):
    while True:
        line = await stream.readline()
        if line:
            cb(line)
        else:
            break


async def _stream_subprocess(cmd, stdout_cb, stderr_cb):
    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    await asyncio.wait([
        _read_stream(process.stdout, stdout_cb),
        _read_stream(process.stderr, stderr_cb)
    ])
    return await process.wait()


# Utils
def end_of_message():
    return b"0\r\n"


# Command handle
async def ping(_, writer):
    writer.write('pong'.encode())
    writer.write(end_of_message())
    await writer.drain()


async def crawl(message, writer):
    def _send_msg_to_client(msg):
        writer.write(msg)

    print(*message.split(' ')[1:])
    print(['bash', '../ex1/script.sh', *message.split(' ')[1:]])

    await _stream_subprocess(
        ['bash', '../ex1/script.sh', *message.split(' ')[1:]],
        _send_msg_to_client, _send_msg_to_client)
    writer.write(end_of_message())
    await writer.drain()


command_map = {'ping': ping, 'crawl': crawl}


async def crawl_server(reader, writer):
    while True:
        data = await reader.read(1048)  # Max number of bytes to read
        if not data:
            break
        message = data.decode()
        print('Data received: {!r}'.format(message))
        command = message.split(' ')[0]
        if command in command_map.keys():
            await command_map.get(command)(message, writer)
        elif command in ['quit', 'exit']:
            break
        else:
            writer.write(('Unknown command %s' % (command)).encode())
            writer.write(end_of_message())
            await writer.drain()
    writer.close()


loop = asyncio.get_event_loop()
coro = asyncio.start_server(crawl_server, '127.0.0.1', 2999, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
