import wave

wf = wave.open("sample audio/01_SaxophoneCloseMic1.wav")

data = None
sample_rate = wf.getframerate()
sample_width = wf.getsampwidth()
channels = wf.getnchannels()

# Welcome to PyShine
# This is client code to receive video and audio frames over UDP

import socket
import threading, pyaudio, time, queue

host_ip = 'localhost'#  socket.gethostbyname(host_name)
print(host_ip)
port = 12345
# For details visit: www.pyshine.com
q = queue.Queue(maxsize=200)

def test_audiostreamer():
	assert 2+2==4

""" 	BUFF_SIZE = 65536//8
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	client_socket.bind((host_ip,port))
	p = pyaudio.PyAudio()
	CHUNK = 1*1024
	stream = p.open(format=p.get_format_from_width(sample_width),
					channels=channels,
					rate=sample_rate,
					output=True,
					frames_per_buffer=CHUNK)
					
	# create socket
	socket_address = (host_ip,port)
	
	def getAudioData():
		while True:
			frame, _ = client_socket.recvfrom(BUFF_SIZE)
			q.put(frame)
			print('Queue size...', q.qsize())

	t2 = threading.Thread(target=getAudioData, args=())
	t2.start()
	print('Now Playing...')
	while True:
		frame = q.get()
		stream.write(frame)

	client_socket.close()
	print('Audio closed')
	os._exit(1) """

if __name__ == "__main__":
	test_audiostreamer()