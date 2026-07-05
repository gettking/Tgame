print(" ")
Game_end = 0
bookx, booky = 3, 0
bit1cek = str()
bit2cek = str()
kayu0cek = str()
kayu1cek = str()
kayu2cek = str()
from quest import quest
import random
import string
import time
import os


####0000
lvl = 0

#map_rumah
rumahx, rumahy = 21, 10
userx, usery = 0, 8
coinx, coiny = 1, 1
invx, invy = 7, 1
crafx, crafy = 1, 3
casx, casy = 3, 8
kesetx, kesety= 8, 3
jamx, jamy = 0, 5
ksuratx, ksuraty = 18, 7
tanggax, tanggay = 6, 8
gentong = {
    (19, 1)
}
jendela = {
    (4, 6), (8, 1), (0, 9)
}
potbunga = {
    (9, 1), (9, 2), (9, 4), (9, 5),
    (5, 5), (6, 5), (7, 5), (8, 5), (5, 6),
    (5, 7), (5, 8)
}
lantai ={
    (4, 0), (5, 0), (6, 0), (3, 1), (0, 7),
    (4, 1), (5, 1), (6, 1), (1, 2), (2, 2),
    (3, 2), (3, 3), (4, 3), (5, 3), (6, 3),
    (3, 4), (1, 5), (2, 5), (3, 5),
    (0, 6), (1, 6), (2, 6), (3, 6), (1, 7), (2, 7), (3, 7), (0, 8), (1, 8)
}
gelondong = {
    (18, 8), (19, 8), (20, 8), (6, 9), (7, 9),
    (8, 9), (9, 9), (10, 9), (11, 9), (12, 9),
    (13, 9), (14, 9), (15, 9), (16, 9), (16, 8),
    (5, 9), (9, 0), (10, 0), (11, 0), (12, 0),
    (13, 0), (14, 0), (15, 0), (16, 0), (17, 0),
    (18, 0), (19, 0), (20, 0), (20, 1), (20, 2),
    (20, 3), (20, 4), (20, 5), (20, 6), (20, 7)
}
respawnC = {}
w_isi = 45
pinturx, pintury = 7, 3
pintux, pintuy = 20, 9
casE = 0
#Global
pusing = 0
info = ""
box_penyimpanan = {}

#map_kebun
kebunx, kebuny = 21, 10
userx1, usery1 = 1, 0
pintux1, pintuy1 = 0, 0
flagx1, flagy1 = 1, 0
apelx, apely = 16, 2
pohon1= {
  (0, 8), (1, 7), (1, 9), (2, 8), (3, 7),
  (3, 9), (4, 8), (5, 9), (5, 7), (6, 8)
}
pohon2= {
  (9, 7), (11, 7), (13, 7), (8, 8), (10, 8),
  (12, 8), (14, 8), (9, 9), (11, 9), (13, 9)
}

daunjatuh = {
    (0, 9), (3, 8), (7, 9), (10, 7), (13, 8)
}
kolam = {
    (17, 1), (18, 1), (17, 2), (17, 3), (17, 4),
    (17, 5), (17, 6), (18, 6), (18, 5), (18, 4),
    (18, 3), (18, 2), (18, 7), (19, 7), (19, 6),
    (19, 5), (19, 4), (19, 3), (19, 2)
}
kapakx, kapaky = 6, 7
respawn1 = {}
respawn2 = {}

w_tumbuh1 = 60
w_tumbuh2 = 60

k_lahan = {
    (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
    (6, 3), (7, 3), (8, 3), (9, 3), (10, 3),
    (11, 3), (12, 3), (13, 3), (14, 4), (0, 4),
    (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
    (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (0, 5), (1, 5), (2, 5), (3, 5),
    (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
    (10, 5), (11, 5), (12, 5), (13, 5), (14, 5),
    (1, 6), (2, 6), (3, 6), (4, 6), (5, 6),
    (6, 6), (7, 6), (8, 6), (9, 6), (10, 6), (11, 6), (12 ,6), (13, 6)
}

flowerk = {
    (0, 3), (14, 3), (1, 2), (2, 2), (3, 2),
    (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2),
    (10, 2), (11, 2), (12, 2), (13, 2), (14, 6), (0, 6)
}
flower2 = {
    (16, 6), (16, 7), (17, 7),
    (19, 1), (20, 1), (20, 2)
}

pohon_tanam = set()
tanam = set()
respawnT = {}
wt_tanam = 20

pohon_tanam2 = set()
tanam2 = set()
respawnT2 = {}
wt_tanam2 = 30

respawnA = {}
wt_muncul = 40

ppasarx, ppasary = 20, 9

#map_pasar
pasarx, pasary = 21, 10
userxp, useryp = 1, 0
Tokbit = {
  (2, 2), (3, 2),
  (2, 3), (3, 3)
}

bpasarx, bpasary = 0, 0

#data_user
Hp = 0
tas = 0
gxc = 0
gcoins = 0
bibit = 0
bibit2 = 0
exp = 0
kayu = 0
kayuT1 = 0
kayuT2 = 0

#walls_rumah
walls = {
  (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
  (4, 2), (4, 4), (4, 5), (4, 6), (4, 7),
  (4, 8), (4, 9), (5, 2), (6, 2), (7, 2),
  (8, 2), (8, 1), (8, 0), (0, 9), (1, 9),
  (2, 9), (3, 9), (7, 0), (1, 0), (2, 0),
  (2, 1), (1, 4), (2, 4), (2, 3), (2, 8),
  (5, 4), (6, 4), (7, 4), (8, 4)
}

#walls_kebun
wallsk = {
  (0, 1), (1, 1),(2, 1)
}

#walls_pasar
wallp = {
  (2, 1), (3, 1),
  (1, 2), (1, 3),
  (3, 4), (4, 3),
  (4, 2)
}

worldpos = "start"

def ldtb(delay=0.17):
  
  for i in [
    
    "🌑",
    "🌑",
    "🌒",
    "🌒",
    "🌓",
    "🌓",
    "🌔",
    "🌔",
    "🌕",
    "🌕",
    "\033[32mPohon sukses ditebang ✓\033[0m"
    ]:
        print(f"\r{i}", end="", flush=True)
        time.sleep(delay)
  
def ldkb():
  
  for i in [
    " ▰▱▱▱▱▱▱▱▱▱",
    " ▰▰▱▱▱▱▱▱▱▱",
    " ▰▰▰▱▱▱▱▱▱▱",
    " ▰▰▰▰▱▱▱▱▱▱",
    " ▰▰▰▰▰▱▱▱▱▱",
    " ▰▰▰▰▰▰▱▱▱▱",
    " ▰▰▰▰▰▰▰▱▱▱",
    " ▰▰▰▰▰▰▰▰▱▱",
    " ▰▰▰▰▰▰▰▰▰▱",
    " ▰▰▰▰▰▰▰▰▰▰",
  ]:
    print(f"\r\033[32m{i}\033[0m", end="", flush=True)
    time.sleep(0.3)

def ldcasfull():
  
  for i in [
    " » Memulai eumam «",
    " \033[31m»\033[0m Memulai eumam \033[31m«\033[0m",
    " \033[33m»\033[0m Memulai eumam \033[33m«\033[0m",
    " \033[32m»\033[0m Memulai eumam \033[32m«\033[0m",
    " » Memulai eumam «",
    " \033[31m»\033[0m Memulai eumam \033[31m«\033[0m",
    " \033[33m»\033[0m Memulai eumam \033[33m«\033[0m",
    " \033[32m»\033[0m Memulai eumam \033[32m«\033[0m",
    " » Memulai eumam «",
    " \033[31m»\033[0m Memulai eumam \033[31m«\033[0m",
    " \033[33m»\033[0m Memulai eumam \033[33m«\033[0m",
    " \033[32m»\033[0m Memulai eumam \033[32m«\033[0m",
    " \033[33mNanti aja ah masih kenyang !\033[0m"
    ]:
      print(f"\r{i}", end="", flush=True)
      time.sleep(0.3)

def ldcas():
  
  for i in [
    " » Memulai eumam «",
    " \033[31m»\033[0m Memulai eumam \033[31m«\033[0m",
    " \033[33m»\033[0m Memulai eumam \033[33m«\033[0m",
    " \033[32m»\033[0m Memulai eumam \033[32m«\033[0m",
    " » Memulai eumam «",
    " \033[31m»\033[0m Memulai eumam \033[31m«\033[0m",
    " \033[33m»\033[0m Memulai eumam \033[33m«\033[0m",
    " \033[32m»\033[0m Memulai eumam \033[32m«\033[0m",
    " » Memulai eumam «",
    " \033[31m»\033[0m Memulai eumam \033[31m«\033[0m",
    " \033[33m»\033[0m Memulai eumam \033[33m«\033[0m",
    " \033[32m»\033[0m Memulai eumam \033[32m«\033[0m",
    " \033[32mAlhamdulillah kenyang juga ✓\033[0m"
    ]:
      print(f"\r{i}", end="", flush=True)
      time.sleep(0.3)

def ldMbrkgl(delay=0.17):
  
  for i in [
    
    "🌑",
    "🌑",
    "🌒",
    "🌒",
    "🌓",
    "🌓",
    "🌔",
    "🌔",
    "🌕",
    "🌕",
    "\033[31mSaldo G-coin kosong !\033[0m"
    ]:
         print(f"\r{i}", end="", flush=True)
         time.sleep(delay)

def ldSwp():
  
  for i in [" ━", " ━━", " ━━━", " ━━━━", " ━━━━━", " ━━━━━━", " ━━━━━━━", " ━━━━━━━━", " ━━━━━━━━━", " ━━━━━━━━━━", " Swap Sukses ✓"]:
    print(f"\r\033[32m{i}\033[0m", end="", flush=True)
    time.sleep(0.5)

def ldSuk():
  
  for i in ["◜", "◠", "◝", "◞", "◡", "◟", " Sukses ✓"]:
    print(f"\r\033[32m{i}\033[0m", end="", flush=True)
    time.sleep(0.6)

def ldGal():
  
  for i in  ["◜", "◠", "◝", "◞", "◡", "◟", " Kode salah !"]:
    print(f"\r\033[31m{i}\033[0m", end="", flush=True)
    time.sleep(0.6)

def wkt(delay=0.15):
  
  for i in [
    "🌑",
    "🌑",
    "🌒",
    "🌒",
    "🌓",
    "🌓",
    "🌔",
    "🌔",
    "🌕",
    "🌕"
    ]:
        print(f"\r{i}", end="", flush=True)
        time.sleep(delay)
wkt()


#dashboard
def infopemain():
  print("┌───────────────────────────────┐")
  print(f"│🍚: {Hp:<5} 🎒: {tas:<5} 🅶: {gxc:<8}│")
  print("└───────────────────────────────┘")
  print(" ➥ \033[36mMembuka tas & peyimpanan [i]\033[0m")

def isiTas():
    
  while True:
    os.system("clear")
    print(" ")
    print(f" ➧ Player exp   : \033[36m{exp}\033[0m")
    print(" ")
    infolvl()
    print(" ")
    print("🎒 :")
    print(f" ➥ Gcoins    : \033[33m{gcoins}\033[0m")
    print(" ")
    print(f" ➥ Kayu      : \033[36m{kayu}\033[0m")
    print(f" ➥ Kayu T.1  : \033[36m{kayuT1}\033[0m")
    print(f" ➥ Kayu T.2  : \033[36m{kayuT2}\033[0m")
    print(f" ➥ Bibit T.1 : \033[36m{bibit}\033[0m")
    print(f" ➥ Bibit T.2 : \033[36m{bibit2}\033[0m")
    print(" ")
    print("🧰 :")
    print(f" ➧ \033[36mBarang yang disimpan :\033[0m")
    print(" ")
    print(f" ➥ Bibit T.1   = \033[32m{box_penyimpanan.get("bibit", 0)}\033[0m")
    print(f" ➥ Bibit T.2   = \033[32m{box_penyimpanan.get("bibit2", 0)}\033[0m")
    print(f" ➥ Kayu T.1(0) = \033[32m{box_penyimpanan.get("kayu", 0)}\033[0m")
    print(f" ➥ Kayu T.1    = \033[32m{box_penyimpanan.get("kayuT1", 0)}\033[0m")
    print(f" ➥ Kayu T.2    = \033[32m{box_penyimpanan.get("kayuT2", 0)}\033[0m")
    print(f" ➥ Koin Gxc    = \033[32m{box_penyimpanan.get("gxc", 0)}\033[0m")
    print(" ")
    back=input(" ⇐ Kembali [x] : ").lower()
    if back == "x":
      break
 
def infolvl():
  global lvl
  
  if exp == 500:
    level = 5
    lvl += 1
  elif exp == 400:
    level = 4
    lvl += 1
  elif exp == 300:
    level = 3
    lvl += 1
  elif exp == 200:
    level = 2
    lvl += 1
  elif exp == 100:
    level = 1
    lvl += 1
  else:
    level = 0
  print(f" ➧ Level pemain : \033[36m{level}\033[0m")

def gentongbuang():
  global bibit, bibit2, kayu, kayuT1, kayuT2, gxc, tas
  while True:
    
    os.system("clear")
    
    print(" ")
    print(" Bibit t.1   - 1")
    print(" Bibit t.2   - 2")
    print(" Kayu t.1(0) - 3")
    print(" Kayu t.1    - 4")
    print(" Kayu t.2    - 5")
    print(" Koin Gxc    - 6")
    print(" Keluar      - ×")
    print(" ")
    buang= input("\033[31mPilih & masukkan jumlah barang untuk dibuang :\033[0m ").lower()
    
    if buang == "1":
        
      jbibit=input(" Masukkan jumlah bibit T.1 : ")
      
      try:
        xbibit = int(jbibit)
        if xbibit <= 0:
          print(" ")
          print(" \033[31mTidak boleh angka 0 !\033[0m")
          print(" ")
          input(" e n t e r ")
          
        elif xbibit > bibit:
          print(" ")
          print(" \033[31mJumlah bibit T.1 kurang !\033[0m")
          print(" ")
          input(" e n t e r ")
          
        else:
          info_kaptasbit = xbibit * 2
          print(" ")
          bibit -= xbibit
          tas -= info_kaptasbit
          print(" \033[32mSukses !\033[0m")
          print(" ")
          input(" e n t e r ")
          
      except ValueError:
        print(" ")
        print("\033[31mInput salah !\033[0m")
        print(" ")
        input(" ➥ Enter.")
        continue
    
    elif buang == "2":
        
      jbibit2=input(" Masukkan jumlah bibit T.2 : ")
      
      try:
        xbibit2 = int(jbibit2)
        if xbibit2 <= 0:
          print(" ")
          print(" \033[31mTidak boleh angka 0 !\033[0m")
          print(" ")
          input(" e n t e r ")
          
        elif xbibit2 > bibit2:
          print(" ")
          print(" \033[31mJumlah bibit T.2 kurang !\033[0m")
          print(" ")
          input(" e n t e r ")
          
        else:
          info_kaptasbit2 = xbibit2 * 3
          print(" ")
          bibit2 -= xbibit2
          tas -= info_kaptasbit2
          print(" \033[32mSukses !\033[0m")
          print(" ")
          input(" e n t e r ")
          
      except ValueError:
        print(" ")
        print("\033[31mInput salah !\033[0m")
        print(" ")
        input(" ➥ Enter.")
        continue
      
    elif buang == "3":
        
      jkayu=input(" Masukkan jumlah kayu T.1(0) : ")
      
      try:
        xkayu = int(jkayu)
        if xkayu <= 0:
          print(" ")
          print(" \033[31mTidak boleh angka 0 !\033[0m")
          print(" ")
          input(" e n t e r ")
          
        elif xkayu > kayu:
          print(" ")
          print(" \033[31mJumlah kayu T.1(0) kurang !\033[0m")
          print(" ")
          input(" e n t e r ")
          
        else:
          info_kaptasyu = xkayu * 1
          print(" ")
          kayu -= xkayu
          tas -= info_kaptasyu
          print(" \033[32mSukses !\033[0m")
          print(" ")
          input(" e n t e r ")
          
      except ValueError:
        print(" ")
        print("\033[31mInput salah !\033[0m")
        print(" ")
        input(" ➥ Enter.")
        continue
    
    elif buang == "4":
        
      jkayuT1=input(" Masukkan jumlah kayu T.1 : ")
      
      try:
        xkayuT1 = int(jkayuT1)
        if xkayuT1 <= 0:
          print(" ")
          print(" \033[31mTidak boleh angka 0 !\033[0m")
          print(" ")
          input(" e n t e r ")
          
        elif xkayuT1 > kayuT1:
          print(" ")
          print(" \033[31mJumlah kayu T.1 kurang !\033[0m")
          print(" ")
          input(" e n t e r ")
          
        else:
          info_kpatasyut1 = xkayuT1 * (2/3)
          print(" ")
          kayuT1 -= xkayuT1
          tas -= info_kpatasyut1
          print(" \033[32mSukses !\033[0m")
          print(" ")
          input(" e n t e r ")
          
      except ValueError:
        print(" ")
        print("\033[31mInput salah !\033[0m")
        print(" ")
        input(" ➥ Enter.")
        continue
    
    elif buang == "5":
        
      jkayuT2=input(" Masukkan jumlah kayu T.2 : ")
      
      try:
        xkayuT2 = int(jkayuT2)
        if xkayuT2 <= 0:
          print(" ")
          print(" \033[31mTidak boleh angka 0 !\033[0m")
          print(" ")
          input(" e n t e r ")
          
        elif xkayuT2 > kayuT2:
          print(" ")
          print(" \033[31mJumlah bibit T.2 kurang !\033[0m")
          print(" ")
          input(" e n t e r ")
          
        else:
          info_kaptasyut2 = xkayuT2 * (4/6)
          print(" ")
          kayuT2 -= xkayuT2
          tas -= info_kaptasyut2
          print(" \033[32mSukses !\033[0m")
          print(" ")
          input(" e n t e r ")
          
      except ValueError:
        print(" ")
        print("\033[31mInput salah !\033[0m")
        print(" ")
        input(" ➥ Enter.")
        continue
    
    elif buang == "6":
        
      jgxc=input(" Masukkan jumlah Token Gxc : ")
      
      try:
        xgxc = int(jgxc)
        if xgxc <= 0:
          print(" ")
          print(" \033[31mTidak boleh angka 0 !\033[0m")
          print(" ")
          input(" e n t e r ")
          
        elif xgxc > gxc:
          print(" ")
          print(" \033[31mJumlah Koin Gxc kurang !\033[0m")
          print(" ")
          input(" e n t e r ")
          
        else:
          print(" ")
          gxc -= xgxc
          print(" \033[32mSukses !\033[0m")
          print(" ")
          input(" e n t e r ")
          
      except ValueError:
        print(" ")
        print("\033[31mInput salah !\033[0m")
        print(" ")
        input(" ➥ Enter.")
        continue

    elif buang == "x":
      break
  
    else:
      print(" ")
      print(" Input salah !")
      print(" ")
      input(" e n t e r ")
  
    
#FUNGSI RUMAH
def d_rumah():
 
    
  pos= (userx, usery)
  print("┌─────────┐")
  print(f"│🏠\033[36m Rumah\033[0m │ \033[32m{pos}\033[0m")
  print("└─────────┘")
  infopemain()
  print("│----------------------------------------│")
  
  #infopusing:p
  print(info)
  
  pos = (userx, usery)
  ob = (bookx, booky)
  if pos == ob:
    print(" [\033[32mBook !\033[0m] m untuk lihat »")
  
  pos = (userx, usery)
  ob = gentong
  if pos in ob:
    print(" [\033[31mBuang barang ditas!\033[0m] m untuk buang »")
  
  pos = (userx, usery)
  ob = (ksuratx, ksuraty)
  if pos == ob:
    print(" [\033[32mInfo Misi Game\033[0m] m untuk lihat »")

  pos = (userx, usery)
  ob = (coinx, coiny)
  if pos == ob:
    print(" [\033[33mBrangkas\033[0m] m untuk masuk »")
    
  pos = (userx, usery)
  ob = (crafx, crafy)
  if pos == ob:
    print(" [\033[32mKerajinan\033[0m] m untuk masuk »")
    
  pos = (userx, usery)
  ob = (pintux, pintuy)
  if pos == ob:
    print(" Exit [\033[32mkebun\033[0m] m untuk pergi »")
    
  pos = (userx, usery)
  ob = (invx, invy)
  if pos == ob:
    print(" [\033[32mPenyimpanan\033[0m] m untuk masuk »")
    
  pos = (userx, usery)
  ob = (casx, casy)
  if pos == ob:
    print(" [\033[33mEnergi\033[0m] m untuk eumam »")
  
  print("│----------------------------------------│")
  print(" ")
  
  for y in range(rumahy):
    ln = ""
    for x in range(rumahx):
        
      if (x, y) == (userx, usery):
        if casE > 0:
          ln += "🥄"
        elif pusing > 0:
          ln += "😵"
        else:
          ln += "😍"
          
      elif (x, y) == (coinx, coiny):
        ln += "🪙"
      elif (x, y) == (invx, invy):
        ln += "🧰"
      elif (x, y) == (crafx, crafy):
        ln += "🧩"
      elif (x, y) == (casx, casy):
        ln += "🍚"
      elif (x, y) in respawnC:
        ln += "🥣"
      elif (x, y) == (pinturx, pintury):
        ln += "🚪"
      elif (x, y) == (pintux, pintuy):
        ln += "🟫"
      elif (x, y) in lantai:
        ln += "⬜"
      elif (x, y) == (jamx, jamy):
        ln += "🕕"
      elif (x, y) in jendela:
        ln += "🪟"
      elif (x,y ) == (tanggax, tanggay):
        ln += "🪜"
      elif (x, y) == (kesetx, kesety):
        ln += "🔳"
      elif (x, y) in potbunga:
        ln += "🪴"
      elif (x, y) in gelondong:
        ln += "🪵"
      elif (x, y) in gentong:
        ln += "️🪣"
      elif (x, y) == (ksuratx, ksuraty):
        ln += "📮"
      elif (x, y) == (bookx, booky):
        ln += "📕"
      elif (x, y) in walls:
        ln += "🧱"
      else:
        ln += "🟩"
        
    print(ln)
    
  
#FUNGSI KEBUN
def d_kebun():
  
  pos = (userx1, usery1)
  print("┌─────────┐")
  print(f"│🏡\033[33m Kebun\033[0m │ \033[32m{pos}\033[0m")
  print("└─────────┘")
  infopemain()
  print("|----------------------------------------|")
  
  print(info)
  
  pos = (userx1, usery1)
  ob = (apelx, apely)
  if pos == ob:
    print(" [\033[32mApel\033[0m] m untuk memakan »")
  
  pos = (userx1, usery1)
  ob = (pintux1, pintuy1)
  if pos == ob:
    print(" [\033[32mRumah\033[0m] m untuk masuk «")
  
  pos = (userx1, usery1)
  ob = k_lahan
  if pos in ob:
    print(" [\033[32mArea lahan\033[0m] info [0]")
    
  pos = (userx1, usery1)
  ob = pohon1
  if pos in ob:
    print(" Area Pohon \033[32mt.1\033[0m(0) 1 untuk menebang.")
  
  pos = (userx1, usery1)
  ob = pohon2
  if pos in ob:
    print(" Area Pohon \033[32mt.2\033[0m(0) 2 untuk menebang.")
  
  pos = (userx1, usery1)
  ob = (ppasarx, ppasary)
  if pos == ob:
    print(" » [\033[32mPasar\033[0m] m untuk pergi kepasar")
  
  
  print("|----------------------------------------|")
  print(" ")
  
  for y in range(kebuny):
    ln = ""
    for x in range(kebunx):
      
      if (x, y) == (userx1, usery1):
        if pusing > 0:
          ln += "😵"
        else:
          ln += "😍"
        
      elif (x, y) == (pintux1, pintuy1):
        ln += "🏠"
      elif (x, y) == (flagx1, flagy1):
        ln += "🎏"
      elif (x, y) in wallsk:
        ln += "🧱"
      elif (x, y) in tanam:
        ln += "🌱"
      elif (x, y) in pohon_tanam:
        ln += "🌳"
      elif (x, y) in tanam2:
        ln += "🌱"
      elif (x, y) in pohon_tanam2:
        ln += "🌲"
      elif (x, y) in k_lahan:
        ln += "🟫"
      elif (x, y) in flowerk:
        ln += "🌻"
      elif (x, y) in pohon1:
        ln += "🌳"
      elif (x, y) in pohon2:
        ln += "🌲"
      elif (x, y) in respawn1:
        ln += "🪵"
      elif (x, y) in respawn2:
        ln += "🪵"
      elif (x, y) in daunjatuh:
        ln += "🍃"
      elif (x, y) == (kapakx, kapaky):
        ln += "🪓"
      elif (x, y) == (ppasarx, ppasary):
        ln += "➡️"
      elif (x, y) in kolam:
        ln += "🟦"
      elif (x, y) == (apelx, apely):
        ln += "🍎"
      elif (x, y) in flower2:
        ln += "🌷"
      else:
        ln += "🟩"
        
    print(ln)
  
def d_pasar():
  
  pos = (userxp, useryp)
  print("┌─────────┐")
  print(f"│🛍\033[33m Pasar\033[0m  │ \033[32m{pos}\033[0m")
  print("└─────────┘")
  infopemain()
  print("|----------------------------------------|")
  
  print(info)
  
  pos = (userxp, useryp)
  ob = wallp
  if pos in ob:
      print(" \033[33mKamu menabrak tembok !\033[0m")
      
  pos = (userxp, useryp)
  ob = (bpasarx, bpasary)
  if pos == ob:
    print(" [\033[32mKebun\033[0m] m untuk pergi kekebun «")
    
  pos = (userxp, useryp)
  ob = Tokbit
  if pos in ob:
    print(" [\033[32mToko Bibit\033[0m] m untuk masuk »")
    
  print("|----------------------------------------|")
  print(" ")
  
  for y in range(pasary):
    ln = ""
    for x in range(pasarx):
      
      if (x, y) == (userxp, useryp):
        if pusing > 0:
          ln += "😵"
        else:
          ln += "😍"
          
      elif (x, y) == (bpasarx, bpasary):
        ln += "🟩"
      elif (x, y) in Tokbit:
        ln += "🍀"
      elif (x, y) in wallp:
        ln += "🧱"
      else:
        ln += "⬜"
        
    print(ln)


def coins():
  
  global gcoins, gxc
  rate_Gxc = 0.628
  
  while True:
    
    global exp
    
    os.system("clear")
    
    print("▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️")
    print(f" » 1 G-coin =\033[32m {rate_Gxc}\033[0m Gxc")
    print("▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️")
    print(f" » G-Coin   = \033[32m{gcoins}\033[0m")
    print("▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️")
    print(" n =\033[31m Exit\033[0m ⇐")
    print("▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️")
    print(" ")
    
    cmd=input(" ➥ Swap G-coin ke Gxc [y or n]: ")
    
    if cmd == "y":
  
      if gcoins <= 0:
          print(" ")
          ldMbrkgl()
          print(" ")
          print(" ")
          input(" ➥ Enter.")
          continue
      
      print(" ")
      wkt()
      while True:
        
        fee = 0.5
        
        os.system("clear")
        print(" ")
        print("┌──────────────────┐")
        print("│x untuk kembali ⇐ │")
        print("└──────────────────┘")
        print(" ")
        jswap=(input(" ➥ Masukkan jumlah or Max : "))
        
        #BACK
        if jswap == "x":
          print(" ")
          wkt()
          break 
        
        if jswap == "max":
          
          if gcoins <= fee:
            print(" ")
            print(" \033[31mSaldo tidak cukup membayar Fee !\033[0m")
            print(" ")
            input(" ➥ Enter.")
            continue
          
          sgxc = gcoins 
          
        else:
          try:
            sgxc = float(jswap)
            if sgxc <= 0:
              print(" ")
              print(" Tidak boleh \033[31m0\033[0m !.")
              print(" ")
              input(" ➥ Enter.")
              continue
            elif sgxc > gcoins:
              print(" ")
              print(" \033[31mSaldo tidak cukup !\033[0m")
              print(" ")
              input(" ➥ Enter.")
              continue
            
          except:
            print(" ")
            print("\033[31mInput salah !\033[0m")
            print(" ")
            input(" ➥ Enter.")
            continue
          
        hasil_swap = sgxc - fee
        if hasil_swap <= 0:
            print(" ")
            print(" \033[31mJumlah swap terlalu kecil !\033[0m")
            print(" ")
            input(" ➥ Enter")
            continue
        
        
        gcoins -= sgxc
        gxc += hasil_swap * rate_Gxc
        Shasil = hasil_swap * rate_Gxc
        
        
        gcoins = round(gcoins, 3)
        gxc = round(gxc, 3)
        
        print(" ")
        ldSwp()
        exp += 1
        print(" ")
        print(" ")
        print(f" Hasil swap = \033[32m{Shasil}\033[0m") 
        print(" ")
        input(" ➥ Enter.")
        continue
      
      
    elif cmd == "n":
      print(" ")
      print(" ➥ Membatalkan swap(\033[31mExit\033[0m) !")
      print(" ")
      wkt()
      break
    
    else:
      print(" ")
      print("\033[31minput salah !\033[0m")
      print(" ")
      input(" ➥ Enter.")
          

def toko_bibit():
  
  global gxc, bibit, tas, exp, lvl, bibit2
  
  #harga_bibit_t.1
  t1_1 = 15
  t1_3 = 45
  t1_5 = 75
  
  #harga_bibit_t.2
  t2_1 = 20
  t2_3 = 60
  t2_5 = 100
  
  while True:
    
    
    os.system("clear")
    
    print(" ")
    print(f" Saldo Gxc = \033[32m{gxc}\033[0m")
    print(" ")
    print(" Tersedia:\n(1) Bibit pohon T.1\n(2) Bibit pohon T.2\n(x) Keluar")
    print(" ")
  
    cmd=input(" ➥ Pilih : ").lower()
  
    if cmd == "1":
      print(" ")
      wkt()
      
      while True:
          
        os.system("clear")
        print(" ")
        print(f"\033[32mHarga untuk 1 bibit T.1 = {t1_1}\033[0m")
        print(" ")
        print(" Beli 1 (1)\n Beli 3 (3)\n Beli 5 (5)")
        print(" ")
        print(" Kembali [x]")
        ubeli=input(" Input kode sesuai pilihan : ").lower()
      
        if ubeli == "1":
          if gxc >= t1_1:
            if tas < 100:
              print(" ")
              print(" ➥ Proses membeli item bibit T.1 »")
              print(" ")
              wkt()
              print(" ")
              exp += 1
              bibit += 1
              tas += 2
              gxc -= t1_1
              gxc = round(gxc, 3)
              print(" ")
              print(" \033[32mSukses ✓\033[0m")
              print(" ")
              input("Tekan Enter...")
            else:
              print(" ")
              print(" \033[31mTas kamu penuh !\033[0m")
              print(" ")
              input(" ➥ Enter.")
          else:
            print(" ")
            print(" ➥ Proses membeli item bibit T.1 »")
            print(" ")
            wkt()
            print(" ")
            print(" ")
            print(" \033[31mToken Gxc tidak cukup !\033[0m")
            print(" ")
            input(" ➥ Enter. ")
        
        elif ubeli == "3":
          if gxc >= t1_3:
            if tas < 100:
              print(" ")
              print(" ➥ Proses membeli item bibit T.1 »")
              print(" ")
              wkt()
              print(" ")
              exp += 3
              bibit += 3
              tas += 6
              gxc -= t1_3
              gxc = round(gxc, 3)
              print(" ")
              print(" \033[32mSukses ✓\033[0m")
              print(" ")
              input(" ➥ Enter.")
            else:
              print(" ")
              print(" \033[31mTas kamu penuh !\033[0m")
              print(" ")
              input(" ➥ Enter.")
          else:
            print(" ")
            print(" ➥ Proses membeli item bibit  T.1 »")
            print(" ")
            wkt()
            print(" ")
            print(" ")
            print(" \033[31mToken Gxc tidak cukup !\033[0m")
            print(" ")
            input(" ➥ Enter.")
          
        elif ubeli == "5":
          if gxc >= t1_5:
            if tas < 100:
              print(" ")
              print(" ➥ Proses membeli item bibit T.1 »")
              print(" ")
              wkt()
              print(" ")
              exp += 5
              bibit += 5
              tas += 10
              gxc -= t1_5
              gxc = round(gxc, 3)
              print(" ")
              print(" \033[32mSukses ✓\033[0m")
              print(" ")
              input(" ➥ Enter.")
            else:
              print(" ")
              print(" \033[31mTas kamu penuh !\033[0m")
              print(" ")
              input(" ➥ Enter.")
          else:
            print(" ")
            print(" ➥ Proses membeli item bibit T.1 »")
            print(" ")
            wkt()
            print(" ")
            print(" ")
            print(" \033[31mToken Gxc tidak cukup !\033[0m")
            print(" ")
            input(" ➥ Enter.")
        
        elif ubeli == "x":
          print(" ")
          print(" Kembali »")
          print(" ")
          wkt()
          break
        
        
        else:
          print(" ")
          print(" \033[31mInput kode salah !\033[0m")
          print(" ")
          input(" ➥ Enter.")
    
    elif cmd == "2":
      print(" ")
      wkt()
        
      while True:
        os.system("clear")
        
        print(" ")
        print(f"\033[32mHarga untuk 1 bibit T.2 = {t2_1}\033[0m")
        print(" ")
        print(" Beli 1 (1)\n Beli 3 (3)\n Beli 5 (5)")
        print(" ")
        print(" Kembali [x]")
        ubeli=input(" Input kode sesuai pilihan : ").lower()
        
        if ubeli == "1":
          if lvl == 1:
            if gxc >= t2_1:
              if tas < 100:
                print(" ")
                print(" ➥ Proses membeli item bibit T.2 »")
                print(" ")
                wkt()
                print(" ")
                exp += 3
                bibit2 += 1
                tas += 3
                gxc -= t2_1
                gxc = round(gxc, 3)
                print(" ")
                print(" \033[32mSukses ✓\033[0m")
                print(" ")
                input(" ➥ Enter.")
              else:
                print(" ")
                print(" \033[31mTas kamu penuh !\033[0m")
                print(" ")
                input(" ➥ Enter.")
            else:
              print(" ")
              print(" ➥ Proses membeli item bibit T.2 »")
              print(" ")
              wkt()
              print(" ")
              print(" ")
              print(" \033[31mToken Gxc tidak cukup !\033[0m")
              print(" ")
              input(" ➥ Enter.")
          else:
            print(" ")
            print(" \033[31mlevel kamu belum memadai !\033[0m")
            print(" ")
            input(" ➥ Enter.")
          
        elif ubeli == "3":
          if lvl == 3:
            if gxc >= t2_3:
              if tas < 100:
                print(" ")
                print(" ➥ Proses membeli item bibit T.2 »")
                print(" ")
                wkt()
                print(" ")
                exp += 9
                bibit2 += 3
                tas += 9
                gxc -= t2_3
                gxc = round(gxc, 3)
                print(" ")
                print(" \033[32mSukses ✓\033[0m")
                print(" ")
                input(" ➥ Enter.")
              else:
                print(" ")
                print(" \033[31mTas kamu penuh !\033[0m")
                print(" ")
                input(" ➥ Enter.")
            else:
              print(" ")
              print(" ➥ Proses membeli item bibit T.2 »")
              print(" ")
              wkt()
              print(" ")
              print(" ")
              print(" \033[31mToken Gxc tidak cukup !\033[0m")
              print(" ")
              input(" ➥ Enter.")
          else:
            print(" ")
            print(" \033[31mlevel kamu belum memadai !\033[0m")
            print(" ")
            input(" ➥ Enter.")
          
        elif ubeli == "5":
          if lvl == 5:
            if gxc >= t2_5:
              if tas < 100:
                print(" ")
                print(" ➥ Proses membeli item bibit T.2 »")
                print(" ")
                wkt()
                print(" ")
                exp += 15
                bibit2 += 5
                tas += 15
                gxc -= t2_5
                gxc = round(gxc, 3)
                print(" ")
                print(" \033[32mSukses ✓\033[0m")
                print(" ")
                input(" ➥ Enter.")
              else:
                print(" ")
                print(" \033[31mTas kamu penuh !\033[0m")
                print(" ")
                input(" ➥ Enter.")
            else:
              print(" ")
              print(" ➥ Proses membeli item bibit T.2 »")
              print(" ")
              wkt()
              print(" ")
              print(" ")
              print(" \033[31mToken Gxc tidak cukup !\033[0m")
              print(" ")
              input(" ➥ Enter.")
          else:
            print(" ")
            print(" \033[31mlevel kamu belum memadai !\033[0m")
            print(" ")
            input(" ➥ Enter.")
        
        elif ubeli == "x":
          print(" ")
          print(" Kembali »")
          print(" ")
          wkt()
          break
        
        else:
          print(" ")
          print(" \033[31mInput kode salah !\033[0m")
          print(" ")
          input(" ➥ Enter.")
     
      
    elif cmd == "x":
      print(" ")
      print(" Keluar dari toko bibit »")
      print(" ")
      wkt()
      break
      
    else:
      print(" ")
      print(" \033[31mInput salah kode salah !\033[0m")
      print(" ")
      input(" ➥ Enter.")

def penyimpanan():
  global bibit, gxc, kayu, kayuT1, box_penyimpanan, tas, kayuT2, bibit2
  
  while True:
      
    os.system("clear")
    
    print(" ")
    print(" ➧ \033[32mTempat penyimpanan.\033[0m")
    print(" ")
    print(" ➥  \033[36mBarang yang disimpan »\033[0m(0)")
    print(" ➥  \033[36mSimpan barang        »\033[0m(1)")
    print(" ➥  \033[36mAmbil barang         »\033[m(2)")
    print(" ➥  \033[33mBuang barang         »\033[0m(3)")
    print(" ➥  exit                 »(x)")
    print(" ")
    cmd=input(" Pilih : ").lower()
    
    if cmd == "0":
      
      while True:
         #2 
        os.system("clear")
        print(" ")
        print(f" ➧ \033[36mBarang yang disimpan :\033[0m 🎒 = ", tas)
        print(" ")
        print(f" ➥ Bibit T.1   = \033[32m{box_penyimpanan.get("bibit", 0)}\033[0m")
        print(f" ➥ Bibit T.2   = \033[32m{box_penyimpanan.get("bibit2", 0)}\033[0m")
        print(f" ➥ Kayu T.1(0) = \033[32m{box_penyimpanan.get("kayu", 0)}\033[0m")
        print(f" ➥ Kayu T.1    = \033[32m{box_penyimpanan.get("kayuT1", 0)}\033[0m")
        print(f" ➥ Kayu T.2    = \033[32m{box_penyimpanan.get("kayuT2", 0)}\033[0m")
        print(f" ➥ Koin Gxc    = \033[32m{box_penyimpanan.get("gxc", 0)}\033[0m")
        print(" ")
        print(" ➥ Kembali »(k)")
        print(" ")
        pilih = input(" pilih : ").lower()
        
        if pilih == "k":
          break
        
        else:
          print(" ")
          print(" \033[31mInput salah !\033[0m")
          print(" ")
          input(" ➥ Enter. ")
        
    
    elif cmd == "1":
      
      while True:
          
        os.system("clear")
        
        print(" ")
        print(" » \033[32mSimpan barang\033[0m «")
        print(" ")
        print(" ➥ \033[36mSimpan semua barang   »\033[0m(1)")
        print(" ➥ \033[36mPilih beberapa barang »\033[0m(2)")
        print(" ➥ Kembali               »(x)")
        print(" ")
        simpan=input(" Pilih : ").lower()
        
        if simpan == "1":
            
          while True:
            
            os.system("clear")
            #4
            info_kaptasyut2 = kayuT2 * (4/6)
            info_kaptasbit2 = bibit2 * 3
            info_kaptasbit = bibit * 2
            info_kaptasyu = kayu * 1
            info_kpatasyut1 = kayuT1 * (2/3)
            if bibit > 0 or kayu > 0 or kayuT1 > 0 or gxc > 0 or bibit2 > 0 or kayuT2 > 0:
              if "bibit" in box_penyimpanan or "kayu" in box_penyimpanan or "kayuT1" in box_penyimpanan or "gxc" in box_penyimpanan or "bibit2" in box_penyimpanan or kayuT2 in box_penyimpanan:
                print(" ")
                print(" ➥ Proses menyimpan »")
                print(" ")
                #00
                box_penyimpanan["bibit"] += bibit
                box_penyimpanan["kayu"] += kayu
                box_penyimpanan["kayuT1"] += kayuT1
                box_penyimpanan["gxc"] += gxc
                box_penyimpanan["bibit2"] += bibit2
                box_penyimpanan["kayuT2"] += kayuT2
                tas -= info_kaptasbit
                tas -= info_kaptasyu
                tas -= info_kpatasyut1
                tas -= info_kaptasyut2
                tas -= info_kaptasbit2
                bibit = 0
                kayu = 0
                kayuT1 = 0
                gxc = 0
                bibit2 = 0
                kayuT2 = 0
                wkt()
                print(" ")
                print(" ")
                print(" \033[32mSukses ✓\033[0m")
                print(" ")
                input(" ➥ Enter.")
                break
              else:
                print(" ")
                print(" ➥ Proses menyimpan »")
                print(" ")
                box_penyimpanan["bibit2"] = bibit2
                box_penyimpanan["kayuT2"] = kayuT2
                box_penyimpanan["bibit"] = bibit
                box_penyimpanan["kayu"] = kayu
                box_penyimpanan["kayuT1"] = kayuT1
                box_penyimpanan["gxc"] = gxc
                tas -= info_kaptasbit
                tas -= info_kaptasyu
                tas -= info_kpatasyut1
                tas -= info_kaptasbit2
                tas -= info_kaptasyut2
                bibit2 = 0
                kayuT2 = 0
                bibit = 0
                kayu = 0
                kayuT1 = 0
                gxc = 0
                wkt()
                print(" ")
                print(" \033[32mSukses ✓\033[0m" )
                print(" ")
                input(" ➥ Enter.")
                break
            else:
              print(" ")
              print(" ")
              print(" \033[31mTas mu tidak memiliki item !\033[0m")
              print(" ")
              input(" ➥ Enter.")
              break
          
        elif simpan == "2":
          
          while True:
            
            os.system("clear")
            
            print(" ")
            print(" ➧ \033[32mPilih barang »\033[0m")
            print(" ")
            print(" ➥ \033[36mBibit       »\033[0m(1)")
            print(" ➥ \033[36mBibit T.2   »\033[0m(2)")
            print(" ➥ \033[36mKayu T.1(0) »\033[0m(3)")
            print(" ➥ \033[36mKayu T.1    »\033[0m(4)")
            print(" ➥ \033[36mKayu T.2    »\033[0m(5)")
            print(" ➥ \033[36mKoin Gxc    »\033[0m(6)")
            print(" ➥ Kembali  »(x)")
            print(" ")
            psimpan=input(" ➥ Pilih :  ").lower()
            
            if psimpan == "1":
              
              info_kaptasbit = bibit * 2
              if bibit > 0:
                if "bibit" in box_penyimpanan:
                  print(" ")
                  print(" Proses menyimpan bibit T.1 »")
                  print(" ")
                  box_penyimpanan["bibit"] += bibit
                  tas -= info_kaptasbit
                  bibit = 0
                  wkt()
                  print(" ")
                  print(" ")
                  print(" \033[32mSukses menyimpan bibit T.1 ✓\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
                  
                else:
                  print(" ")
                  print(" Proses menyimpan bibit T.1 »")
                  print(" ")
                  box_penyimpanan["bibit"] = bibit
                  tas -= info_kaptasbit
                  bibit = 0
                  wkt()
                  print(" ")
                  print(" ")
                  print(" \033[32mSukses menyimpan bibit T.1 ✓\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
              else:
                print(" ")
                print(" \033[31mTas mu tidak ada item bibit T.1 !\033[0m")
                print(" ")
                input(" ➥ Enter.")
            
            elif psimpan == "2":
              info_kaptasbit2 = bibit2 * 3
              if bibit2 > 0:
                if "bibit" in box_penyimpanan:
                  print(" ")
                  print(" Proses menyimpan bibit T.2 »")
                  print(" ")
                  box_penyimpanan["bibit2"] += bibit2
                  tas -= info_kaptasbit2
                  bibit2 = 0
                  wkt()
                  print(" ")
                  print(" ")
                  print(" \033[32mSukses menyimpan bibit T.2 ✓\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
                else:
                  print(" ")
                  print(" Proses menyimpan bibit T.2 »")
                  print(" ")
                  box_penyimpanan["bibit2"] = bibit2
                  tas -= info_kaptasbit2
                  bibit2 = 0
                  wkt()
                  print(" ")
                  print(" ")
                  print(" \033[32mSukses menyimpan bibit T.2 ✓\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
              else:
                print(" ")
                print(" \033[31mTas mu tidak ada item bibit T.2 !\033[0m")
                print(" ")
                input(" ➥ Enter.")
                
            elif psimpan == "3":
              
              info_kaptasyu = kayu * 1
              if kayu > 0:
                if "kayu" in box_penyimpanan:
                  print(" ")
                  print(" Proses menyimpan kayu T.1(0) »")
                  print(" ")
                  box_penyimpanan["kayu"] += kayu
                  tas -= info_kaptasyu
                  kayu = 0
                  wkt()
                  print(" ")
                  print(" ")
                  print(" \033[32mSukses menyimpan kayu T.1(0) ✓\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
                else:
                  print(" ")
                  print(" Proses menyimpan kayu T.1(0) »")
                  print(" ")
                  box_penyimpanan["kayu"] = kayu
                  tas -= info_kaptasyu
                  kayu = 0
                  wkt()
                  print(" ")
                  print(" ")
                  print(" \033[32mSukses menyimpan kayu T.1(0) ✓\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
              else:
                print(" ")
                print(" \033[31mTas mu tidak ada item kayu T.1(0) !\033[0m")
                print(" ")
                input(" ➥ Enter.")
            
            elif psimpan == "4":
              
              info_kpatasyut1 = kayuT1 * (2/3)
              if kayuT1 > 0:
                if "kayuT1" in box_penyimpanan:
                  print(" ")
                  print(" Proses menyimpan kayu T.1 »")
                  print(" ")
                  box_penyimpanan["kayuT1"] += kayuT1
                  tas -= info_kpatasyut1
                  kayuT1 = 0
                  wkt()
                  print(" ")
                  print(" ")
                  print(" \033[32mSukses menyimpan kayu T.1 ✓\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
                else:
                  print(" ")
                  print(" Proses menyimpan kayu T.1 »")
                  print(" ")
                  box_penyimpanan["kayuT1"] = kayuT1
                  tas -= info_kpatasyut1
                  kayuT1 = 0
                  wkt()
                  print(" ")
                  print(" ")
                  print(" \033[32mSukses menyimpan kayu T.1 ✓\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
              else:
                print(" ")
                print(" \033[31mTas mu tidak ada item kayu T.1 !\033[0m")
                print(" ")
                input(" ➥ Enter.")
            
            elif psimpan == "5":
              
              info_kaptasyut2 = kayuT2 * (4/6)
              if kayuT2 > 0:
                if "kayuT2" in box_penyimpanan:
                  print(" ")
                  print(" Proses menyimpan kayu T.2 »")
                  print(" ")
                  box_penyimpanan["kayuT2"] += kayuT2
                  tas -= info_kaptasyut2
                  kayuT2 = 0
                  wkt()
                  print(" ")
                  print(" ")
                  print(" \033[32mSukses menyimpan kayu T.2 ✓\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
                else:
                  print(" ")
                  print(" Proses menyimpan kayu T.1 »")
                  print(" ")
                  box_penyimpanan["kayuT2"] = kayuT2
                  tas -= info_kaptasyut2
                  kayuT2 = 0
                  wkt()
                  print(" ")
                  print(" ")
                  print(" \033[32mSukses menyimpan kayu T.2 ✓\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
              else:
                print(" ")
                print(" \033[31mTas mu tidak ada item kayu T.2 !\033[0m")
                print(" ")
                input(" ➥ Enter.")
            
            
            elif psimpan == "6":
              
              if gxc > 0:
                if "gxc" in box_penyimpanan:
                  print(" ")
                  print(" Proses menyimpan Koin Gxc »")
                  print(" ")
                  box_penyimpanan["gxc"] += gxc
                  gxc = 0
                  wkt()
                  print(" ")
                  print(" ")
                  print(" \033[32mSukses menyimpan koin Gxc ✓\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
                else:
                  print(" ")
                  print(" Proses menyimpan koin Gxc »")
                  print(" ")
                  box_penyimpanan["gxc"] = gxc
                  gxc = 0
                  wkt()
                  print(" ")
                  print(" ")
                  print(" \033[32mSukses menyimpan koin Gxc ✓\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
              else:
                print(" ")
                print(" \033[31mKamu belum memiliki koin Gxc !\033[0m")
                print(" ")
                input(" ➥ Enter.")
            
            
            elif psimpan == "x":
              break
            
            else:
              print(" ")
              print(" \033[31mInput salah !\033[0m")
              print(" ")
              input(" ➥ Enter.")
              
        elif simpan == "x":
          break
           
        else:
          print(" ")
          print(" \033[31mInput salah !\033[0m")
          print(" ")
          input(" ➥ Enter.")
            
     
    elif cmd == "2":
      
      while True:
        
        os.system("clear")
        
        print(" ")
        print(" ➧ \033[32mAmbil barang »\033[0m")
        print(" ")
        print(" ➥ \033[36mAmbil semua barang    »\033[0m(1)")
        print(" ➥ \033[36mPilih beberapa barang »\033[0m(2)")
        print(" ➥ kembali               »(3)")
        print(" ")
        abarang=input(" Pilih : ").lower()
        
        if abarang == "1":
          
          while True:
            
            os.system("clear")
            
            info_kaptasbit = 2
            info_kaptasbit2 = 3
            info_kaptasyu = 1
            info_kpatasyut1 = (2/3)
            info_kaptasyut2 = (4/6)
            
            jmlbit = box_penyimpanan.get("bibit", 0)
            jmlbit2 = box_penyimpanan.get("bibit2", 0)
            jmlyu = box_penyimpanan.get("kayu", 0)
            jmlyut1 = box_penyimpanan.get("kayuT1", 0)
            jmlyut2 = box_penyimpanan.get("kayuT2", 0)
            jmlgxc = box_penyimpanan.get("gxc", 0)
            if tas < 100:
              if "bibit" in box_penyimpanan or "kayu" in box_penyimpanan or "kayuT1" in box_penyimpanan or "gxc" in box_penyimpanan or "bibit2" in box_penyimpanan or "kayuT2" in box_penyimpanan:
                print(" ")
                print(" Mengambil semua item »")
                print(" ")
                wkt()
                box_penyimpanan["bibit"] = 0
                box_penyimpanan["bibit2"] = 0
                box_penyimpanan["kayu"] = 0
                box_penyimpanan["kayuT1"] = 0
                box_penyimpanan["kayuT2"] = 0
                box_penyimpanan["gxc"] = 0
                tas += jmlbit * info_kaptasbit
                tas += jmlbit2 * info_kaptasbit2
                tas += jmlyu * info_kaptasyu
                tas += jmlyut1 * info_kpatasyut1
                tas += jmlyut2 * info_kaptasyut2
                bibit += jmlbit
                bibit2 += jmlbit2
                kayu += jmlyu
                kayuT1 += jmlyut1
                kayuT2 += jmlyut2
                gxc += jmlgxc
                print(" ")
                print(" \033[32mMengambil semua item sukses ✓\033[0m")
                print(" ")
                input(" ➥ Enter.")
                break
              else:
                print(" ")
                print(" \033[31mTidak ada item dipenyimpanan !\033[0m")
                print(" ")
                input(" ➥ Enter.")
                break
            else:
              print(" ")
              print(" \033[31mTas kamu sudah penuh !\033[0m")
              print(" ")
              input(" ➥ Enter.")
              break
                 
        elif abarang == "2":
          
          while True:
            
            os.system("clear")
            
            print(" ")
            print(" \033[36mPilih beberapa barang »\033[0m")
            print(" ")
            print(" ➥ Bibit T.1   »(1)")
            print(" ➥ Bibit T.2   »(2)")
            print(" ➥ Kayu T.1(0) »(3)")
            print(" ➥ Kayu T.1    »(4)")
            print(" ➥ Kayu T.2    »(5)")
            print(" ➥ Koin Gxc    »(6)")
            print(" ➥ Kembali     »(x)")
            print(" ")
            pabarang=input(" Pilih : ").lower()
            
            if pabarang == "1":
              print(" ")
              
              while True:
                
                os.system("clear")
                
                info_kaptasbit = 2
                jmlbit = box_penyimpanan.get("bibit", 0)
                if tas < 100:
                  if "bibit" in box_penyimpanan:
                    print(" ")
                    print(" Mengambil item bibit T.1 »")
                    print(" ")
                    wkt()
                    box_penyimpanan["bibit"] = 0
                    tas += jmlbit * info_kaptasbit
                    bibit += jmlbit
                    print(" ")
                    print(" \033[32mSukses mengambil item bibit T.1 ✓\033[0m")
                    print(" ")
                    input(" ➥ Enter.")
                    break
                  else:
                    print(" ")
                    print(" \033[31mItem bibit T.1 tidak ada dipenyimpanan !\033[0m")
                    print(" ")
                    input(" ➥ Enter.")
                    break
                else:
                  print(" ")
                  print(" \033[31mTas kamu sudah penuh !\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
                  break
            
            elif pabarang == "2":
              print(" ")
              
              while True:
                
                os.system("clear")
                
                info_kaptasbit2 = 3
                jmlbit = box_penyimpanan.get("bibit2", 0)
                if tas < 100:
                  if "bibit2" in box_penyimpanan:
                    print(" ")
                    print(" Mengambil item bibit T.2 »")
                    print(" ")
                    wkt()
                    box_penyimpanan["bibit2"] = 0
                    tas += jmlbit2 * info_kaptasbit2
                    bibit += jmlbit2
                    print(" ")
                    print(" \033[32mSukses mengambil item bibit T.2 ✓\033[0m")
                    print(" ")
                    input(" ➥ Enter.")
                    break
                  else:
                    print(" ")
                    print(" \033[31mItem bibit T.2 tidak ada dipenyimpanan !\033[0m")
                    print(" ")
                    input(" ➥ Enter.")
                    break
                else:
                  print(" ")
                  print(" \033[31mTas kamu sudah penuh !\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
                  break
            
            elif pabarang == "3":
              print(" ")
              
              while True:
                
                os.system("clear")
                
                info_kaptasyu = 1
                jmlyu = box_penyimpanan.get("kayu", 0)
                if tas < 100:
                  if "kayu" in box_penyimpanan:
                    print(" ")
                    print(" Mengambil item kayu T.1(0) »")
                    print(" ")
                    wkt()
                    box_penyimpanan["kayu"] = 0
                    tas += jmlyu * info_kaptasyu
                    kayu += jmlyu
                    print(" ")
                    print(" \033[32mSukses mengambil item kayu T.1(0) ✓\033[0m")
                    print(" ")
                    input(" ➥ Enter.")
                    break
                  else:
                    print(" ")
                    print(" \033[31mItem kayu T.1(0) tidak ada dipenyimpanan !\033[0m")
                    print(" ")
                    input(" ➥ Enter.")
                    break
                else:
                  print(" ")
                  print(" \033[31mTas kamu sudah penuh !\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
                  break
            
            elif pabarang == "4":
              print(" ")
              
              while True:
                
                os.system("clear")
                
                info_kpatasyut1 = (2/3)
                jmlyut1 = box_penyimpanan.get("kayuT1", 0)
                if tas < 100:
                  if "kayuT1" in box_penyimpanan:
                    print(" ")
                    print(" Mengambil item kayu T.1 »")
                    print(" ")
                    wkt()
                    box_penyimpanan["kayuT1"] = 0
                    tas += jmlyut1 * info_kpatasyut1
                    kayuT1 += jmlyut1
                    print(" ")
                    print(" \033[32mSukses mengambil item kayu T.1 ✓\033[0m")
                    print(" ")
                    input(" ➥ Enter.")
                    break
                  else:
                    print(" ")
                    print(" \033[31mItem kayu T.1 tidak ada dipenyimpanan !\033[0m")
                    print(" ")
                    input(" ➥ Enter.")
                    break
                else:
                  print(" ")
                  print(" \033[31mTas kamu sudah penuh !\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
                  break
             
            elif pabarang == "5":
              print(" ")
              
              while True:
                
                os.system("clear")
                
                info_kaptasyut2 = (4/6)
                jmlyut2 = box_penyimpanan.get("kayuT2", 0)
                if tas < 100:
                  if "kayuT2" in box_penyimpanan:
                    print(" ")
                    print(" Mengambil item kayu T.2 »")
                    print(" ")
                    wkt()
                    box_penyimpanan["kayuT2"] = 0
                    tas += jmlyut2 * info_kaptasyut2
                    kayuT2 += jmlyut2
                    print(" ")
                    print(" \033[32mSukses mengambil item kayu T.2 ✓\033[0m")
                    print(" ")
                    input(" ➥ Enter.")
                    break
                  else:
                    print(" ")
                    print(" \033[31mItem kayu T.2 tidak ada dipenyimpanan !\033[0m")
                    print(" ")
                    input(" ➥ Enter.")
                    break
                else:
                  print(" ")
                  print(" \033[31mTas kamu sudah penuh !\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
                  break
              
            elif pabarang == "6":
              print(" ")
              
              while True:
                
                os.system("clear")
                
                jmlgxc = box_penyimpanan.get("gxc", 0)
                if tas < 100:
                  if "gxc" in box_penyimpanan:
                    print(" ")
                    print(" Mengambil item koin Gxc »")
                    print(" ")
                    wkt()
                    box_penyimpanan["gxc"] = 0
                    gxc += jmlgxc
                    print(" ")
                    print(" \033[32mSukses mengambil item koin Gxc ✓\033[0m")
                    print(" ")
                    input(" ➥ Enter.")
                    break
                  else:
                    print(" ")
                    print(" \033[31mItem koin Gxc tidak ada dipenyimpanan !\033[0m")
                    print(" ")
                    input(" ➥ Enter.")
                    break
                else:
                  print(" ")
                  print(" \033[31mTas kamu sudah penuh !\033[0m")
                  print(" ")
                  input(" ➥ Enter.")
                  break
            
            elif pabarang == "x":
              break
            
            else:
              print(" ")
              print(" \033[31mInput salah !\033[0m")
              print(" ")
              input(" ➥ Enter.")
          
            
        elif abarang == "3":
          break
        
        else:
          print(" ")
          print(" input salah ")
          print(" ")
          input(" enter ")
             
            
    elif cmd == "3":#00000
      
      while True:
        
        os.system("clear")
        
        print(" ")
        print(" ➧ \033[33mBuang barang !\033[0m")
        print(" ")
        print(" ➥ Buang semua barang    »(1)")
        print(" ➥ Pilih beberapa barang »(2)")
        print(" ➥ Kembali               »(3)")
        print(" ")
        buang=input(" ➥ Pilih : ").lower()
        
        if buang == "1":
          if box_penyimpanan:
            print(" ")
            print(" ➥ \033[33mProses membuang semua barang !\033[0m")
            print(" ")
            wkt()
            print(" ")
            box_penyimpanan.clear()
            print(" ")
            print(" \033[32mSukses membuang semua barang ✓\033[0m")
            print(" ")
            input(" ➥ Enter.")
          else:
            print(" ")
            wkt()
            print(" ")
            print(" ")
            print(" \033[31mPenyimpanan kosong !\033[0m")
            print(" ")
            input(" ➥ Enter.")
        
        elif buang == "2":
          
          while True:
              
            os.system("clear")
            
            print(" ")
            print(" ➧ \033[33mPilih barang yang ingin dibuang !\033[0m")
            print(" ")
            print(" ➥ Bibit T.1   »(1)")
            print(" ➥ Bibit T.2   »(2)")
            print(" ➥ Kayu T.1(0) »(3)")
            print(" ➥ Kayu T.1    »(4)")
            print(" ➥ Kayu T.2    »(5)")
            print(" ➥ Koin Gxc    »(6)")
            print(" ➥ Kembali     »[x]")
            print(" ")
            pbuang=input(" ➥ Pilih : ").lower()
            
            if pbuang == "1":
              if "bibit" in box_penyimpanan:
                print(" ")
                print(" \033[33mMembuang item bibit T.1 !\033[0m")
                print(" ")
                wkt()
                print(" ")
                del box_penyimpanan["bibit"]
                print(" ")
                print(" \033[32mSukses membuang item bibit T.1 ✓\033[0m")
                print(" ")
                input(" ➥ Enter.")
              else:
                print(" ")
                print(" \033[31mItem bibit T.1 tidak ada dipenyimpanan !\033[0m")
                print(" ")
                input(" ➥ Enter.")
            
            elif pbuang == "2":
              if "bibit2" in box_penyimpanan:
                print(" ")
                print(" \033[33mMembuang item bibit T.2 !\033[0m")
                print(" ")
                wkt()
                print(" ")
                del box_penyimpanan["bibit2"]
                print(" ")
                print(" \033[32mSukses membuang item bibit T.2 ✓\033[0m")
                print(" ")
                input(" ➥ Enter.")
              else:
                print(" ")
                print(" \033[31mItem bibit T.2 tidak ada dipenyimpanan !\033[0m")
                print(" ")
                input(" ➥ Enter.")
            
            elif pbuang == "3":
              if "kayu" in box_penyimpanan:
                print(" ")
                print(" \033[33mMembuang item kayu T.1(0) !\033[0m")
                print(" ")
                wkt()
                print(" ")
                del box_penyimpanan["kayu"]
                print(" ")
                print(" \033[32mSukses membuang item kayu ✓\033[0m")
                print(" ")
                input(" ➥ Enter.")
              else:
                print(" ")
                print(" \033[31mItem kayu T.1(0) tidak ada dipenyimpanan !\033[0m")
                print(" ")
                input(" ➥ Enter.")
            
            elif pbuang == "4":
              if "kayuT1" in box_penyimpanan:
                print(" ")
                print(" \033[33mMembuang item kayu T.1 !\033[0m")
                print(" ")
                wkt()
                print(" ")
                del box_penyimpanan["kayuT1"]
                print(" ")
                print(" \033[32mSukses membuang item kayu T.1 ✓\033[0m")
                print(" ")
                input(" ➥ Enter.")
              else:
                print(" ")
                print(" \033[31mItem kayu T.1 tidak ada dipenyimpanan !\033[0m")
                print(" ")
                input(" ➥ Enter.")
            
            elif pbuang == "5":
              if "kayuT2" in box_penyimpanan:
                print(" ")
                print(" \033[33mMembuang item kayu T.2 !\033[0m")
                print(" ")
                wkt()
                print(" ")
                del box_penyimpanan["kayuT2"]
                print(" ")
                print(" \033[32mSukses membuang item kayu T.2 ✓\033[0m")
                print(" ")
                input(" ➥ Enter.")
              else:
                print(" ")
                print(" \033[31mItem kayu T.2 tidak ada dipenyimpanan !\033[0m")
                print(" ")
                input(" ➥ Enter.")
                
            elif pbuang == "6":
              if "gxc" in box_penyimpanan:
                print(" ")
                print(" \033[33mMembuang item koin Gxc !\033[0m")
                print(" ")
                wkt()
                print(" ")
                del box_penyimpanan["gxc"]
                print(" ")
                print(" \033[32mSukses membuang item koin Gxc ✓\033[0m")
                print(" ")
                input(" ➥ Enter.")
              else:
                print(" ")
                print(" \033[31mItem koin Gxc tidak ada dipenyimpanan !\033[0m")
                print(" ")
                input(" ➥ Enter.")
            
            elif pbuang == "x":
              break
            
            else:
              print(" ")
              print(" \033[31mInput salah !\033[0m")
              print(" ")
              input(" ➥ Enter.")
                
        elif buang == "3":
          break
      
        else: 
          print(" ")
          print(" \033[31mInput salah !\033[0m")
          print(" ")
          input(" ➥ Enter.")
    
    elif cmd == "x":
      print(" ")
      print(" ➥ Keluar")
      print(" ")
      wkt()
      break
        
    else:
      print(" ")
      print(" \033[31mInput salah !\033[0m")
      print(" ")
      input(" ➥ Enter.")
        
def infolahan():
    
  while True:
    os.system("clear")
    
    print(" ")
    print(" \033[36mNote\033[0m :")
    print(" ")
    print(" ➧ Untuk bagian ➟ Pohon T.1 🌳")
    print(" Huruf \033[32mp\033[0m untuk menanam.")
    print(" Huruf \033[32mx\033[0m untuk menebang.")
    print(" ➧ Untuk bagian ➟ Pohon T.2 🌲")
    print(" Huruf \033[32mq\033[0m untuk menanam.")
    print(" Huruf \033[32mc\033[0m untuk menebang.")
    print(" ")
    cmd=input(" Keluar [x] :").lower()
    
    if cmd == "x":
      break
      
def kerajinan():
  
  print(" ")
  print(" Kerajinan ")
  print(" ")
  input(" ➥ Enter.")
  
def book():
  
  os.system("python ibook.py")
  
def misi():
  global bibit, bibit2, kayu, kayuT1, kayuT2, Game_end, bit1cek, bit2cek, kayu0cek, kayu1cek, kayu2cek
  
  while True:
    os.system("clear")
    
    
    if bibit >= 50:
      bit1cek += "✓"
      Game_end += 20
    elif bibit2 >= 45:
      bit2cek = "✓"
      Game_end += 20
    elif kayu >= 50:
      kayu0cek = "✓"
      Game_end += 20
    elif kayuT1 >= 200:
      kayu1cek = "✓"
      Game_end += 20
    elif kayuT2 >= 280:
      kayu2cek = "✓"
      Game_end += 20
      
    print(f"» Bibit T.1 ×50 [\033[32m{bit1cek}\033[0m]")
    print(f"» Bibit T.2 ×45 [\033[32m{bit2cek}\033[0m]")
    print(f"» Kayu T.1/2(0) x50 [\033[32m{kayu0cek}\033[0m]")
    print(f"» Kayu T.1 ×200 [\033[32m{kayu1cek}\033[0m]")
    print(f"» Kayu T.2 ×280 [\033[32m{kayu2cek}\033[0m]")
    
    
    
    cmd=input(" Cek Misi [c] - Keluar [x] : ").lower()
    if cmd == "x":
      break
    
    elif cmd == "c":
      if Game_end >= 100:
        break
      else:
        print(" ")
        print(" \033[31mMisi belum selesai !\033[0m")
        print(" ")
        input(" ➥ Enter.")
        continue
    
#?
while True:
  
  nowA = time.time()
  for posA in list(respawnA.keys()):
    if nowA >= respawnA[posA]:
      apelx, apely = posA
      del respawnA[posA]
  
  nowC = time.time()
  for posC in list(respawnC.keys()):
    if nowC >= respawnC[posC]:
      casx, casy = posC
      del respawnC[posC]
  
  nowT2 = time.time()
  for posT2 in list(respawnT2.keys()):
    if nowT2 >= respawnT2[posT2]:
      tanam2.remove(posT2)
      pohon_tanam2.add(posT2)
      del respawnT2[posT2]
  
  nowT = time.time()
  for posT in list(respawnT.keys()):
    if nowT >= respawnT[posT]:
      tanam.remove(posT)
      pohon_tanam.add(posT)
      del respawnT[posT]

  now1 = time.time()
  for pos1 in list(respawn1.keys()):
    if now1 >= respawn1[pos1]:
      pohon1.add(pos1)
      del respawn1[pos1]
  
  now2 = time.time()
  for pos2 in list(respawn2.keys()):
    if now2 >= respawn2[pos2]:
      pohon2.add(pos2)
      del respawn2[pos2]
  
  
  os.system("clear")
  #START#
  if worldpos == "start":
    #Random_Kode
    sandi = "".join(random.choices(string.ascii_letters + string.digits, k=9))
    
    print(" ")
    print("\033[32mNote\033[0m : \033[36mProgres Game » [75%]\033[0m")
    print(" ")
    print("╔══════════╗")
    print("║\033[95mMade In\033[0m ♥️ ║ × ☕ + ✊")
    print("╚══════════╝")
    print(" 2  0  2  6 ")
    print("┌───────────┐")
    print(f"│\033[32m {sandi}\033[0m","│")
    print("└───────────┘")
    print(" Masukkan kode untuk memulai game.")
    print(" ")
    kode=(input("➥ Kode : "))
    
    if kode == sandi or kode == "y":
      print(" ")
      print(" Mulai masuk ➟")
      print(" ")
      ldSuk()
      worldpos = "Rumah"
      print(" ")
      print(" ")
      input(" ➥ Masuk ! Enter.")
    else:
      print(" ")
      print(" Mulai masuk ➟")
      print(" ")
      ldGal()
      print(" ")
      print(" ")
      input(" ➥ Ulangi ! Enter")
    
  #RUMAH(HOME)
  elif worldpos == "Rumah":
    d_rumah()
    print(" ")
    cmd=input(" ➧ perintah : ").lower()

    oldx, oldy = userx, usery
    
    #testing
    if cmd == "p":
      worldpos = "pasar"
    if cmd == "u":
      worldpos = "start"
    if cmd == "k":
      worldpos = "kebun"
    if cmd == "i":
      isiTas()
    
    if cmd == "w":
      usery -= 1
    elif cmd == "s":
      usery += 1
    elif cmd == "a":
      userx -= 1
    elif cmd == "d":
      userx += 1

      
    if userx < 0:
      userx = 0
    elif userx >= rumahx:
      userx = rumahx -1
    
    if usery < 0:
      usery = 0
    elif usery >= rumahy:
      usery = rumahy -1
    
    if (userx, usery) in walls or (userx, usery) in gelondong:
      userx, usery = oldx, oldy
      info = " \033[33maduhhh 😵\033[0m"
      pusing = 3
    else:
        info = ""

    if pusing > 0:
      pusing -= 1
      
    if (userx, usery) == (casx, casy):
      casE = 2
    if casE > 0:
      casE -= 1
    
    if cmd == "m":
      pos = (userx, usery)
      obj = (bookx, booky)
      if pos == obj:
        book()
      
    if cmd == "m":
      pos = (userx, usery)
      obj = (ksuratx, ksuraty)
      if pos == obj:
        misi()
    
    if cmd == "m":
      pos = (userx, usery)
      obj = gentong
      if pos in gentong:
        gentongbuang()
    
    if cmd == "m":
      pos = (userx, usery)
      obj = (invx, invy)
      if pos == obj:
          print(" ")
          print(" Membuka penyimpanan »")
          print(" ")
          wkt()
          penyimpanan()
    
    if cmd == "m":
      pos = (userx, usery)
      obj = (crafx, crafy)
      if pos == obj:
          print(" ")
          print(" Membuka kerajinan »")
          print(" ")
          wkt()
          kerajinan()
      
    if cmd == "m":
      pos = (userx, usery)
      obj = (pintux, pintuy)
      if (userx, usery) == (pintux, pintuy):
        print(" ")
        print(" Pergi menuju kebun »")
        print(" ")
        ldkb()
        worldpos = "kebun"
      
    if cmd == "m":
      pos = (userx, usery)
      obj = (coinx, coiny)
      if pos == obj:
        print(" ")
        print("membuka brankas!")
        print(" ")
        wkt()
        coins()

    if cmd == "m":
      pos = (userx, usery)
      obj = (casx, casy)
      if pos == obj:
        if Hp < 100:
            print(" ")
            ldcas()
            print(" ")
            print(" ")
            input(" ➥ Enter.")
            Hp = 100
            
            if casx is not None and (userx, usery) == (casx, casy):
              casx, casy = None, None
              respawnC[userx, usery] = nowC + w_isi
              
        elif Hp == 100:
          print(" ")
          ldcasfull()
          print(" ")
          print(" ")
          input(" ➥ Enter.")
  
  #KEBUN
  elif worldpos == "kebun":
    
    d_kebun()
    print(" ")
    cmd=input(" ➧ perintah : ").lower()
    
    oldx, oldy = userx1, usery1
    
    if cmd == "0":
      infolahan()
    if cmd == "i":
      isiTas()
    if cmd == "w":
      usery1 -= 1
    elif cmd == "s":
      usery1 += 1
    elif cmd == "a":
      userx1 -= 1
    elif cmd == "d":
      userx1 += 1
      
    if userx1 < 0:
      userx1 = 0
    elif userx1 >= kebunx:
      userx1 = kebunx -1
      
    if usery1 < 0:
      usery1 = 0
    elif usery1 >= kebuny:
      usery1 = kebuny -1
      
    if (userx1, usery1) in wallsk:
      userx1, usery1 = oldx, oldy
      pusing = 3
      info = " \033[33maduhhh 😵\033[0m"
    else:
        info = ""
      
      
    if pusing > 0:
      pusing -= 1
    
    if cmd == "m":
      pos = (userx1, usery1)
      obj = (apelx, apely)
      if Hp < 50:
        if pos == obj:
          print(" ")
          print(" Memakan apel »")
          print(" ")
          wkt()
          Hp += 50
          print(" ")
          print(" \033[32mSukses memakan apel ✓\033[0m")
          respawnA[apelx, apely] = nowA + wt_muncul
          apelx, apely = -1, -1
          print(" ")
          input(" ➥ Enter.")
      else:
        print(" ")
        print(" \033[31mEnergi mu masih cukup !\033[0m")
        print(" ")
        input(" ➥ Enter.")
  
    #PART_menanam pohon t.1
    if cmd == "p":
      pos = (userx1, usery1)
      obj = k_lahan
      tm = tanam
      tm2 = tanam2
      pt = pohon_tanam
      pt2 = pohon_tanam
      if pos in obj:
        if pos in tm or pos in pt:
          print(" ")
          print(" \033[33mSudah ada tanaman !\033[0m")
          print(" ")
          input(" ➥ Enter.")
          
        elif pos in tm2 or pos in pt2:
          print(" ")
          print(" \033[31mSudah ada pohon T.2 yang ditanam disini !\033[0m")
          print(" ")
          input(" ➥ Enter.")
      
        elif Hp >= 2:
          if bibit >= 1:
            print(" ")
            print(" ➥ Mulai menanam bibit T.1")
            print(" ")
            exp += 2
            Hp -= 2
            wkt()
            bibit -= 1
            tas -= 2
            print(" ")
            tanam.add((userx1, usery1))
            print(" \033[32mSukses menanam bibit T.1 ✓\033[0m")
            print(" ")
            input(" ➥ Enter.")
            respawnT[userx1, usery1] = nowT + wt_tanam
          else:
            print(" ")
            print(" \033[31mBibit T.1 tidak ada!!!\033[0m")
            print(" ")
            input(" ➥ Enter.")
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          print(" ")
          input(" ➥ Enter.")
      else:
        print(" ")
        print(" \033[31mHanya bisa dilahan menanam!\033[0m")
        print(" ")
        input(" ➥ Enter.")
    
    #PART_menebang_pohon_t.1
    if cmd == "x":
      pos = (userx1, usery1)
      lhn = k_lahan
      tm = tanam
      pt = pohon_tanam
      if pos in tm:
        print(" ")
        print(" \033[33mPohon masih muda !\033[0m")
        print(" ")
        input(" ➥ Enter.")
        
      elif pos in pt:
        if Hp >= 2:
          if tas < 100:
            print(" ")
            print(" ➥ Mulai menebang.")
            print(" ")
            wkt()
            print(" ")
            kayuT1 += 3
            tas += 2
            exp += 5
            Hp -= 2
            pohon_tanam.remove(pos)
            gxc += 19
            gxc = round(gxc, 3)
            print(" \033[32mMenebang sukses ✓\033[0m")
            print(" ")
            input(" ➥ Enter.")
          else:
            print(" ")
            print(" \033[31mTas kamu penuh !\033[0m")
            print(" ")
            input(" ➥ Enter.")
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          print(" ")
          input(" ➥ Enter.")
      
      elif pos in lhn:
        print(" ")
        print(" \033[33mTidak ada objek tanaman !\033[0m")
        print(" ")
        input(" ➥ Enter.")
          
      else:
        print(" ")
        print(" \033[31mBukan diarea lahan !\033[0m")
        print(" ")
        input(" ➥ Enter.")
    
    #part menanam pohon T.2
    if cmd == "q":
      pos = (userx1, usery1)
      obj = k_lahan
      tm1 = tanam
      tm = tanam2
      pt1 = pohon_tanam
      pt = pohon_tanam2
      if pos in obj:
        if pos in tm or pos in pt:
          print(" ")
          print(" \033[33mSudah ada tanaman !\033[0m")
          print(" ")
          input(" ➥ Enter.")
        
        elif pos in tm1 or pos in pt1:
          print(" ")
          print(" \033[31mSudah ada pohon T.1 yang ditanam disini !\033[0m")
          print(" ")
          input(" ➥ Enter.")
        
        elif Hp >= 4:
          if bibit2 >= 1:
            print(" ")
            print(" ➥ Mulai menanam bibit T.2")
            print(" ")
            exp += 6
            Hp -= 4
            wkt()
            bibit2 -= 1
            tas -= 3
            print(" ")
            tanam2.add((userx1, usery1))
            print(" \033[32mSukses menanam bibit T.2 ✓\033[0m")
            print(" ")
            input(" ➥ Enter.")
            respawnT2[userx1, usery1] = nowT2 + wt_tanam2
          else:
            print(" ")
            print(" \033[31mBibit T.2 tidak ada!!!\033[0m")
            print(" ")
            input(" ➥ Enter.")
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          print(" ")
          input(" ➥ Enter.")
      else:
        print(" ")
        print(" \033[31mHanya bisa dilahan menanam!\033[0m")
        print(" ")
        input(" ➥ Enter.")
    
    #part menebanh pohon T.2
    if cmd == "c":
      pos = (userx1, usery1)
      lhn = k_lahan
      tm = tanam2
      pt = pohon_tanam2
      if pos in tm:
        print(" ")
        print(" \033[33mPohon masih muda !\033[0m")
        print(" ")
        input(" ➥ Enter.")
        
      elif pos in pt:
        if Hp >= 4:
          if tas < 100:
            print(" ")
            print(" ➥ Mulai menebang.")
            print(" ")
            wkt()
            print(" ")
            kayuT2 += 6
            tas += 4
            exp += 6
            Hp -= 4
            pohon_tanam2.remove(pos)
            gxc += 25
            gxc = round(gxc, 3)
            print(" \033[32mMenebang sukses ✓\033[0m")
            print(" ")
            input(" ➥ Enter.")
          else:
            print(" ")
            print(" \033[31mTas kamu penuh !\033[0m")
            print(" ")
            input(" ➥ Enter.")
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          print(" ")
          input(" ➥ Enter.")
      
      elif pos in lhn:
        print(" ")
        print(" \033[33mTidak ada objek tanaman !\033[0m")
        print(" ")
        input(" ➥ Enter.")
          
      else:
        print(" ")
        print(" \033[31mBukan diarea lahan !\033[0m")
        print(" ")
        input(" ➥ Enter.")     
        
        
        
    
    #PART_kembali kerumah
    if cmd == "m":
      pos = (userx1, usery1)
      obj = (pintux1, pintuy1)
      if pos == obj:
        print(" ")
        print(" Masuk ke dalam Rumah «")
        print(" ")
        ldkb()
        worldpos = "Rumah"
    
    #PART_pergi kepasar
    if cmd == "m":
      pos = (userx1, usery1)
      obj = (ppasarx, ppasary)
      if pos == obj:
        print(" ")
        print(" Berjalan menuju pasar »")
        print(" ")
        ldkb()
        worldpos = "pasar"
        
    #PART_menebang pohon t.1(0)
    if cmd == "1":
      pos = (userx1, usery1)
      obj = pohon1
      if pos in obj:
        if Hp >= 3:
          if tas < 100:
            print(" ")
            print(" ➥ Mulai menebang...")
            print(" ")
            kayu += 1
            Hp -= 3
            gcoins += 7
            gcoins = round(gcoins, 3)
            pohon1.remove((userx1, usery1))
            respawn1[userx1, usery1] = now1 + w_tumbuh1
            ldtb()
            print(" ")
            tas += 1
            exp += 2
            print(" ")
            input(" ➥ Enter.")
          else:
            print(" ")
            print(" \033[31mTas kamu penuh !\033[0m")
            print(" ")
            input(" ➥ Enter.")
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          print(" ")
          input(" ➥ Enter.")
      else:
        print(" ")
        print(" \033[33mTunggu pohon tumbuh!\033[0m")
        print(" ")
        input(" ➥ Enter.")
    
  
      
    #PART_menebang pohon t.2(0) 
    if cmd == "2":
      pos = (userx1, usery1)
      obj = pohon2
      if pos in obj:
        if Hp >= 3:
          if tas < 100:
            print(" ")
            print(" ➥ Mulai menebang...")
            print(" ")
            kayu += 1
            Hp -= 3
            gcoins += 7
            gcoins = round(gcoins, 3)
            pohon2.remove((userx1, usery1))
            respawn2[userx1, usery1] = now2 + w_tumbuh2
            ldtb()
            print(" ")
            tas += 1
            exp += 2
            print(" ")
            input(" ➥ Enter.")
          else:
            print(" ")
            print(" \033[31mTas kamu penuh !\033[0m")
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          print(" ")
          input(" ➥ Enter.")
      else:
        print(" ")
        print(" \033[33mTunggu pohon tumbuh!\033[0m")
        print(" ")
        input(" ➥ Enter.")
        
  #PASAR
  else:
    
    d_pasar()
    print(" ")
    cmd=input(" ➥ perintah : ").lower()
    
    oldx, oldy = userxp, useryp
    
    if cmd == "i":
      isiTas()
    
    if cmd == "w":
      useryp -= 1
      
    elif cmd == "s":
      useryp += 1
      
    elif cmd == "a":
      userxp -= 1
    
    elif cmd == "d":
      userxp += 1
      
    if userxp < 0:
      userxp = 0
    elif userxp >= pasarx:
      userxp = pasarx -1
      
    if useryp < 0:
      useryp = 0
    elif useryp >= pasary:
      useryp = pasary -1
     
    pos = (userxp, useryp)
    obj = wallp
    if pos in obj:
      userxp, useryp = oldx, oldy
      pusing = 3
      info = " \033[33maduhhh 😵\033[0m"
    else:
        info = ""
        
    if pusing > 0:
      pusing -= 1
     
     
    if cmd == "m":
      pos = (userxp, useryp)
      obj = (bpasarx, bpasary)
      if pos == obj:
        print(" ")
        print(" « pergi kekebun")
        print(" ")
        ldkb()
        worldpos = "kebun"
    
    if cmd == "m":
      pos = (userxp, useryp)
      obj = Tokbit
      if pos in obj:
        print(" ")
        print(" Masuk ketoko Bibit »")
        print(" ")
        wkt()
        toko_bibit()

  if Game_end >= 100:
    print(" ")
    print(" \033[32mOsot bolosot aku hebat !\033[0m")
    print(" ")
    break