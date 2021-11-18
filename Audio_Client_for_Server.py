import pyaudio
import socket
import threading
from pynput import keyboard

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

        self.clientsocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.clientsocket.connect((self.HOST, self.PORT))

        # start Recording
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                                      frames_per_buffer=self.CHUNK)

        print("[AUDIO SERVER] recording...")
        while True:
            self.clientsocket.send(self.stream.read(self.CHUNK))
            if self.breaked:
                break

        print("[AUDIO SERVER] finished recording")

        self.clientsocket.close()
        # stop Recording
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

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

        while True:
            breaked = True
            try:
                self.s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                self.s.connect((self.HOST, self.PORT))
            except:
                breaked = False
            if breaked:
                break
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, output=True,
                                      frames_per_buffer=self.CHUNK)

        while True:
            data = self.s.recv(self.CHUNK)
            self.stream.write(data)
            if self.breaked:
                break

        print("[AUDIO CLIENT] Recver stopped")
        self.s.close()
        self.stream.close()
        self.audio.terminate()

sender = Audio_Sender("2a02:908:1c46:c100:ddde:aec7:f6fa:aa8", 54534) #::1
recver = Audio_Recver("2a02:908:1c46:c100:ddde:aec7:f6fa:aa8", 54535) #::1
sender.start()
recver.start()

print("[AUDIO CLIENT] Press ESC to stop")

def on_press(key):
    if key == keyboard.Key.esc:
        recver.breaked = True
        sender.breaked = True
        return False

with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()