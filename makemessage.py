#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement

import argparse
import os
import traceback
import struct

def main():

    #示例：lscript.py -i /home/user/PAL -e gb2312 -o dialog.txt
    parser = argparse.ArgumentParser(description='Output FFFF info of Script file.')
    parser.add_argument('-i','--input', dest='inpath', help='Game path')
    parser.add_argument('-o','--output', dest='outfile', help='Output file')
    parser.add_argument('-w','--width', dest='wordwidth', help='Word width in bytes')
    parser.add_argument('-e','--encoding', dest='encoding', help='Encoding name')
    options = parser.parse_args()

    if options.inpath == None or len(options.inpath) == 0:
        print 'Game path must be specified!'
        parser.print_help()
        return

    if options.encoding == None or len(options.encoding) == 0:
        print 'Encoding must be specified!'
        parser.print_help()
        return

    if options.outfile == None or len(options.outfile) == 0:
        print 'Output file must be specified!'
        parser.print_help()
        return

    if options.inpath[-1] != '/' and options.inpath[-1] != '\\':
        options.inpath += '/'

    if options.wordwidth == None:
        options.wordwidth = 10
    else:
        options.wordwidth = int(options.wordwidth)

    script_bytes = []
    index_bytes = []
    msg_bytes = []
    word_bytes = []

    is_msg_group = 0    #是否正在处理文字组的标示。
    msg_count = 0
    last_index = -1

    for file_ in os.listdir(options.inpath):
        if file_.lower() == 'sss.mkf':
            try:
                with open(options.inpath + file_, 'rb') as f:
                    f.seek(12, os.SEEK_SET)
                    offset_begin, script_begin, file_end = struct.unpack('<III', f.read(12))
                    f.seek(offset_begin, os.SEEK_SET)
                    index_bytes = f.read(script_begin - offset_begin)
                    script_bytes = f.read(file_end - script_begin)
            except:
                traceback.print_exc()
                return
        elif file_.lower() == 'm.msg':
            try:
                with open(options.inpath + file_, 'rb') as f:
                    msg_bytes = f.read()
            except:
                traceback.print_exc()
                return
        elif file_.lower() == 'word.dat':
            try:
                with open(options.inpath + file_, 'rb') as f:
                    data_bytes=f.read()
            except:
                traceback.print_exc()
                return

    if len(data_bytes) % options.wordwidth != 0:
        data_bytes += [0x20 for i in range(0, options.wordwidth - len(data_bytes) % options.wordwidth)]

    output = "# All lines, except those inside [BEIGN MESSAGE] and [END MESSAGE], can be commented by adding the sharp '#' mark at the first of the line.\n\n"

    output += "# This section contains the information that will be displayed when a user finishes the game.\n"
    output += "# Only the keys listed here are valid. Other keys will be ignored.\n"
    output += "[BEGIN CREDITS]\n"
    output += "# Place the translated text of 'Classical special build' here in no more than 24 half-wide characters.\n"
    output += "1= Classical special build\n"
    output += "# Place the translated porting information template at the following two lines. Be aware that each replaced line will be truncated into at most 40 half-wide characters.\n"
    output += "6= ${platform} port by ${author}, ${year}.\n"
    output += "7=\n"
    output += "# Place the translated GNU licensing information at the following three lines. Be aware that each line will be truncated into at most 40 half-wide characters.\n"
    output += "8=   This is a free software and it is\n"
    output += "9=   published under GNU General Public\n"
    output += "10=    License v3.\n"
    output += "# Place the translated text at the following line. Be aware that each line will be truncated into at most 40 half-wide characters.\n"
    output += "11=    ...Press Enter to continue\n"
    output += "[END CREDITS]\n\n"

    output += "# This section contains the words used by the game.\n"
    output += "[BEGIN WORDS]\n"
    output += "# Each line is a pattern of 'key=value', where key is an integer and value is a string.\n"
    for i in range(0, len(data_bytes) / options.wordwidth):
        output += "%d=%s\n" % (i, data_bytes[i * options.wordwidth: (i + 1) * options.wordwidth].rstrip('\x20\x00').decode(options.encoding).encode('utf-8'))
    output += "[END WORDS]\n\n"

    output += "# The following sections contain dialog/description texts used by the game.\n\n"

    print "Now Processing. Please wait..."
    
    for i in range(0, len(script_bytes) / 8):
        op, w1, w2, w3 = struct.unpack('<HHHH', script_bytes[i * 8 : (i + 1) * 8])
        if op == 0xFFFF:

            if is_msg_group == 0:
                is_msg_group = 1
                output += "%s %d\n" % ('[BEGIN MESSAGE]', w1)

            last_index = w1
            msg_count += 1
            msg_begin, msg_end = struct.unpack("<II",index_bytes[w1 * 4 : (w1 + 2) * 4])

            try:
                output += "%s\n" % (msg_bytes[msg_begin : msg_end].decode(options.encoding, 'replace').encode('utf-8'))
            except:
                traceback.print_exc()

        elif op == 0x008E:

            if is_msg_group == 1:
                output += "%s\n" % ('[CLEAR MESSAGE]')

        else:
            if is_msg_group == 1:
                is_msg_group = 0
                output += "%s %d\n\n" % ('[END MESSAGE]', last_index)

    try:
        with open(options.outfile, "wt") as f:
            f.write(output)
    except:
        traceback.print_exc()

    print "OK! Extraction finished!"
    print "Original Dialog script count: " + str(msg_count)

if __name__ == '__main__':
    main()
