import os
import time
from typing import Dict, List, Set
import keyboard
import threading
import pyaudio
import wave


class PyaudioPlayingThread(threading.Thread):
    def __init__(self, sound_path: str):
        super().__init__()
        self.sound_path = sound_path
        self.p = pyaudio.PyAudio()

    def run(self):
        with wave.open(self.sound_path, 'rb') as f:
            data = f.readframes(1024)

            # 这里用 try catch 也是主播太菜了不会写啊
            # 这个 channels 不知道为什么，我没办法从 data 这里拿到
            try:
                stream = self.p.open(
                    format=self.p.get_format_from_width(f.getsampwidth()),
                    channels=2,
                    rate=f.getframerate(),
                    frames_per_buffer=1024,
                    output=True
                )
            except OSError:
                stream = self.p.open(
                    format=self.p.get_format_from_width(f.getsampwidth()),
                    channels=1,
                    rate=f.getframerate(),
                    frames_per_buffer=1024,
                    output=True
                )

            while len(data) > 0:
                stream.write(data)
                data = f.readframes(1024)

            stream.stop_stream()
            stream.close()
            self.p.terminate()


# 为什么要写这么 ↑↓ 的东西呢？
# 主要是因为，我觉得，这样写，延迟会小一点，用内存换时间
# 哎，主播太菜了啊，不会写啊

keythreads: Dict[str, PyaudioPlayingThread] = {}


def updateThreads():
    # 初始化所有的线程对象

    for key in getAllKeyAvailable():
        if key not in keythreads:
            keythreads[key] = PyaudioPlayingThread(sound_path=getSoundPathByKey(key))


def getAllKeyAvailable() -> List[str]:
    base = os.path.join(os.getcwd(), 'int16_sounds')

    return [f.split('.')[0].replace("点", '.') for f in os.listdir(base) if os.path.isfile(os.path.join(base, f))]


def getSoundPathByKey(key: str):
    return os.path.join(os.getcwd(), 'int16_sounds', f'{key}.wav')


def playSound(key: str):
    soundPath = getSoundPathByKey(key)
    
    if os.path.exists(soundPath):
        if key in keythreads:
            keythreads[key].start()
            keythreads[key] = PyaudioPlayingThread(sound_path=soundPath)
        else:
            PyaudioPlayingThread(sound_path=soundPath).start()
            keythreads[key] = PyaudioPlayingThread(sound_path=soundPath)


lastTimeKeyDown: Set[str] = set()


if __name__ == "__main__":
    updateThreads()

    while True:
        for key in getAllKeyAvailable():
            try:
                if keyboard.is_pressed(key):
                    if key not in lastTimeKeyDown:
                        playSound(key)
                        lastTimeKeyDown.add(key)
                else:
                    if key in lastTimeKeyDown:
                        lastTimeKeyDown.remove(key)
            except ValueError as e:
                print(repr(e))

        time.sleep(0.01)
