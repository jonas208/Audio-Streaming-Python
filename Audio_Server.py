import pyaudio
import socket
import threading
from pynput import keyboard
import select

class Audio_Sender(threading.Thread):

    def __init__(self, host, port):

        threading.Thread.__init__(self)

        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 4096
        self.HOST = host
        self.PORT = port

        self.audio = pyaudio.PyAudio()

        self.breaked = False

    def run(self):

        self.serversocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.serversocket.bind((self.HOST, self.PORT))
        self.serversocket.listen(5)

        # start Recording
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                                      frames_per_buffer=self.CHUNK, stream_callback=self.callback)

        self.read_list = [self.serversocket]
        print("[AUDIO SERVER] recording...")

        while True:
            readable, writable, errored = select.select(self.read_list, [], [])
            for s in readable:
                if s is self.serversocket:
                    (clientsocket, address) = self.serversocket.accept()
                    self.read_list.append(clientsocket)
                    print("[AUDIO SERVER] Connection from", address)
                else:
                    data = s.recv(1024)
                    if not data:
                        self.read_list.remove(s)
            if self.breaked:
                break

        print("[AUDIO SERVER] finished recording")

        self.serversocket.close()
        # stop Recording
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def callback(self, in_data, frame_count, time_info, status):
        for s in self.read_list[1:]:
            s.send(in_data)
        return (None, pyaudio.paContinue)

class Audio_Recver(threading.Thread):

    def __init__(self, host, port):

        threading.Thread.__init__(self)

        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 4096
        self.HOST = host
        self.PORT = port

        self.breaked = False

    def run(self):

        self.s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(5)
        self.clientsocket, self.address = self.s.accept()

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, output=True,
                                      frames_per_buffer=self.CHUNK)

        while True:
            data = self.clientsocket.recv(self.CHUNK)
            self.stream.write(data)
            if self.breaked:
                break

        print("[AUDIO SERVER] Recver stopped")
        self.s.close()
        self.stream.close()
        self.audio.terminate()

#p = pyaudio.PyAudio()
#print(p.get_default_host_api_info())
#print(p.get_device_count())

sender = Audio_Sender("::1", 54535) #::1
recver = Audio_Recver("::1", 54534) #::1
sender.start()
recver.start()

print("[SERVER] Press ESC to stop")

def on_press(key):
    if key == keyboard.Key.esc:
        recver.breaked = True
        sender.breaked = True
        return False

with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()
