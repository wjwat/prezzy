#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import os
import sys
from msvcrt import getch




HELP = """\TC\RB\WF\BR HELP \RA
Q, q, Ctrl-C   QUIT
A, a, left     Previous Slide
D, d, right    Next Slide
W, w, up       Scroll up
S, s, down     Scroll down
E, e           Hide status line

\TC================================================================================
\TC\RB\WF\BR Prezzy File Tags \RA

          \YF\BRForeground\RA:                  \YF\BRBackground\RA:                 \YF\BROther\RA:
 Black:   \\ \bBLF       \WB\BLFExample\RA     |     \\ \bBLB      \BLB\WFExample\RA     |     \\ \bBR       \BRExample
   Red:   \\ \bRF        \RFExample\RA     |     \\ \bRB       \RBExample\RA     |     \\ \bDI       \DIExample
 Green:   \\ \bGF        \GFExample\RA     |     \\ \bGB       \GBExample\RA     |     \\ \bNO       \BRExam\\NOple
Yellow:   \\ \bYF        \YFExample\RA     |     \\ \bYB       \YBExample\RA     |     \\ \bRA       \RB\YFExam\RAple
  Blue:   \\ \bBF        \BFExample\RA     |     \\ \bBB       \BBExample\RA     |     \\ \bTC       See Below
Maroon:   \\ \bMF        \MFExample\RA     |     \\ \bMB       \MBExample\RA     |     \\ \bTR       See Below
  Cyan:   \\ \bCF        \CFExample\RA     |     \\ \bCB       \CBExample\RA
 White:   \\ \bWF        \WFExample\RA     |     \\ \bWB       \WB\BLFExample\RA
 Reset:   \\ \bRESF      \RFExam\RESFple     |     \\ \bRESB     \RBExam\RESBple\RA

\TCCentered Text
\TRRight aligned text

\TC================================================================================
\\TC\\RFPress any key to exit
"""


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


class Edges:
  top_bottom = "-"
  corners = "+"
  sides = "|"


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

    # Help includes backspace char, account for the \b and the character that is
    # removed.
    backspace_count = line.count("\b")
    count += backspace_count * 2

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


def display_slide(slides, current_pos, offset, status_line):
  columns, lines = os.get_terminal_size()
  top_bottom = Edges.corners + Edges.top_bottom * (columns - 2) + Edges.corners
  slide_lines = slides[current_pos].split("\n")
  slide_len = len(slide_lines)
  line_offset = 3 if status_line else 2

  clear()

  print(top_bottom)

  for i in range(lines - line_offset):
    if slide_len > lines and offset != 0:
      i += offset

    if i < slide_len:
      t, c = parse_tags(slide_lines[i], columns - 4)
      line_len = len(t)
      l = f"{Edges.sides} " + t + " " * (columns - line_len - 4 + c) + f" \033[0m{Edges.sides}"
      print(l)
    else:
      print(Edges.sides + " " * (columns - 2) + Edges.sides)

  if status_line:
    print(top_bottom)
  else:
    print(top_bottom, end='\r')


def main(file):
  current_pos = 0
  current_offset = 0
  slides = read_file(file)
  slides_len = len(slides)
  status_line = True

  while True:
    display_slide(slides, current_pos, current_offset, status_line)
    columns, lines = os.get_terminal_size()
    current_slide_len = len(slides[current_pos].split("\n"))

    if status_line:
      print(f"SLIDE {current_pos + 1} of {slides_len} : {columns} x {lines} | OFFSET: {current_offset} / {current_slide_len}", end="\r")

    key = ord(getch())

    # Next Slide: Dd
    if key in (100, 68, 77):
      current_pos = min(current_pos + 1, slides_len - 1)
      current_offset = 0
    # Previous Slide: Aa
    elif key in (97, 70, 75):
      current_pos = max(current_pos - 1, 0)
      current_offset = 0
    # Scroll up: Ww
    elif key in (119, 87, 72):
      current_offset = max(current_offset - 3, 0)
    # Scroll Down: Ss
    elif key in (115, 83, 80):
      if current_slide_len > lines:
        current_offset = min(current_offset + 3, current_slide_len - 3)
    # Disable status line: Ee
    elif key in (101, 69):
      status_line = not status_line
    # Display Help: ?, F1
    elif key in (63, 59):
      display_slide([HELP], 0, 0, status_line)
      getch()
    # QUIT: Qq, Ctrl-C
    elif key == 113 or key == 81 or key == 3:
      print("\033[0m")
      clear()
      return


if __name__ == '__main__':
  main(sys.argv[1])
