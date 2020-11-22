import tkinter
import tkinter as tk
import tkinter.messagebox
import pyaudio
import wave


class RecAUD:

    def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=1, rate=44100, py=pyaudio.PyAudio()):

        self.main = tkinter.Tk()
        self.collections = []
        self.main.title('Record')
        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.p = py
        self.frames = []
        self.st = 1
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        self.buttons = tkinter.Frame(self.main, padx=120, pady=20)

        self.buttons.pack(fill=tk.BOTH)

        self.strt_rec = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Start Recording', command=lambda: self.start_record())
        self.strt_rec.grid(row=0, column=0, padx=50, pady=5)
        self.stop_rec = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Stop Recording', command=lambda: self.stop())
        self.stop_rec.grid(row=1, column=0, columnspan=1, padx=50, pady=5)

        tkinter.mainloop()

    def start_record(self):
        self.st = 1
        self.strt_rec["bg"] = "red"
        self.main.configure(background='black')
        self.frames = []
        stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        while self.st == 1:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            print("----->recording<----------")
            self.main.update()

        stream.close()

        wf = wave.open('Data/test_recording.wav', 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def stop(self):
        self.st = 0
        self.strt_rec["bg"] = self.stop_rec.cget("bg")
