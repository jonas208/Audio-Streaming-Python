# Audio-Streaming-Python
This is a Client-Server-System which can send audio from a microphone from the server to client and in the other direction.

You have to change the IP-Adress. You can do this at line 105 and 106 in the server and in line 87 and 88 in the client. For the first test, I recommend using the localhost and run the server and client on the same system. If you use IPv6 it is "::1", otherwise it is "127.0.0.1". You can change the ports in the same lines aswell.

This is made for an IPv6-Network, you can change it to IPv4 at the server at line 26 and 81 (self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)) and at the client at line 25 and 66 (self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)).

Possible errors:

- The Scripts might not work on Linux because they use the module "PyAudio" (https://pypi.org/project/PyAudio/), which uses different audio-packeges and apis from the OS which might be not installed on your system.
- If you get an error installing "PyAudio", you have to download the .whl files manually. You can get this files at https://pypi.org/project/PyAudio/#files or https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio .
