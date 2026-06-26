import os
import time

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

os.system("python Tgame.py")
