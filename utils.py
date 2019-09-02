import numpy as np
from scipy.io.wavfile import read
import librosa
import torch

max_wav_value=32768.0

def get_mask_from_lengths(lengths):
    max_len = torch.max(lengths).item()
    ids = torch.arange(0, max_len, out=torch.cuda.LongTensor(max_len))
    mask = (ids < lengths.unsqueeze(1)).byte()
    return mask


def load_wav_to_torch(full_path):
    sampling_rate, data = read(full_path)
    return torch.FloatTensor(data.astype(np.float32)), sampling_rate


def load_filepaths_and_text(filename, split="|"):
    with open(filename, encoding='utf-8') as f:
            def split_line(line):
                parts = line.strip().split(split)
                if len(parts) > 3:
                    raise Exception(
                        "incorrect line format for file: {}".format(filename))
                path = parts[0]

                text = parts[1]
                speaker_id = int(parts[2])

                return path, text, speaker_id
            filepaths_and_text = [split_line(line) for line in f]
    return filepaths_and_text

def to_gpu(x):
    x = x.contiguous()

    if torch.cuda.is_available():
        x = x.cuda(non_blocking=True)
    return torch.autograd.Variable(x)
