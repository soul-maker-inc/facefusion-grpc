#!/bin/python3
from concurrent import futures
import logging
import os
import grpc
from grpc_services import roop_pb2_grpc, roop_pb2
from facefusion_grpc import RoopService
from grpc_reflection.v1alpha import reflection

SERVICE_PORT = os.environ.get('PORT') or "50051"

def serve():
    logging.info("creating grpc server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    logging.info("add roop service")
    s1 = RoopService()
    s1.setup()
    roop_pb2_grpc.add_RoopServicer_to_server(s1, server)
    logging.info("add deepface service")

    SERVICE_NAMES = (
        roop_pb2.DESCRIPTOR.services_by_name['Roop'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port("[::]:" + SERVICE_PORT)
    server.start()
    logging.info("Server started, listening on %s",SERVICE_PORT)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    serve()
