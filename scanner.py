import argparse
import asyncio
import logging


logging.basicConfig(
     level=logging.INFO,
     format='%(asctime)s %(levelname)s %(message)s',
     datefmt='%Y-%m-%d %H:%M:%S'
)

async def connect_to_server(host,port,semaphore, timeout, banner):
    writer = None
    
    async with semaphore: 
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host,port),
                timeout=timeout
            )

            banner_text = ''

            if banner:
                request = (
                        f'GET / HTTP/1.1\r\n'
                        f'Host: {host}\r\n'
                        f'Connection: close\r\n\r\n'
                )
                writer.write(request.encode())
                await writer.drain()
            
                response = await asyncio.wait_for(reader.read(1024), timeout=timeout)
                response_text = response.decode(errors='replace')

                banner_text = response_text.split('\r\n\r\n')[0]
                banner_text = banner_text.replace('\r\n', ' | ')

            result = f'PORT {port} OPEN'
            if banner_text:
                result += f' | BANNER: {banner_text}'
            return result
        
        except OSError:
                return f'PORT {port} CLOSED'
        except asyncio.TimeoutError:
                return f'PORT {port} TIMEOUT'
        finally:
            if writer is not None:
                writer.close()
                try:
                    await writer.wait_closed()
                except OSError:
                    pass
            
async def main(): 
    semaphore = asyncio.Semaphore(10)
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    parser.add_argument('-p','--ports', nargs='+', type=int)
    parser.add_argument('--start-port', type=int)
    parser.add_argument('--end-port', type=int)
    parser.add_argument('-v','--verbose', action='store_true')
    parser.add_argument('-t', '--time', type=float, default=5)
    parser.add_argument('-b', '--banner', action='store_true')

    args = parser.parse_args()
    if args.verbose:
         logging.getLogger().setLevel(logging.DEBUG)
    else:
         logging.getLogger().setLevel(logging.INFO)
    if args.ports is not None and (args.start_port is not None or args.end_port is not None):
        parser.error("Cannot use --ports together with --start-port or --end-port.")
    tasks = []

    if args.time <= 0:
         parser.error("Timeout must be greater than 0.")

    if args.ports is not None:
        ports = args.ports
    else:
        if args.start_port is None or args.end_port is None:
            parser.error("Specify --ports or both --start-port and --end-port")
        elif args.start_port > args.end_port:
            parser.error("--start-port cannot be greater than --end-port.")
        ports = list(range(args.start_port, args.end_port + 1))

    for port in ports:
        if port < 1 or port > 65535:
            parser.error("Port numbers must be between 1 and 65535.")

    logging.info(f'Target: {args.host}')
    logging.info(f'Ports to scan: {ports}')


    for port in ports:
        tasks.append(connect_to_server(args.host, port, semaphore, args.time, args.banner))
    results = await asyncio.gather(*tasks)

    for result in results:
        logging.info(result)

asyncio.run(main())