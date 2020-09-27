# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc

import taskFour_pb2
import taskFour_pb2_grpc


class Greeter(taskFour_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return taskFour_pb2.HelloReply(message='Hello, %s!' % request.name)


    def UserName(self, request, context):
        print("Name received: " + request.userName)
        return taskFour_pb2.UserNameReply(message=request.userName)

    def PasswordEnter(self, request, context):
        print("Password received: " + request.password)
        return taskFour_pb2.PasswordEnterReply(message=request.password)

    def PasswordConfirmation(self, request, context):
        print("Password confirmation received: " + request.passwordConfirmed)
        return taskFour_pb2.PasswordConfirmationReply(message=request.passwordConfirmed)

    def LoginAttempt(self, request, context):
        print("Attempting a login: " + request.loginAttempt)
        return taskFour_pb2.LoginAttemptReply(message=request.loginAttempt)





def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    taskFour_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
