from IPython.terminal.interactiveshell import TerminalInteractiveShell
from IPython import get_ipython
from PIL import ImageGrab
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pyaudio
import tkinter as tk

shell = TerminalInteractiveShell.instance()

get_ipython().run_line_magic('matplotlib', 'tk')

pixel_size = 8


def create_canvas(root, width, height):
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.pack()
    return canvas


def draw_image(canvas, data, pixel_size=pixel_size):
    color_mapping = [
        (91, 152, 188),
        (39, 99, 128),
        (135, 180, 198),
        (130, 130, 95),
        (255, 255, 254),
        (252, 238, 129),
        (248, 224, 85),
        (244, 200, 76),
        (238, 187, 62),
        (242, 228, 192),
        (235, 175, 50),
        (221, 188, 119),
        (146, 93, 9),
        (212, 148, 42),
        (112, 70, 6),
        (196, 124, 24),
    ]

    original_width = max(len(row) for row in data)
    original_height = len(data)

    image_array = np.zeros((original_height, original_width, 3), dtype=np.uint8)

    for i in range(original_height):
        for j in range(len(data[i])):
            color = color_mapping[int(data[i][j])]
            image_array[i, j] = color

    for i in range(original_height):
        for j in range(len(data[i])):
            draw_pixel(canvas, i, j, image_array[i, j], pixel_size)


def draw_pixel(canvas, i, j, color, pixel_size):
    x0, y0 = j * pixel_size, i * pixel_size
    x1, y1 = (j + 1) * pixel_size, (i + 1) * pixel_size
    hex_color = "#{:02x}{:02x}{:02x}".format(*color)
    canvas.create_rectangle(x0, y0, x1, y1, fill=hex_color, outline="")


def refresh_image(canvas, data, pixel_size=pixel_size):
    canvas.delete("all")  # 清空画布
    draw_image(canvas, data, pixel_size)


def save_image():
    canvas.update()
    x = root.winfo_rootx() + canvas.winfo_x()
    y = (root.winfo_rooty() +

         canvas.winfo_y())
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()

    image = ImageGrab.grab(bbox=(x, y, x1, y1))
    image.save("./pic/output.bmp")
    print("Image saved successfully!")


root = tk.Tk()
root.title("图像显示")
canvas = create_canvas(root, 100 * pixel_size, 100 * pixel_size)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000

CHUNK = 2048
trigger_frequency = 500
cnt = 0

target_frequencies = [697, 770, 852, 941, 1209, 1336, 1477, 1633, trigger_frequency]
frequency_range = 20
frequency_bounds = [(f - frequency_range, f + frequency_range) for f in target_frequencies]
fig, ax = plt.subplots()
bars = ax.bar(range(len(target_frequencies)), np.zeros(len(target_frequencies)))
ax.set_ylim(4, 8)
ax.set_xticks(range(len(target_frequencies)))
ax.set_xticklabels([f"{freq} Hz" for freq in target_frequencies])

dtmf_freqs = {
    '0': [(697, 1209), (1209, 697)],
    '1': [(697, 1336), (1336, 697)],
    '2': [(697, 1477), (1477, 697)],
    '3': [(697, 1633), (1633, 697)],
    '4': [(770, 1209), (1209, 770)],
    '5': [(770, 1336), (1336, 770)],
    '6': [(770, 1477), (1477, 770)],
    '7': [(770, 1633), (1633, 770)],
    '8': [(852, 1209), (1209, 852)],
    '9': [(852, 1336), (1336, 852)],
    '10': [(852, 1477), (1477, 852)],
    '11': [(852, 1633), (1633, 852)],
    '12': [(941, 1209), (1209, 941)],
    '13': [(941, 1336), (1336, 941)],
    '14': [(941, 1477), (1477, 941)],
    '15': [(941, 1633), (1633, 941)],
}

threshold = 5.5

is_sampling = False
samples = []
current_sample = []
result = []
pic_data = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], []]
i = 1


def freqs_to_char(freq_pair):
    for char, freq_pairs in dtmf_freqs.items():
        if freq_pair in freq_pairs:
            return char
    return None


p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


def update(frame):
    global cnt, is_sampling, current_sample, samples, pic_data, i

    try:
        refresh_image(canvas, pic_data)

        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)

        fft_result = np.fft.fft(data)
        frequencies_fft = np.fft.fftfreq(len(fft_result), 1 / RATE)

        magnitudes = [np.mean(np.abs(fft_result[(frequencies_fft >= f_low) & (frequencies_fft <= f_high)]))
                      for (f_low, f_high) in frequency_bounds]
        trigger_amplitude = np.log10(magnitudes[8])

        if not is_sampling and trigger_amplitude > threshold:
            is_sampling = True
            current_sample = []

        elif is_sampling and trigger_amplitude < threshold:
            is_sampling = False
            if current_sample:
                chars = [char for char in current_sample if char is not None]
                most_common_char = max(set(chars), key=chars.count)

                # print(f"Detected character: {most_common_char}")
                if most_common_char == '15' and len(pic_data[i]) != 0:
                    pic_data.append([])
                    i = i + 1
                else:
                    pic_data[i].append(most_common_char)
                print(pic_data)

        if is_sampling:
            if any(np.log10(m + 1) > threshold for m in magnitudes[:8]):
                max_indices = np.argsort(magnitudes[:8])[-2:]
                freq1 = target_frequencies[max_indices[0]]
                freq2 = target_frequencies[max_indices[1]]
                freq_pair = (freq1, freq2)
                current_sample.append(freqs_to_char(freq_pair))

        for bar, magnitude in zip(bars, magnitudes):
            magnitude_log = np.log10(magnitude + 1)
            bar.set_height(magnitude_log)
        return bars

    except Exception as e:
        print(f"Error: {e}")


ani = animation.FuncAnimation(fig, update, blit=False, interval=10)

plt.show(block=True)

stream.stop_stream()
stream.close()
p.terminate()

save_image()