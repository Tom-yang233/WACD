import pyaudio
import numpy as np
import struct
from PIL import Image

global DTMF_1_sig, DTMF_2_sig, DTMF_3_sig, DTMF_4_sig, DTMF_A_sig, DTMF_B_sig, DTMF_C_sig, DTMF_D_sig, trigger_sig
global index, pic, CHUNK


def sin_signal(t, freq, phi=0, AMPLITUDE=4096):
    sig = np.cos(2 * np.pi * (freq * t + phi)) * AMPLITUDE
    return sig.astype(np.int16)


def bmp_file_in(file_path):
    img = Image.open(file_path)
    pic = [15]

    color_palette = img.getpalette()
    img_data = np.array(img)
    color_index_array = np.zeros_like(img_data, dtype=np.uint8)

    for i in range(16):
        mask = (img_data == i)
        color_index_array[mask] = i

    for i in color_index_array:
        for j in i:
            if j == 15:
                j=14
            pic.append(int(j))
        pic.append(15)

    return pic, color_palette


def process():
    global index
    if index >= len(pic):
        return None
    if pic[index] == -1:
        out_data = DTMF_1_sig + trigger_sig
    elif pic[index] == 0:
        out_data = DTMF_1_sig + DTMF_A_sig + trigger_sig
    elif pic[index] == 1:
        out_data = DTMF_1_sig + DTMF_B_sig + trigger_sig
    elif pic[index] == 2:
        out_data = DTMF_1_sig + DTMF_C_sig + trigger_sig
    elif pic[index] == 3:
        out_data = DTMF_1_sig + DTMF_D_sig + trigger_sig
    elif pic[index] == 4:
        out_data = DTMF_2_sig + DTMF_A_sig + trigger_sig
    elif pic[index] == 5:
        out_data = DTMF_2_sig + DTMF_B_sig + trigger_sig
    elif pic[index] == 6:
        out_data = DTMF_2_sig + DTMF_C_sig + trigger_sig
    elif pic[index] == 7:
        out_data = DTMF_2_sig + DTMF_D_sig + trigger_sig
    elif pic[index] == 8:
        out_data = DTMF_3_sig + DTMF_A_sig + trigger_sig
    elif pic[index] == 9:
        out_data = DTMF_3_sig + DTMF_B_sig + trigger_sig
    elif pic[index] == 10:
        out_data = DTMF_3_sig + DTMF_C_sig + trigger_sig
    elif pic[index] == 11:
        out_data = DTMF_3_sig + DTMF_D_sig + trigger_sig
    elif pic[index] == 12:
        out_data = DTMF_4_sig + DTMF_A_sig + trigger_sig
    elif pic[index] == 13:
        out_data = DTMF_4_sig + DTMF_B_sig + trigger_sig
    elif pic[index] == 14:
        out_data = DTMF_4_sig + DTMF_C_sig + trigger_sig
    elif pic[index] == 15:
        out_data = DTMF_4_sig + DTMF_D_sig + trigger_sig
    else:
        out_data = DTMF_A_sig

    if index < len(pic):
        print(index, pic[index])
        index += 1
        return out_data


def callbackOut(in_data, frame_count, time_info, status_flag):
    global CHUNK

    out_data_int = process()
    if out_data_int is None:
        return None, pyaudio.paComplete
    else:
        out_data_byte = struct.pack('<' + str(CHUNK) + 'h', *out_data_int)
        return out_data_byte, pyaudio.paContinue


def tx_pic(file_path, RATE=48000, CHANNELS=1, _CHUNK=20000, FORMAT=pyaudio.paInt16, AMPLITUDE=4096, trigger_freq=500):
    global DTMF_1_sig, DTMF_2_sig, DTMF_3_sig, DTMF_4_sig, DTMF_A_sig, DTMF_B_sig, DTMF_C_sig, DTMF_D_sig, trigger_sig
    global pic, index, CHUNK

    t = np.arange(0, _CHUNK / RATE, 1 / RATE)
    CHUNK = _CHUNK

    DTMF_1_sig = sin_signal(t, freq=697, AMPLITUDE=AMPLITUDE)
    DTMF_2_sig = sin_signal(t, freq=770, AMPLITUDE=AMPLITUDE)
    DTMF_3_sig = sin_signal(t, freq=852, AMPLITUDE=AMPLITUDE)
    DTMF_4_sig = sin_signal(t, freq=941, AMPLITUDE=AMPLITUDE)

    DTMF_A_sig = sin_signal(t, freq=1209, AMPLITUDE=AMPLITUDE)
    DTMF_B_sig = sin_signal(t, freq=1336, AMPLITUDE=AMPLITUDE)
    DTMF_C_sig = sin_signal(t, freq=1477, AMPLITUDE=AMPLITUDE)
    DTMF_D_sig = sin_signal(t, freq=1633, AMPLITUDE=AMPLITUDE)

    trigger_sig = sin_signal(t, freq=trigger_freq, AMPLITUDE=AMPLITUDE)
    trigger_sig[0:int(_CHUNK/10)] = 0
    trigger_sig[int(9*_CHUNK/10):_CHUNK] = 0

    pic = bmp_file_in(file_path)[0]
    index = 0

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callbackOut)

    stream.start_stream()
    while stream.is_active():
        pass
    stream.stop_stream()
    stream.close()
    p.terminate()
