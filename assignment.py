from scipy.io import wavfile
import numpy as np
import scipy.io
import os
from os.path import dirname, join as pjoin

# C:\Users\lavaleta\Desktop\RAF\Godina 4\Prepoznavanje govora\Data
global_data = 0
global_samplerate = 0
global_left = 0
global_right = 0

def init_variables(wav_fname, p, q, dft_window):
    wav_fname+=".wav"
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    WAV_FILE = pjoin(ROOT_DIR, "Data", wav_fname)
    samplerate, data = wavfile.read(WAV_FILE)

    length = data.shape[0] / samplerate

    if data.shape == (len(data), 2):
        data = data.T[0]

    print("sample rate =", samplerate)
    print(f"length =", round(length, 2), "s")

    win_len = samplerate * 0.01

    average_noise = calc_average_noise(data[:int(samplerate/10)], length, samplerate)

    endpointing_data = endpointing(data, average_noise, win_len)

    endpointing_data = flatten_down(flatten_up(endpointing_data, p), q)

    print("average_noise =", round(average_noise, 3))

    print("Data length before trim =", len(data))

    after_endpointing = trim_endpointing(endpointing_data, data, win_len)

    if isinstance(after_endpointing, int):
        print("No word found")
        return [data, length], -1, -1, -1, -1, round(length, 2)

    print("Data length after trim = ", len(after_endpointing))

    global global_data
    global_data = after_endpointing
    global global_samplerate
    global_samplerate = samplerate

    return [data, length], round(average_noise, 3), len(data), len(after_endpointing), samplerate, round(length, 2)

def calc_average_noise(data, length, samplerate):
    if(length < 0.1):
        return print("Error")
    sample_len = int(samplerate/10)
    return np.mean(np.abs(data[:sample_len])) + 2*np.std(np.abs(data[:sample_len]))

def endpointing(data, average_noise, win_len):

    endpointing_data = np.zeros(data.shape,data.dtype)
    win_len=int(win_len)
    j=0
    for i in range(1,len(data)):
        if i%win_len==0:
            avg = np.mean(np.abs(data[i-win_len:i]))
            if avg > average_noise:
                endpointing_data[j] = 1
            else:
                endpointing_data[j] = 0
            j+=1

    endpointing_data = endpointing_data[:j]
    return endpointing_data;

def flatten_up(data, window):
    state = "NOISE"
    noise_len = 0

    for i in range(len(data)):
        if state == "NOISE":
            if data[i] != 0:
                state = "SIGNAL"
        elif state == "SIGNAL":
            if data[i] != 1:
                state = "MAYBE_NOISE"
                noise_len = 1
        else:
            if data[i] == 0:
                noise_len += 1
            else:
                if noise_len < window:
                    for j in range(noise_len):
                        data[i-j-1] = 1
                state = "SIGNAL"
    return data

def flatten_down(data, window):
    signal_len = 0
    state = 0

    for i in range(len(data)):
        if state == 0:
            if data[i] == 1:
                signal_len=1
                state = 1
        elif state == 1:
            if data[i] == 1:
                signal_len+=1
            else:
                if signal_len < window:
                    for j in range(signal_len):
                        data[i-j-1] = 0
                state = 0
    return data

def trim_endpointing(endpointing_data, data, win_len):
    first = -1
    last = -1
    for i in range(len(endpointing_data)):
        if endpointing_data[i] == 1:
            first = i
            break
    if int(first) == -1:
        return -1

    endpointing_data = endpointing_data[::-1]
    for i in range(len(endpointing_data)):
        if endpointing_data[i] == 1:
            last = i
            break

    endpointing_data = endpointing_data[::-1]
    if int(last) == -1:
        return -1

    global global_left
    global_left=int(first*win_len)
    global global_right
    global_right=int(len(data)-(last*win_len))

    return data[int(first*win_len):int((len(data)-(last*win_len)))]

def dft(data):
    dft_data = scipy.fft.fft(data)[0:int(len(data)/2)]/len(data)
    dft_data[1:] = dft_data[1:]*2
    return np.abs(dft_data)

def hamming(data):
    return data * np.hamming(len(data))

def hanning(data):
    return data * np.hanning(len(data))

