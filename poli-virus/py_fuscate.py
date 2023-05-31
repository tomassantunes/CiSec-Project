#!/usr/bin/env python
# coding: utf-8
# By Sandaru Ashen: https://github.com/Sl-Sanda-Ru, https://t.me/Sl_Sanda_Ru


import os
import sys
import subprocess
import argparse
import random
import time
import marshal
import lzma
import gzip
import bz2
import binascii
import zlib

import requests
import tqdm
import colorama

PYTHON_VERSION = 'python' + '.'.join(str(i) for i in sys.version_info[:2])

def encode(source:str) -> str:
    selected_mode = random.choice((lzma, gzip, bz2, binascii, zlib))
    marshal_encoded = marshal.dumps(compile(source, 'Py-Fuscate', 'exec'))
    if selected_mode is binascii:
        return 'import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads(binascii.a2b_base64({})))'.format(binascii.b2a_base64(marshal_encoded))
    return 'import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads({}.decompress({})))'.format(selected_mode.__name__, selected_mode.compress(marshal_encoded))

def parse_args():
    parser = argparse.ArgumentParser(description='obfuscate python programs'.title())
    parser._optionals.title = "syntax".title()
    parser.add_argument('-i', '--input', type=str, help='input file name'.title(), required=True)
    parser.add_argument('-o', '--output', type=str, help='output file name'.title(), required=True)
    parser.add_argument('-c', '--complexity', type=int,
                        help='complexity of obfuscation. 100 recomended'.title(), required=True)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    return parser.parse_args()

def main():
    args = parse_args()
    print('\t[+] encoding '.title() + args.input)
    with tqdm.tqdm(total=args.complexity) as pbar:
        with open(args.input) as iput:
            for i in range(args.complexity):
                if i == 0:
                    encoded = encode(source=iput.read())
                else:
                    encoded = encode(source=encoded)
                time.sleep(0.1)
                pbar.update(1)
    with open(args.output, 'w') as output:
        output.write(encoded)
if __name__ == '__main__':
    main()