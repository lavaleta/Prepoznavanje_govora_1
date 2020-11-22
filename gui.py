import tkinter as tk
import assignment as assign
import numpy as np
import pyaudio
import wave
import sys
import mic
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter.filedialog import asksaveasfile
from tkinter import filedialog

load = False
local_data = False
mfcc_local = False
lpc_local = False
last_action = False
bool_audio = True

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(padx=20, pady=20)
        self.create_widgets()
        self.master.geometry("400x560") # 360x400
        root.iconbitmap(assign.pjoin(assign.os.path.dirname(assign.os.path.abspath(__file__)), "Data", "sound.ico"))

    def create_widgets(self):
        self.hi_there = tk.Label(self, height=1, width=16, text="wav file")
        self.hi_there.grid(column=1, row=0, padx=10, pady=5)

        txt0 = tk.Text(self, height=1, width=20)
        txt0.insert(tk.END, "test_recording")
        self.txt0 = txt0
        self.txt0.grid(column=0, row=0, padx=10, pady=5)

        self.hi_there = tk.Label(self,height = 1, width = 16, text ="p (flatten up)")
        self.hi_there.grid(column=1, row=1,padx=10, pady=5)

        txt1 = tk.Text(self, height=1, width=20)
        txt1.insert(tk.END, "7")
        self.txt1 = txt1
        self.txt1.grid(column=0, row=1,padx=10, pady=5)

        self.hi_there = tk.Label(self, height=1, width=16, text="q (flatten down)")
        self.hi_there.grid(column=1, row=2,padx=10, pady=5)

        txt2 = tk.Text(self, height=1, width=20)
        txt2.insert(tk.END, "7")
        self.txt2 = txt2
        self.txt2.grid(column=0, row=2,padx=10, pady=5)

        self.hi_there = tk.Label(self,height = 1, width = 16, text ="DFT window")
        self.hi_there.grid(column=1, row=3, padx=10, pady=5)

        v1 = tk.IntVar()

        Rad4 = tk.Radiobutton(self, text="DFT window in samples", variable=v1, value=0)
        Rad4.grid(sticky=tk.W)
        self.hi_there = Rad4
        self.hi_there.grid(column=0, row=4, padx=10, pady=5)

        Rad5 = tk.Radiobutton(self, text="DFT window in milliseconds", variable=v1, value=1)
        Rad5.grid(sticky=tk.W)
        self.hi_there = Rad5
        self.hi_there.grid(column=1, row=4, padx=10, pady=5)

        txt3 = tk.Text(self, height=1, width=20)
        txt3.insert(tk.END, "10")
        self.txt3 = txt3
        self.txt3.grid(column=0, row=3,padx=10, pady=5)

        self.hi_there = tk.Button(self, height=1, width=16, text="Enter data", command= lambda: self.enter_data())
        self.hi_there.grid(column=1, row=5, padx=10, pady=5)

        self.hi_there = tk.Button(self, height=1, width=16, text="Hold for mic", command=lambda: self.mic_on())
        self.hi_there.grid(column=0, row=5, padx=10, pady=5)

        txt4 = tk.Text(self, height=1, width=20)
        txt4.insert(tk.END, "10-5-3")
        self.txt4 = txt4
        self.txt4.grid(column=0, row=6, padx=10, pady=5)

        self.hi_there = tk.Label(self, height=1, width=16, text="LPC window-offset-p")
        self.hi_there.grid(column=1, row=6, padx=10, pady=5)

        v2 = tk.IntVar()

        Rad8 = tk.Radiobutton(self, text="LPC window in samples", variable=v2, value=0)
        Rad8.grid(sticky=tk.W)
        self.hi_there = Rad8
        self.hi_there.grid(column=0, row=7, padx=10, pady=5)

        Rad9 = tk.Radiobutton(self, text="LPC window in milliseconds", variable=v2, value=1)
        Rad9.grid(sticky=tk.W)
        self.hi_there = Rad9
        self.hi_there.grid(column=1, row=7, padx=10, pady=5)

        txt5 = tk.Text(self, height=1, width=20)
        txt5.insert(tk.END, "13")
        self.txt5 = txt5
        self.txt5.grid(column=0, row=8, padx=10, pady=5)

        self.hi_there = tk.Label(self, height=1, width=16, text="MFCC filter number")
        self.hi_there.grid(column=1, row=8, padx=10, pady=5)

        v3 = tk.IntVar()

        RadA = tk.Radiobutton(self, text="No coefficient", variable=v3, value=0)
        RadA.grid(sticky=tk.W)
        self.hi_there = RadA
        self.hi_there.grid(column=0, row=9, padx=10, pady=5)

        RadB = tk.Radiobutton(self, text="Δ", variable=v3, value=1)
        RadB.grid(sticky=tk.W)
        self.hi_there = RadB
        self.hi_there.grid(column=0, row=10, padx=10, pady=5)

        RadC = tk.Radiobutton(self, text="ΔΔ", variable=v3, value=2)
        RadC.grid(sticky=tk.W)
        self.hi_there = RadC
        self.hi_there.grid(column=0, row=11, padx=10, pady=5)

        self.hi_there = tk.Label(self, height=1, width=16, text="Dynamic parameters")
        self.hi_there.grid(column=1, row=10, padx=10, pady=5)

        txt6 = tk.Text(self, height=1, width=20)
        txt6.insert(tk.END, "2")
        self.txt6 = txt6
        self.txt6.grid(column=0, row=12, padx=10, pady=5)

        self.hi_there = tk.Label(self, height=1, width=16, text="t (Δ)")
        self.hi_there.grid(column=1, row=12, padx=10, pady=5)

        self.hi_there = tk.Button(self, height=1, width=17, text="LPC", command=lambda: self.lpc_click(v2.get()))
        self.hi_there.grid(sticky=tk.W)
        self.hi_there.grid(column=0, row=13, padx=10, pady=5)

        self.hi_there = tk.Button(self, height=1, width=16, text="MFCC", command=lambda: self.mfcc_click(v3.get(), v1.get()))
        self.hi_there.grid(column=1, row=13, padx=10, pady=5)

        lbl1 = tk.Label(self, height=1, width=16, text="Number of words: /")
        self.lbl1 = lbl1
        self.lbl1.grid(column=0, row=14, padx=10, pady=5)

        txt7 = tk.Text(self, height=1, width=20)
        txt7.insert(tk.END, "1")
        self.txt7 = txt7
        self.txt7.grid(column=0, row=15, padx=10, pady=5)

        self.hi_there = tk.Button(self, height=1, width=16, text="DTW", command=lambda: self.dtw_click(v3.get()))
        self.hi_there.grid(column=1, row=15, padx=10, pady=5)

    def enter_data(self):
        wav = self.txt0.get("1.0","end-1c")
        p = self.txt1.get("1.0","end-1c")
        q = self.txt2.get("1.0","end-1c")
        win = self.txt3.get("1.0","end-1c")

        plt, av_noise, data_len_b, data_len_a, samplerate, len = assign.init_variables(wav, int(p), int(q), win)

        global load
        load = True

        if data_len_b == -1:
            tk.messagebox.showwarning(title="Warning!", message="No word found.")
            return

        global local_data
        local_data = assign.global_data
        self.lbl1['text'] = "Number of words:" + str(assign.global_data.shape[0])

    def mic_on(self):
        some = mic.RecAUD()

    def plot_hist(self, selected):
        global load
        if load != True:
            tk.messagebox.showwarning(title="Warning!", message="No data loaded.")
            return

        window = self.txt3.get("1.0","end-1c")

        window = window.split("-")
        data = ""
        samplerate = assign.global_samplerate
        if selected == 0:
            data = assign.dft(assign.global_data[int(samplerate*float(window[0])):int(samplerate*float(window[1]))])
        elif selected == 1:
            data = assign.dft(assign.hamming(assign.global_data[int(samplerate*float(window[0])):int(samplerate*float(window[1]))]))
        elif selected == 2:
            data = assign.dft(assign.hanning(assign.global_data[int(samplerate*float(window[0])):int(samplerate*float(window[1]))]))

        freqs = assign.scipy.fft.fftfreq(len(data)) * samplerate

        print(len(freqs))

        data = np.interp(data, (data.min(), data.max()), (0, 100))

        fig = Figure(figsize=(5, 5), dpi=100)
        plot1 = fig.add_subplot(111)

        plot1.stem(freqs, data, label="Mono sound")
        plot1.set_xlabel('Frequency in Hertz [Hz]')
        plot1.set_ylabel('Frequency Domain (Spectrum) Magnitude')
        plot1.set_xlim(0, samplerate / 2)
        test = tk.Tk()
        test.title("Histogram")
        canvas = FigureCanvasTkAgg(fig, master=test)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, test)
        toolbar.update()
        canvas.get_tk_widget().pack()
        return

    def plot_spec(self, sel):
        global load
        if load != True:
            tk.messagebox.showwarning(title="Warning!", message="No data loaded.")
            return

        window = self.txt3.get("1.0", "end-1c")
        window = window.split("-")
        window = float(window[1])-float(window[0])

        win_size = int(assign.global_samplerate*window)

        new_data = np.empty(len(assign.global_data.shape))

        for i in range(len((assign.global_data)/win_size)):
            data = assign.global_data[i*win_size:i*win_size+win_size]
            if len(data) == 0:
                break;
            if sel == 0:
                data = assign.dft(data)
            elif sel == 1:
                data = assign.dft(assign.hamming(data))
            elif sel == 2:
                data = assign.dft(assign.hanning(data))

            new_data = np.append(new_data, data)

        global dft_data
        dft_data = new_data

        global dft
        dft = 1

        fig = Figure(figsize=(6, 5), dpi=100)
        plot1 = fig.add_subplot(111)

        plot1.specgram(new_data[0], Fs=assign.global_samplerate)
        plot1.set_xlabel('Time')
        plot1.set_ylabel('Frequency')
        xcoords=[2500, 5000, 7500, 10000, 12500, 15000, 17500, 20000]
        for xc in xcoords:
            plot1.axhline(y=xc, c='k', lw=1)

        test = tk.Tk()
        test.title("Spectrogram")
        canvas = FigureCanvasTkAgg(fig, master=test)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, test)
        toolbar.update()
        canvas.get_tk_widget().pack()
        return

    def lpc_click(self, option):
        global load
        if load != True:
            tk.messagebox.showwarning(title="Warning!", message="No data loaded.")
            return

        global local_data

        tmp = self.txt4.get("1.0", "end-1c")
        tmp = tmp.split("-")

        win = int(tmp[0])
        offset = int(tmp[1])
        p = int(tmp[2])

        if option == 1:
            win = int(assign.global_samplerate*(win/1000))
            offset =int(assign.global_samplerate*(offset/1000))

        loc_data = local_data

        j=0
        for a in loc_data:
            loc_data[j] = assign.lpc_prep(a, win, offset, p)

        global lpc_local
        lpc_local = loc_data
        global last_action
        last_action = "LPC"

        return file_save(lpc_local)

    def mfcc_click(self, option, option1):
        self.enter_data()
        global load
        if load != True:
            tk.messagebox.showwarning(title="Warning!", message="No data loaded.")
            return

        global local_data
        global last_action
        global mfcc_local
        last_action = "MFCC"

        filters = int(self.txt5.get("1.0", "end-1c"))
        t = int(self.txt6.get("1.0", "end-1c"))
        window = int(self.txt3.get("1.0", "end-1c"))
        tmp_win = window
        if option1 == 1:
            tmp_win = int(assign.global_samplerate*(window/1000))

        tmp = local_data

        dft = assign.dft(tmp, tmp_win)

        mfcc = dft

        j=0

        if option1 == 1:
            window /= 1000
        else:
            window /= assign.global_samplerate
        np.set_printoptions(threshold=sys.maxsize)

        for d in dft:
            tmp = assign.mfcc_local(d, window, filters)
            mfcc[j] = tmp.flatten('F')
            j+=1

        if option == 1:
            j=0
            for m in mfcc:
                dft[j] = assign.delta1(m.reshape((1, m.shape[0])), t)
                j += 1

            tmp = np.append(mfcc, dft)
            mfcc_local = tmp

            return file_save(tmp)
        elif option == 2:
            j = 0
            delta1 = mfcc
            for m in mfcc:
                dft[j] = assign.delta1(m.reshape((1, m.shape[0])), t)
                delta1[j] = assign.delta2(m.reshape((1, m.shape[0])), t)
                j += 1

            tmp = np.append(mfcc, dft)
            tmp = np.append(tmp, delta1)
            print(tmp.shape)
            mfcc_local = tmp
            return file_save(tmp)
        mfcc_local = mfcc
        return file_save(mfcc)

    def dtw_click(self, opt):
        global load
        if load != True:
            tk.messagebox.showwarning(title="Warning!", message="No data loaded.")
            return

        global local_data
        global lpc_local
        global mfcc_local
        global last_action
        word_index = int(self.txt7.get("1.0", "end-1c"))

        lookup = np.load(browseFiles(), allow_pickle=True)

        print('Ovo je akcije bre:', last_action)

        if last_action == "LPC":
            word = lpc_local[word_index - 1]

            min = sys.float_info.max
            min_i = -1
            for i, a in enumerate(lookup):
                d = assign.dtw_local(a.astype(np.double), word.astype(np.double))
                if min > d:
                    min = d
                    min_i = i

            path = assign.dtw.warping_path(lookup[i], word)
            assign.dtwvis.plot_warping(lookup[i], word, path, filename="warp.png")
            print("Min distance", min)
        elif last_action == "MFCC":
            word = mfcc_local[word_index - 1]
            if opt == 1: word = np.append(word, mfcc_local[word_index + 3 - 1], axis=0)
            if opt == 2:
                word = np.append(word, mfcc_local[word_index + 3 - 1], axis=0)
                word = np.append(word, mfcc_local[word_index + 6 - 1], axis=0)

            min_i = -1
            min = sys.float_info.max


            if opt == 0:
                for i in range(lookup.shape[0]):
                    d2 = 0
                    d3 = 0
                    d1 = assign.dtw_local(lookup[i].astype(np.double), word.astype(np.double))
                    d_sum = d1 + d2 + d3

                    if min > d_sum:
                        min = d_sum
                        min_i = i

            if opt == 1:
                crazy = int(lookup.shape[0] / 3)
                for i in range(int(lookup.shape[0] / 3)):
                    d1 = assign.dtw_local(lookup[i][0].astype(np.double), word[0].astype(np.double))
                    d2 = assign.dtw_local(lookup[i+crazy][0].astype(np.double), word[1].astype(np.double))
                    d_sum = d1 + d2

                    if min > d_sum:
                        min = d_sum
                        min_i = i

            if opt == 2:
                crazy = int(lookup.shape[0] / 3)
                for i in range(int(lookup.shape[0] / 3)):

                    d1 = assign.dtw_local(lookup[i][0].astype(np.double), word[0].astype(np.double))
                    d2 = assign.dtw_local(lookup[i + crazy][0].astype(np.double), word[1].astype(np.double))
                    d3 = assign.dtw_local(lookup[i + crazy + crazy][0].astype(np.double), word[2].astype(np.double))
                    d_sum = d1 + d2 + d3

                    if min > d_sum:
                        min = d_sum
                        min_i = i

            min_data = lookup[i]
            min_word = word
            if opt != 0:
                min_word = word[0]

            path = assign.dtw.warping_path(min_data, min_word)
            assign.dtwvis.plot_warping(min_data, min_word, path, filename="warp.png")

                # prikazati neki grafik = valjda reseno xD
                # dodati mikrofone
                # snimiti wav fajlove

            print(min_i, min)





def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("NumPy",
                                                      "*.npy*"),
                                                     ("all files",
                                                      "*.*")))

    return filename


def file_save(data):
    root1 = tk.Tk()
    root1.geometry('200x100')

    def save():
        files = [('File', '*.npy')]
        file = asksaveasfile(filetypes=files, defaultextension=files)
        np.save(file.name, data)
        root1.destroy()

    def quit_local():
        root1.destroy()

    btn1 = tk.Button(root1, text='Save', command=lambda: save(), height = 1, width = 5)
    btn1.grid(column=1, row=1, padx=30, pady=20)
    btn2 = tk.Button(root1, text='Cancel', command=lambda: quit_local(), height = 1, width = 5)
    btn2.grid(column=2, row=1, padx=30, pady=20)
    root1.title("Save")


root = tk.Tk()
root.title("Project 1")
root.resizable(False, False)
app = Application(master=root)
app.mainloop()