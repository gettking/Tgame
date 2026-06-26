import os
import time
from feedback import feedback

print()
print("Sakedap ya nyonyot aku ♥️")
print()
print("🌐 Memeriksa update...")
time.sleep(1)

hasil = os.popen("git pull").read()

if "Already up to date" in hasil:
    print("✅ Game sudah versi terbaru.")
elif "Updating" in hasil or "Fast-forward" in hasil:
    print("🎉 Update berhasil!")
elif "Could not resolve host" in hasil:
    print("📡 Tidak ada koneksi internet.")
else:
    print(hasil)

time.sleep(2)

# MENU setelah update
while True:
    print("\n=== GAME MENU ===")
    print("1. Mulai Game")
    print("2. Kirim Laporan / Saran")
    print("3. Keluar")

    pilih = input("\nPilih: ")

    if pilih == "1":
        os.system("python Tgame.py")
        break

    elif pilih == "2":
        feedback()

    elif pilih == "3":
        break
