import random
import string
import time
import os

print("tetsting")
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
    
def wkt():
  for i in range(3, 0, -1):
    print(i)
    time.sleep(0.3)
    

def d_rumah():
  print(">🏠< Rumah")
  print(f"♥️  =", Hp,"%  🎒  =", tas, " 🪙 =", gxc)
  print(f"♣  =", bibit)
  print("|-----------------------------------|")
  
  pos = (userx, usery)
  ob = (coinx, coiny)
  if pos == ob:
    print(" [Brangkas] m untuk masuk »")
    
  pos = (userx, usery)
  ob = (crafx, crafy)
  if pos == ob:
    print(" [Kerajinan]")
    
  pos = (userx, usery)
  ob = (pintux, pintuy)
  if pos == ob:
    print(" Pintu keluar[kebun] m untuk pergi »")
    
  pos = (userx, usery)
  ob = (invx, invy)
  if pos == ob:
    print(" [Penyimpanan]")
    
  pos = (userx, usery)
  ob = (casx, casy)
  if pos == ob:
    print(" [Energi] m untuk mengisi »")
  
  print("|-----------------------------------|")
  
  for y in range(rumahy):
    ln = ""
    for x in range(rumahx):
        
        
      if (x, y) == (userx, usery):
        ln += "🔷"
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
    
  
  
    
def d_kebun():
  
  print(">🏡< Kebun")
  print(f"♥️  =", Hp,"%  🎒 =", tas, " 🪙 =", gxc)
  print(f"♣  =", bibit)
  print(" ")
  
  for y in range(kebuny):
    ln = ""
    for x in range(kebunx):
      if (x, y) == (userx1, usery1):
        ln += "🔷"
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
        ln += "🔷"
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
    
    print("▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️")
    print(f" » 1 G-coin =", rate_Gxc, "Gxc")
    print("▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️")
    print(f" » G-Coin =", gcoins)
    print("▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️")
    
    cmd=input("Swap G-coin ke Gxc [y or n]")
    
    if cmd == "y":
      
      if gcoins <= 0:
          print("Saldo G-coin kosong !")
          input("Tekan Enter...")
          continue
      
      while True:
        
        os.system("clear")
        
        jswap=(input("Masukkan jumlah or Max : "))
        #testing
        if jswap == "x":
          break 
        
        elif jswap == "max":
          sgxc = gcoins
          
        else:
          try:
            sgxc = float(jswap)
          
          except:
            print("Input salah !")
            input("Tekan Enter...")
            continue
          
        if sgxc <= 0:
          print("Angka tidak boleh 0 atau minus!")
          continue
        
        elif sgxc > gcoins:
          print("jumlah G-coin kurang !")
          continue
        break
      
      if jswap == "x":
        continue
      
      gcoins -= sgxc
      gxc += sgxc * rate_Gxc
      
      gcoins = round(gcoins, 3)
      gxc = round(gxc, 3)
      
      print(f"Swap G-coin sukses ✓ Token Gxc =", gxc)
      input("Tekan Enter...")
    
    elif cmd == "n":
      print("membatalkan swap !")
      break
    
    else:
      print("input salah !")
          

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
          print("proses membelei item bibit »")
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
  
  if worldpos == "start":
    #Random_Kode
    sandi = "".join(random.choices(string.ascii_letters + string.digits, k=4))
    
    print(f"Kode masuk :", sandi)
    print("Masukkan kode untuk memulai game.")
    kode=(input("Kode : "))
    
    if kode == sandi or kode == "y":
      print("mulai masuk »")
      wkt()
      worldpos = "Rumah"
      print("sukses ✓")
      input("Tekan Enter...")
    else:
      print("mulai masuk »")
      wkt()
      print("kode salah !")
      input("Tekan Enter...")
    
  
  elif worldpos == "Rumah":
    d_rumah()
    print(" ")
    cmd=input("perintah :").lower()
    
    oldx, oldy = userx, usery
    
    #testing
    if cmd == "p":
      worldpos = "pasar"
      
    if cmd == "u":
      worldpos = "start"
    
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
      
    if cmd == "m":
      pos = (userx, usery)
      obj = (pintux, pintuy)
      if (userx, usery) == (pintux, pintuy):
        print("Pergi menuju kebun »")
        input("Enter...")
        wkt()
        print("Kamu berada dikebun ✓")
        worldpos = "kebun"
      
    if cmd == "m":
      pos = (userx, usery)
      obj = (coinx, coiny)
      if pos == obj:
        print("membuka brankas!")
        input("Enter...")
        wkt()
        coins()

    if cmd == "m":
      pos = (userx, usery)
      obj = (casx, casy)
      if pos == obj:
        if Hp < 100:
            print("» Memulai mengisi daya «")
            wkt()
            Hp = 100
            
            if casx is not None and (userx, usery) == (casx, casy):
              casx, casy = None, None
              respawnC[userx, usery] = nowC + w_isi
              print("Sukses ✓")

        elif Hp == 100:
          print("Daya sepertinya penuh!")
          input("Tekan Enter...")
        
  
  elif worldpos == "kebun":
    
    d_kebun()
    print(" ")
    cmd=input("perintah :").lower()
    
    oldx, oldy = userx1, usery1
    
    if cmd == "w":
      usery1 -= 1
    elif cmd == "s":
      usery1 += 1
    elif cmd == "a":
      userx1 -= 1
    elif cmd == "d":
      userx1 += 1
      
    if cmd == "t":
      postn = (userx1, usery1)
      if postn in k_lahan:
        if postn in tanam or postn in pohon_tanam:
          print("Sudah ada tanaman !")
          input("Tekan Enter...")
          continue
          
        if Hp >= 2.5:
          if bibit >= 1:
            print("mulai menanam . . .")
            Hp -= 2.5
            wkt()
            bibit -= 1
            tas -= 2
            tanam.add((userx1, usery1))
            print("sukses menanam ✓")
            input("Tekan Enter...")
            respawnT[userx1, usery1] = nowT + wt_tanam
          else:
            print("Bibit tidak ada!!!")
            input("Tekan Enter...")
        else:
          print("♥️ = 🔋")
      else:
        print("Hanya bisa dilahan menanam!")
        input("Tekan Enter...")

    if cmd == "x":
      postb = (userx1, usery1)
      if postb in tanam:
        print("pohon terlalu muda untuk ditebang!")
      elif postb in pohon_tanam:
        if Hp >= 2.5:
          print("mulai menebang . . .")
          Hp -= 2.5
          wkt()
          pohon_tanam.remove(postb)
          gxc += 19
          gcoins = round(gcoins, 3)
          print("menebang sukses ✓")
          input("Tekan Enter...")
        else:
          print("♥️ = 🔋")
      else:
        print("Tidak ada objek tanaman!")
        input("Tekan Enter...")
    
    
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
      
    if (userx1, usery1) == (pintux1, pintuy1):
      print("Masuk ke dalam Rumah «")
      wkt()
      print("Kamu berada dirumah ✓")
      worldpos = "Rumah"
      
    if (userx1, usery1) == (ppasarx, ppasary):
      print("Berjalan menuju pasar »")
      wkt()
      print("Kamu berada dipasar ✓")
      input("Tekan Enter...")
      worldpos = "pasar"
      
    if (userx1, usery1) in pohon1:
      cmd=input("tebang pohon ? [y or n]").lower()
      if cmd == "y":
        if Hp >= 3.5:
          print("memulai menebang...")
          wkt()
          Hp -= 3.5
          gcoins += 7
          gcoins = round(gcoins, 3)
          pohon1.remove((userx1, usery1))
          respawn1[userx1, usery1] = now1 + w_tumbuh1
          print("sukses menebang!")
          input("Tekan Enter...")
        else:
          print("♥️ = 🔋")
        
      elif cmd == "n":
        print("membatalkan menebang...")
        input("Tekan Enter...")
        
    
    elif (userx1, usery1) in pohon2:
      cmd=input("tebang pohon ? [y or n]").lower()
      
      if cmd == "y":
        if Hp >= 3.5:
          print("memulai menebang...")
          wkt()
          Hp -= 3.5
          gcoins += 7
          gcoins = round(gcoins, 3)
          pohon2.remove((userx1, usery1))
          respawn2[userx1, usery1] = now2 + w_tumbuh2
          print("sukses menebang!")
        else:
          print("♥️ = 🔋")
      
      elif cmd == "n":
        print("membatalkan menebang...")
  
  else:
    d_pasar()
    print(" ")
    cmd=input("perintah :").lower()
    
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
      
    if (userxp, useryp) == (bpasarx, bpasary):
      print("« pergi kekebun")
      wkt()
      worldpos = "kebun"
      
    if (userxp, useryp) in Tokbit:
      print("Masuk ketoko Bibit »")
      wkt()
      print("Didalam toko ✓")
      input("Tekan Enter...")
      toko_bibit()
  