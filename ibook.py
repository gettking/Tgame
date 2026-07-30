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
  print(" \033[32mDalam pengerjaan.\033[0m")
  print(" ")
  print(" Keluar [x]")
  cmd= _getch()
  
  if cmd == "x":
    break
 
