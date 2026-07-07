import os
import time
import sys as _sys

def _getch():
    """Baca 1 karakter tanpa perlu Enter — Linux/Termux"""
    try:
        import tty, termios
        fd = _sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = _sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        if ch == '\x03':          # Ctrl+C
            raise KeyboardInterrupt
        if ch == '\x1c':          # Ctrl+\ (SIGQUIT)
            raise KeyboardInterrupt
        return ch.lower()
    except KeyboardInterrupt:
        raise
    except Exception:
        line = input()
        return (line + " ")[0].lower()
import types as _types
_mp_mod = _types.SimpleNamespace()

while True:
    
  os.system("clear")
  print(" ")
  print(" \033[36mManual book\033[0m")
  print(" ")
  print("> \033[32muntuk  isi energi\033[0m\n+100")
  print("> \033[32muntuk menebang 1 pohon liar (T.1/2 (0)\033[0m\n+ 1 kayu T.1/2(0)\n+ 2 kapasitas tas\n+ 7 gcoin\n- 3 energi")
  print("> \033[32muntuk membeli 1 bibit T.1\033[0m\n= 15 Gxc\n+ 2 kapasitas tas")
  print("> \033[32muntuk membeli 1 bibit T.2\033[0m\n= 20 Gxc\n+ 3 kapasitas tas")
  print("> \033[32muntuk menanam 1 bibit T.1\033[0m\n- 2 energi")
  print("> \033[32muntuk menanam 1 bibit T.2\033[0m\n- 4 energi")
  print("> \033[32muntuk menebang pohon T.1\033[0m\n+ 19 Gxc\n+ 3 Kayu T.1\n+ 2  kapasitas tas\n- 2 energi")
  print("> \033[32muntuk menebang pohon T.2\033[0m\n+ 25 Gxc\n+ 6 kayu T.2\n+ 4 kapasitas tas\n- 4 energi")
  print(" ")
  print(" Keluar [x]")
  cmd= _getch()
  
  if cmd == "x":
    break
 
