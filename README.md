# audiostreamer

This application reads a .wav file and converts it into a real-time UDP packet stream to a specified IP address and port, allows for easy configuration of delay/packet size through the command line and for the ability to start multiple audio streams with multiple different .wav files.

## Usage

For the Development of this module, Ubuntu-22.04 and python3.10 was used, but most python3 versions should work. To install the neccesary dependencies run the following command

```
pip install -r requirements.txt
```

The application can then be run and configured using the `--ip`, `-port`, `--wav_file`, `--delay_ms` and `--verbose` parameters. Note that `--verbose` has no input, and `--wav_file` can have several. Here is an example

```
python3 audiostreamer.py --wav_file samples/01_SaxophoneCloseMic1.wav samples/02_SaxophoneCloseMic2.wav --delay_ms 10 --ip localhost --port 123 --verbose 
```

## Unit-Testing

The `/tests` folder has a unit-test for veryfing the the audionode module. To run the unit-test install the requirements using,

```
pip install -r tests/test_requirements.txt
```

and then use the pytest command (this command will take as long as the audio file duration)

```
pytest
```

Note: these test only verify that the node is functioning properly, it is not meant to evaluate network performance. Additional care needs to be taken when applying to a IP network, as UDP packets can be fragmented and packets can be lost. Fragmentation is not guaranteed to fall between frames eigher, possibly resulting in temporary corruption.

## Results

- One 24-bit/44100hz audio stream used around 1% of cpu capacity on M1 Macbook pro.
- When using 10ms delay on a 33 second audio clip, the average measured delay was 9.99969ms

## challenges

- running a for loop at a specified frequency turned out to be more difficult than expected. Even though time.sleep() is in absolute terms very accurate, it always drifted to the point where the receive buffer would either overrun or underrun. To mitigate this, the loop was modified to actively adjust sleep time based on UTC time as a way to correct for drift.

## Further work

- For real live streamed audio, it might be benefitial to send timestamp too. Precise UTC time can be used, which can synched using NTP, which can have sub millisecond accuracy in local networks (https://en.wikipedia.org/wiki/Network_Time_Protocol).

- As of now, to differentiate different audio streams you can only look at the originating port. Alternative solutions can be implemented.