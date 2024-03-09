# 注意，此文件用于将其他格式的 WAV 文件，转换为 Wave 库才能
# 读取的 WAV 文件。主要是这个库只能读取 Int16 格式的，没法
# 读取 float32 格式的，而 FL Studio 的 Edison 插件默认导
# 出的 WAV 文件是 float32 格式的，所以，这个脚本用来转换音频
# 到 int16 格式。


import os
import numpy
import soundfile as sf

sounds_folder = 'sounds'
output_folder = 'int16_sounds'


if __name__ == '__main__':
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(sounds_folder):
        if file.endswith('.wav'):
            file_path = os.path.join(sounds_folder, file)
            data, sample_rate = sf.read(file_path)
            output_path = os.path.join(output_folder, file)
            sf.write(output_path, (data * 32768).astype(numpy.int16), sample_rate)

