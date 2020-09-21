# Comp4000Project
Task #1: is very straight forward. 

Task #2: General instructions can be found at grpc.io/docs/languages/python/quickstart. 
https://linuxize.com/post/how-to-install-pip-on-ubuntu-20.04/ following this is what ended up actually working, and I have updated the commands below to work as well. 

Below is what worked for the class VM:

sudo apt update

sudo apt install python3-pip

python -m pip install grpcio

python -m pip install grpcio-tools

pip3 install --upgrade pip

pip3 install protobuf

open one terminal 
-> python greeter_server.py

open another terminal 
-> python greeter_client.py
you should immediately see output: "Greeter client received: Hello you"


Task #3: 

Taking the base helloworld.proto from the grpc examples folder,
modify the greeter service adding the second field to represent the second string we are asked for in this task. 
If you have not already - pip install grpcio-tools

Then you need to run: 

python -m grcp_tools.protoc -I ~/...../python/helloworld --python_out=. --grpc_python_out=. ~/..../python/helloworld/helloworldTaskThree.proto

This will generate the new files that we will now reference in greeter_server.py and greeter_client.py
After making the changes to those two files run commands similar to Task #2 to start the server and client to produce an image exactly as shown in task3.png.
