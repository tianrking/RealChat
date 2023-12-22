import asyncio
import websockets

connected = set()

async def echo(websocket, path):
    print(f"A client has connected.")
    connected.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message from client: {message}")
            for conn in connected:
                await conn.send(message)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"A client has disconnected.")
    finally:
        connected.remove(websocket)

async def main():
    async with websockets.serve(echo, "localhost", 12345):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())

