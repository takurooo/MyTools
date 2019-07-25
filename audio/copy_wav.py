# --------------------------------------
# import
# --------------------------------------
import os
import sys
import argparse

from wave_utils import WavReader, WavWriter


# --------------------------------------
# define
# --------------------------------------

# --------------------------------------
# class
# --------------------------------------

# --------------------------------------
# function
# --------------------------------------


def get_args():
    parser = argparse.ArgumentParser(description="wave copy")
    parser.add_argument("in_file", type=str,
                        help="path2your_wavefile", default=None)
    return parser.parse_args()
# --------------------------------------
# main
# --------------------------------------


def main(args):
    wav_reader = WavReader(args.in_file)
    wav_reader.print_info()
    pcm = wav_reader.read_pcm()

    wav_writer = WavWriter("out.wav")
    wav_writer.set_params(wav_reader.params)
    wav_writer.write_pcm(pcm)


if __name__ == "__main__":
    main(get_args())
