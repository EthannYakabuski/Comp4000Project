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
import json
import grpc

import taskFour_pb2
import taskFour_pb2_grpc


import bcrypt
import random
import datetime
import string
#unique usernames assumed
#stores the login information for users and their hashed passwords in JSON
loginStorageDict = {} 
#not actually needed
saltStorageDict = {}
#stores the authentication tokens with usernames as keys
authenticationTokens = {}
#stores time out dates, with authentication tokens as keys (assuming unique 64 bit strings for each user)
authenticationTokenTimeOuts = {}; 

#https://linuxhint.com/parse_json_python/
#I had never done this in python before, but it doesn't seem
#like there's an easier way to do it
#this class stores JSON data into a python dictionary
#code ripped directly from above link
class read_data(object):
    def __init__(self,jsonData):
        self.__dict__ = json.loads(jsonData)


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
        #loginAttemptJSON = json.loads(request.loginAttempt)
        #for x in loginAttemptJSON:
           # print("%s: %s" % (x, loginAttemptJSON[x]))
        dataReader = read_data(request.loginAttempt)
        usernameAttempted = dataReader.username
        passwordAttempted = dataReader.password
        if usernameAttempted in loginStorageDict:
            print("This username already exists - move onto password verification")
            #recover the same salt that was used to store the password
            saltStored = saltStorageDict[usernameAttempted]
            if bcrypt.checkpw(passwordAttempted.encode('utf8'),loginStorageDict[usernameAttempted]) :
                print("Matching passwords")
                returnResult = "Logged in successfully"
                #login successful code here
                #https://stackoverflow.com/a/23728630/2213647
                #this is cryptographically secure
                token = "".join(random.SystemRandom().choice(string.digits) for _ in range(64))
                print(token)
                #now store this token in conjunction with the username
                authenticationTokens[usernameAttempted] = token
                #store when this token is no longer valid, in conjunction with the token itself
                #arbitrary expiration time of 2022, we can update this later
                #a new token is generated for this username everytime this person logs in
                #in this way, on a valid login request the server is "updating"
                #the expiration time of the token
                authenticationTokenTimeOuts[token] = datetime.datetime(2022,1,1)
            else :
                print("Passwords did not match")
                returnResult = "Password did not match the one stored on server"
                token = "bad token"
        else :
            print("This username is new - move onto account creation")
            salt = bcrypt.gensalt()
            hashedPassword = bcrypt.hashpw(passwordAttempted.encode('utf8'),salt)
            #this creates a key,value pair in our loginStorageDictionary as : (usernameAttempted,hash(passwordAttempted))
            saltStorageDict[usernameAttempted] = salt
            loginStorageDict[usernameAttempted] = hashedPassword
            returnResult = "New account created"
            #the user should be given an authentication token on their first login (when they make the account)
            #this is incase they want to change pass/delete account while still on their first login
            token = "".join(random.SystemRandom().choice(string.digits) for _ in range(64))
            authenticationTokens[usernameAttempted] = token
            authenticationTokenTimeOuts[token] = datetime.datetime(2022,1,1)
            print("current logins are:", loginStorageDict)
        #print("Username attempted: " + usernameAttempted) 
        #print("Password attempted: " + passwordAttempted)
        return taskFour_pb2.LoginAttemptReply(message=request.loginAttempt,Result=returnResult,authenticationToken=token)





def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    taskFour_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()





