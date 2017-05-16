#! /usr/bin/env python2

import scipy.io.wavfile as sio
import numpy as np
from random import shuffle
from sys import argv
from fabric.api import *

THRESHOLD = 0.8
SIZE_LIMIT = 10

def rms(ss):
    """
    Takes the root-mean-square of an array of samples
    """
    return np.sqrt(np.abs(np.mean(np.square(ss))))

def find_ceiling(ss, factor):
    """
    Attempts to find the sample at which the silence ends
    """
    slice = len(ss)
    while not (rms(ss[0:slice]) < THRESHOLD):
        slice = int(len(ss)/factor)
        factor += 1
    return slice

def convert(infile):
    """
    Takes a path to a file and tries to remove leading silence
    """
    pcm = sio.read("/tmp/%s.to_silence.wav" % infile)
    sample_rate, samples = pcm

    # length in minutes
    length = (len(samples) / float(sample_rate)) / 60.0

    # the first n samples to cut out
    ceiling = find_ceiling(samples, 2)

    # the total number of samples
    total = float(len(pcm[1]))

    if length <= SIZE_LIMIT:
        sio.write("/tmp/%s.silenced.wav" % infile, pcm[0], pcm[1][ceiling:])
        local("cp /tmp/\"%s.silenced.wav\" ./shortened/\"%s.wav\"" % (infile, infile))
        local("rm /tmp/\"%s.silenced.wav\"" % infile)

    local("rm /tmp/\"%s.to_silence.wav\"" % infile)

def to_wav(infile):
    """
    Takes a path to a file and converts it to PCM (wav format)
    """
    local("ffmpeg -i \"%s\" /tmp/\"%s.to_silence.wav\"" % (infile, infile))

def silence(infile):
    """
    Converts a file to PCM and then removes silence
    """
    to_wav(infile)
    convert(infile)

def silence_all():
    """
    Removes the silence from all files in a given directory
    """
    if len(argv) < 2:
        print "You must pass a directory as the first argument"
        return

    with lcd(argv[1]):
        local("mkdir -p ./shortened")
        fileset = local("ls .", capture=True).split("\n")
        shuffle(fileset)
        for f in fileset:
            if f.split(".")[-1] in ["ogg", "opus", "m4a", "mp3"]:
                try:
                    silence(f)
                    local("rm -f /tmp/*wav")
                except Exception:
                    pass

silence_all()
