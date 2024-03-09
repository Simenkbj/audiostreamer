# audiostreamer

This application reads a .wav file and convert this into a real-time “live” IP stream and transmit this to the Audionode IP address. There is no requirement to a given protocol and format of the IP stream. It should be possible to start a number of Audiostreamers simultaneously on the same PC or on several PC’s so a multitrack recording with one track played by each Audiostreamer can be simultaneously generated.

## unit-test

A simple test has been made to verify the quality of the audiorecorder. 

# TODO

- Specify that localhost routing only checks for faults in serialization and deserialization, not packet faults caused by the network (and hence, things like packet fragmentation is not tested)

- remember to send timestamp. This can be just the number of the buffer being sent, but the downside being that it requires all audiostreamers to have the same buffer size for audio syncing down the line. For real live streamed audio, this timestamp can be replaced with precise UTC time which can synched using NTP (which has sub millisecond accuracy in local networks) to prevent time drift. Ideally, the timestamp would also be the timestamp for the first sample in a frame.

- Make sure that the song is divisible by the delay

# Usage

Have python 3.11 installed, although it should work on most versions. On linux, it can simply be installed using

sudo apt-get install python3.11

pip install -r requirements.txt

python3 audiostreamer.py --ip 192.168.0.125 --port 12345 --delay_ms 10 --verbose

### note: python3.11.7 was used

### challenges

- running a for loop at a specified frequency turned out to be more difficult than expected. Even though time.sleep() is in absolute terms very accurate, it still drifted to the point where the receive buffer would either overrun or underrun constantly. To mitigate this, the loop was instead modified to actively adjust sleep time based on UTC time, to prevent any drift from occuring.

### Assumptions

- The receiver end already knows what format the .wav file has (bitrate, bitdepth, channel(s))