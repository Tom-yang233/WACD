import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import sounddevice as sd
from scipy.signal import butter, lfilter

class RealTimePlotApp:
    def __init__(self, master, fs, carrier_frequency):
        self.master = master
        self.master.title("Real-time Waveform Plot")
        self.fs = fs
        self.carrier_frequency = carrier_frequency

        # 创建Matplotlib图形
        self.fig = Figure(figsize=(8, 8), dpi=100)
        self.ax_raw = self.fig.add_subplot(4, 1, 1)
        self.ax_i = self.fig.add_subplot(4, 1, 2)
        self.ax_q = self.fig.add_subplot(4, 1, 3)
        self.ax_constellation = self.fig.add_subplot(4, 1, 4)

        # 创建Tkinter画布
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # 设置回调函数
        self.callback_count = 0
        self.callback_interval = 100  # 每100毫秒更新一次
        self.stream = sd.InputStream(callback=self.callback, channels=1, samplerate=self.fs)

        # 低通滤波参数
        self.cutoff_frequency = 466  # 我们选择1000 Hz作为低通滤波截止频率
        self.filter_order = 4

        # 创建低通滤波器
        self.b, self.a = butter(self.filter_order, self.cutoff_frequency / (0.5 * self.fs), btype='low')

        # 开始流
        self.stream.start()

        # 固定y轴尺度
        self.ax_raw.set_ylim([-0.5, 0.5])
        self.ax_i.set_ylim([-0.5, 0.5])
        self.ax_q.set_ylim([-0.5, 0.5])

        # 初始x轴范围
        self.ax_raw.set_xlim([0, 0.005])
        self.ax_i.set_xlim([0, 0.005])
        self.ax_q.set_xlim([0, 0.005])
        self.ax_constellation.set_xlim([-0.3, 0.3])  # 星座图的x轴范围
        self.ax_constellation.set_ylim([-0.3, 0.3])  # 星座图的y轴范围

    def apply_lowpass_filter(self, signal):
        # 应用低通滤波器
        filtered_signal = lfilter(self.b, self.a, signal)
        return filtered_signal

    def callback(self, indata, frames, time, status):
        if status:
            print(status)

        t = np.linspace(0, frames / self.fs, frames, endpoint=False)
        window = np.hamming(len(indata[:, 0]))
        windowed_signal = indata[:, 0] * window
        demodulated_signal = windowed_signal * np.exp(-1j * 2 * np.pi * self.carrier_frequency * t)

        # 应用低通滤波
        i_filtered = self.apply_lowpass_filter(demodulated_signal.real)
        q_filtered = self.apply_lowpass_filter(demodulated_signal.imag)

        # 更新图形
        self.ax_raw.clear()
        self.ax_raw.plot(t, indata[:, 0])
        self.ax_raw.set_title('Raw Audio Signal')
        self.ax_raw.set_xlabel('Time (s)')
        self.ax_raw.set_ylabel('Amplitude')
        self.ax_raw.set_ylim([-0.5, 0.5])  # 固定y轴尺度

        self.ax_i.clear()
        self.ax_i.plot(t, i_filtered)
        self.ax_i.set_title('Filtered I Signal')
        self.ax_i.set_xlabel('Time (s)')
        self.ax_i.set_ylabel('Amplitude')
        self.ax_i.set_ylim([-0.5, 0.5])  # 固定y轴尺度

        self.ax_q.clear()
        self.ax_q.plot(t, q_filtered)
        self.ax_q.set_title('Filtered Q Signal')
        self.ax_q.set_xlabel('Time (s)')
        self.ax_q.set_ylabel('Amplitude')
        self.ax_q.set_ylim([-0.5, 0.5])  # 固定y轴尺度

        # 星座图
        self.ax_constellation.clear()
        self.ax_constellation.scatter(i_filtered, q_filtered, marker='.', alpha=0.1)  # 调整透明度
        self.ax_constellation.set_title('IQ Constellation Diagram')
        self.ax_constellation.set_xlabel('I Signal')
        self.ax_constellation.set_ylabel('Q Signal')
        self.ax_constellation.set_xlim([-0.1, 0.1])  # 星座图的x轴范围
        self.ax_constellation.set_ylim([-0.1, 0.1])  # 星座图的y轴范围

        # 设置x轴范围
        self.ax_raw.set_xlim([t[0], t[-1] + 0.005])
        self.ax_i.set_xlim([t[0], t[-1] + 0.005])
        self.ax_q.set_xlim([t[0], t[-1] + 0.005])

        self.canvas.draw()

        self.callback_count += 1
        if self.callback_count % (1000 // self.callback_interval) == 0:
            print("Updating plot...")

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    fs = 44100  # 采样率
    carrier_frequency = 600  # 本振频率

    root = tk.Tk()
    app = RealTimePlotApp(root, fs, carrier_frequency)
    app.run()
