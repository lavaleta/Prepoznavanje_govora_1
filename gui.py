import tkinter as tk
import assignment as assign
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

load = False

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # self.pack()
        self.grid(padx=20, pady=20)
        self.create_widgets()
        self.master.geometry("360x360") # 360x400
        root.iconbitmap(assign.pjoin(assign.os.path.dirname(assign.os.path.abspath(__file__)), "Data", "sound.ico"))

    def create_widgets(self):
        self.hi_there = tk.Label(self, height=1, width=16, text="wav file")
        self.hi_there.grid(column=1, row=0, padx=10, pady=5)

        txt0 = tk.Text(self, height=1, width=20)
        txt0.insert(tk.END, "Man_sample")
        self.txt0 = txt0
        self.txt0.grid(column=0, row=0, padx=10, pady=5)

        self.hi_there = tk.Label(self,height = 1, width = 16, text ="p (flatten up)")
        self.hi_there.grid(column=1, row=1,padx=10, pady=5)

        txt1 = tk.Text(self, height=1, width=20)
        txt1.insert(tk.END, "10")
        self.txt1 = txt1
        self.txt1.grid(column=0, row=1,padx=10, pady=5)

        self.hi_there = tk.Label(self, height=1, width=16, text="q (flatten down)")
        self.hi_there.grid(column=1, row=2,padx=10, pady=5)

        txt2 = tk.Text(self, height=1, width=20)
        txt2.insert(tk.END, "150")
        self.txt2 = txt2
        self.txt2.grid(column=0, row=2,padx=10, pady=5)

        self.hi_there = tk.Label(self,height = 1, width = 16, text ="window (ms)")
        self.hi_there.grid(column=1, row=3, padx=10, pady=5)

        txt3 = tk.Text(self, height=1, width=20)
        txt3.insert(tk.END, "0.2-0.4")
        self.txt3 = txt3
        self.txt3.grid(column=0, row=3,padx=10, pady=5)

        self.hi_there = tk.Button(self, height=1, width=16, text="Enter data", command= lambda: self.enter_data())
        self.hi_there.grid(column=1, row=4, padx=10, pady=5)

        v = tk.IntVar()
        # v.set("0")

        Rad1 = tk.Radiobutton(self, text="No window", variable=v, value=0)
        Rad1.grid(sticky=tk.W)
        self.hi_there = Rad1
        self.hi_there.grid(column=0, row=5, padx=10, pady=5)

        Rad2 = tk.Radiobutton(self, text="Hamming", variable=v, value=1)
        Rad2.grid(sticky=tk.W)
        self.hi_there = Rad2
        self.hi_there.grid(column=0, row=6, padx=10, pady=5)

        Rad3 = tk.Radiobutton(self, text="Hanning", variable=v, value=2)
        Rad3.grid(sticky=tk.W)
        self.hi_there = Rad3
        self.hi_there.grid(column=0, row=7, padx=10, pady=5)

        self.hi_there = tk.Label(self, height=1, width=16, text="window function")
        self.hi_there.grid(column=1, row=6, padx=10, pady=5)

        self.hi_there = tk.Button(self, height=1, width=16, text="Histogram", command= lambda: self.plot_hist(v.get()))
        self.hi_there.grid(column=0, row=8, padx=10, pady=5)

        self.hi_there = tk.Button(self, height=1, width=16, text="Spectrogram", command= lambda: self.plot_spec())
        self.hi_there.grid(column=1, row=8, padx=10, pady=5)

    def enter_data(self):
        global load
        load = True

        wav = self.txt0.get("1.0","end-1c")

        p = self.txt1.get("1.0","end-1c")

        q = self.txt2.get("1.0","end-1c")

        win = self.txt3.get("1.0","end-1c")

        print(wav, p , q, win)

        plt, av_noise, data_len_b, data_len_a, samplerate, len = assign.init_variables(wav, int(p), int(q), win)

        test = tk.Tk()
        test.title("Amplitude/Time")

        data = plt[0]
        time = np.linspace(0., len, data.shape[0])

        fig = Figure(figsize=(5, 5), dpi=100)
        plot1 = fig.add_subplot(111)

        plot1.plot(time, data[:], label="Mono sound")
        canvas = FigureCanvasTkAgg(fig,master=test)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas,test)
        toolbar.update()
        canvas.get_tk_widget().pack()

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
            data = assign.dft(assign.global_data[int(samplerate*float(window[0])):int(samplerate*float(window[1]))]) # windowwwwwwwwwwwwwwwwwww
        elif selected == 1:
            data = assign.dft(assign.hamming(assign.global_data[int(samplerate*float(window[0])):int(samplerate*float(window[1]))]))
        elif selected == 2:
            data = assign.dft(assign.hanning(assign.global_data[int(samplerate*float(window[0])):int(samplerate*float(window[1]))]))

        freqs = assign.scipy.fft.fftfreq(len(data)) * samplerate

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

    def plot_spec(self):
        global load
        if load != True:
            tk.messagebox.showwarning(title="Warning!", message="No data loaded.")
            return

        # assign.plot_spectrogram(assign.global_data, assign.global_samplerate)

        fig = Figure(figsize=(5, 5), dpi=100)
        plot1 = fig.add_subplot(111)

        plot1.specgram(assign.global_data, Fs=assign.global_samplerate)
        plot1.set_xlabel('Time')
        plot1.set_ylabel('Frequency')
        test = tk.Tk()
        test.title("Spectrogram")
        canvas = FigureCanvasTkAgg(fig, master=test)
        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, test)
        toolbar.update()
        canvas.get_tk_widget().pack()
        return

root = tk.Tk()
root.title("Project 1")
root.resizable(False, False)
app = Application(master=root)
app.mainloop()