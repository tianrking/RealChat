import asyncio
import websockets

async def receive_message(websocket):
    while True:
        message = await websocket.recv()
        print(f"\rReceived: {message}\nYou: ", end='')

async def send_message(websocket):
    while True:
        message = await asyncio.get_event_loop().run_in_executor(None, input, "You: ")
        await websocket.send(message)

async def main():
    uri = "ws://localhost:12345"
    async with websockets.connect(uri) as websocket:
        # 同时启动发送和接收任务
        receive_task = asyncio.create_task(receive_message(websocket))
        send_task = asyncio.create_task(send_message(websocket))
        # 等待任务完成
        done, pending = await asyncio.wait(
            [receive_task, send_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

asyncio.run(main())

