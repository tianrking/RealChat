import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import asyncio

async def run():
    # Establish channel
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.ChatServiceStub(channel)
        # Initiate the stream
        stream = stub.Chat()

        try:
            # Continuously send and receive messages
            while True:
                message = input("Enter your message: ")
                await stream.write(helloworld_pb2.ChatMessage(message=message))  # send a message
                response = await stream.read()  # receive a message
                print(response.message)
        finally:
            await stream.done_writing()  # Close the sending side of the stream

if __name__ == '__main__':
    asyncio.run(run())

