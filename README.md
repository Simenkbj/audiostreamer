# audiostreamer

This application reads a .wav file and convert this into a real-time “live” IP stream and transmit this to the Audionode IP address. There is no requirement to a given protocol and format of the IP stream. It should be possible to start a number of Audiostreamers simultaneously on the same PC or on several PC’s so a multitrack recording with one track played by each Audiostreamer can be simultaneously generated.

# TODO
- implement a way to start several audiostreamers at the same time. maybe make one audiostreamer for each file in a folder? -> then async or threads may have to be imported.

- mention the minimum delay that is possible, as there may be some overhead with this tech stack which bottlenecks the network in terms of overhead.

- Specify that localhost routing only checks for faults in serialization and deserialization, not packet faults caused by the network (and hence, things like packet fragmentation is not tested)

- sending is using sleep function to send, which does not take into account the time it actually takes to run the code, therefore not sending often enough. Just use the clock to time the transmissions, the most important thing is that the transmissions dont drift with time, not that they are very accurate.

- remember to send timestamp. This can be just the number of the buffer being sent, but the downside being that it requires all audiostreamers to have the same buffer size for audio syncing down the line. For real live streamed audio, this timestamp can be replaced with precise UTC time which can synched using NTP (which has sub millisecond accuracy in local networks) to prevent time drift. Ideally, the timestamp would also be the timestamp for the first sample in a frame.

- mention packet fragmentation maybe?

# Usage

Have python 3.11 installed, although it should work on most versions. On linux, it can simply be installed using

sudo apt-get install python3.11

pip install -r requirements.txt

python3 audiostreamer.py --ip 192.168.0.125 --port 12345 --delay_ms 10 --verbose

### note: python3.11.7 was used