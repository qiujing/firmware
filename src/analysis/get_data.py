import csv
import math
import os

import gensim
from gensim.models.doc2vec import Doc2Vec
from tqdm import tqdm


def get_entropy(filepath):
    f = open(filepath, 'rb')
    data = f.read()
    entropy = 0
    for x in range(256):
        p_x = data.count(x) / len(data)
        if p_x > 0:
            entropy += -p_x * math.log(p_x, 2)
    entropy /= 8
    return entropy


def get_avg(filepath):
    f = open(filepath, 'rb')
    data = f.read()

    block_size = 1
    sum = 0
    for x in range(0, len(data) // block_size):
        start = x * block_size
        end = start + block_size
        for b in data[start:end]:
            sum += b
    avg = sum / len(data)

    return avg


def is_visible_char(ch):
    return (64 < ch < 91) or (47 < ch < 58) or (96 < ch < 123)


# 从单个文件扫描字符串
def extract_string_from_file(filename):
    firmware = open(filename, 'rb')
    data = firmware.read()
    s = ''
    word = ''
    for b in data:
        if is_visible_char(b):
            word += chr(b)
        else:
            length = len(word)
            if length > 0:
                if length > 1:  # 只加入长度不低于2的单词
                    s += ' ' + word
                word = ''
    return s


if __name__ == '__main__':
    # logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model = Doc2Vec.load("model_all_string")
    dir = ['HiWiFi', 'MERCURY', 'MIWIFI', 'TENDA', 'TP-LINK']
    ROOT = '/home/qiujing/firmware2'

    output_path = '/home/qiujing/project/firmware-detect/data/data.csv'

    # scan all firmare files
    fileList = []
    for i, d in enumerate(dir):
        label = i + 1  # label start from 1
        path = os.path.join(ROOT, d)
        for root, dirs, files in os.walk(path):
            for filename in files:
                filepath = os.path.join(path, filename)
                if filename.endswith('.bin'):
                    fileList.append((filepath, label))
    # print(len(fileList))

    # generate data one by one
    with open(output_path, 'w', encoding='utf-8') as a:
        fwcsv = csv.writer(a)
        for filepath, label in tqdm(fileList):
            size = os.path.getsize(filepath)
            entropy = get_entropy(filepath)
            avg = get_avg(filepath)
            s = extract_string_from_file(filepath)
            text = gensim.utils.simple_preprocess(s)
            inferred_vector_dm = model.infer_vector(text)

            row = [size, entropy, avg]
            for i in inferred_vector_dm:
                row.append(float(i))
            row.append(label)
            fwcsv.writerow(row)
