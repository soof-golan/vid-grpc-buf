import asyncio
import logging

import grpc
from grpc_buf.gen.proto.api_pb2_grpc import ExampleApiServicer, add_ExampleApiServicer_to_server
from grpc_buf.gen.proto.api_pb2 import Example, GetExampleRequest, GetExampleResponse, CreateExampleRequest, \
    CreateExampleResponse


storage: dict[str, Example] = {
    "1": Example(
        id="1",
        name="Example 1"
    ),
}


class ExampleApi(ExampleApiServicer):
    async def GetExample(self, request: GetExampleRequest, context) -> GetExampleResponse:
        logging.info("GetExample called")
        result = storage.get(request.id, None)
        if result is None:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Example not found")
        response = GetExampleResponse(
            example=result
        )
        return response

    async def CreateExample(self, request: CreateExampleRequest, context) -> CreateExampleResponse:
        logging.info("CreateExample called")
        if request.example.id in storage:
            await context.abort(grpc.StatusCode.ALREADY_EXISTS, "Example already exists")
        storage[request.example.id] = request.example
        return CreateExampleResponse(
            example=request.example
        )


async def main():
    logging.info("Starting server")
    server = grpc.aio.server()
    add_ExampleApiServicer_to_server(ExampleApi(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
