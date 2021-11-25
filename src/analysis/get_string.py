import os


def is_visible_char(ch):
    return (64 < ch < 91) or (47 < ch < 58) or (96 < ch < 123)


def extract_string_from_file(filename):
    firmware = open(filename, 'rb')
    data = firmware.read()
    s = ''
    word = ''
    for i in data:
        if is_visible_char(i):
            word += chr(i)
        else:
            length = len(word)
            if length > 0:
                if length > 1:  # a word contains at least 2 characters
                    s += ' ' + word
                word = ''
    return s


def scan_string(path, output_filename):
    if not os.path.exists(path):
        print(path + ' not exists')
        return
    try:
        with open(output_filename, 'w', encoding='utf-8') as a:
            filename = os.walk(path)
            path = path + os.sep
            for root, dirs, files in filename:
                for f in files:
                    filename = path + f
                    if filename.endswith('.bin'):
                        s = extract_string_from_file(filename)
                        # print(f + ': ' + s)
                        a.write(s + '\n')
    except Exception as err:
        print(err)


if __name__ == '__main__':
    dir = ['HiWiFi', 'MERCURY', 'MIWIFI', 'TENDA', 'TP-LINK']
    for d in dir:
        scan_string('/home/qiujing/firmware/' + d, '/home/qiujing/project/firmware-detect/data/' + d + '-str.txt')
    # s = extract_string_from_file('/home/qiujing/firmware2/MERCURY/mr816v1.bin')
    # print(s)
