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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging
import json
import grpc

import taskFour_pb2
import taskFour_pb2_grpc

token = 0

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('192.168.46.108:10001') as channel:
        stub = taskFour_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(taskFour_pb2.HelloRequest(name='Task Four'))
        print('Greeter client received: ' + response.message)
        inputUserName = input("Enter your username: ")
        response = stub.UserName(taskFour_pb2.UserNameRequest(userName=inputUserName))
        inputUserPass = input("Enter your password: ")
        response = stub.PasswordEnter(taskFour_pb2.PasswordEnterRequest(password=inputUserPass))
        inputUserPassConfirmation = input("Confirm your password: ")
        response = stub.PasswordConfirmation(taskFour_pb2.PasswordConfirmationRequest(passwordConfirmed=inputUserPassConfirmation))
        if samePass(inputUserPass,inputUserPassConfirmation) :
            print("sending login information to server -")
            loginAttemptJSON = json.dumps({"username":inputUserName,"password":inputUserPass})
            response = stub.LoginAttempt(taskFour_pb2.LoginAttemptRequest(loginAttempt=loginAttemptJSON))
            print(response.Result)
            token = response.authenticationToken
            if response.Result == "Success" :
                print("This was the token received from the server: " + token)
                print("Welcome to the ZDJE team client - (1) Update pass - (2) Delete acc")
                userChoice = input("Enter your choice: ")
                print(userChoice)
                if userChoice == "1" :
                    print("user wishes to change their password")
                    changedPassword = input("Enter your new password: ")
                    confirmUsername = input("Confirm your username: ")
                    response = stub.AuthenticateRequest(taskFour_pb2.AuthenticateRequestRequest(tokenToVerify=token,choice=userChoice,newPassword=changedPassword,confirmedUserName=confirmUsername))
                    print(response.replyMessage)
                elif userChoice == "2" :
                    print("user wishes to delete their account")
                    confirmUsername = input("Confirm your username: ")
                    response = stub.AuthenticateRequest(taskFour_pb2.AuthenticateRequestRequest(tokenToVerify=token,choice=userChoice,confirmedUserName=confirmUsername))
                    print(response.replyMessage)
            else :
                print("the two passwords you entered weren't the same")


def samePass(pass1, pass2):
    if pass1 == pass2 :
        #print("passwords match")
        return (pass1 == pass2)
    else :
        #print("passwords do not match")
        return (pass1 == pass2)




if __name__ == '__main__':
    logging.basicConfig()
    run()
