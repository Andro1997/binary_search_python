from datetime import datetime
import re
import os

def get_length(l):
    l.seek(0, os.SEEK_END)
    return l.tell()

def get_start_pos_line(f, mid_pos, start):
    space = "\n"
    f.seek(mid_pos)
    char = f.read(1)
    while mid_pos >= start and char != space:
        mid_pos -= 1
        f.seek(mid_pos)
        char = f.read(1)
    return mid_pos + 1 if char == space else mid_pos

def get_end_pos_line(f, mid_pos, end):
    space = "\n"
    f.seek(mid_pos)
    char = f.read(1)
    while mid_pos < end and char != space:
        mid_pos += 1
        f.seek(mid_pos)
        char = f.read(1)
    return mid_pos - 1 if char == space else mid_pos

def get_format_for_line_dt(line):
    regul = '^(?:[^\s]+\s){3}\[([^\]]*)\].*$'
    re_line = re.match(regul, line)
    string = re_line.group(2)[:-6]
    dt = datetime.strptime(string, "%d/%b/%Y:%H:%M:%S")
    return dt

def binary_search(f, ts, start, end):
    if start == end:
        return start
    mid_pos = int((start + end) // 2)
    mid_start = get_start_pos_line(f, mid_pos)
    mid_end = get_end_pos_line(f, mid_pos)
    f.seek(mid_start)
    line = f.read(mid_end - mid_start)
    format_line = get_format_for_line_dt(line)
    if format_line < ts:
        new_start = mid_end + 1
        if new_start >= end:
            return new_start
        return binary_search(f, ts, new_start, end)
    else:
        new_end = mid_start - 1
        if new_end < start:
            return mid_start
        return binary_search(f, ts, start, new_end)

def get_endlist(f, ts):
    start = 0
    stop = get_length(f)
    pos = binary_search(f, ts, start, stop)
    if pos == stop:
        return ""
    else:
        f.seek(pos)
        return f.read()
with open('my_log', encoding="latin-1") as f:
    timestop = '01/Jul/1995:04:38:24'
    print(get_endlist(f, timestop))