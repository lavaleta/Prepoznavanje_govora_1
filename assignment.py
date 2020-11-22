import numpy as np
import scipy.io
import os
from scipy.io import wavfile
from python_speech_features.base import mfcc, delta
from os.path import dirname, join as pjoin
from dtaidistance import dtw, dtw_visualisation as dtwvis

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

    average_noise = calc_average_noise(data[:int(samplerate/10)], win_len, samplerate)

    print("average_noise =", round(average_noise, 3))
    for i, v in enumerate(data):
        if v != 0:
            print(i)
            break

    endpointing_data = endpointing(data, average_noise, win_len)

    endpointing_data = flatten(endpointing_data, p, q)

    print("Data length before trim =", len(data))

    after_endpointing = np.array(trim_endpointing(endpointing_data, data, win_len))

    if isinstance(after_endpointing, int):
        print("No word found")
        return [data, length], -1, -1, -1, -1, round(length, 2)

    print("Data length after trim = ", len(after_endpointing[0]))

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

def flatten(data, p, q):
    signalLen = 0
    index = 0

    data = data.tolist()
    for i in data:
        if i == 0:
            signalLen += 1
        else:
            if p > signalLen > 0:
                for j in range(index - signalLen, index):
                    data[j] = 1
            signalLen = 0
        index += 1

    signalLen = 0
    index = 0

    for i in data:
        if i == 1:
            signalLen += 1
        else:
            if q > signalLen > 0:
                print(index)
                for j in range(index - signalLen, index):
                    data[j] = 0
            signalLen = 0
        index += 1
    return data

def trim_endpointing(endpointing_data, data, win_len):
    first = -1
    last = -1
    sig = False
    new_data = np.empty(10, dtype=object)
    j=0
    for i in range(len(endpointing_data)):
        if endpointing_data[i] == 1 and sig is False:
            first = i
            sig = True
        elif endpointing_data[i] == 0 and sig is True:
            last = i
            sig = False
            new_data[j] = data[int(first*win_len):int(last*win_len)]
            j+=1
    return new_data[:j]

def dft(data, win):
    j=0
    for a in data:
        dft_data = None
        for i in range(1,len(a)):
            if i % win == 0:
                tmp = scipy.fft.fft(a[i-win:i])[0:int(len(a[i-win:i]) / 2)] / len(a[i-win:i])
                tmp[1:] = tmp[1:] * 2
                dft_data = np.append(dft_data, tmp)
        dft_data = dft_data[1:]
        data[j] = np.abs(dft_data)
    return data

def hamming(data):
    return data * np.hamming(len(data))

def hanning(data):
    return data * np.hanning(len(data))

def lpc_prep(data, win, offset, p):

    i = win
    lpc_data = np.empty(2)
    lpc_data = lpc_data[:0]
    while i < len(data):
        tmp_data = data[i-win:i]
        i += offset
        lpc_data = np.append(lpc_data, lpc(tmp_data, p))

    return  data[:i-offset]

def lpc(data, p):
    R = [data.dot(data)]
    if R[0] == 0:
        return [1] + [0] * (p-2) + [-1]
    else:
        for i in range(1, p + 1):
            r = data[i:].dot(data[:-i])
            R.append(r)
        R = np.array(R)
        A = np.array([1, -R[1] / R[0]])
        E = R[0] + R[1] * A[1]
        for k in range(1, p):
            if (E == 0):
                E = 10e-17
            alpha = - A[:k+1].dot(R[k+1:0:-1]) / E
            A = np.hstack([A,0])
            A = A + alpha * A[::-1]
            E *= (1 - alpha**2)
        return A

def mfcc_local(data, win, nfilters):
    return mfcc(data, samplerate=global_samplerate, winlen=int(win), nfilt=int(nfilters))

def dtw_local(word, data):
    return dtw.distance_fast(word, data)

def delta1(features, t):
    return delta(features, t)

def delta2(features, t):
    return delta(delta(features, t), t)