import sys
import os
import binwalk


def scan(file):
    try:
        for module in binwalk.scan(file, signature=True, quiet=True):
            return len(module.results) > 1
    except binwalk.ModuleException:
        pass
    return False


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python ' + sys.argv[0] + ' dir')
        exit(0)
    ok = 0
    failed = 0
    for fpath, dirs, fs in os.walk(sys.argv[1]):
        for f in fs:
            if f.endswith('.bin'):
                filename = os.path.join(fpath, f)
                ret = scan(filename)
                if not ret:
                    print(filename + ' failed')
                    failed += 1
                else:
                    ok += 1
    print('OK: ' + str(ok))
    print('Failed: ' + str(failed))
