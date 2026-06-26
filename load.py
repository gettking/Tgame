import time

for i in [
    "» Mengisi Daya «",
    "\033[31m»\033[0m Mengisi Daya \033[31m«\033[0m",
    "\033[33m»\033[0m Mengisi Daya \033[33m«\033[0m",
    "\033[32m»\033[0m Mengisi Daya \033[32m«\033[0m",
    "» Mengisi Daya «",
    "\033[31m»\033[0m Mengisi Daya \033[31m«\033[0m",
    "\033[33m»\033[0m Mengisi Daya \033[33m«\033[0m",
    "\033[32m»\033[0m Mengisi Daya \033[32m«\033[0m",
    "» Mengisi Daya «",
    "\033[31m»\033[0m Mengisi Daya \033[31m«\033[0m",
    "\033[33m»\033[0m Mengisi Daya \033[33m«\033[0m",
    "\033[32m»\033[0m Mengisi Daya \033[32m«\033[0m",
    ]:
      print(f"\r{i}", end="", flush=True)
      time.sleep(0.3)

