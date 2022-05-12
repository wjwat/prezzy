#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import os
import sys
from msvcrt import getch


COLORS = {
  # Foreground
  "BLF" : "\033[30m", # Black fg
  "RF" : "\033[31m", # Red
  "GF" : "\033[32m", # Green
  "YF" : "\033[33m", # Yellow
  "BF" : "\033[34m", # Blue
  "MF" : "\033[35m", # Maroon
  "CF" : "\033[36m", # Cyan
  "WF" : "\033[37m", # White
  "RESF" : "\033[39m", # Reset fg
  # Background
  "BLB" : "\033[40m", # Black bg
  "RB" : "\033[41m", # Red
  "GB" : "\033[42m", # Green
  "YB" : "\033[43m", # Yellow
  "BB" : "\033[44m", # Blue
  "MB" : "\033[45m", # Maroon
  "CB" : "\033[46m", # Cyan
  "WB" : "\033[47m", # White
  "RESB" : "\033[49m", # Reset bg
  # Style
  "BR" : "\033[1m",  # Bright
  "DI" : "\033[2m",  # Dim
  "NO" : "\033[22m", # Normal
  "RA" : "\033[0m",  # Reset all
}


def clear():
  os.system("cls || clear")


def read_file(file):
  contents = None
  with open(file, "r", encoding="utf8") as f:
    contents = f.read().split("---\n")

  return contents


def parse_tags(line, columns):
  count = 0
  if "\\" in line:
    count = 0

    for fgk, fgv in COLORS.items():
      temp_count = line.count(f"\\{fgk}")

      if temp_count == 0:
        continue

      count += temp_count * len(fgv)
      line = line.replace(f"\\{fgk}", f"{fgv}")

  if "\\TC" in line:
    line = line.replace("\\TC", "")
    line = " " * (math.floor((columns - len(line) + count) / 2)) + line
  elif "\\TR" in line:
    line = line.replace("\\TR", "")
    line = " " * (columns - len(line) + count) + line

  return (line, count)


def display_slide(slides, current_pos, offset):
  columns, lines = os.get_terminal_size()
  top_bottom = "+" + "-" * (columns - 2) + "+"
  slide_lines = slides[current_pos].split("\n")
  slide_len = len(slide_lines)

  clear()

  print(top_bottom)

  for i in range(lines - 3):
    if slide_len > lines and offset != 0:
      i += offset

    if i < slide_len:
      t, c = parse_tags(slide_lines[i], columns - 4)
      line_len = len(t)
      l = "| " + t + " " * (columns - line_len - 4 + c) + " \033[0m|"
      print(l)
    else:
      print("|" + " " * (columns - 2) + "|")

  print(top_bottom)


def main(file):
  current_pos = 0
  current_offset = 0
  slides = read_file(file)
  slides_len = len(slides)

  while True:
    display_slide(slides, current_pos, current_offset)
    columns, lines = os.get_terminal_size()
    current_slide_len = len(slides[current_pos].split("\n"))

    print(f"SLIDE {current_pos + 1} of {slides_len} : {columns} x {lines} | OFFSET: {current_offset} / {current_slide_len}", end="\r")

    key = ord(getch())

    if key == 100 or key == 68:   # Aa / right
      current_pos = min(current_pos + 1, slides_len - 1)
    elif key == 97 or key == 70:  # Dd / left
      current_pos = max(current_pos - 1, 0)
    elif key == 119 or key == 87: # Ww / up
      current_offset = max(current_offset - 3, 0)
    elif key == 115 or key == 83: # Ss / down
      current_offset = min(current_offset + 3, current_slide_len - 3)
    elif key == 113 or key == 81: # q
      print("\033[0m")
      clear()
      return


if __name__ == '__main__':
  main(sys.argv[1])
