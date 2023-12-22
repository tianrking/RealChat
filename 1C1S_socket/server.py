from concurrent import futures
import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import asyncio

class ChatService(helloworld_pb2_grpc.ChatServiceServicer):
    async def Chat(self, request_iterator, context):
        async for message in request_iterator:
            print("Client says: " + message.message)
            # echo back the received message
            yield helloworld_pb2.ChatMessage(message="Server says: You sent " + message.message)

async def serve():
    server = grpc.aio.server()
    helloworld_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()

    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(0)

if __name__ == '__main__':
    asyncio.run(serve())

