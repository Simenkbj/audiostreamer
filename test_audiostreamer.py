import wave
from audiostreamer import *
import socket
import threading, pyaudio, queue, argparse

running = True

def simpleAudioRecorder(port, queue_size, wav_file):
	# create socket
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	client_socket.bind(('localhost',port))

	# open wavefile to extract information
	wf = wave.open("samples/minecraft.wav")
	sample_rate = wf.getframerate()
	sample_width = wf.getsampwidth()
	channels = wf.getnchannels()

	# create queue
	q = queue.Queue(maxsize=int(queue_size))

	# create audio stream
	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(sample_width),
					channels=channels,
					rate=sample_rate,
					output=True,
					frames_per_buffer=1024*8)
					
	# create socket
	socket_address = ('localhost',port)
	
	# receive one frame
	frame, _ = client_socket.recvfrom(1024*20)
	q.put(frame)
	print('Queue size...', q.qsize())

	# receive frames and write to stream
	while running:
		try:
			frame, _ = client_socket.recvfrom(1024*20)
			q.put(frame)
			#print('Queue size...', q.qsize())
			if not q.empty():
				frame = q.get()
				stream.write(frame)

		except KeyboardInterrupt:
			client_socket.close()
			stream.stop_stream()
			stream.close()
			p.terminate()
			break

def test_audiostreamer():
	# start the recorder thread
	t1 = threading.Thread(target=simpleAudioRecorder, args=(12345, 100, 'samples/minecraft.wav'))
	t1.start()
	
	# start the audiostreamer thread
	t2 = threading.Thread(target=audiostreamer, args=('localhost', 12345, 10, ['samples/minecraft.wav']))
	t2.start()

	# join the threads after playback is done
	t2.join()
	running=False
	t1.join()
	assert 2+2==4

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--port", help="port", default=12345)
	parser.add_argument("--queue_size", help="queue size", default=100)
	parser.add_argument("--wav", help=".wav file", nargs='+')
	args = parser.parse_args()
	simpleAudioRecorder(args.port, args.queue_size, args.wav)