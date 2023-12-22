import asyncio
import websockets
import json

# 假设这是客户端的唯一标识，实际应用中可能是用户输入或随机生成
client_id = "client1"

async def receive_message(websocket):
    while True:
        message = await websocket.recv()
        data = json.loads(message)
        # 如果信息来源不是自己，则打印信息
        if data["sender"] != client_id:
            print(f"\rReceived from {data['sender']}: {data['message']}\nYou: ", end='')

async def send_message(websocket):
    while True:
        message = await asyncio.get_event_loop().run_in_executor(None, input, "You: ")
        # 发送带有发送者标识的消息
        await websocket.send(json.dumps({"sender": client_id, "message": message}))

async def main():
    uri = "ws://localhost:12345"
    async with websockets.connect(uri) as websocket:
        receive_task = asyncio.create_task(receive_message(websocket))
        send_task = asyncio.create_task(send_message(websocket))
        done, pending = await asyncio.wait(
            [receive_task, send_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

asyncio.run(main())

