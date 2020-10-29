from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import os
from os.path import dirname, join as pjoin

# C:\Users\lavaleta\Desktop\RAF\Godina 4\Prepoznavanje govora\Data
global_data = 0
global_samplerate = 0

def init_variables(wav_fname, p, q, dft_window):
    wav_fname+=".wav"
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    WAV_FILE = pjoin(ROOT_DIR, "Data", wav_fname)
    samplerate, data = wavfile.read(WAV_FILE)

    length = data.shape[0] / samplerate

    print("sample rate =", samplerate)
    print(f"length =", round(length, 2), "s")

    average_noise = calc_average_noise(data[int(samplerate/100):], length, samplerate)

    endpointing_data = endpointing(data, average_noise)

    endpointing_data = flatten_down(flatten_up(endpointing_data, p), q)

    print("average_noise =", round(average_noise, 3))

    print("Data length before trim =", len(data))

    # one = 0
    # zero = 0
    for i in range(len(data)):
        if(endpointing_data[i] == 1):
            print(i, data[i])
        # else:
        #     print(i, data[i])

    after_endpointing = trim_endpointing(endpointing_data, data)

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
    print(sample_len)
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
                    for j in range(noise_len):
                        data[i-j] = 1
                state = "SIGNAL"
    return data

def flatten_down(data, window):
    signal_len = 0

    for i in range(len(data)):

        if data[i] == 1:
            signal_len += 1
        else:
            if signal_len < window:
                for j in range(signal_len):
                    data[i-j-1] = 0
            signal_len = 0
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
    dft_data = scipy.fft.fft(data)[0:int(len(data)/2)]/len(data)
    dft_data[1:] = dft_data[1:]*2
    return np.abs(dft_data)

def hamming(data):
    return data * np.hamming(len(data))

def hanning(data):
    return data * np.hanning(len(data))

# def plot_dft(dft_data, samplerate):
#     freqs = scipy.fft.fftfreq(len(dft_data)) * samplerate
#
#     fig, ax = plt.subplots()
#
#     ax.stem(freqs, dft_data)
#     ax.set_xlabel('Frequency in Hertz [Hz]')
#     ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
#     ax.set_xlim(0, samplerate/2)
#
#     plt.show()
#
# def plot_spectrogram(data, samplerate):
#
#     plt.title('Spectrogram')
#     plt.specgram(data, Fs=samplerate)
#     plt.xlabel('Time')
#     plt.ylabel('Frequency')
#     plt.show()
#
# def plot_amp(data, length):
#     time = np.linspace(0., length, data.shape[0])
#     plt.plot(time, data[:], label="Mono sound")
#     plt.legend()
#     plt.xlabel("Time [s]")
#     plt.ylabel("Amplitude")
#     # plt.show()
#     return [data, length]
