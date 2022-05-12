import os
import sys
from msvcrt import getch


COLORS = {
  # Foreground
  "BLACKFG"   : "\033[30m",
  "REDFG"     : "\033[31m",
  "GREENFG"   : "\033[32m",
  "YELLOWFG"  : "\033[33m",
  "BLUEFG"    : "\033[34m",
  "MAGENTAFG" : "\033[35m",
  "CYANFG"    : "\033[36m",
  "WHITEFG"   : "\033[37m",
  "RESETFG" : "\033[39m",
  # Background
  "BLACKBG"   : "\033[40m",
  "REDBG"     : "\033[41m",
  "GREENBG"   : "\033[42m",
  "YELLOWBG"  : "\033[43m",
  "BLUEBG"    : "\033[44m",
  "MAGENTABG" : "\033[45m",
  "CYANBG"    : "\033[46m",
  "WHITEBG"   : "\033[47m",
  "RESETBG"   : "\033[49m",
  # Style
  "BRIGHT"    : "\033[1m",
  "DIM"       : "\033[2m",
  "NORMAL"    : "\033[22m",
  "RESET_ALL" : "\033[0m",
}


def clear():
  os.system("cls || clear")


def read_file(file):
  contents = None
  with open(file, "r") as f:
    contents = f.read().split("---\n")

  return contents


def parse_colors(line):
  count = 0
  if "\\" in line:
    count = 0

    for fgk, fgv in COLORS.items():
      temp_count = line.count(f"\\{fgk}")

      if temp_count == 0:
        continue

      count += temp_count * len(fgv)
      line = line.replace(f"\\{fgk}", f"{fgv}")


  return (line, count)


def display_slide(slides, current_pos):
  columns, lines = os.get_terminal_size()
  top_bottom = "+" + "-" * (columns - 2) + "+"
  slide_lines = slides[current_pos].split("\n")
  slide_len = len(slide_lines)

  clear()

  print(top_bottom)

  for i in range(lines - 3):
    if i < slide_len:
      t, c = parse_colors(slide_lines[i])
      line_len = len(t)
      l = "| " + t + " " * (columns - line_len - 4 + c) + " \033[0m|"
      print(l)
    else:
      print("|" + " " * (columns - 2) + "|")

  print(top_bottom)


def main(file):
  current_pos = 0
  slides = read_file(file)
  slides_len = len(slides)

  while True:
    display_slide(slides, current_pos)
    print(f"SLIDE {current_pos + 1} of {slides_len} : {os.get_terminal_size()}", end="\r")
    key = ord(getch())

    if key == 102 or key == 65:   # right
      current_pos = min(current_pos + 1, slides_len - 1)
    elif key == 97 or key == 70:  # left
      current_pos = max(current_pos - 1, 0)
    elif key == 113 or key == 81: # q
      print("\033[0m")
      clear()
      return


if __name__ == '__main__':
  main(sys.argv[1])