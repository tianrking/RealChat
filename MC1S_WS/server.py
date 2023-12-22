import asyncio
import websockets
import json

connected = set()

async def server(websocket, path):
    global connected
    connected.add(websocket)
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"Received message {data['message']} from {data['sender']}")
                new_message = json.dumps({"sender": data['sender'], "message": data['message']})
                for conn in connected:
                    if conn != websocket:  # Do not send the message back to the sender
                        await conn.send(new_message)
            except json.JSONDecodeError:
                print("Received an invalid message.")
    finally:
        connected.remove(websocket)

start_server = websockets.serve(server, "localhost", 12345)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

