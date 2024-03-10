import wave, socket, threading, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from audiostreamer import *

WAV_FILE = 'samples/01_SaxophoneCloseMic1.wav'
IP_ADDRESS = 'localhost'
DELAY = 10 # in milliseconds
PORT = 12345

# open wavefile to extract information
wf = wave.open(WAV_FILE)
raw_data = wf.readframes(wf.getnframes())
rx_buffer = []

# define variable for testing delay
timestamps = []

def test_audiostreamer():
	"""
	This test passes if the application can be run without errors.
	"""

	def	audiorecorder(port):

		# create socket
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		client_socket.bind(('localhost', port))
		client_socket.settimeout(1)

		# receive frames and write to stream
		while True:
			try:
				frame, _ = client_socket.recvfrom(65536)
				timestamps.append(time.time())
				rx_buffer.append(frame)
			except socket.timeout:
				client_socket.close()
				break

	# start the recorder thread	
	t1 = threading.Thread(target=audiorecorder, args=(PORT,))
	t1.start()
	
	# start the audiostreamer thread
	t2 = threading.Thread(target=audiostreamer, args=(IP_ADDRESS, PORT, DELAY, [WAV_FILE]))
	t2.start()

	# join the threads after playback is done
	t2.join()
	t1.join()

def test_length_in_bytes():
	"""
	This test passes if the length of the .wav file is equal to the length of the received data
	"""
	assert len(raw_data) == len(b''.join(rx_buffer))

def test_content():
	"""
	This test passes if the content of the .wav file is equal to the content of the received data
	"""
	assert raw_data == b''.join(rx_buffer)

def test_delay():
	"""
	This test passes if the delay is within 1% of the expected delay
	"""
	# calculate the average time between each frame
	delta = [timestamps[i+1]-timestamps[i] for i in range(len(timestamps)-1)]
	average = sum(delta)/len(delta)
	print(average)

	assert abs(average-DELAY/1000) < 0.01*DELAY/1000