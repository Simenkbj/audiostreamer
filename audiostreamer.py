import wave, time, socket, argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="port (default '12345')", default=12345)
    parser.add_argument("--ip", help="ip address (default 'localhost')", default='localhost')
    parser.add_argument("--delay_ms", help="delay in milliseconds (default '10ms')", default=10)
    parser.add_argument("--wav", help=".wav file", default="sample audio/01_SaxophoneCloseMic1.wav")
    parser.add_argument("--verbose", help="display additional debug information", action='store_true')
    args = parser.parse_args()

    # Open the .wav file as a wave object
    wf = wave.open("sample audio/minecraft.wav")

    # extract some information from the wave object
    sample_rate = wf.getframerate()
    sample_width = wf.getsampwidth()
    channels = wf.getnchannels()

    if args.verbose:
        print(f'streaming {sample_width*8}-bit/{sample_rate}Hz with {channels} channel(s)')

    BUFF_SIZE = 65536//8
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    # calculate the number of frames(samples) per transmission based on the desired delay
    num_frames_per_transmission = args.delay_ms * sample_rate // 1000
        
    data = None

    num_frames = wf.getnframes()

    for i in range(1, num_frames // num_frames_per_transmission):
        start_time = time.time()  # Start time of the loop iteration

        data = wf.readframes(num_frames_per_transmission)
        server_socket.sendto(data, (args.ip, args.port))

        # Calculate frame duration based on the sample rate
        frame_duration = num_frames_per_transmission / sample_rate

        end_time = time.time()  # End time of the loop iteration
        elapsed_time = end_time - start_time  # Calculate elapsed processing time

        # Calculate the time to sleep to maintain the desired frame rate, ensuring it doesn't go negative
        sleep_time = max(0, frame_duration - elapsed_time)

        time.sleep(0.8*sleep_time)


if __name__ == "__main__":
    main()