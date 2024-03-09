import wave
from audiostreamer import *
import socket
import threading, pyaudio, queue

wf = wave.open("samples/minecraft.wav")

data = None
sample_rate = wf.getframerate()
sample_width = wf.getsampwidth()
channels = wf.getnchannels()

running=False

host_ip = 'localhost'
print(host_ip)
port = 12345
q = queue.Queue(maxsize=100)

def audiorecorder():

	BUFF_SIZE = 65536//8
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
	time.sleep(1)
	print('Now Playing...')
	while True:
		frame = q.get()
		stream.write(frame)

	client_socket.close()
	print('Audio closed')
	os._exit(1)

def test_audiostreamer():
	t1 = threading.Thread(target=audiorecorder, args=())
	t1.start()
	t2 = threading.Thread(target=audiostreamer, args=())
	t2.start()
	t2.join()
	running=False
	t1.join()
	print('Done')
	assert 2+2==4

if __name__ == "__main__":
	audiorecorder()