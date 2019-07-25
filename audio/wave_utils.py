# --------------------------------------
# import
# --------------------------------------
import wave

# --------------------------------------
# define
# --------------------------------------

# --------------------------------------
# class
# --------------------------------------


class WavReader:

    def __init__(self, filename):
        self.wav = wave.open(filename, 'rb')
        self.params = self.wav.getparams()

    def read_pcm(self):
        start = 0
        end = self.wav.getsampwidth()
        pcm = []
        buf = self.wav.readframes(-1)
        for _ in range(self.wav.getnframes()):
            sample = []
            for _ in range(self.wav.getnchannels()):
                data = int.from_bytes(buf[start:end], 'little', signed=True)
                start = end
                end += self.wav.getsampwidth()
                sample.append(data)
            pcm.append(sample)
        self.wav.rewind()
        return pcm

    def get_ch(self):
        return self.params.nchannels

    def get_sampwidth(self):
        return self.params.sampwidth

    def get_framerate(self):
        return self.params.framerate

    def print_info(self):
        pcm_size = self.wav.getnchannels() * self.wav.getsampwidth() * \
            self.wav.getnframes()
        print("{:8d} Hz".format(self.wav.getframerate()))
        print("{:8d} ch".format(self.wav.getnchannels()))
        print("{:8d} bit".format(self.wav.getsampwidth()*8))
        print("{:8d} frames".format(self.wav.getnframes()))
        print("{:8d} bytes".format(pcm_size))


class WavWriter:

    def __init__(self, filename):
        self.filename = filename
        self.ch = None
        self.sampwidth = None
        self.framerate = None
        self.compname = 'not compressed'
        self.comptype = 'NONE'

    def write_pcm(self, pcm):
        assert self.ch is not None, "channels is None."
        assert self.sampwidth is not None, "sampwidth is None."

        converted_pcm = 0
        for i, sample in enumerate(pcm):
            for ch in range(self.ch):
                data = sample[ch].to_bytes(
                    self.sampwidth, 'little', signed=True)
                if i == 0:
                    converted_pcm = data
                else:
                    converted_pcm = converted_pcm + data

        self.wav = wave.open(self.filename, 'wb')

        self.wav.setsampwidth(self.sampwidth)
        self.wav.setframerate(self.framerate)
        self.wav.setnchannels(self.ch)

        self.wav.writeframes(converted_pcm)

        self.wav.close()

    def set_params(self, params):
        self.ch = params.nchannels
        self.sampwidth = params.sampwidth
        self.framerate = params.framerate
        self.comptype = params.comptype
        self.compname = params.compname

    def set_ch(self, ch):
        self.ch = ch

    def set_sampwidth(self, sampwidth):
        self.sampwidth = sampwidth

    def set_framerate(self, framerate):
        self.framerate = framerate
