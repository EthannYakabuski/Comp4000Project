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
"The Python implementation of the GRPC helloworld.Greeter client."

from __future__ import print_function

from __future__ import with_statement

import logging
import json
import grpc

import os
import sys
import errno


from fuse import FUSE, FuseOSError, Operations


import taskFour_pb2
import taskFour_pb2_grpc

token = 0
inputUserName = ""

#this entire PassThrough class is property of the below: 
#https://github.com/skorokithakis/python-fuse-sample
#as per milestone recommendations we are using this as a starting point

def samePass(pass1, pass2):
    if pass1 == pass2 :
        #print("passwords match")
        return (pass1 == pass2)
    else :
        #print("passwords do not match")
        return (pass1 == pass2)

class Passthrough(Operations):
    def __init__(self, root):
        self.root = root

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        return os.symlink(target, self._full_path(name))

    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        return os.link(self._full_path(name), self._full_path(target))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)

class client(Passthrough):
    def __init__(self,root):
        self.root = root

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid', 'st_blocks'))

    


def main(root, mount):
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
                print("Welcome to the ZDJE team client - (1) Update pass - (2) Delete acc - (3) FUSE")
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
                elif userChoice == "3" :
                    print("client receiving the list of files that are on the remote server that they can interact with")
                    FUSE(client(mount), root, nonempty=True, nothreads=False, foreground = True, **{'allow_other': True})
                    
                    


                    
                    


            else:
                print("the two passwords you entered weren't the same")

if __name__ == '__main__':
    logging.basicConfig()
    main("fuse", "top")
