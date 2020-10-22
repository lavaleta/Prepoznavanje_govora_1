from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import os
from os.path import dirname, join as pjoin

# C:\Users\lavaleta\Desktop\RAF\Godina 4\Prepoznavanje govora\Data

wav_fname = "Man_sample.wav"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
WAV_FILE = pjoin(ROOT_DIR, "Data", wav_fname)
samplerate, data = wavfile.read(WAV_FILE)

p = 10
q = 300
dft_window = 0.2

length = data.shape[0] / samplerate

samplerate, data = wavfile.read(WAV_FILE)

print("sample rate =", samplerate)
print(f"length =",round(length, 2),"s")

def plot_amp(data, length):
    time = np.linspace(0., length, data.shape[0])
    plt.plot(time, data[:], label="Mono sound")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()

def calc_average_noise(data, length, samplerate):
    if(length < 0.1):
        return print("Error")
    sample_len = int(samplerate/10)
    return np.mean(data[:sample_len]) + 2*np.std(data[:sample_len])

def endpointing(data, average_noise):

    endpointing_data = np.empty(data.shape,data.dtype)

    for i in range(len(data)):
        if abs(data[i]) > average_noise:
            endpointing_data[i] = 1;
        else:
            endpointing_data[i] = 0;
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
                    tmp_index = i
                    for j in range(noise_len):
                        tmp_index -= 1
                        data[tmp_index] = 1
                state = "SIGNAL"
    return data

def flatten_down(data, window):
    state = "NOISE"
    signal_len = 0

    for i in range(len(data)):
        if state == "NOISE":
            if data[i] != 0:
                state = "MAYBE_SIGNAL"
                signal_len = 1
        elif state == "MAYBE_SIGNAL":
            if data[i] == 1:
                signal_len += 1
            else:
                if signal_len < window:
                    tmp_index = i
                    for j in range(signal_len):
                        tmp_index -= 1
                        data[tmp_index] = 0
                state = "NOISE"
    return data

def trim_endpointing(endpointing_data, data):
    first = 0
    last = 0
    for i in range(len(endpointing_data)):
        if endpointing_data[i] == 1:
            first = i
            break
    if first == 0:
        return "Error"

    endpointing_data = endpointing_data[::-1]
    for i in range(len(endpointing_data)):
        if endpointing_data[i] == 1:
            last = i
            break
    return data[first:(len(endpointing_data)-last)]

def dft(data):
    dft_data = np.abs(scipy.fft.fft(data))
    return dft_data

def plot_dft(dft_data, samplerate,dft_window):
    freqs = scipy.fft.fftfreq(len(dft_data)) * samplerate
    # print(freqs.shape)
    #
    # fig, ax = plt.subplots()
    #
    # ax.stem(freqs, dft_data)
    # ax.set_xlabel('Frequency in Hertz [Hz]')
    # ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
    # ax.set_xlim(0, samplerate / 2)
    #
    # plt.show()

    plt.hist(dft_data, bins=freqs.shape[0])
    plt.show()

plot_amp(data, length)

average_noise = calc_average_noise(data[500:],length,samplerate)

endpointing_data = endpointing(data, average_noise)

endpointing_data = flatten_down(flatten_up(endpointing_data, p), q)

print("average_noise =", round(average_noise,3))

print("Data length before trim =", len(data))

data = trim_endpointing(endpointing_data, data)

print("Data length after trim = ", len(data))

dft_data = dft(data[:int(samplerate*dft_window)])

plot_dft(dft_data, samplerate, dft_window)

