#Install: pip install paho-mqtt
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

def _init_mp_module():
    import json as _json
    import threading as _threading
    import time as _time

    _BROKER  = "broker.emqx.io"
    _PORT    = 1883
    _PREFIX  = "tgame/v1"

    _state = {
        "client": None,
        "lock": _threading.Lock(),
        "nama": "P1",
        "room": "defaultroom",
        "pemain_lain": {},
        "terhubung": False,
        "game_over_received": False,
    }

    def _topik_saya():
        return f"{_PREFIX}/{_state['room']}/{_state['nama']}"

    def _topik_room_all():
        return f"{_PREFIX}/{_state['room']}/#"

    def _on_connect(client, userdata, flags, *args, **kwargs):
        rc = args[0] if args else 0
        if hasattr(rc, 'value'):
            rc = rc.value
        if rc == 0:
            _state["terhubung"] = True
            client.subscribe(_topik_room_all(), qos=0)
        else:
            _state["terhubung"] = False

    def _on_disconnect(client, userdata, *args, **kwargs):
        _state["terhubung"] = False

    def _on_message(client, userdata, msg):
        try:
            bagian = msg.topic.split("/")
            if len(bagian) < 4:
                return
            nama_pengirim = bagian[3]
            if nama_pengirim == _state["nama"]:
                return
            data = _json.loads(msg.payload.decode("utf-8"))
            with _state["lock"]:
                if data.get("game_over"):
                    _state["game_over_received"] = True
                _state["pemain_lain"][nama_pengirim] = {
                    "n": nama_pengirim,
                    "w": data.get("w", "Rumah"),
                    "x": data.get("x", 0),
                    "y": data.get("y", 0),
                    "game_end": data.get("game_end", 0),
                    "last": _time.time(),
                }
        except Exception:
            pass

    def sambung(room, nama):
        try:
            import paho.mqtt.client as mqtt
        except ImportError:
            return False
        _state["nama"]        = (nama or "P1").replace(" ","_").replace("/","_")
        _state["room"]        = (room or "room1").replace(" ","_").replace("/","_")
        _state["pemain_lain"] = {}
        _state["terhubung"]   = False
        try:
            try:
                from paho.mqtt.enums import CallbackAPIVersion
                cl = mqtt.Client(
                    callback_api_version=CallbackAPIVersion.VERSION1,
                    client_id=f"tgame_{_state['nama']}_{int(_time.time())}",
                )
            except (ImportError, AttributeError):
                cl = mqtt.Client(client_id=f"tgame_{_state['nama']}_{int(_time.time())}")
            cl.on_connect    = _on_connect
            cl.on_disconnect = _on_disconnect
            cl.on_message    = _on_message
            cl.connect(_BROKER, _PORT, keepalive=30)
            cl.loop_start()
            for _ in range(60):
                if _state["terhubung"]:
                    break
                _time.sleep(0.1)
            if _state["terhubung"]:
                _state["client"] = cl
                return True
            cl.loop_stop()
            return False
        except Exception:
            return False

    def terhubung():
        return _state["terhubung"] and _state["client"] is not None

    def kirim(state_lokal):
        if terhubung():
            try:
                payload = _json.dumps({
                    "w": state_lokal.get("world","Rumah"),
                    "x": state_lokal.get("x",0),
                    "y": state_lokal.get("y",0),
                    "game_end": state_lokal.get("game_end", 0),
                    "game_over": state_lokal.get("game_over", False),
                })
                _state["client"].publish(_topik_saya(), payload, qos=0, retain=False)
            except Exception:
                pass
        now = _time.time()
        with _state["lock"]:
            mati = [n for n,d in _state["pemain_lain"].items() if now-d.get("last",0)>15]
            for n in mati:
                del _state["pemain_lain"][n]
        return get_others()

    def cek_game_over():
        with _state["lock"]:
            return _state["game_over_received"]

    def get_scores():
        with _state["lock"]:
            return [{"n": d["n"], "game_end": d.get("game_end", 0)}
                    for d in _state["pemain_lain"].values()]

    def get_others():
        with _state["lock"]:
            return list(_state["pemain_lain"].values())

    def putus():
        _state["terhubung"] = False
        if _state["client"]:
            try:
                _state["client"].loop_stop()
                _state["client"].disconnect()
            except Exception:
                pass
            _state["client"] = None

    def nama():
        return _state["nama"]

    return sambung, terhubung, kirim, get_others, putus, nama, cek_game_over, get_scores

(_mp_mod.sambung, _mp_mod.terhubung, _mp_mod.kirim,
 _mp_mod.get_others, _mp_mod.putus, _mp_mod.nama,
 _mp_mod.cek_game_over, _mp_mod.get_scores) = _init_mp_module()
del _init_mp_module, _types
# ── akhir mp_client inline ────────────────────────────────────

Game_end = 0
bookx, booky = 3, 0
bit1cek = ""
bit2cek = ""
kayu0cek = ""
kayu1cek = ""
kayu2cek = ""
papan0cek = ""
papan1cek = ""
papan2cek = ""
kursi0cek = ""
kursi1cek = ""
kursi2cek = ""
tenggelam = 0
pancingx, pancingy = 3, 1
pancingan = 0

ikan = {
  "🐟 ⭐ ": 0,
  "🐟 ✨ ": 0,
  "🐠 🌟 ": 0,
  "🐠 💫 ": 0,
  "🐠 🎖️ ": 0
}

import random 
import string
import time
import os

_mp = _mp_mod
MP_AKTIF = True
NAMA_PEMAIN = "P1"
_pemain_lain = []   # [{n, w, x, y}, ...] — dari broker


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
papan0 = 0
papan1 = 0
papan2 = 0
kursi0 = 0
kursi1 = 0
kursi2 = 0

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
apelx, apely = 15, 2
cacingx, cacingy = 16, 8
cacing = 0
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
pinggir_kolam = {
    (19, 0), (18, 0), (17, 0), (16, 1),
    (16, 2), (16, 3), (16, 4), (16, 5),
    (18, 8), (19, 8), (20, 7), (20, 6),
    (20, 5), (20, 4), (20, 3), (17, 8)
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

kapak = 0
respawnA = {}
wt_muncul = 40

respawnK = {}
wt_munculk = 60

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

# ─── Helper MP ───────────────────────────────
def _pos_mp():
    if worldpos == "Rumah":
        return worldpos, userx, usery
    elif worldpos == "kebun":
        return worldpos, userx1, usery1
    else:
        return worldpos, userxp, useryp

def _sync_mp(game_over=False):
    global _pemain_lain
    if not MP_AKTIF or not _mp.terhubung():
        return
    try:
        w, x, y = _pos_mp()
        _pemain_lain = _mp.kirim({
            "world": w, "x": x, "y": y,
            "game_end": Game_end,
            "game_over": game_over,
        })
    except Exception:
        pass

def _dashboard():
    """Tampilkan leaderboard Game_end semua pemain"""
    if not MP_AKTIF or not _mp.terhubung():
        return
    scores = _mp.get_scores()
    if not scores:
        return
    print("┌─────────────────────────┐")
    print("│  📊 Progress Misi       │")
    myn = NAMA_PEMAIN[:8]
    print(f"│  💫 {myn:<8}: {Game_end:>3}/100   │")
    for s in scores:
        n = s.get("n","?")[:8]
        ge = s.get("game_end", 0)
        print(f"│  💫 {n:<8}: {ge:>3}/100   │")
    print("└─────────────────────────┘")
# ─────────────────────────────────────────────

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
  pos = (cacingx, cacingy)
  print("┌───────────────────────────────┐")
  print(f"│🍚: {Hp:<5} 🎒: {tas:<5} 🅶: {gxc:<8}│ 🪱 : {cacing} \033[33m{pos}\033[0m")
  print("└───────────────────────────────┘")
  print(f" ➥ \033[36mBuka tas & peyimpanan [i]\033[0m Exp : \033[32m{exp}\033[0m")

def kaptas(isi):
  return tas + isi <= 100
  
def isiTas():
    
  while True:
    os.system("clear")
    print(" ")
    print(f" ➧ Player exp   : \033[36m{exp}\033[0m")
    print(" ")
    infolvl()
    print(" ")
    print(" • Papan •")
    print(f" \033[36m[]\033[0m   : {papan0}")
    print(f" \033[32m[]]\033[0m  : {papan1}")
    print(f" \033[31m[]]]\033[0m : {papan2}")
    print(" ")
    print(" • Kursi •")
    print(f" \033[36m║╗\033[0m   : {kursi0}")
    print(f" \033[32m║╗╗\033[0m  : {kursi1}")
    print(f" \033[31m║╗╗╗\033[0m : {kursi2}")
    print(" ")
    print(f" • Gcoins    : \033[33m{gcoins}\033[0m")
    print(" ")
    print("🎒 :")
    print(" \033[36m➧ Barang yang ada ditas :\033[0m")
    print(" ")
    print(f" ➥ Kayu      : \033[36m{kayu}\033[0m")
    print(f" ➥ Kayu T.1  : \033[36m{kayuT1}\033[0m")
    print(f" ➥ Kayu T.2  : \033[36m{kayuT2}\033[0m")
    print(f" ➥ Bibit T.1 : \033[36m{bibit}\033[0m")
    print(f" ➥ Bibit T.2 : \033[36m{bibit2}\033[0m")
    print(" ")
    print("🧰 :")
    print(" \033[36m➧ Barang yang disimpan :\033[0m")
    print(" ")
    print(f" ➥ Bibit T.1   : \033[32m{box_penyimpanan.get('bibit', 0)}\033[0m")
    print(f" ➥ Bibit T.2   : \033[32m{box_penyimpanan.get('bibit2', 0)}\033[0m")
    print(f" ➥ Kayu T.1(0) : \033[32m{box_penyimpanan.get('kayu', 0)}\033[0m")
    print(f" ➥ Kayu T.1    : \033[32m{box_penyimpanan.get('kayuT1', 0)}\033[0m")
    print(f" ➥ Kayu T.2    : \033[32m{box_penyimpanan.get('kayuT2', 0)}\033[0m")
    print(f" ➥ Koin Gxc    : \033[32m{box_penyimpanan.get('gxc', 0)}\033[0m")
    print(" ")
    print(" ⇐ Kembali [x] : ")
    back = _getch()
    
    if back == "x":
      break
 
def infolvl():
  global lvl
  
  if exp >= 500:
    level = 5
    lvl += 1
  elif exp >= 400:
    level = 4
    lvl += 1
  elif exp >= 300:
    level = 3
    lvl += 1
  elif exp >= 200:
    level = 2
    lvl += 1
  elif exp >= 100:
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
    print("\033[31mPilih & masukkan jumlah barang untuk dibuang :\033[0m ")
    buang=_getch()
    
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
          info_kpatasyut1 = xkayuT1 * 1
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
          info_kaptasyut2 = xkayuT2 * 1
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
  print(f"│🏠\033[36m Rumah\033[0m │ ✛ : \033[32m{pos}\033[0m   𝐆𝐄 : {Game_end}   🪓 : {kapak}   🎣 : {pancingan}")
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
  print(" \033[36mHasil Memancing\033[0m » h untuk melihat")
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
      elif MP_AKTIF and any(
          p.get('w') == 'Rumah' and p.get('x') == x and p.get('y') == y
          for p in _pemain_lain):
        ln += "🥰"
          
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
  print(f"│🏡\033[33m Kebun\033[0m │ ✛ : \033[32m{pos}\033[0m   𝐆𝐄 : {Game_end}   🪓 : {kapak}   🎣 : {pancingan}")
  print("└─────────┘")
  infopemain()
  print("|----------------------------------------|")
  
  print(info)
  
  pos = (userx1, usery1)
  ob = (pancingx, pancingy)
  if pos == ob:
    print(" [\033[32mPancingan\033[0m] m untuk ambil »")
    
  pos = (userx1, usery1)
  ob = (cacingx, cacingy)
  if pos == ob:
    print(" \033[32mKamu menemukan cacing !\033[0m m untuk ambil »")
  
  pos = (userx1, usery1)
  ob = pinggir_kolam
  if pos in ob:
    print(" [\033[32mArea memancing\033[0m] m untuk mulai »")
  
  pos = (userx1, usery1)
  ob = kolam
  if pos in ob:
    print(" \033[31mKamu bisa tenggelam !\033[0m")
  
  pos = (userx1, usery1)
  ob = (kapakx, kapaky)
  if pos == ob:
    print(" [\033[32mKapak\033[0m] m untuk ambil »")
  
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
  print(" \033[36mHasil Memancing\033[0m » h untuk melihat")
  print(" ")
  
  for y in range(kebuny):
    ln = ""
    for x in range(kebunx):
      
      if (x, y) == (userx1, usery1):
        if pusing > 0:
          ln += "😵"
        elif tenggelam > 0:
          ln += "🫥"
        else:
          ln += "😍"
      elif MP_AKTIF and any(
          p.get('w') == 'kebun' and p.get('x') == x and p.get('y') == y
          for p in _pemain_lain):
        ln += "🥰"
        
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
      elif (x, y) in pinggir_kolam:
        ln += "🟧"
      elif (x, y) == (apelx, apely):
        ln += "🍎"
      elif (x, y) in flower2:
        ln += "🌷"
      elif (x, y) == (pancingx, pancingy):
        ln += "🎣"
      elif (x, y) == (cacingx, cacingy):
        ln += "🪱"
      else:
        ln += "🟩"
        
    print(ln)
  
def d_pasar():
  
  pos = (userxp, useryp)
  print("┌─────────┐")
  print(f"│🛍\033[33m Pasar\033[0m  │ ✛ : \033[32m{pos}\033[0m   𝐆𝐄 : {Game_end}   🪓 : {kapak}   🎣 : {pancingan}")
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
  print(" \033[36mHasil Memancing\033[0m » h untuk melihat")
  print(" ")
  
  for y in range(pasary):
    ln = ""
    for x in range(pasarx):
      
      if (x, y) == (userxp, useryp):
        if pusing > 0:
          ln += "😵"
        else:
          ln += "😍"
      elif MP_AKTIF and any(
          p.get('w') == 'pasar' and p.get('x') == x and p.get('y') == y
          for p in _pemain_lain):
        ln += "🥰"
          
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
    print(" ➥ Swap G-coin ke Gxc [y or n]: ")
    cmd= _getch()
    
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
        jswap=input(" ➥ Masukkan jumlah or Max : ").lower()
        
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
    print(" ➥ Pilih : ")
    cmd = _getch()
  
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
        print(" Input kode sesuai pilihan : ")
        ubeli=_getch()
      
        if ubeli == "1":
          if gxc >= t1_1:
            if tas + 2 <= 100:
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
            if tas + 6 <= 100:
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
            if tas + 10 <= 100:
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
        print(" Input kode sesuai pilihan : ")
        ubeli=_getch()
        
        if ubeli == "1":
          if lvl >= 2:
            if gxc >= t2_1:
              if tas + 3 <= 100:
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
          if lvl >= 3:
            if gxc >= t2_3:
              if tas + 9 <= 100:
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
          if lvl >= 5:
            if gxc >= t2_5:
              if tas + 15 <= 100:
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
    print(" Pilih : ")
    cmd=_getch()
    
    if cmd == "0":
      
      while True:
         #2 
        os.system("clear")
        print(" ")
        print(f" ➧ \033[36mBarang yang disimpan :\033[0m 🎒 = ", tas)
        print(" ")
        print(f" ➥ Bibit T.1   = \033[32m{box_penyimpanan.get('bibit', 0)}\033[0m")
        print(f" ➥ Bibit T.2   = \033[32m{box_penyimpanan.get('bibit2', 0)}\033[0m")
        print(f" ➥ Kayu T.1(0) = \033[32m{box_penyimpanan.get('kayu', 0)}\033[0m")
        print(f" ➥ Kayu T.1    = \033[32m{box_penyimpanan.get('kayuT1', 0)}\033[0m")
        print(f" ➥ Kayu T.2    = \033[32m{box_penyimpanan.get('kayuT2', 0)}\033[0m")
        print(f" ➥ Koin Gxc    = \033[32m{box_penyimpanan.get('gxc', 0)}\033[0m")
        print(" ")
        print(" ➥ Kembali »(k)")
        print(" ")
        print(" pilih : ")
        pilih=_getch()
        
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
        print(" Pilih : ")
        simpan= _getch()
        
        if simpan == "1":
            
          while True:
            
            os.system("clear")
            #4
            info_kaptasyut2 = kayuT2 * 1
            info_kaptasbit2 = bibit2 * 3
            info_kaptasbit = bibit * 2
            info_kaptasyu = kayu * 1
            info_kpatasyut1 = kayuT1 * 1
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
            print(" ➥ Pilih :  ")
            psimpan=_getch()
            
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
                if "bibit2" in box_penyimpanan:
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
              
              info_kpatasyut1 = kayuT1 * 1
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
              
              info_kaptasyut2 = kayuT2 * 1
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
        print(" Pilih : ")
        abarang=_getch()
        
        if abarang == "1":
          
          while True:
            
            os.system("clear")
            
            info_kaptasbit = 2
            info_kaptasbit2 = 3
            info_kaptasyu = 1
            info_kpatasyut1 = 1
            info_kaptasyut2 = 1
            
            jmlbit = box_penyimpanan.get('bibit', 0)
            jmlbit2 = box_penyimpanan.get('bibit2', 0)
            jmlyu = box_penyimpanan.get('kayu', 0)
            jmlyut1 = box_penyimpanan.get('kayuT1', 0)
            jmlyut2 = box_penyimpanan.get('kayuT2', 0)
            jmlgxc = box_penyimpanan.get('gxc', 0)
            
            kbibit = (jmlbit * info_kaptasbit)
            kbibit2 = (jmlbit2 * info_kaptasbit2)
            kkayu = (jmlyu * info_kaptasyu)
            kkayuT1 = (jmlyut1 * info_kpatasyut1)
            kkayuT2 = (jmlyut2 * info_kaptasyut2)
            
            total_slotTas = kbibit + kbibit2 + kkayu + kkayuT1 + kkayuT2

            if tas + total_slotTas <= 100:
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
            print(" Pilih : ")
            pabarang=_getch()
            
            if pabarang == "1":
              print(" ")
              
              while True:
                
                os.system("clear")
                
                info_kaptasbit = 2
                jmlbit = box_penyimpanan.get('bibit', 0)
                bbt = (jmlbit * info_kaptasbit)
                
                if tas + bbt <= 100:
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
                jmlbit2 = box_penyimpanan.get('bibit2', 0)
                bbt2 = (jmlbit2 * info_kaptasbit2)
                
                if tas + bbt2 <= 100:
                  if "bibit2" in box_penyimpanan:
                    print(" ")
                    print(" Mengambil item bibit T.2 »")
                    print(" ")
                    wkt()
                    box_penyimpanan["bibit2"] = 0
                    tas += jmlbit2 * info_kaptasbit2
                    bibit2 += jmlbit2
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
                jmlyu = box_penyimpanan.get('kayu', 0)
                ky = (jmlyu * info_kaptasyu)
                
                if tas + ky <= 100:
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
                
                info_kpatasyut1 = 1
                jmlyut1 = box_penyimpanan.get('kayuT1', 0)
                ky1 = (jmlyut1 * info_kpatasyut1)
                
                if tas + ky1 <= 100:
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
                
                info_kaptasyut2 = 1
                jmlyut2 = box_penyimpanan.get('kayuT2', 0)
                ky2 = (jmlyut2 * info_kaptasyut2)
                
                if tas + ky2 <= 100:
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
                
                jmlgxc = box_penyimpanan.get('gxc', 0)
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
        print(" ➥ Pilih : ")
        buang= _getch()
        
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
            print(" ➥ Pilih : ")
            pbuang=_getch()
            
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
    print(" Keluar [x] :")
    cmd = _getch()
    
    if cmd == "x":
      break
      
def kerajinan():
  global kayu, kayuT1, kayuT2, papan0, papan1, papan2, tas, exp
  
  while True:
    os.system("clear")
    
    print(" ")
    print(" \033[36mKerajinan :\033[0m")
    print(" ")
    print(" ➥ Buat papan  »(1)")
    print(" ➥ Buat kursi  »(2)")
    print(" ➥ Buat meja   »(3)")
    print(" ➥ Buat lemari »(4)")
    print(" ➥ Keluar      »[x]")
    print(" ")
    print(" Pilih : ")
    cmd=_getch()
    
    if cmd == "1":
      
      while True:
        os.system("clear")
        
        print(" ")
        print(" Pilih jenis papan : ")
        print(" ")
        print(" ➥ Papan Biasa \033[36m[]\033[0m    »(1)")
        print("    perlu ×2 Kayu T.1/2(0)")
        print(" ")
        print(" ➥ Papan T.1   \033[32m[]]\033[0m   »(2)")
        print("    perlu ×6 Kayu T.1")
        print(" ")
        print(" ➥ Papan T.2   \033[33m[]]]\033[0m  »(3)")
        print("    perlu ×12 kayu T.2")
        print(" ")
        print(" ➥ Kembali           »[x]")
        print(" ")
        print(" Pilih : ")
        papan=_getch()
        
        if papan == "1":
          if kayu >= 2:
            print(" ")
            print(" Proses membuat \033[36m[]\033[0m »")
            print(" ")
            tas -= 2
            kayu -= 2
            exp += 4
            papan0 += 1
            time.sleep(1.23)
            print(" ➥ \033[32mSukses ✓\033[0m")
            
          else:
            print(" ")
            print(" \033[31mKayu T.1/2(0) tidak ada !\033[0m")
            print(" ")
            time.sleep(0.345)
            
        elif papan == "2":
          if kayuT1 >= 6:
            print(" ")
            print(" Proses membuat \033[32m[]]\033[0m »")
            print(" ")
            tas -= 6
            kayuT1 -= 6
            exp += 5
            papan1 += 1
            time.sleep(1.23)
            print(" ➥ \033[32mSukses ✓\033[0m")
            
          else:
            print(" ")
            print(" \033[31mKayu T.1 tidak ada !\033[0m")
            print(" ")
            time.sleep(0.345)
        
        elif papan == "3":
          if kayuT2 >= 12:
            print(" ")
            print(" Proses membuat \033[33m[]]]\033[0m »")
            print(" ")
            tas -= 12
            kayuT2 -= 12
            exp += 6
            papan2 += 1
            time.sleep(1.23)
            print(" ➥ \033[32mSukses ✓\033[0m")
            
          else:
            print(" ")
            print(" \033[31mKayu T.2 tidak ada !\033[0m")
            print(" ")
            time.sleep(0.345)
        
        elif papan == "x":
          break
        
        else:
          print(" ")
          print(" \033[31mInput salah !\033[0m")
          print(" ")
          time.sleep(0.345)
    
    elif cmd == "2":
      
      while True:
          
        os.system("clear")
        
        print(" ")
        print(" Pilih jenis kursi : ")
        print(" ")
        print(" ➥ Kursi biasa \033[36m║╗\033[0m   »(1)")
        print("   Perlu 2x Papan biasa dan ×4 kayu T.1/2(0)")
        print(" ")
        print(" ➥ Kursi T.1   \033[32m║╗╗\033[0m  »(2)")
        print("   Perlu 2× Papan T.1 dan ×6 Kayu T.1") 
        print(" ")
        print(" ➥ Kursi T.2   \033[31m║╗╗╗\033[0m »(3)")
        print("   Perlu 2× Papan T.2 dan ×12 Kayu T.2")
        print(" ")
        print(" ➥ Kembali          »[x]")
        print(" ")
        print(" Pilih : ")
        kursi=_getch()
        
        if kursi == "1":
          if papan0 >= 2:
            if kayu >= 4:
              print(" ")
              print(" Proses membuat \033[36m║╗\033[0m »")
              print(" ")
              tas -= 4
              papan0 -= 2
              kayu -= 4
              exp += 10
              kursi0 += 1
              time.sleep(1.23)
              print(" ➥ \033[32mSukses ✓\033[0m")
            else:
              print(" ")
              print(" \033[31mKayu T.1/2(0) tidak ada !\033[0m")
              print(" ")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mPapan biasa tidak ada !\033[0m")
            print(" ")
            time.sleep(0.345)
            
        elif kursi == "2":
          if papan1 >= 2:
            if kayuT1 >= 6:
              print(" ")
              print(" Proses membuat \033[32m║╗╗\033[0m »")
              print(" ")
              tas -= 6
              papan1 -= 2
              kayuT1 -= 6
              exp += 15
              kursi1 += 15
              time.sleep(1.23)
              print(" ➥ \033[32mSukses ✓\033[0m")
            else:
              print(" ")
              print(" \033[31mKursi T.1 tidak ada !\033[0m")
              print(" ")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mPapan T.1 tidak ada !\033[0m")
            print(" ")
            time.sleep(0.345)
            
        elif kursi == "3":
          if papan2 >= 2:
            if kayuT2 >= 12:
              print(" ")
              print(" Proses membuat \033[31m║╗╗╗\033[0m")
              print(" ")
              tas -= 12
              papan2 -= 2
              kayuT2 -= 12
              exp += 20
              kursi2 += 1
              time.sleep(1.23)
              print(" ➥ \033[32mSukses ✓\033[0m")
            else:
              print(" ")
              print(" \033[31mKursi T.2 tidak ada !\033[0m")
              print(" ")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mPapan T.2 tidak ada !\033[0m")
            print(" ")
            time.sleep(0.345)
            
        elif kursi == "x":
          break
        
        else:
          print(" ")
          print(" \033[31mInput salah !\033[0m")
          print(" ")
          time.sleep(0.345)
              
            
    elif cmd == "x":
      print(" ")
      print(" Keluar »")
      print(" ")
      wkt()
      break
    
    else: 
      print(" ")
      print(" \033[31mInput salah !\033[0m")
      print(" ")
      time.sleep(0.345)
    
def memancing():
  global pancingan, cacing, ikan
  
  if pancingan > 0:
    if cacing >= 1:
      print(" Memulai memancing »")
      pancingan -= 1
      cacing -= 1
      jenis = random.choices(list(ikan.keys()),
      weights=[45, 35, 10, 7, 3])[0]
      ikan[jenis] += 1
      time.sleep(2.345)
      print(" ")
      print(f" \033[32mSukses! +1 {jenis}")
      print(" ")
      input(" ➥ Enter.")
    else:
      print(" ")
      print(" \033[31mCari cacing !\033[0m")
      time.sleep(0.345)
  else:
    print(" ")
    print(" \033[31mAmbil pancingan terlebih dahulu !\033[0m")
    print(" ")
    time.sleep(0.456)
    
def hasilpancing():
  global ikan
  
  while True:
      
    os.system("clear")
    
    print(" ")
    print(" \033[36m••• Hasil memancing •••\033[0m")
    print(" ")
    key1 = "🐟 ⭐ "
    key2 = "🐟 ✨ "
    key3 = "🐠 🌟 "
    key4 = "🐠 💫 "
    key5 = "🐠 🎖️ "
    print("➥ 🐟 ⭐ (ikan biasa) : ", ikan[key1])
    print(" ")
    print("➥ 🐟 ✨ (ikan besar) : ", ikan[key2])
    print(" ")
    print("➥ 🐠 🌟 (ikan super) : ", ikan[key3])
    print(" ")
    print("➥ 🐠 💫 (ikan kilau) : ", ikan[key4])
    print(" ")
    print("➥ 🐠 🎖  (ikan super) : ", ikan[key5])
    print(" ")
    print(" Keluar      [x]")
    print("")
    cmd = _getch()
    
    if cmd == "x":
      break
    
  
def book():
  
  os.system("python ibook.py")
  
def misi():
  global papan0, papan1, papan2, kursi0, kursi1, kursi2, Game_end, papan0cek, papan1cek, papan2cek, kursi0cek, kursi1cek, kursi2cek
  
  
  if papan0 >= 10 and papan0cek != "✓":
    papan0cek = "✓"
    Game_end += 15
  elif papan1 >= 15 and papan1cek != "✓":
    papan1cek = "✓"
    Game_end += 15
  elif papan2 >= 20 and papan2cek != "✓":
    papan2cek = "✓"
    Game_end += 20
  elif kursi0 >= 5 and kursi0cek != "✓":
    kursi0cek = "✓"
    Game_end += 15
  elif kursi1 >= 10 and kursi1cek != "✓":
    kursi1cek = "✓"
    Game_end += 15
  elif kursi2 >= 15 and kursi2cek != "✓":
    kursi2cek = "✓"
    Game_end += 20
  
  while True:
    os.system("clear")
    
    print(" ")
    print(f"» \033[36mPapan biasa\033[0m      ×10  [\033[32m{papan0cek}\033[0m]")
    print(" ")
    print(f"» \033[32mPapan T.1\033[0m        ×15  [\033[32m{papan1cek}\033[0m]")
    print(" ")
    print(f"» \033[31mPapan T.2\033[0m        x20  [\033[32m{papan2cek}\033[0m]")
    print(" ")
    print(f"» \033[36mKursi Biasa\033[0m      ×5   [\033[32m{kursi0cek}\033[0m]")
    print(" ")
    print(f"» \033[32mKursi T.1\033[0m        ×10  [\033[32m{kursi1cek}\033[0m]")
    print(" ")
    print(f"» \033[31mKursi T.2\033[0m        ×15  [\033[32m{kursi2cek}\033[0m]")
    print(" ")
    print(" Keluar [x] : ")
    cmd=_getch()
    
    if cmd == "x":
      break

while True:
    
  nowK = time.time()
  for posK in list(respawnK.keys()):
    if nowK >= respawnK[posK]:
      kapakx, kapaky = posK
      del respawnK[posK]
  
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
      # ── ONLINE MULTIPLAYER SETUP ────────────────
      if MP_AKTIF:
        print(" ")
        print("╔════════════════════════════════════╗")
        print("║  ONLINE MULTIPLAYER (via internet) ║")
        print("╚════════════════════════════════════╝")
        print(" Install: pip install paho-mqtt")
        print(" Kosongi semua untuk mode offline")
        print(" ")
        _nama_input = input(" ➞ Nama pemain kamu  : ").strip()
        NAMA_PEMAIN = _nama_input if _nama_input else "P1"
        _room_input = input(" ➞ Kode room (bebas) : ").strip()
        if _room_input:
          print(" ")
          print(" \033[36mMenghubungkan ke internet...\033[0m")
          if _mp.sambung(_room_input, NAMA_PEMAIN):
            print(f" \033[32mTerhubung! Halo {NAMA_PEMAIN} 👋\033[0m")
            print(f" \033[32mRoom: {_room_input}\033[0m")
          else:
            print(" \033[31mGagal. Pastikan: pip install paho-mqtt\033[0m")
            print(" Mode offline.")
          print(" ")
        else:
          print(" Mode offline (single player).")
          print(" ")
      # ──────────────────────────────────────────
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
    _dashboard()
    print(" [wasd]gerak  [m]aksi  [i]tas  [p]asar  [k]ebun")
    cmd = _getch()

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
    
    if cmd == "h":
      hasilpancing()
      
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
            time.sleep(0.567)
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
    _dashboard()
    print(" [wasd]gerak  [m]aksi  [i]tas  [0]info lahan")
    cmd = _getch()
    
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
      
    if (userx1, usery1) in kolam:
      tenggelam = 2
      if Hp > 0:
        Hp -= 1
      elif Hp == 0:
        print(" ")
        os.system("clear")
        print(" \033[33mKamu tenggelam !\033[0m")
        print("    \033[31mGame over\033[0m   ")
        break
    
    if tenggelam > 0:
      tenggelam -= 1
    
    if cmd == "m":
      pos = (userx1, usery1)
      obj = (apelx, apely)
      if Hp < 50:
        if pos == obj:
          print(" ")
          print(" Memakan apel »")
          print(" ")
          time.sleep(0.36)
          Hp += random.randint(20, 50)
          respawnA[apelx, apely] = nowA + wt_muncul
          apelx, apely = -1, -1
    
    if cmd == "m":
      pos = (userx1, usery1)
      obj = (kapakx, kapaky)
      if kapak < 2:
        if pos == obj:
          print(" ")
          print(" Mengambil kapak »")
          print(" ")
          kapak += 20
          time.sleep(0.36)
          respawnK[kapakx, kapaky] = nowK + wt_munculk
          kapakx, kapaky = -1, -1
    
    if cmd == "m":
      pos = (userx1, usery1)
      obj = (pancingx, pancingy)
      if pos == obj:
        if pancingan == 0:
          print(" ")
          print(" Mengambil pancingan »")
          pancingan += 1
          time.sleep(0.345)
        
    if cmd == "m":
      pos = (userx1, usery1)
      obj = (cacingx, cacingy)
      if pos == obj:
        if cacing <= 1:
          cacing += 2
          cacingx, cacingy = random.randint(0, kebunx -1), random.randint(0, kebuny -1)
    if cmd == "m":
      pos = (userx1, usery1)
      obj = pinggir_kolam
      if pos in obj:
        memancing()
    
    if cmd == "h":
      hasilpancing()
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
          time.sleep(0.234)
          
        elif pos in tm2 or pos in pt2:
          print(" ")
          print(" \033[31mSudah ada pohon T.2 yang ditanam disini !\033[0m")
          print(" ")
          time.sleep(0.3)
      
        elif Hp >= 2:
          if bibit >= 1:
            print(" ")
            print(" ➥ Mulai menanam bibit T.1")
            print(" ")
            exp += 2
            Hp -= 2
            time.sleep(1.5)
            bibit -= 1
            tas -= 2
            print(" ")
            tanam.add((userx1, usery1))
            print(" \033[32mSukses menanam bibit T.1 ✓\033[0m")
            print(" ")
            time.sleep(0.3)
            respawnT[userx1, usery1] = nowT + wt_tanam
          else:
            print(" ")
            print(" \033[31mBibit T.1 tidak ada!!!\033[0m")
            print(" ")
            time.sleep(0.3)
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          print(" ")
          time.sleep(0.3)
    
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
        time.sleep(0.3)
        
      elif pos in pt:
        if kapak >= 2:
          if Hp >= 2:
            if tas + 3 <= 100:
              print(" ")
              print(" ➥ Mulai menebang.")
              print(" ")
              time.sleep(1.5)
              print(" ")
              kapak -= 2
              kayuT1 += 3
              tas += 3
              exp += 5
              Hp -= 2
              pohon_tanam.remove(pos)
              gxc += 19
              gxc = round(gxc, 3)
              print(" \033[32mMenebang sukses ✓\033[0m")
              print(" ")
              time.sleep(0.3)
            else:
              print(" ")
              print(" \033[31mTas kamu penuh !\033[0m")
              print(" ")
              time.sleep(0.3)
          else:
            print(" ")
            print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
            print(" ")
            time.sleep(0.3)
        else:
          print(" ")
          print(" \033[31mDimana kapak mu !\033[0m")
          print(" ")
          time.sleep(0.3)
      
      elif pos in lhn:
        print(" ")
        print(" \033[33mTidak ada objek tanaman !\033[0m")
        print(" ")
        time.sleep(0.3)
    
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
          time.sleep(0.3)
        
        elif pos in tm1 or pos in pt1:
          print(" ")
          print(" \033[31mSudah ada pohon T.1 yang ditanam disini !\033[0m")
          print(" ")
          time.sleep(0.3)
        
        elif Hp >= 4:
          if bibit2 >= 1:
            print(" ")
            print(" ➥ Mulai menanam bibit T.2")
            print(" ")
            exp += 6
            Hp -= 4
            time.sleep(1.5)
            bibit2 -= 1
            tas -= 3
            print(" ")
            tanam2.add((userx1, usery1))
            print(" \033[32mSukses menanam bibit T.2 ✓\033[0m")
            print(" ")
            time.sleep(0.3)
            respawnT2[userx1, usery1] = nowT2 + wt_tanam2
          else:
            print(" ")
            print(" \033[31mBibit T.2 tidak ada!!!\033[0m")
            print(" ")
            time.sleep(0.3)
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          print(" ")
          time.sleep(0.3)
    
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
        time.sleep(0.3)
        
      elif pos in pt:
        if kapak >= 2:
          if Hp >= 4:
            if tas + 6 <= 100:
              print(" ")
              print(" ➥ Mulai menebang.")
              print(" ")
              time.sleep(1.5)
              print(" ")
              kapak -= 2
              kayuT2 += 6
              tas += 6
              exp += 6
              Hp -= 4
              pohon_tanam2.remove(pos)
              gxc += 25
              gxc = round(gxc, 3)
              print(" \033[32mMenebang sukses ✓\033[0m")
              print(" ")
              time.sleep(0.3)
            else:
              print(" ")
              print(" \033[31mTas kamu penuh !\033[0m")
              print(" ")
              time.sleep(0.3)
          else:
            print(" ")
            print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
            print(" ")
            time.sleep(0.3)
        else:
          print(" ")
          print(" \033[31mDimana kapak mu !\033[0m")
          print(" ")
          time.sleep(0.3)
          
      elif pos in lhn:
        print(" ")
        print(" \033[33mTidak ada objek tanaman !\033[0m")
        print(" ")
        time.sleep(0.3)
          
    
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
        if kapak >= 1:
          if Hp >= 3:
            if tas + 1 <= 100:
              print(" ")
              print(" ➥ Mulai menebang...")
              print(" ")
              kapak -= 1
              kayu += 1
              Hp -= 3
              gcoins += 7
              gcoins = round(gcoins, 3)
              pohon1.remove((userx1, usery1))
              respawn1[userx1, usery1] = now1 + w_tumbuh1
              ldtb()
              tas += 1
              exp += 2
              time.sleep(0.12)
            else:
              print(" ")
              print(" \033[31mTas kamu penuh !\033[0m")
              print(" ")
              time.sleep(0.3)
          else:
            print(" ")
            print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
            print(" ")
            time.sleep(0.3)
        else:
          print(" ")
          print(" \033[31mDimana kapak mu !\033[0m")
          print(" ")
          time.sleep(0.3)
      
    #PART_menebang pohon t.2(0) 
    if cmd == "2":
      pos = (userx1, usery1)
      obj = pohon2
      if pos in obj:
        if kapak >= 1:
          if Hp >= 3:
            if tas + 1 <= 100:
              print(" ")
              print(" ➥ Mulai menebang...")
              print(" ")
              kapak -= 1
              kayu += 1
              Hp -= 3
              gcoins += 7
              gcoins = round(gcoins, 3)
              pohon2.remove((userx1, usery1))
              respawn2[userx1, usery1] = now2 + w_tumbuh2
              ldtb()
              tas += 1
              exp += 2
              time.sleep(0.12)
            else:
              print(" ")
              print(" \033[31mTas kamu penuh !\033[0m")
              time.sleep(0.3)
          else:
            print(" ")
            print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
            print(" ")
            time.sleep(0.3)
        else:
          print(" ")
          print(" \033[31mDimana kapak mu !\033[0m")
          print(" ")
          time.sleep(0.3)
      
        
  #PASAR
  else:
    
    d_pasar()
    _dashboard()
    print(" [wasd]gerak  [m]aksi  [i]tas")
    cmd = _getch()
    
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
    
    if cmd == "h":
      hasilpancing()
     
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

  # ── SYNC MULTIPLAYER setiap akhir loop ────
  _sync_mp()
  # ──────────────────────────────────────────

  # Cek apakah pemain lain sudah menyelesaikan misi
  if MP_AKTIF and _mp.terhubung() and _mp.cek_game_over():
    os.system("clear")
    print(" ")
    print(" \033[31m╔══════════════════════════════════╗\033[0m")
    print(" \033[31m║  GAME OVER — Pemain lain menang! ║\033[0m")
    print(" \033[31m╚══════════════════════════════════╝\033[0m")
    print(" ")
    input(" ➥ Enter untuk keluar.")
    break

  if Game_end == 100:
    # Broadcast game over ke semua pemain di room
    _sync_mp(game_over=True)
    os.system("clear")
    print(" ")
    print(" \033[32m╔═══════════════════════════════╗\033[0m")
    print(" \033[32m║  🏆 KAMU MENANG! Misi selesai! ║\033[0m")
    print(" \033[32m╚═══════════════════════════════╝\033[0m")
    print(" ")
    print(" \033[32mOsot bolosot aku hebat!\033[0m")
    print(" ")
    input(" ➥ Enter untuk keluar.")
    break
