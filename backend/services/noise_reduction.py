import librosa
import noisereduce as nr
import soundfile as sf

def reduce_noise(input_path, output_path):
    y, sr = librosa.load(input_path, sr=None)
    reduced = nr.reduce_noise(y=y, sr=sr)
    sf.write(output_path, reduced, sr)
    return output_path