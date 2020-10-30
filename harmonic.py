from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import os
from os.path import dirname, join as pjoin

wav_fname = "harmonic"
wav_fname+=".wav"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
WAV_FILE = pjoin(ROOT_DIR, "Data", wav_fname)
Fs = 44100
T = 1/Fs
t1 = 0.1
N1 = Fs*t1
t_vec1 = np.arange(N1)*T
A1 = 100

t2 = 5
N2 = Fs*t2
t_vec2 = np.arange(N2)*T
A2 = 500

def makeHarmonic(A, freq, t_vec):
	omega = 2*np.pi*freq
	y = A * np.sin(omega*t_vec)
	return y

t_vec_vinal = np.arange(N1+N2)*T

y1 = makeHarmonic(A1, 50, t_vec1)
y1 = np.append(y1, makeHarmonic(A2, 50, t_vec2))
plt.plot(t_vec_vinal,y1)
plt.show()