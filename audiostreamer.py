import wave, time, socket, argparse, threading

def audiostreamer(ip_address, port, delay_ms, wav_files, verbose=False):
    """
    Stream audio data from .wav files over UDP.

    This function reads .wav files and streams the audio data over UDP to a specified IP address and port.
    It supports streaming multiple .wav files simultaneously and allows for setting a delay between transmissions.

    Command Line Arguments:
    --port: The port number to send the audio data to. Default is '12345'.
    --ip: The IP address to send the audio data to. Default is 'localhost'.
    --delay_ms: The delay between audio transmissions in milliseconds. Default is '10ms'.
    --wav: The .wav file(s) to stream. Default is 'samples/minecraft.wav'. Multiple files can be specified.
    --verbose: Display additional debug information. This is an optional flag.

    Note: Large delays will cause small hiccups in the audio stream right in the beginning of the stream. This is because
    the stream is adjusting frequency to sync up with the other streams.
    """

    # Define the function that will be run in a separate thread for each .wav file
    def startStream(wav_file):

        # Open the .wav file as a wave object
        wf = wave.open(wav_file)

        sample_rate = wf.getframerate()
        sample_width = wf.getsampwidth()
        channels = wf.getnchannels()
        num_frames = wf.getnframes()

        if verbose:
            print(f'streaming {sample_width*8}-bit/{sample_rate}Hz with {channels} channel(s)')

        # calculate the number of frames(samples) per transmission based on the desired delay. The delay is rounded
        # so that a whole number of frames are sent.
        num_frames_per_transmission = int(delay_ms) * sample_rate // 1000

        for i in range(1, num_frames // num_frames_per_transmission):

            # Read the next chunk of audio data and send it
            data = wf.readframes(num_frames_per_transmission)
            server_socket.sendto(data, (ip_address, port))

            # calculate the difference between the number of samples that should have been sent and the number of samples that have been sent
            samples_should_have_been_sent = (time.time()-begin_time)*sample_rate
            samples_have_been_sent = num_frames_per_transmission*i
            delta = samples_should_have_been_sent-samples_have_been_sent

            # Then calculate by how much we are ahead/behind and adjust the sleep time accordingly
            delta_time = -delta/sample_rate

            print(f'{wav_file}: {delta_time:.6f} seconds behind')

            time.sleep(max(delta_time, 0))

    # Create a common server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Define start time, making sure that all streams are in sync
    begin_time = time.time()

    # Create a thread for each .wav file
    threads = []
    for wav_file in wav_files:
        thread = threading.Thread(target=startStream, args=(wav_file,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Close the server socket
    server_socket.close()

    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="port (default '12345')", default=12345)
    parser.add_argument("--ip", help="ip address (default 'localhost')", default='localhost')
    parser.add_argument("--delay_ms", help="delay in milliseconds (default '10ms')", default=10)
    parser.add_argument("--wav", help=".wav file", default="samples/minecraft.wav", nargs='*')
    parser.add_argument("--verbose", help="display additional debug information", action='store_true')
    args = parser.parse_args()
    audiostreamer(args.ip, args.port, args.delay_ms, args.wav, args.verbose)