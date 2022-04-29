# import pyaudio
# p = pyaudio.PyAudio()
# for ii in range(p.get_device_count()):
# print(ii,p.get_device_info_by_index(ii).get('name'),p.get_device_info_by_index(ii).get('maxInputChannels'),p.get_device_info_by_index(ii).get('defaultSampleRate'))

import wave

import pyaudio

CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
dev_index = 0


def record():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=dev_index,
                    frames_per_buffer=CHUNK)

    print("Start recording")

    frames = []

    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
    except KeyboardInterrupt:
        print("Done recording")
    except Exception as e:
        print(str(e))

    sample_width = p.get_sample_size(FORMAT)

    stream.stop_stream()
    stream.close()
    p.terminate()

    return sample_width, frames


def record_to_file(file_path):
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    sample_width, frames = record()
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


if __name__ == '__main__':
    print('#' * 80)
    print("Please speak word(s) into the microphone")
    print('Press Ctrl+C to stop the recording')

    record_to_file('outpu.wav')

    print("Result written to output.wav")
    print('#' * 80)
