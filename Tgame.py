import random
import string
import time
import os

#map_rumah
rumahx, rumahy = 5, 5
userx, usery = 2, 2
coinx, coiny = 0, 0
invx, invy = 4, 0
crafx, crafy = 0, 4
casx, casy = 4, 4
respawnC = {}
w_isi = 10
pintux, pintuy = 4, 2
pusing = 0
casE = 0



#map_kebun
kebunx, kebuny = 11, 5
userx1, usery1 = 1, 0
pintux1, pintuy1 = 0, 0
flagx1, flagy1 = 1, 0
pohon1= {
  (0, 4), (2, 4), (4, 4),
  (6, 4), (8, 4), (10, 4)
}
pohon2= {
  (1, 4), (3, 4), (5, 4),
  (7, 4), (9, 4)
}

respawn1 = {}
respawn2 = {}

w_tumbuh1 = 60
w_tumbuh2 = 60

k_lahan = {
  (10, 0), (9, 0), (8, 0),
  (10, 1), (9, 1), (8, 1),
  (10, 2), (9, 2), (8, 2)
}
pohon_tanam = set()
tanam = set()
respawnT = {}
wt_tanam = 20

ppasarx, ppasary = 10, 3


#map_pasar
pasarx, pasary = 21, 10
userxp, useryp = 1, 0
Tokbit = {
  (2, 2), (3, 2),
  (2, 3), (3, 3)
}

bpasarx, bpasary = 0, 0


#data_user
Hp = 100
tas = 0
gxc = 0
gcoins = 0
bibit = 0
exp = 0

#walls_rumah
walls = {
  (1, 1), (2, 1), (3, 1), #(3, 2),
  (3, 3), (2, 3), (1, 3)
}

#walls_kebun
wallsk = {
  (0, 1), (1, 1)
}

worldpos = "start"

def ldkb():
  
  for i in [
    " \033[32m▰▰▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱\033[0m",
    " \033[32m▰▰▰▰▰▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱\033[0m",
    " \033[32m▰▰▰▰▰▰▰▰▰▰▰▰▰▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱\033[0m",
    " \033[32m▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱\033[0m",
    " \033[32m▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱\033[0m",
    " \033[32m▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\033[0m"
    ]:
      print(f"\r{i}", end="", flush=True)
      time.sleep(0.5)

def ldcasfull():
  
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
    "\033[33mDaya sudah full !\033[0m"
    ]:
      print(f"\r{i}", end="", flush=True)
      time.sleep(0.3)

def ldcas():
  
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
    "\033[32mDaya terisi penuh ✓\033[0m"
    ]:
      print(f"\r{i}", end="", flush=True)
      time.sleep(0.3)

def ldMbrkgl():
  
  for i in ["◇", "◈", "◆", "◇", "◈", "◆", "◇", "◈", "◆", "◇", "◈", "◆",  "\033[31mSaldo G-coin kosong !\033[0m"]:
    print(f"\r{i}", end="", flush=True)
    time.sleep(0.2)

def ldMbrk():
  
  for i in ["◇", "◈", "◆", "◇", "◈", "◆", "◇", "◈", "◆", "◇", "◈", "◆",  " "]:
    print(f"\r{i}", end="", flush=True)
    time.sleep(0.2)

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

def wkt(delay=0.5):
  
  fase = ["🌑", "🌒", "🌓", "🌔", "🌕"]
  for bulan in fase:
    print(f"\r{bulan}", end="", flush=True)
    time.sleep(delay)
  print()
wkt()

#FUNGSI RUMAH
def d_rumah():

  print("┌─────────┐")
  print("│🏠\033[32m Rumah\033[0m │")
  print("└─────────┘")
  print("┌────────────────────────────┐")
  print(f"│🔋: {Hp:<5} 🎒: {tas:<5} Ⓖ: {gxc:<5}│")
  print(f"│🫘: {bibit:<5}  ✦: {exp:<5} ⓖ: {gcoins:<5}│")
  print("└────────────────────────────┘")
  
  print("│---------------------------------│")
  
  pos = (userx, usery)
  ob = (coinx, coiny)
  if pos == ob:
    print("│ [\033[33mBrangkas\033[0m] m untuk masuk »      │")
    
  pos = (userx, usery)
  ob = (crafx, crafy)
  if pos == ob:
    print("│ [\033[33mKerajinan\033[0m]                     │")
    
  pos = (userx, usery)
  ob = (pintux, pintuy)
  if pos == ob:
    print("│ Exit [\033[32mkebun\033[0m] m untuk pergi »    │")
    
  pos = (userx, usery)
  ob = (invx, invy)
  if pos == ob:
    print("│ [\033[33mPenyimpanan\033[0m]                   │")
    
  pos = (userx, usery)
  ob = (casx, casy)
  if pos == ob:
    print("│ [\033[33mEnergi\033[0m] m untuk mengisi »      │")
  
  print("│---------------------------------│")
  print(" ")
  
  for y in range(rumahy):
    ln = ""
    for x in range(rumahx):
        
      if (x, y) == (userx, usery):
        if casE > 0:
          ln += "⚡"
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
        ln += "🔋"
      elif (x, y) in respawnC:
        ln += "🪫"
      elif (x, y) == (pintux, pintuy):
        ln += "🚪"
      elif (x, y) in walls:
        ln += "🧱"
      else:
        ln += "⬜"
        
    print(ln)
    
  
#FUNGSI KEBUN
def d_kebun():
  
  print("┌─────────┐")
  print("│🏡\033[32m Kebun\033[0m │")
  print("└─────────┘")
  
  
  print("┌────────────────────────────┐")
  print(f"│🔋: {Hp:<5} 🎒: {tas:<5} Ⓖ: {gxc:<5}│")
  print(f"│🫘: {bibit:<5}  ✦: {exp:<5} ⓖ: {gcoins:<5}│")
  print("└────────────────────────────┘")
  
  print("|-----------------------------------|")
  
  pos = (userx1, usery1)
  ob = (pintux1, pintuy1)
  if pos == ob:
    print(" [Rumah] m untuk masuk «")
  
  pos = (userx1, usery1)
  ob = k_lahan
  if pos in ob:
    print(" [\033[32mArea lahan\033[0m]\n p untuk menanam.\n x untuk menebang. ")
    
  pos = (userx1, usery1)
  ob = pohon1
  if pos in ob:
    print(" Area Pohon t.1(0) 1 untuk menebang.")
  
  pos = (userx1, usery1)
  ob = pohon2
  if pos in ob:
    print(" Area Pohon t.2(0) 2 untuk menebang.")
  
  pos = (userx1, usery1)
  ob = (ppasarx, ppasary)
  if pos == ob:
    print(" » [Pasar] m untuk pergi kepasar.")
  
  
  print("|-----------------------------------|")
  
  for y in range(kebuny):
    ln = ""
    for x in range(kebunx):
      
      if (x, y) == (userx1, usery1):
        if pusing > 0:
          ln += "😵"
        else:
          ln += "😍"
        
      elif (x, y) == (pintux1, pintuy1):
        ln += "🚪"
      elif (x, y) == (flagx1, flagy1):
        ln += "🎏"
      elif (x, y) in wallsk:
        ln += "🧱"
      elif (x, y) in tanam:
        ln += "🌱"
      elif (x, y) in pohon_tanam:
        ln += "🌳"
      elif (x, y) in k_lahan:
        ln += "🟩"
        
      elif (x, y) in pohon1:
        ln += "🌳"
      elif (x, y) in pohon2:
        ln += "🌲"
      elif (x, y) in respawn1:
        ln += "🪵"
      elif (x, y) in respawn2:
        ln += "🪵"
      
      elif (x, y) == (ppasarx, ppasary):
        ln += "➡️"
      else:
        ln += "🟦"
    print(ln)
  
def d_pasar():
  
  print(">🛍< Pasar")
  print(f"♥️  =", Hp,"%  🎒 =", tas, " 🪙 =", gxc)
  print(f"♣  =", bibit)
  print(" ")
  
  for y in range(pasary):
    ln = ""
    for x in range(pasarx):
      if (x, y) == (userxp, useryp):
        ln += "😍"
      elif (x, y) == (bpasarx, bpasary):
        ln += "🔙"
      elif (x, y) in Tokbit:
        ln += "🍀"
      else:
        ln += "🔲"
    print(ln)


def coins():
  
  global gcoins, gxc
  rate_Gxc = 0.628
  
  while True:
    
    os.system("clear")
    
    print("▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️")
    print(f" » 1 G-coin =\033[32m {rate_Gxc}\033[0m Gxc")
    print("▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️")
    print(f" » G-Coin   = \033[32m{gcoins}\033[0m")
    print("▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️")
    print(" n =\033[31m Exit\033[0m ⇐")
    print(" ")
    
    cmd=input("Swap G-coin ke Gxc [y or n]: ")
    
    if cmd == "y":
  
      
      if gcoins <= 0:
          print(" ")
          ldMbrkgl()
          print(" ")
          print(" ")
          input(" ➥ Enter.")
          continue
      
      print(" ")
      ldMbrk()
      while True:
        
        os.system("clear")
        print("┌──────────────────┐")
        print("│x untuk kembali ⇐ │")
        print("└──────────────────┘")
        jswap=(input(" ➥ Masukkan jumlah or Max : "))
        
        #BACK
        if jswap == "x":
          print(" ")
          ldMbrk()
          break 
        
        if jswap == "max":
          sgxc = gcoins
          
        else:
          try:
            sgxc = float(jswap)
          
          except:
            print(" ")
            print("\033[31mInput salah !\033[0m")
            print(" ")
            input(" ➥ Enter.")
            continue
          
        if sgxc <= 0:
          print(" ")
          print("\033[31mAngka tidak boleh 0 atau minus!\033[0m")
          print(" ")
          input(" ➥ Enter.")
          continue
        
        elif sgxc > gcoins:
          print(" ")
          print("\033[31mjumlah G-coin kurang !\033[0m")
          print(" ")
          input(" ➥ Enter.")
          continue
        
        
        gcoins -= sgxc
        gxc += sgxc * rate_Gxc
        
        gcoins = round(gcoins, 3)
        gxc = round(gxc, 3)
        
        print(" ")
        ldSwp()
        print(" ")
        print(" ")
        print(f" Token Gxc = \033[33m{gxc}\033[0m")
        print(" ")
        input(" ➥ Enter.")
        continue
      
      
    elif cmd == "n":
      print(" ")
      print("membatalkan swap(\033[31mExit\033[0m) !")
      print(" ")
      ldMbrk()
      break
    
    else:
      print(" ")
      print("\033[31minput salah !\033[0m")
      print(" ")
      input(" ➥ Enter.")
          

def toko_bibit():
  
  global gxc, bibit, tas
  
  #harga_bibit_t.1
  t1_1 = 15
  t1_3 = 45
  t1_5 = 75
  
  while True:
    
    
    os.system("clear")
    
    print(f"Saldo Gxc =", gxc)
    print("tersedia:\n(1) Bibit pohon t.1\n(2) Coming Soon\n(x) keluar")
    print(" ")
  
    cmd=input("beli : ").lower()
    
    #testing
    if cmd == "x":
      break
  
    if cmd == "1" or cmd == "satu":
      print(f"Harga untuk 1 bibit =", t1_1)
      print("beli 1 (1)\nbeli 3 (3)\nbeli 5 (5)")
      ubeli=input("input kode sesuai pilihan :").lower()
      
      if ubeli == "1":
        if gxc >= t1_1:
          print("proses membeli item bibit »")
          wkt()
          bibit += 1
          tas += 2
          gxc -= t1_1
          gxc = round(gxc, 3)
          print("Sukses ✓")
          input("Tekan Enter...")
        else:
          print("proses membeli item bibit »")
          wkt()
          print("Token Gxc tidak cukup!")
          continue
        
      elif ubeli == "3":
        if gxc >= t1_3:
          print("proses membeli item bibit »")
          wkt()
          bibit += 3
          tas += 6
          gxc -= t1_3
          gxc = round(gxc, 3)
          print("Sukses ✓")
          input("Tekan Enter...")
        else:
          print("proses membeli item bibit »")
          wkt()
          print("Token Gxc tidak cukup!")
          continue
          
      elif ubeli == "5":
        if gxc >= t1_5:
          print("proses membeli item bibit »")
          wkt()
          bibit += 5
          tas += 10
          gxc -= t1_5
          gxc = round(gxc, 3)
          print("Sukses ✓")
          input("Tekan Enter...")
        else:
          print("proses membeli item bibit »")
          wkt()
          print("Token Gxc tidak cukup!")
          continue
          
      else:
        print("input kode salah!")
        input("Tekan Enter...")
          
  
while True:
  
  nowC = time.time()
  for posC in list(respawnC.keys()):
    if nowC >= respawnC[posC]:
      casx, casy = posC
      del respawnC[posC]
  
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
      
    if (userx, usery) in walls:
      userx, usery = oldx, oldy
      pusing = 3
    if pusing > 0:
      pusing -= 1
      
    if (userx, usery) == (casx, casy):
      casE = 2
      
    if casE > 0:
      casE -= 1
    
      
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
        ldMbrk()
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
      
    if pusing > 0:
      pusing -= 1
  
    #PART_menanam pohon t.1
    if cmd == "p":
      pos = (userx1, usery1)
      obj = k_lahan
      tm = tanam
      pt = pohon_tanam
      if pos in obj:
        if pos in tm or pos in pt:
          print(" ")
          print(" \033[33mSudah ada tanaman !\033[0m")
          print(" ")
          input(" ➥ Enter.")
        elif Hp >= 2:
          if bibit >= 1:
            print(" ")
            print(" mulai menanam.")
            print(" ")
            Hp -= 2
            wkt()
            bibit -= 1
            tas -= 2
            tanam.add((userx1, usery1))
            print(" \033[32mSukses menanam ✓\033[0m")
            print(" ")
            input(" ➥ Enter.")
            respawnT[userx1, usery1] = nowT + wt_tanam
          else:
            print(" ")
            print(" \033[31mBibit tidak ada!!!\033[0m")
            print(" ")
            input(" ➥ Enter.")
        else:
          print(" ")
          print(" ♥️ = 🔋")
          print(" ")
          input(" ➥ Enter.")
      else:
        print(" ")
        print(" \033[31mHanya bisa dilahan menanam!\033[0m")
        print(" ")
        input(" ➥ Enter.")
        
    #PART_menebang
    if cmd == "x":
      pos = (userx1, usery1)
      kbn = (kebunx, kebuny)
      tm = tanam
      pt = pohon_tanam
      if pos in tm:
        print(" ")
        print(" \033[33mPohon masih muda !\033[0m")
        print(" ")
        input(" ➥ Enter.")
      
      if pos in kbn:
        print(" ")
        print(" \033[33mHanya bisa dilahan menanam!\033[0m")
        
      elif pos in pt:
        if Hp >= 2:
          print(" ")
          print(" Mulai menebang.")
          print(" ")
          wkt()
          Hp -= 2
          pohon_tanam.remove(pos)
          gxc += 19
          gxc = round(gxc, 3)
          print(" Menebang sukses ✓")
          print(" ")
          input(" ➥ Enter.")
        else:
          print(" ")
          print(" ♥️ = 🔋")
          print(" ")
          input(" ➥ Enter.")
      else:
        print(" ")
        print(" Tidak ada objek tanaman!")
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
          print(" ")
          print(" Mulai menebang...")
          wkt()
          Hp -= 3
          gcoins += 7
          gcoins = round(gcoins, 3)
          pohon1.remove((userx1, usery1))
          respawn1[userx1, usery1] = now1 + w_tumbuh1
          print(" ")
          print(" \033[32mPohon sukses ditebang ✓\033[0m")
          print(" ")
          tas += 3
          input(" ➥ Enter.")
        else:
          print(" ")
          print(" ♥️ = 🔋")
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
          print(" ")
          print(" Mulai menebang...")
          wkt()
          Hp -= 3
          gcoins += 7
          gcoins = round(gcoins, 3)
          pohon2.remove((userx1, usery1))
          respawn2[userx1, usery1] = now2 + w_tumbuh2
          print(" ")
          print(" \033[32mPohon sukses ditebang ✓\033[0m")
          print(" ")
          tas += 3
          input(" ➥ Enter.")
        else:
          print(" ")
          print(" ♥️ = 🔋")
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
     
    if cmd == "m":
      pos = (userxp, useryp)
      obj = (bpasarx, bpasary)
      if pos == obj:
        print(" ")
        print(" « pergi kekebun")
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
        print(" \033[32mDidalam toko ✓\033[0m")
        print(" ")
        input(" ➥ Enter.")
        toko_bibit()
  