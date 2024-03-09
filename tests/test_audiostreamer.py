import wave, socket, threading, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from audiostreamer import *

WAV_FILE = 'samples/01_SaxophoneCloseMic1.wav'

# open wavefile to extract information
wf = wave.open(WAV_FILE)
raw_data = wf.readframes(wf.getnframes())
rx_buffer = []

def test_audiostreamer():

	def	audiorecorder(port, queue_size, wav_file):

		# create socket
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		client_socket.bind(('localhost', port))
		client_socket.settimeout(1)

		# receive frames and write to stream
		while True:
			try:
				frame, _ = client_socket.recvfrom(65536)
				rx_buffer.append(frame)

			except socket.timeout:
				client_socket.close()
				break

	# start the recorder thread	
	t1 = threading.Thread(target=audiorecorder, args=(12345, 100, WAV_FILE))
	t1.start()
	
	# start the audiostreamer thread
	t2 = threading.Thread(target=audiostreamer, args=('localhost', 12345, 10, [WAV_FILE]))
	t2.start()

	# join the threads after playback is done
	t2.join()
	t1.join()


def test_length():
		assert len(raw_data) == len(b''.join(rx_buffer))

def test_content():
		assert raw_data == b''.join(rx_buffer)