import asyncio


async def crawl_client(loop):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 2999, loop=loop)

    while True:
        command = input('Type command: ')
        writer.write(command.encode())
        if command in ['quit', 'exit']:
            break

        end_of_message = False
        print('Received:')
        while True:
            data = await reader.read(1048)
            if data[-3:] == b"0\r\n":
                data = data[:-3]
                end_of_message = True
            print(data.decode())
            if end_of_message:
                break

    print('Close the socket')
    writer.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(crawl_client(loop))
loop.close()
