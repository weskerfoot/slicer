#! /usr/bin/env python2

import scipy.io.wavfile as sio
import numpy as np
from random import shuffle
from sys import argv
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.project import rsync_project
import fabric.operations as op
from sys import argv

def rms(ss):
    return np.sqrt(np.abs(np.mean(np.square(ss))))

def findCeiling(ss, factor):
    slice = len(ss)
    while not (rms(ss[0:slice]) < 1.2):
        slice = int(len(ss)/factor)
        factor += 1
    return slice

def convert(infile):
    pcm = sio.read("/tmp/%s.to_silence.wav" % infile)
    sample_rate, samples = pcm

    # length in minutes
    length = (len(samples) / float(sample_rate)) / 60.0

    # the first n samples to cut out
    ceiling = findCeiling(samples, 2)

    # the total number of samples
    total = float(len(pcm[1]))

    if length <= 8:
        sio.write("/tmp/%s.silenced.wav" % infile, pcm[0], pcm[1][ceiling:])
        local("cp /tmp/\"%s.silenced.wav\" ./shortened/\"%s.wav\"" % (infile, infile))
        local("rm /tmp/\"%s.silenced.wav\"" % infile)

    local("rm /tmp/\"%s.to_silence.wav\"" % infile)

def to_wav(infile):
    local("ffmpeg -i \"%s\" /tmp/\"%s.to_silence.wav\"" % (infile, infile))

def silence(infile):
    to_wav(infile)
    convert(infile)

def silence_all():
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
