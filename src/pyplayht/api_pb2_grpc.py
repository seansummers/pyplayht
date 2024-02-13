# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import api_pb2 as api__pb2


class TtsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Tts = channel.unary_stream(
                '/playht.v1.Tts/Tts',
                request_serializer=api__pb2.TtsRequest.SerializeToString,
                response_deserializer=api__pb2.TtsResponse.FromString,
                )


class TtsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Tts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TtsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Tts': grpc.unary_stream_rpc_method_handler(
                    servicer.Tts,
                    request_deserializer=api__pb2.TtsRequest.FromString,
                    response_serializer=api__pb2.TtsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'playht.v1.Tts', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Tts(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Tts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/playht.v1.Tts/Tts',
            api__pb2.TtsRequest.SerializeToString,
            api__pb2.TtsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
