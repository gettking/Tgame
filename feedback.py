import os
from datetime import datetime

def feedback():
    os.system("clear")

    print("=== LAPOR BUG / SARAN ===\n")

    nama = input("Nama (opsional): ")
    tipe = input("Tipe (bug/saran/lainnya): ")
    isi = input("Isi laporan: ")

    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = f"""
[{waktu}]
Nama : {nama}
Tipe : {tipe}
Isi  : {isi}
-------------------------
"""

    with open("feedback.txt", "a") as f:
        f.write(data)

    print("\n✔ Laporan terkirim, terima kasih!")
    input("Enter untuk kembali...")
