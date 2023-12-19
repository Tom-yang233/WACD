import numpy as np
import sounddevice as sd

def generate_qam_symbols(data, symbol_duration=1):
    # 映射数据到16QAM符号
    qam_mapping = {
        (0, 0, 0, 0): complex(3, 3),
        (0, 0, 0, 1): complex(3, 1),
        (0, 0, 1, 0): complex(3, -3),
        (0, 0, 1, 1): complex(3, -1),
        (0, 1, 0, 0): complex(1, 3),
        (0, 1, 0, 1): complex(1, 1),
        (0, 1, 1, 0): complex(1, -3),
        (0, 1, 1, 1): complex(1, -1),

        (1, 0, 0, 0): complex(3, 3),
        (1, 0, 0, 1): complex(3, 1),
        (1, 0, 1, 0): complex(3, -3),
        (1, 0, 1, 1): complex(3, -1),
        (1, 1, 0, 0): complex(1, 3),
        (1, 1, 0, 1): complex(1, 1),
        (1, 1, 1, 0): complex(1, -3),
        (1, 1, 1, 1): complex(1, -1),
    }

    symbols = []
    for i in range(0, len(data), 4):
        bits = data[i:i + 4]
        if len(bits) < 4:
            bits.extend([0] * (4 - len(bits)))
        symbol = qam_mapping.get(tuple(bits), complex(0, 0))
        symbols.append(symbol)

    return symbols


def modulate_qam(symbols, fs=44100, duration=1, carrier_frequency=600):
    # 16QAM调制
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    modulated_signal = np.array([])

    for symbol in symbols:
        modulated_signal = np.concatenate([modulated_signal, symbol * np.exp(1j * 2 * np.pi * carrier_frequency * t)])

    # 归一化信号的幅度
    modulated_signal_normalized = modulated_signal / np.max(np.abs(modulated_signal))

    return modulated_signal_normalized


def main():
    # 生成随机数据
    data = np.random.randint(0, 2, 500)

    # 映射为16QAM符号
    symbols = generate_qam_symbols(data)

    # 调制为音频信号，使用1000 Hz的频率
    modulated_signal = modulate_qam(symbols, carrier_frequency=600)

    # 播放音频信号
    fs = 44100  # 采样率
    sd.play(modulated_signal.real, samplerate=fs)
    sd.wait()


if __name__ == "__main__":
    main()