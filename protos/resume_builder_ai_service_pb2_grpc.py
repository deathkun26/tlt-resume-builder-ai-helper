# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import resume_builder_ai_service_pb2 as protos_dot_resume__builder__ai__service__pb2


class ResumeAIServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ParseResume = channel.unary_unary(
                '/resume.parser.ResumeAIService/ParseResume',
                request_serializer=protos_dot_resume__builder__ai__service__pb2.ParseResumeRequest.SerializeToString,
                response_deserializer=protos_dot_resume__builder__ai__service__pb2.ParseResumeResponse.FromString,
                )
        self.SuggestionSummary = channel.unary_unary(
                '/resume.parser.ResumeAIService/SuggestionSummary',
                request_serializer=protos_dot_resume__builder__ai__service__pb2.SuggestionSummaryRequest.SerializeToString,
                response_deserializer=protos_dot_resume__builder__ai__service__pb2.SuggestionSummaryResponse.FromString,
                )


class ResumeAIServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ParseResume(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SuggestionSummary(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ResumeAIServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ParseResume': grpc.unary_unary_rpc_method_handler(
                    servicer.ParseResume,
                    request_deserializer=protos_dot_resume__builder__ai__service__pb2.ParseResumeRequest.FromString,
                    response_serializer=protos_dot_resume__builder__ai__service__pb2.ParseResumeResponse.SerializeToString,
            ),
            'SuggestionSummary': grpc.unary_unary_rpc_method_handler(
                    servicer.SuggestionSummary,
                    request_deserializer=protos_dot_resume__builder__ai__service__pb2.SuggestionSummaryRequest.FromString,
                    response_serializer=protos_dot_resume__builder__ai__service__pb2.SuggestionSummaryResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'resume.parser.ResumeAIService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ResumeAIService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ParseResume(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/resume.parser.ResumeAIService/ParseResume',
            protos_dot_resume__builder__ai__service__pb2.ParseResumeRequest.SerializeToString,
            protos_dot_resume__builder__ai__service__pb2.ParseResumeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SuggestionSummary(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/resume.parser.ResumeAIService/SuggestionSummary',
            protos_dot_resume__builder__ai__service__pb2.SuggestionSummaryRequest.SerializeToString,
            protos_dot_resume__builder__ai__service__pb2.SuggestionSummaryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
