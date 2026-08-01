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
infoblue = ""

misi = {
    "cek.bibit1": "", "cek.buah.stoberi": "",
    "cek.bibit2": "", "cek.buah.melon": "",
    "cek.kayu0": "", "cek.buah.nanas": "",
    "cek.kayu1": "", "cek.buah.lemon": "",
    "cek.kayu2": "", "cek.buah.jeruk": "",
    "cek.bibit.stoberi": "", "cek.buah.anggur": "",
    "cek.bibit.melon": "", "cek.buah.apelmerah": "",
    "cek.bibit.nanas": "", "cek.buah.apelhijau": "",
    "cek.bibit.lemon": "", "cek.buah.pir": "",
    "cek.bibit.jeruk": "", "cek.buah.mangga": "",
    "cek.bibit.anggur": "", "cek.papan0": "",
    "cek.bibit.apelmerah": "", "cek.papan1": "",
    "cek.bibit.apelhijau": "", "cek.papan2": "",
    "cek.bibit.pir": "", "cek.kursi0": "",
    "cek.bibit.mangga": "", "cek.kursi1": "",
    "cek.kursi2": "", "cek.meja0": "",
    "cek.meja1": "", "cek.meja2": "", "cek.lemari0": "", "cek.lemari1": "", "cek.lemari2": "",
    "cek.ikanbiasa": "", "cek.ikanbesar": "",
    "cek.ikansuper": "", "cek.ikankilau": "",
    "cek.ikanjuara": ""
}
kapasitas_tas = {
    "kayu": 1,
    "kayuT1": 1,
    "kayuT2": 1,
    "bibit": 2,
    "bibit2": 3,
    "lobak": 3,
    "jamur": 3,
    "wortel": 3,
    "tomat": 3,
    "stoberi": 3,
    "jagung": 3,
    "cabai": 3,
    "terong": 3,
    "paprika": 3,
    "bawang_bombai": 3,
    "bawang_putih": 3,
    "melon": 3,
    "nanas": 3,
    "lemon": 3,
    "jeruk": 3,
    "anggur": 3,
    "apel_merah": 3,
    "apel_hijau": 3,
    "pir": 3,
    "mangga": 3,
    #buah
    "buah.stoberi": 1,
    "buah.melon": 1,
    "buah.nanas": 1,
    "buah.lemon": 1,
    "buah.jeruk": 1,
    "buah.anggur": 1,
    "buah.apelmerah": 1,
    "buah.apelhijau": 1,
    "buah.pir": 1,
    "buah.mangga": 1
}
bluebox = {
    "kayu": 0, "buah.stoberi": 0,
    "kayuT1": 0, "buah.melon": 0,
    "kayuT2": 0, "buah.nanas": 0,
    "bibit": 0, "buah.lemon": 0,
    "bibit2": 0, "buah.jeruk": 0,
    "b.stoberi": 0, "buah.anggur": 0,
    "b.melon": 0, "buah.apelmerah": 0,
    "b.nanas": 0, "buah.apelhijau": 0,
    "b.lemon": 0 , "buah.pir": 0,
    "b.jeruk": 0, "buah.mangga": 0,
    "b.anggur": 0,
    "b.apelmerah": 0,
    "b.apelhijau": 0,
    "b.pir": 0,
    "b.mangga": 0
}
kapasitas_box = {
    "kayu": 300, "buah.stoberi": 250,
    "kayuT1": 300, "buah.melon": 250,
    "kayuT2": 300, "buah.nanas": 250,
    "bibit": 200,  "buah.lemon": 250,
    "bibit2": 200, "buah.jeruk": 250,
    "b.stoberi": 200, "buah.anggur": 250,
    "b.melon": 200, "buah.apelmerah": 250,
    "b.nanas": 200, "buah.apelhijau": 250,
    "b.lemon": 200, "buah.pir": 250,
    "b.jeruk": 200, "buah.mangga": 250,
    "b.anggur": 200,
    "b.apelmerah": 200,
    "b.apelhijau": 200,
    "b.pir": 200,
    "b.mangga": 200
}
ambil_isi_bluebox = {
  "kayu": (2, 1), "buah.stoberi": (2, 1),
  "kayuT1": (5, 1), "buah.melon": (5, 1),
  "kayuT2": (8, 1), "buah.nanas": (8, 1),
  "bibit": (11, 1), "buah.lemon": (11, 1),
  "bibit2": (14, 1), "buah.jeruk": (14, 1),
  "b.stoberi": (2, 4), "buah.anggur": (2, 4),
  "b.melon": (5, 4), "buah.apelmerah": (5, 4),
  "b.nanas": (8, 4), "buah.apelhijau": (8, 4),
  "b.lemon": (11, 4), "buah.pir": (11, 4),
  "b.jeruk": (14, 4), "buah.mangga": (14, 4),
  "b.anggur": (2, 7),
  "b.apelmerah": (5, 7),
  "b.apelhijau": (8, 7),
  "b.pir": (11, 7),
  "b.mangga": (14, 7)
}

masuk_isi_bluebox = {
  "_bkayu": (1, 1), "buah.stoberi": (1, 1),
  "_bkayu1": (4, 1), "buah.melon": (4, 1),
  "_bkayu2": (7, 1), "buah.nanas": (7, 1),
  "_bbibit": (10, 1), "buah.lemon": (10, 1),
  "_bbibit2": (13, 1), "buah.jeruk": (13, 1),
  "_bstoberi": (1, 4), "buah.anggur": (1, 4),
  "_bmelon": (4, 4), "buah.apelmerah": (4, 4),
  "_bnanas": (7, 4), "buah.apelhijau": (7, 4),
  "_blemon": (10, 4), "buah.pir": (10, 4),
  "_bjeruk": (13, 4), "buah.mangga": (13, 4),
  "_banggur": (1, 7), 
  "_bapelmerah": (4, 7),
  "_bapelhijau": (7, 7),
  "_bpir": (10, 7),
  "_bmangga": (13, 7)
}

#harga_bibit_buah & sayur
harga_bibit_buah_sayur = {
  "lobak": 20,
  "jamur": 25,
  "wortel": 30,
  "tomat": 35,
  "stoberi": 40,
  "jagung": 45,
  "cabai": 50,
  "terong": 55,
  "paprika": 60,
  "bawang_bombai": 65,
  "bawang_putih": 70,
  "melon": 75,
  "nanas": 80,
  "lemon": 85,
  "jeruk": 90,
  "anggur": 95,
  "apel_merah": 100,
  "apel_hijau": 105,
  "pir": 110,
  "mangga": 120
}
#daftar buah & sayur
list_buah_sayur = {
  "lobak": 0,
  "jamur": 0,
  "wortel": 0,
  "tomat": 0,
  "stoberi": 0,
  "jagung": 0,
  "cabai": 0,
  "terong": 0,
  "paprika": 0,
  "bawang_bombai": 0,
  "bawang_putih": 0,
  "melon": 0,
  "nanas": 0,
  "lemon": 0,
  "jeruk": 0,
  "anggur": 0,
  "apel_merah": 0,
  "apel_hijau": 0,
  "pir": 0,
  "mangga": 0
}
#list_bibit_buah_sayur
list_bibit_buah_sayur = {
  "lobak": 0,
  "jamur": 0,
  "wortel": 0,
  "tomat": 0,
  "stoberi": 0,
  "jagung": 0,
  "cabai": 0,
  "terong": 0,
  "paprika": 0,
  "bawang_bombai": 0,
  "bawang_putih": 0,
  "melon": 0,
  "nanas": 0,
  "lemon": 0,
  "jeruk": 0,
  "anggur": 0,
  "apel_merah": 0,
  "apel_hijau": 0,
  "pir": 0,
  "mangga": 0
}

npcmebelx, npcmebely = 5, 3
Game_end = 0
bookx, booky = 3, 0

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
#map_portal
bluex, bluey = 17, 9
bluex1, bluey1 = 17, 9
userbx, userby = 0, 2
userbx1, userby1 = 0, 2
redb = {
    "x": 16, "x1": 16,
    "y": 0, "y1": 0
}
#$$
wallblue = {
    (0, 1), (0, 0), (1, 0), (2, 0), (3, 0),
    (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
    (9, 0), (3, 1), (6, 1), (9, 1), (10, 0),
    (11, 0), (12, 0), (13, 0), (14, 0), (15, 0),
    (15, 1), (12, 1), (0, 4), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),
    (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3), (15, 3), (15, 4), (12, 4), (6, 4), (9, 4), (3, 4), (0, 6), (1, 6), (2, 6), (3, 6),
    (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6),
    (10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (15, 6), (15, 7), (12, 7), (9, 7), (6, 7), (3, 7), (0, 7)
}
#map_rumah
pedang = {
    "pedang1": 0,
    "x1": 17,
    "y1": 6,
    "damage1": random.randint(15, 35),
    "hp1": 25,
    "reloadhp": 25,
    "status1": False
}

monster = {
    #kerajaanHitam
    "semut_hitam": {
        "damage": random.choices([6, 5, 4, 10], weights = [50, 30, 10, 10], k = 1)[0],
        "hp": 50,
        "x": 15,
        "y": 4,
        "status": False,
        "plester": 3,
        "reward_kunci1": 1,
        "exp": 50
        
    },
    "nyamuk_hitam" : {
        "damage": random.choices([8, 7, 6, 12], weights = [50, 30, 10, 10], k = 1)[0],
        "hp": 100,
        "x": 0,
        "y": 17,
        "status": False,
        "plester": 3,
        "reward_kunci1": 1,
        "exp": 50
    },
    "laba2_hitam": {
        "damage": random.choices([20, 19, 18, 24], weights = [50, 30, 10, 10], k = 1)[0],
        "hp": 200,
        "x": 19,
        "y": 21,
        "status": False,
        "plester": 3,
        "reward_kunci1": 1,
        "exp": 50
    },
    "lalat_anomali": {
        "damage": random.choices([40, 39, 38, 44], weights = [50, 30, 10, 10], k = 1)[0],
        "hp": 400,
        "x": 8,
        "y": 23,
        "status": False,
        "plester": 5,
        "reward_kunci1": 1,
        "exp": 50
    },
    #BOSS kerajaan hitam
    "2face": {
        "damage": random.choices([70, 69, 68, 74], weights = [50, 30, 10, 10], k = 1)[0],
        "hp": 999,
        "x": 10,
        "y": 14,
        "status": False,
        "plester": 10,
        "reward_pil1": 1,
        "exp": 200
    }
}

rw_rbt = {
    "plester": 0,
    
    "kunci1": 0,
    "pil1": 0
}

wl_rbt = {
    (11, 14)
}
pa = {
    
    "semut_hitam": (13, 11),
    "nyamuk_hitam": (14, 15),
    "laba2_hitam": (14, 18)
    
}
kunci_rbt = {
    
    "kunci1": {
         "x": 12,
         "y": 14
    },
    "need1": 4,
    "status1": False
}

blue = {
    "world": "Rumah",
    "x": 16,
    "y": 3,
    "Status": False
}

ruang_bawah_tanah = {
    "ruangx1": 20,
    "ruangy1": 25,
    "userx1": 19,
    "usery1": 0
}

batas_rbt = {
    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
    (5, 0), (6, 0), (7, 0), (8, 0), (9, 0),
    (10, 0), (11, 0), (12, 0),
    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
    (5, 1), (6, 1), (7, 1), (8, 1), (9, 1),
    (10, 1), (11, 1), (12, 1),
    (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
    (5, 2), (6, 2), (7, 2), (8, 2), (9, 2),
    (10, 2), (11, 2), (12, 2),
    (0, 3), (1, 3), (2, 3), (3, 3), (4, 3),
    (5, 3), (6, 3), (7, 3), (8, 3), (9, 3),
    (10, 3), (11, 3), (12, 3),
    (0, 4), (1, 4), (2, 4), (3, 4), (4, 4),
    (5, 4), (6, 4), (7, 4), (8, 4), (9, 4),
    (10, 4), (11, 4), (12, 4),
    (0, 5), (1, 5), (2, 5), (3, 5), (4, 5),
    (5, 5), (6, 5), (7, 5), (8, 5), (9, 5),
    (10, 5), (11, 5), (12, 5),
    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6),
    (5, 6), (6, 6), (7, 6), (8, 6), (9, 6),
    (10, 6), (11, 6), (12, 6),
    (15, 7), (16, 7), (17, 7), (18, 7), (19, 7),
    (15, 12), (15, 11), (15, 10), (15, 9), (15, 8),
    (16, 12), (16, 11), (16, 10), (16, 9), (16, 8),
    (0, 10), (1, 10), (2, 10), (3, 10), (4, 10),
    (5, 10), (6, 10), (7, 10), (8, 10), (9, 10),
    (10, 10), (11, 10), (12, 10),
    (0, 9), (1, 9), (2, 9), (3, 9), (4, 9),
    (5, 9), (6, 9), (7, 9), (8, 9), (9, 9),
    (10, 9), (11, 9), (12, 9),
    (0, 8), (1, 8), (2, 8), (3, 8), (4, 8),
    (5, 8), (6, 8), (7, 8), (8, 8), (9, 8),
    (10, 8), (11, 8), (12, 8),
    (0, 7), (1, 7), (2, 7), (3, 7), (4, 7),
    (5, 7), (6, 7), (7, 7), (8, 7), (9, 7),
    (10, 7), (11, 7), (12, 7),
    (15, 16), (15, 17), (15, 18), (15, 19),
    (15, 20), (15, 21),
    (16, 16), (16, 17), (16, 18), (16, 19),
    (16, 20), (16, 21), (17, 16), (18, 16),
    (18, 17), (18, 18), (18, 19), (18, 20),
    (17, 22), (18, 22), (19, 22),
    (17, 23), (18, 23), (19, 23),
    (17, 24), (18, 24), (19, 24), (16, 22),
    (16, 23), (16, 24), (0, 11),
    (1, 11), (2, 11),
    (3, 11), (4, 11), (5, 11), (6, 11),
    (0, 12), (1, 12), (2, 12),
    (3, 12), (4, 12), (5, 12), (6, 12),
    (0, 13), (1, 13), (2, 13),
    (3, 13), (4, 13), (5, 13), (6, 13),
    (0, 14), (1, 14), (2, 14),
    (3, 14), (4, 14), (5, 14), (6, 14),
    (0, 15), (1, 15), (2, 15),
    (3, 15), (4, 15), (5, 15), (6, 15),
    (0, 16), (1, 16), (2, 16),
    (3, 16), (4, 16), (5, 16), (6, 16),
    (1, 18), (2, 18), (3, 18), (4, 18), (5, 18),
    (6, 18), (7, 18), (8, 18), (9, 18), (10, 18),
    (11, 18), (12, 18), (13, 18),
    (1, 19), (2, 19), (3, 19), (4, 19), (5, 19),
    (6, 19), (7, 19), (8, 19), (9, 19), (10, 19),
    (11, 19), (12, 19), (13, 19),
    (1, 20), (2, 20), (3, 20), (4, 20), (5, 20),
    (6, 20), (7, 20), (8, 20), (9, 20), (10, 20),
    (11, 20), (12, 20), (13, 20),
    (1, 21), (2, 21), (3, 21), (4, 21), (5, 21),
    (6, 21), (7, 21), (8, 21), (9, 21), (10, 21),
    (11, 21), (12, 21), (13, 21),
    (1, 22), (2, 22), (3, 22), (4, 22), (5, 22),
    (6, 22), (7, 22), (8, 22), (9, 22), (10, 22),
    (11, 22), (12, 22), (13, 22), (1, 23),
    (1, 24), (2, 24), (3, 24), (4, 24), (5, 24),
    (6, 24), (7, 24), (8, 24), (9, 24), (10, 24),
    (11, 24), (12, 24), (13, 24),
    (16, 15), (17, 15), (18, 15), (17, 14),
    (18, 14), (18, 9), (18, 10), (18, 11),
    (18, 12), (18, 13), (14, 13), (14, 14),
    (15, 13), (8, 12), (9, 12), (10, 12),
    (11, 12), (12, 12),(8, 16), (9, 16),
    (10, 16), (11, 16), (12, 16), (8, 13),
    (8, 14), (8, 15), (12, 13), (12, 15),
    (18, 0), (18, 1), (18, 2), (18, 3), (18, 4),
    (18, 5), (16, 1), (16, 2), (16, 3), (16, 4),
    (16, 5), (16, 6), (14, 1), (15, 1), (13, 3),
    (14, 3), (14, 5), (15, 5), (14, 6), (15, 6),
    (13, 8), (13, 9), (14, 11), (14, 12),
    (13, 16), (14, 16), (15, 22), (15, 23)
    
}

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
meja0 = 0
meja1 = 0
meja2 = 0
lemari0 = 0
lemari1 = 0
lemari2 = 0

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

tanam_bibit_buah = {
    #stoberi
    "tanam.bibit.stoberi": set(),
    "panen.buah.stoberi": set(),
    "respawn.tanam.stoberi": {},
    "waktu.tanam.stoberi": 35,
    #melon
    "tanam.bibit.melon": set(),
    "panen.buah.melon": set(),
    "respawn.tanam.melon": {},
    "waktu.tanam.melon": 35,
    #nanas
    "tanam.bibit.nanas": set(),
    "panen.buah.nanas": set(),
    "respawn.tanam.nanas": {},
    "waktu.tanam.nanas": 35,
    #lemon
    "tanam.bibit.lemon": set(),
    "panen.buah.lemon": set(),
    "respawn.tanam.lemon": {},
    "waktu.tanam.lemon": 35,
    #jeruk
    "tanam.bibit.jeruk": set(),
    "panen.buah.jeruk": set(),
    "respawn.tanam.jeruk": {},
    "waktu.tanam.jeruk": 35,
    #anggur
    "tanam.bibit.anggur": set(),
    "panen.buah.anggur": set(),
    "respawn.tanam.anggur": {},
    "waktu.tanam.anggur": 40,
    #apel merah
    "tanam.bibit.apelmerah": set(),
    "panen.buah.apelmerah": set(),
    "respawn.tanam.apelmerah": {},
    "waktu.tanam.apelmerah": 40,
    #apel hijau
    "tanam.bibit.apelhijau": set(),
    "panen.buah.apelhijau": set(),
    "respawn.tanam.apelhijau": {},
    "waktu.tanam.apelhijau": 40,
    #pir
    "tanam.bibit.pir": set(),
    "panen.buah.pir": set(),
    "respawn.tanam.pir": {},
    "waktu.tanam.pir": 40,
    #mangga
    "tanam.bibit.mangga": set(),
    "panen.buah.mangga": set(),
    "respawn.tanam.mangga": {},
    "waktu.tanam.mangga": 40
}

ppasarx, ppasary = 20, 9

#map_pasar
pasarx, pasary = 21, 10
userxp, useryp = 1, 0
lantaip = {
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
    (0, 7), (0, 8), (0, 9), (1, 9), (2, 9), (3, 9),
    (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9),
    (10, 9), (11, 9), (12, 9), (13, 9), (14, 9),
    (15, 9), (16, 9), (17, 9), (18, 9), (19, 9),
    (20, 9), (20, 8), (20, 7), (20, 6), (20, 5),
    (20, 4), (20, 3), (20, 2), (20, 1), (20, 0),
    (19, 0), (14, 0), (13, 0), (12, 0), (7, 0),
    (6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0),
    (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
    (7, 4), (9, 4), (10, 4), (11, 4), (12, 4),
    (13, 4), (14, 4), (16, 4), (17, 4), (18, 4),
    (19, 4)
}
Tk = {
    (15, 8)
}
tik1 = {
    (17, 6)
}
tik2 = {
    (18, 6)
}
tip1 = {
    (15, 6)
}
tip2 = {
    (16, 6)
}
figurikan = {
    (15, 7), (16, 7), (17, 7), (18, 7)
}
pancuranikan = {
    (16, 8), (17, 8), (18, 8)
}
karpetpasar = {
    (8, 4), (15, 4), (8, 9), (15, 9)
}
Tokbit = {
  (15, 3)
}
ataptokbit = {
    (17, 1), (18, 1)
}
depantokbit={
    (16, 3), (17, 3), (18, 3)
}
jendela_tokbit = {
    (15, 2)
}

tp = {
    (15, 1)
}
kp = {
    (16, 1)
}
b1p = {
    (16, 2)
}
b2p = {
    (17, 2)
}
b3p = {
    (18, 2)
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
  (19, 3), (19, 2), (19, 1), (15, 0), (16, 0),
  (17, 0), (18, 0), (14, 1), (14, 2), (14, 3),
  (14, 6), (14, 7), (14, 8), (15, 5), (16, 5),
  (17, 5), (18, 5), (19, 6), (19, 7), (19, 8),
  (12, 3), (12, 2), (12, 1), (8, 0), (9, 0),
  (10, 0), (11, 0), (7, 1), (7, 2), (7, 3),
  (7, 8), (7, 7), (7, 6), (8, 5), (9, 5), (10, 5),
  (11, 5), (12, 6), (12, 7), (12, 8)
}

worldpos = "start"
asal_world = None

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
  
  print("┌─────────────────────────────────────────┐")
  print(f"│🍚: {Hp:<5} 🎒: {tas:<5} 🅶: {gxc:<7} g: {gcoins:<7}│")
  print("└─────────────────────────────────────────┘")
  infolvl()
  print(" ➥ \033[36mBuka tas & penyimpanan\033[0m [\033[32mi\033[0m]")
  print(f" ➥ \033[36mHasil Memancing\033[0m [\033[32mh\033[0m]")
  print(f" ➥ \033[34mBluebox\033[0m [\033[32ml\033[0m]")

  
def isiTas():
    
  while True:
    os.system("clear")
    print(" ")
    print(" ")
    print(" ")
    print(" • Papan •   • Kursi •   • Meja •     • Lemari •")
    print(f" \033[36m[]\033[0m   : {papan0}    \033[36m║╗\033[0m   : {kursi0}    \033[36m╔═╗\033[0m   : {meja0}    \033[36m╠╣\033[0m   : {lemari0}")
    print(f" \033[32m[]]\033[0m  : {papan1}    \033[32m║╗╗\033[0m  : {kursi1}    \033[32m╔═╗╗\033[0m  : {meja1}    \033[32m╠╣\033[0m   : {lemari1}")
    print(f" \033[31m[]]]\033[0m : {papan2}    \033[31m║╗╗╗\033[0m : {kursi2}    \033[31m╔═╗╗╗\033[0m : {meja2}    \033[31m╠╣\033[0m   : {lemari2}")
    print(" ")
    print("🎒 Next[\033[32mt\033[0m] untuk lihat barang lainnya.")
    print(" \033[36m➧ Barang yang ada ditas :\033[0m")
    print(" ")
    print(f" ➥ Kayu      : \033[36m{kayu}\033[0m")
    print(f" ➥ Kayu T.1  : \033[36m{kayuT1}\033[0m")
    print(f" ➥ Kayu T.2  : \033[36m{kayuT2}\033[0m")
    print(f" ➥ Bibit T.1 : \033[36m{bibit}\033[0m")
    print(f" ➥ Bibit T.2 : \033[36m{bibit2}\033[0m")
    print(" ")
    print("🧰")
    print(" \033[36m➧ Barang yang disimpan :\033[0m")
    print(" ")
    print(f" ➥ Bibit T.1   : \033[32m{box_penyimpanan.get('bibit', 0)}\033[0m")
    print(f" ➥ Bibit T.2   : \033[32m{box_penyimpanan.get('bibit2', 0)}\033[0m")
    print(f" ➥ Kayu T.1(0) : \033[32m{box_penyimpanan.get('kayu', 0)}\033[0m")
    print(f" ➥ Kayu T.1    : \033[32m{box_penyimpanan.get('kayuT1', 0)}\033[0m")
    print(f" ➥ Kayu T.2    : \033[32m{box_penyimpanan.get('kayuT2', 0)}\033[0m")
    print(f" ➥ Koin Gxc    : \033[32m{box_penyimpanan.get('gxc', 0)}\033[0m")
    print(" ")
    print(" ⇐ Kembali [\033[32mx\033[0m] Tas.Next[\033[32mt\033[0m] penyimpanan.Next[\033[31mp\033[0m]")
    cmd = _getch()
    
    if cmd == "x":
      break
    
    elif cmd == "t":
      
      while True:
        os.system("clear")
        
        print(" ")
        print("🎒 Next[\033[32mn\033[0m] untuk lihat barang lainnya.")
        print(" \033[36m➧ Barang yang ada ditas :\033[0m")
        print(" ")
        print(f" ➥ Bibit stoberi    : \033[36m{list_bibit_buah_sayur["stoberi"]}\033[0m")
        print(f" ➥ Bibit Melon      : \033[36m{list_bibit_buah_sayur["melon"]}\033[0m")
        print(f" ➥ Bibit nanas      : \033[36m{list_bibit_buah_sayur["nanas"]}\033[0m")
        print(f" ➥ Bibit lemon      : \033[36m{list_bibit_buah_sayur["lemon"]}\033[0m")
        print(f" ➥ Bibit jeruk      : \033[36m{list_bibit_buah_sayur["jeruk"]}\033[0m")
        print(f" ➥ Bibit anggur     : \033[36m{list_bibit_buah_sayur["anggur"]}\033[0m")
        print(f" ➥ B.Apel merah     : \033[36m{list_bibit_buah_sayur["apel_merah"]}\033[0m")
        print(f" ➥ B.Apel hijau     : \033[36m{list_bibit_buah_sayur["apel_hijau"]}\033[0m")
        print(f" ➥ Bibit pir        : \033[36m{list_bibit_buah_sayur["pir"]}\033[0m")
        print(f" ➥ Bibit mangga     : \033[36m{list_bibit_buah_sayur["mangga"]}\033[0m")
        print(" ")
        print(" ⇐ Kembali [\033[32mx\033[0m] ")
        cmd = _getch()
        
        if cmd == "x":
          break
        
        elif cmd == "n":
          ob = list_buah_sayur
          while True:
            os.system("clear")
            
            print(" ")
            print("🎒 Next[\033[31mn\033[0m] untuk lihat barang lainnya.")
            print(" \033[36m➧ Barang yang ada ditas :\033[0m")
            print(" ")
            print(f" ➥ Buah stoberi    :  \033[32m{ob["stoberi"]}\033[0m")
            print(f" ➥ Buah melon      :  \033[32m{ob["melon"]}\033[0m")
            print(f" ➥ Buah nanas      :  \033[32m{ob["nanas"]}\033[0m")
            print(f" ➥ Buah lemon      :  \033[32m{ob["lemon"]}\033[0m")
            print(f" ➥ Buah jeruk      :  \033[32m{ob["jeruk"]}\033[0m")
            print(f" ➥ Buah anggur     :  \033[32m{ob["anggur"]}\033[0m")
            print(f" ➥ Buah apel merah :  \033[32m{ob["apel_merah"]}\033[0m")
            print(f" ➥ Buah apel hijau :  \033[32m{ob["apel_hijau"]}\033[0m")
            print(f" ➥ Buah pir        :  \033[32m{ob["pir"]}\033[0m")
            print(f" ➥ Buah mangga     :  \033[32m{ob["mangga"]}\033[0m")
            print(" ")
            print(" ⇐ Kembali [\033[32mx\033[0m] ")
            cmd = _getch()
            
            if cmd == "x":
              break
        
 
def infolvl():
  global lvl, exp, pedang
  
  if exp >= 12345:
    level = 20
    exp += 1
  elif exp >= 9876:
    level = 19
    lvl += 1
  elif exp >= 8910:
    level = 18
    lvl += 1
  elif exp >= 7891:
    level = 17
    lvl += 1
  elif exp >= 6789:
    level = 16
    lvl += 1
  elif exp >= 5678:
    level = 15
    lvl += 1
  elif exp >= 4567:
    level = 14
    lvl += 1
  elif exp >= 3456:
    level = 13
    lvl += 1
  elif exp >= 2345:
    level = 12
    lvl += 1
  elif exp >= 1234:
    level = 11
    lvl += 1
  elif exp >= 1000:
    level = 10
    lvl += 1
  elif exp >= 900:
    level = 9
    lvl += 1
  elif exp >= 800:
    level = 8
    lvl += 1
  elif exp >= 700:
    level = 7
    lvl += 1
  elif exp >= 600:
    level = 6
    lvl += 1
  elif exp >= 500:
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
  print(f" ➧ \033[32mLevel\033[0m : \033[36m{level}\033[0m  ➧ \033[32mExp\033[0m : \033[36m{exp}\033[0m  🗡️ : \033[32m{pedang["pedang1"]}\033[0m")

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
  
  korblue = (blue["x"], blue["y"])
  
  pos= (userx, usery)
  posc = (cacingx, cacingy)
  print("┌─────────┐")
  print(f"│🏠\033[36m Rumah\033[0m │ ✛ : \033[32m{pos}\033[0m {infoblue:<3} \033[34m{korblue}\033[0m") 
  print("└─────────┘")
  print(f"𝐆𝐄 : {Game_end}    🪓 : {kapak}   🎣 : {pancingan}   🪱 : {cacing} \033[33m{posc}\033[0m")
  infopemain()
  print("│----------------------------------------│")
  
  #infopusing:p
  print(info)
  
  pos = (userx, usery)
  ob = (tanggax, tanggay)
  if pos == ob:
    print(" [\033[32mRuang bawah tanah\033[0m] m untuk masuk »")
    
  pos = (userx, usery)
  ob = (blue["x"], blue["y"])
  if pos == ob:
    print(" [\033[34mBlue-Box\033[0m] m untuk masuk »")
    
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
      elif (x, y) == (blue["x"], blue["y"]):
        if worldpos == blue["world"] and not blue["Status"]:
          ln += "🟦"
        else:
          ln += "🟩"
      else:
        ln += "🟩"
        
    print(ln)
    
  
#FUNGSI KEBUN
def d_kebun():
 
  korblue = (blue["x"], blue["y"])
  
  pos = (userx1, usery1)
  posc = (cacingx, cacingy)
  print("┌─────────┐")
  print(f"│🏡\033[33m Kebun\033[0m │ ✛ : \033[32m{pos}\033[0m {infoblue:<3} \033[34m{korblue}\033[0m")
  print("└─────────┘")
  print(f"𝐆𝐄 : {Game_end}    🪓 : {kapak}   🎣 : {pancingan}   🪱 : {cacing} \033[33m{posc}\033[0m")
  infopemain()
  print("|----------------------------------------|")
  
  print(info)
  
  pos = (userx1, usery1)
  ob = (blue["x"], blue["y"])
  if pos == ob:
    print(" [\033[34mBlue-Box\033[0m] m untuk masuk »")
    
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
    print(" [\033[32mArea lahan\033[0m] info [k]")
    
  pos = (userx1, usery1)
  ob = pohon1
  if pos in ob:
    print(" Area Pohon \033[32mt.1\033[0m(0) m untuk menebang.")
  
  pos = (userx1, usery1)
  ob = pohon2
  if pos in ob:
    print(" Area Pohon \033[32mt.2\033[0m(0) m untuk menebang.")
  
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
      elif (x, y) in tanam_bibit_buah["tanam.bibit.stoberi"]:
        ln += "🌱"
      elif (x, y) in tanam_bibit_buah["panen.buah.stoberi"]:
        ln += "🍓"
      elif (x, y) in tanam_bibit_buah["tanam.bibit.melon"]:
        ln += "🌱"
      elif (x, y) in tanam_bibit_buah["panen.buah.melon"]:
        ln += "🍈"
      elif (x, y) in tanam_bibit_buah["tanam.bibit.nanas"]:
        ln += "🌱"
      elif (x, y) in tanam_bibit_buah["panen.buah.nanas"]:
        ln += "🍍"
      elif (x, y) in tanam_bibit_buah["tanam.bibit.lemon"]:
        ln += "🌱"
      elif (x, y) in tanam_bibit_buah["panen.buah.lemon"]:
        ln += "🍋"
      elif (x, y) in tanam_bibit_buah["tanam.bibit.jeruk"]:
        ln += "🌱"
      elif (x, y) in tanam_bibit_buah["panen.buah.jeruk"]:
        ln += "🍊"
      elif (x, y) in tanam_bibit_buah["tanam.bibit.anggur"]:
        ln += "🌱"
      elif (x, y) in tanam_bibit_buah["panen.buah.anggur"]:
        ln += "🍇"
      elif (x, y) in tanam_bibit_buah["tanam.bibit.apelmerah"]:
        ln += "🌱"
      elif (x, y) in tanam_bibit_buah["panen.buah.apelmerah"]:
        ln += "🍎"
      elif (x, y) in tanam_bibit_buah["tanam.bibit.apelhijau"]:
        ln += "🌱"
      elif (x, y) in tanam_bibit_buah["panen.buah.apelhijau"]:
        ln += "🍏"
      elif (x, y) in tanam_bibit_buah["tanam.bibit.pir"]:
        ln += "🌱"
      elif (x, y) in tanam_bibit_buah["panen.buah.pir"]:
        ln += "🍐"
      elif (x, y) in tanam_bibit_buah["tanam.bibit.mangga"]:
        ln += "🌱"
      elif (x, y) in tanam_bibit_buah["panen.buah.mangga"]:
        ln += "🥭"
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
      elif (x, y) == (blue["x"], blue["y"]):
        if worldpos == blue["world"] and not blue["Status"]:
          ln += "🟦"
        else:
          ln += "🟩"
      else:
        ln += "🟩"
        
    print(ln)
  
def d_pasar():
  
  korblue = (blue["x"], blue["y"])
  
  pos = (userxp, useryp)
  posc = (cacingx, cacingy)
  print("┌─────────┐")
  print(f"│🛍\033[33m Pasar\033[0m  │ ✛ : \033[32m{pos}\033[0m {infoblue:<3} \033[34m{korblue}\033[0m")
  print("└─────────┘")
  print(f"𝐆𝐄 : {Game_end}    🪓 : {kapak}   🎣 : {pancingan}   🪱 : {cacing} \033[33m{posc}\033[0m")
  infopemain()
  print("|----------------------------------------|")
  
  print(info)
  
  pos = (userxp, useryp)
  ob = (blue["x"], blue["y"])
  if pos == ob:
    print(" [\033[34mBlue-Box\033[0m] m untuk masuk »")
  
  pos = (userxp, useryp)
  ob = Tk
  if pos in ob:
    print(" [\033[32mToko Jual/beli ikan\033[0m] m untuk masuk »")
  
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
  
  pos = (userxp, useryp)
  ob = (npcmebelx, npcmebely)
  if pos == ob:
    print("[\033[32mPembeli mebel\033[0m] m untuk transaksi »")
    
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
      elif MP_AKTIF and any(
          p.get('w') == 'pasar' and p.get('x') == x and p.get('y') == y
          for p in _pemain_lain):
        ln += "🥰"
          
      elif (x, y) == (bpasarx, bpasary):
        ln += "🏡"
      elif (x, y) in Tokbit:
        ln += "🍀"
      elif (x, y) in wallp:
        ln += "🧱"
      elif (x, y) in tp:
        ln += "🆃🅾"
      elif (x, y) in kp:
        ln += "🅺🅾"
      elif (x, y) in b1p:
        ln += "🅱🅸"
      elif (x, y) in b2p:
        ln += "🅱🅸"
      elif (x, y) in b3p:
        ln += "🆃!"
      elif (x, y) in jendela_tokbit:
        ln += "🪟"
      elif (x, y) in depantokbit:
        ln += "🎍"
      elif (x, y) in ataptokbit:
        ln += "💈"
      elif (x, y) in karpetpasar:
        ln += "🔳"
      elif (x, y) in tip1:
        ln += "\033[32m🆃🅾\033[0m"
      elif (x, y) in tip2:
        ln += "\033[32m🅺🅾\033[0m"
      elif (x, y) in figurikan:
        ln += "🐟"
      elif (x, y) in pancuranikan:
        ln += "⛲"
      elif (x, y) in tik1:
        ln += "\033[34m🅸🅺\033[0m"
      elif (x, y) in tik2:
        ln += "\033[34m🅰🅽\033[0m"
      elif (x, y) in Tk:
        ln += "🎏"
      elif (x, y) in lantaip:
        ln += "⬜"
      elif (x, y) == (npcmebelx, npcmebely):
        ln += "🥸"
      elif (x, y) == (blue["x"], blue["y"]):
        if worldpos == blue["world"] and not blue["Status"]:
          ln += "🟦"
        else:
          ln += "🟩"
      else:
        ln += "🟩"
        
    print(ln)


def coins():
  
  global gcoins, gxc, exp
  rate_Gxc = 1
  
  while True:
    
    
    os.system("clear")
    
    print("▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️")
    print(f" » 1 G-coin =\033[32m {rate_Gxc}\033[0m Gxc")
    print("▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️")
    print(f" » G-Coin   : \033[32m{gcoins}\033[0m")
    print("▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️ ▫️")
    print(f" » Koin Gxc : \033[32m{gxc}\033[0m")
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
        
        
        gcoins = round(gcoins, 1)
        gxc = round(gxc, 1)
        
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
  
  global gxc, bibit, tas, exp, lvl, bibit2, kapasitas_tas, list_buah_sayur, harga_bibit_buah_sayur, list_bibit_buah_sayur
  
  ob = list_bibit_buah_sayur
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
    print(" Tersedia :")
    print(" ➥ Bibit pohon T.1 »(1)")
    print(" ➥ Bibit pohon T.2 »(2)")
    print(" ➥ Bibit buah      »(3)")
    print(" ➥ Bibit sayur     »(4)")
    print(" ➥ Keluar          »[x]")
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
              time.sleep(0.345)
            else:
              print(" ")
              print(" \033[31mTas kamu penuh !\033[0m")
              print(" ")
              time.sleep(0.345)
          else:
            print(" ")
            print(" ➥ Proses membeli item bibit T.1 »")
            print(" ")
            wkt()
            print(" ")
            print(" ")
            print(" \033[31mToken Gxc tidak cukup !\033[0m")
            print(" ")
            time.sleep(0.345)
        
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
              time.sleep(0.345)
            else:
              print(" ")
              print(" \033[31mTas kamu penuh !\033[0m")
              print(" ")
              time.sleep(0.345)
          else:
            print(" ")
            print(" ➥ Proses membeli item bibit  T.1 »")
            print(" ")
            wkt()
            print(" ")
            print(" ")
            print(" \033[31mToken Gxc tidak cukup !\033[0m")
            print(" ")
            time.sleep(0.345)
          
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
              time.sleep(0.345)
            else:
              print(" ")
              print(" \033[31mTas kamu penuh !\033[0m")
              print(" ")
              time.sleep(0.345)
          else:
            print(" ")
            print(" ➥ Proses membeli item bibit T.1 »")
            print(" ")
            wkt()
            print(" ")
            print(" ")
            print(" \033[31mToken Gxc tidak cukup !\033[0m")
            print(" ")
            time.sleep(0.345)
        
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
          time.sleep(0.345)
    
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
                time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mTas kamu penuh !\033[0m")
                print(" ")
                time.sleep(0.345)
            else:
              print(" ")
              print(" ➥ Proses membeli item bibit T.2 »")
              print(" ")
              wkt()
              print(" ")
              print(" ")
              print(" \033[31mToken Gxc tidak cukup !\033[0m")
              print(" ")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mlevel kamu belum memadai !\033[0m")
            print(" ")
            time.sleep(0.345)
          
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
                time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mTas kamu penuh !\033[0m")
                print(" ")
                time.sleep(0.345)
            else:
              print(" ")
              print(" ➥ Proses membeli item bibit T.2 »")
              print(" ")
              wkt()
              print(" ")
              print(" ")
              print(" \033[31mToken Gxc tidak cukup !\033[0m")
              print(" ")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mlevel kamu belum memadai !\033[0m")
            print(" ")
            time.sleep(0.345)
          
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
                time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mTas kamu penuh !\033[0m")
                print(" ")
                time.sleep(0.345)
            else:
              print(" ")
              print(" ➥ Proses membeli item bibit T.2 »")
              print(" ")
              wkt()
              print(" ")
              print(" ")
              print(" \033[31mToken Gxc tidak cukup !\033[0m")
              print(" ")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mlevel kamu belum memadai !\033[0m")
            print(" ")
            time.sleep(0.345)
        
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
          time.sleep(0.345)
    
    elif cmd == "3":
      print(" ")
      wkt()
      
      while True:
        os.system("clear")
        
        print(" ")
        print(" Tersedia bibit buah :")
        print(" ")
        print(f" ➥ Stoberi    »(1)  \033[32m{ob["stoberi"]}\033[0m")
        print(f" ➥ Melon      »(2)  \033[32m{ob["melon"]}\033[0m")
        print(f" ➥ Nanas      »(3)  \033[32m{ob["nanas"]}\033[0m")
        print(f" ➥ Lemon      »(4)  \033[32m{ob["lemon"]}\033[0m")
        print(f" ➥ Jeruk      »(5)  \033[32m{ob["jeruk"]}\033[0m")
        print(f" ➥ Anggur     »(6)  \033[32m{ob["anggur"]}\033[0m")
        print(f" ➥ Apel merah »(7)  \033[32m{ob["apel_merah"]}\033[0m")
        print(f" ➥ Apel hijau »(8)  \033[32m{ob["apel_hijau"]}\033[0m")
        print(f" ➥ Pir        »(9)  \033[32m{ob["pir"]}\033[0m")
        print(f" ➥ Mangga     »(0)  \033[32m{ob["mangga"]}\033[0m")
        print(" ➥ Kembali    »[x]")
        print(" ")
        print(" Pilih bibit buah :")
        pbuah = _getch()
        
        if pbuah == "1":
          print(" ")
          wkt()
          
          while True:
            os.system("clear")
            
            print(" ")
            print(" \033[32mbibit stoberi\033[0m :")
            print(" ")
            print(" ➥ Beli 1 bibit »(1)")
            print(" ➥ Beli 3 bibit »(2)")
            print(" ➥ Beli 5 bibit »(3)")
            print(" ➥ Kembali      »[x]")
            print(" ")
            print(" Pilih : ")
            pstoberi = _getch()
            
            if pstoberi == "1":
              gabung = kapasitas_tas["stoberi"] * 1
              if gxc >= harga_bibit_buah_sayur["stoberi"] * 1:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 1 bibit stoberi »")
                  gxc -= harga_bibit_buah_sayur["stoberi"] * 1
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["stoberi"] * 1
                  list_bibit_buah_sayur["stoberi"] += 1
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif pstoberi == "2":
              gabung = kapasitas_tas["stoberi"] * 3
              if gxc >= harga_bibit_buah_sayur["stoberi"] * 3:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 3 bibit stoberi »")
                  gxc -= harga_bibit_buah_sayur["stoberi"] * 3
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["stoberi"] * 3
                  list_bibit_buah_sayur["stoberi"] += 3
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif pstoberi == "3":
              gabung = kapasitas_tas["stoberi"] * 5
              if gxc >= harga_bibit_buah_sayur["stoberi"] * 5:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 5 bibit stoberi »")
                  gxc -= harga_bibit_buah_sayur["stoberi"] * 5
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["stoberi"] * 5
                  list_bibit_buah_sayur["stoberi"] += 5
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif pstoberi == "x":
              print(" ")
              print(" Kembali »")
              time.sleep(0.345)
              break
            
            else:
              print(" ")
              print(" \033[31mInput salah !\033[0m")
              time.sleep(0.345)
        
        elif pbuah == "2":
          print(" ")
          wkt()
          
          while True:
            os.system("clear")
            
            print(" ")
            print(" \033[32mbibit melon\033[0m :")
            print(" ")
            print(" ➥ Beli 1 bibit »(1)")
            print(" ➥ Beli 3 bibit »(2)")
            print(" ➥ Beli 5 bibit »(3)")
            print(" ➥ Kembali      »[x]")
            print(" ")
            print(" Pilih : ")
            pmelon = _getch()
            
            if pmelon == "1":
              gabung = kapasitas_tas["melon"] * 1
              if gxc >= harga_bibit_buah_sayur["melon"] * 1:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 1 bibit melon »")
                  gxc -= harga_bibit_buah_sayur["melon"] * 1
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["melon"] * 1
                  list_bibit_buah_sayur["melon"] += 1
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif pmelon == "2":
              gabung = kapasitas_tas["melon"] * 3
              if gxc >= harga_bibit_buah_sayur["melon"] * 3:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 3 bibit melon »")
                  gxc -= harga_bibit_buah_sayur["melon"] * 3
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["melon"] * 3
                  list_bibit_buah_sayur["melon"] += 3
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif pmelon == "3":
              gabung = kapasitas_tas["melon"] * 5
              if gxc >= harga_bibit_buah_sayur["melon"] * 5:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 5 bibit melon »")
                  gxc -= harga_bibit_buah_sayur["melon"] * 5
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["melon"] * 5
                  list_bibit_buah_sayur["melon"] += 5
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif pmelon == "x":
              print(" ")
              print(" Kembali »")
              time.sleep(0.345)
              break
            
            else:
              print(" ")
              print(" \033[31mInput salah !\033[0m")
              time.sleep(0.345)
              
        elif pbuah == "3":
          print(" ")
          wkt()
          
          while True:
            os.system("clear")
            
            print(" ")
            print(" \033[32mbibit nanas\033[0m :")
            print(" ")
            print(" ➥ Beli 1 bibit »(1)")
            print(" ➥ Beli 3 bibit »(2)")
            print(" ➥ Beli 5 bibit »(3)")
            print(" ➥ Kembali      »[x]")
            print(" ")
            print(" Pilih : ")
            pnanas = _getch()
            
            if pnanas == "1":
              gabung = kapasitas_tas["nanas"] * 1
              if gxc >= harga_bibit_buah_sayur["nanas"] * 1:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 1 bibit nanas »")
                  gxc -= harga_bibit_buah_sayur["nanas"] * 1
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["nanas"] * 1
                  list_bibit_buah_sayur["nanas"] += 1
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif pnanas == "2":
              gabung = kapasitas_tas["nanas"] * 3
              if gxc >= harga_bibit_buah_sayur["nanas"] * 3:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 3 bibit nanas »")
                  gxc -= harga_bibit_buah_sayur["nanas"] * 3
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["nanas"] * 3
                  list_bibit_buah_sayur["nanas"] += 3
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif pnanas == "3":
              gabung = kapasitas_tas["nanas"] * 5
              if gxc >= harga_bibit_buah_sayur["nanas"] * 5:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 5 bibit nanas »")
                  gxc -= harga_bibit_buah_sayur["nanas"] * 5
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["nanas"] * 5
                  list_bibit_buah_sayur["nanas"] += 5
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif pnanas == "x":
              print(" ")
              print(" Kembali »")
              time.sleep(0.345)
              break
            
            else:
              print(" ")
              print(" \033[31mInput salah !\033[0m")
              time.sleep(0.345) 
        
        elif pbuah == "4":
          print(" ")
          wkt()
          
          while True:
            os.system("clear")
            
            print(" ")
            print(" \033[32mbibit lemon\033[0m :")
            print(" ")
            print(" ➥ Beli 1 bibit »(1)")
            print(" ➥ Beli 3 bibit »(2)")
            print(" ➥ Beli 5 bibit »(3)")
            print(" ➥ Kembali      »[x]")
            print(" ")
            print(" Pilih : ")
            plemon = _getch()
            
            if plemon == "1":
              gabung = kapasitas_tas["lemon"] * 1
              if gxc >= harga_bibit_buah_sayur["lemon"] * 1:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 1 bibit lemon »")
                  gxc -= harga_bibit_buah_sayur["lemon"] * 1
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["lemon"] * 1
                  list_bibit_buah_sayur["lemon"] += 1
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif plemon == "2":
              gabung = kapasitas_tas["lemon"] * 3
              if gxc >= harga_bibit_buah_sayur["lemon"] * 3:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 3 bibit lemon »")
                  gxc -= harga_bibit_buah_sayur["lemon"] * 3
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["lemon"] * 3
                  list_bibit_buah_sayur["lemon"] += 3
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif plemon == "3":
              gabung = kapasitas_tas["lemon"] * 5
              if gxc >= harga_bibit_buah_sayur["lemon"] * 5:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 5 bibit lemon »")
                  gxc -= harga_bibit_buah_sayur["lemon"] * 5
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["lemon"] * 5
                  list_bibit_buah_sayur["lemon"] += 5
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif plemon == "x":
              print(" ")
              print(" Kembali »")
              time.sleep(0.345)
              break
            
            else:
              print(" ")
              print(" \033[31mInput salah !\033[0m")
              time.sleep(0.345)
        
        elif pbuah == "5":
          print(" ")
          wkt()
          
          while True:
            os.system("clear")
            
            print(" ")
            print(" \033[32mbibit jeruk\033[0m :")
            print(" ")
            print(" ➥ Beli 1 bibit »(1)")
            print(" ➥ Beli 3 bibit »(2)")
            print(" ➥ Beli 5 bibit »(3)")
            print(" ➥ Kembali      »[x]")
            print(" ")
            print(" Pilih : ")
            pjeruk = _getch()
            
            if pjeruk == "1":
              gabung = kapasitas_tas["jeruk"] * 1
              if gxc >= harga_bibit_buah_sayur["jeruk"] * 1:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 1 bibit jeruk »")
                  gxc -= harga_bibit_buah_sayur["jeruk"] * 1
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["jeruk"] * 1
                  list_bibit_buah_sayur["jeruk"] += 1
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif pjeruk == "2":
              gabung = kapasitas_tas["jeruk"] * 3
              if gxc >= harga_bibit_buah_sayur["jeruk"] * 3:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 3 bibit jeruk »")
                  gxc -= harga_bibit_buah_sayur["jeruk"] * 3
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["jeruk"] * 3
                  list_bibit_buah_sayur["jeruk"] += 3
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif pjeruk == "3":
              gabung = kapasitas_tas["jeruk"] * 5
              if gxc >= harga_bibit_buah_sayur["jeruk"] * 5:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 5 bibit jeruk »")
                  gxc -= harga_bibit_buah_sayur["jeruk"] * 5
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["jeruk"] * 5
                  list_bibit_buah_sayur["jeruk"] += 5
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif pjeruk == "x":
              print(" ")
              print(" Kembali »")
              time.sleep(0.345)
              break
            
            else:
              print(" ")
              print(" \033[31mInput salah !\033[0m")
              time.sleep(0.345)
        
        elif pbuah == "6":
          print(" ")
          wkt()
          
          while True:
            os.system("clear")
            
            print(" ")
            print(" \033[32mbibit anggur\033[0m :")
            print(" ")
            print(" ➥ Beli 1 bibit »(1)")
            print(" ➥ Beli 3 bibit »(2)")
            print(" ➥ Beli 5 bibit »(3)")
            print(" ➥ Kembali      »[x]")
            print(" ")
            print(" Pilih : ")
            panggur = _getch()
            
            if panggur == "1":
              gabung = kapasitas_tas["anggur"] * 1
              if gxc >= harga_bibit_buah_sayur["anggur"] * 1:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 1 bibit anggur »")
                  gxc -= harga_bibit_buah_sayur["anggur"] * 1
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["anggur"] * 1
                  list_bibit_buah_sayur["anggur"] += 1
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif panggur == "2":
              gabung = kapasitas_tas["anggur"] * 3
              if gxc >= harga_bibit_buah_sayur["anggur"] * 3:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 3 bibit anggur »")
                  gxc -= harga_bibit_buah_sayur["anggur"] * 3
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["anggur"] * 3
                  list_bibit_buah_sayur["anggur"] += 3
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif panggur == "3":
              gabung = kapasitas_tas["anggur"] * 5
              if gxc >= harga_bibit_buah_sayur["anggur"] * 5:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 5 bibit anggur »")
                  gxc -= harga_bibit_buah_sayur["anggur"] * 5
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["anggur"] * 5
                  list_bibit_buah_sayur["anggur"] += 5
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif panggur == "x":
              print(" ")
              print(" Kembali »")
              time.sleep(0.345)
              break
            
            else:
              print(" ")
              print(" \033[31mInput salah !\033[0m")
              time.sleep(0.345)
        
        elif pbuah == "7":
          print(" ")
          wkt()
          
          while True:
            os.system("clear")
            
            print(" ")
            print(" \033[32mbibit apel merah\033[0m :")
            print(" ")
            print(" ➥ Beli 1 bibit »(1)")
            print(" ➥ Beli 3 bibit »(2)")
            print(" ➥ Beli 5 bibit »(3)")
            print(" ➥ Kembali      »[x]")
            print(" ")
            print(" Pilih : ")
            papel_merah = _getch()
            
            if papel_merah == "1":
              gabung = kapasitas_tas["apel_merah"] * 1
              if gxc >= harga_bibit_buah_sayur["apel_merah"] * 1:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 1 bibit apel merah »")
                  gxc -= harga_bibit_buah_sayur["apel_merah"] * 1
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["apel_merah"] * 1
                  list_bibit_buah_sayur["apel_merah"] += 1
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif papel_merah == "2":
              gabung = kapasitas_tas["apel_merah"] * 3
              if gxc >= harga_bibit_buah_sayur["apel_merah"] * 3:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 3 bibit apel merah »")
                  gxc -= harga_bibit_buah_sayur["apel_merah"] * 3
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["apel_merah"] * 3
                  list_bibit_buah_sayur["apel_merah"] += 3
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif papel_merah == "3":
              gabung = kapasitas_tas["apel_merah"] * 5
              if gxc >= harga_bibit_buah_sayur["apel_merah"] * 5:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 5 bibit apel merah »")
                  gxc -= harga_bibit_buah_sayur["apel_merah"] * 5
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["apel_merah"] * 5
                  list_bibit_buah_sayur["apel_merah"] += 5
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif papel_merah == "x":
              print(" ")
              print(" Kembali »")
              time.sleep(0.345)
              break
            
            else:
              print(" ")
              print(" \033[31mInput salah !\033[0m")
              time.sleep(0.345)
        
        elif pbuah == "8":
          print(" ")
          wkt()
          
          while True:
            os.system("clear")
            
            print(" ")
            print(" \033[32mbibit apel hijau\033[0m :")
            print(" ")
            print(" ➥ Beli 1 bibit »(1)")
            print(" ➥ Beli 3 bibit »(2)")
            print(" ➥ Beli 5 bibit »(3)")
            print(" ➥ Kembali      »[x]")
            print(" ")
            print(" Pilih : ")
            papel_hijau = _getch()
            
            if papel_hijau == "1":
              gabung = kapasitas_tas["apel_hijau"] * 1
              if gxc >= harga_bibit_buah_sayur["apel_hijau"] * 1:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 1 bibit apel hijau »")
                  gxc -= harga_bibit_buah_sayur["apel_hijau"] * 1
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["apel_hijau"] * 1
                  list_bibit_buah_sayur["apel_hijau"] += 1
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif papel_hijau == "2":
              gabung = kapasitas_tas["apel_hijau"] * 3
              if gxc >= harga_bibit_buah_sayur["apel_hijau"] * 3:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 3 bibit apel hijau »")
                  gxc -= harga_bibit_buah_sayur["apel_hijau"] * 3
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["apel_hijau"] * 3
                  list_bibit_buah_sayur["apel_hijau"] += 3
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif papel_hijau == "3":
              gabung = kapasitas_tas["apel_hijau"] * 5
              if gxc >= harga_bibit_buah_sayur["apel_hijau"] * 5:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 5 bibit apel hijau »")
                  gxc -= harga_bibit_buah_sayur["apel_hijau"] * 5
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["apel_hijau"] * 5
                  list_bibit_buah_sayur["apel_hijau"] += 5
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif papel_hijau == "x":
              print(" ")
              print(" Kembali »")
              time.sleep(0.345)
              break
            
            else:
              print(" ")
              print(" \033[31mInput salah !\033[0m")
              time.sleep(0.345)
        
        elif pbuah == "9":
          print(" ")
          wkt()
          
          while True:
            os.system("clear")
            
            print(" ")
            print(" \033[32mbibit pir\033[0m :")
            print(" ")
            print(" ➥ Beli 1 bibit »(1)")
            print(" ➥ Beli 3 bibit »(2)")
            print(" ➥ Beli 5 bibit »(3)")
            print(" ➥ Kembali      »[x]")
            print(" ")
            print(" Pilih : ")
            ppir = _getch()
            
            if ppir == "1":
              gabung = kapasitas_tas["pir"] * 1
              if gxc >= harga_bibit_buah_sayur["pir"] * 1:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 1 bibit pir »")
                  gxc -= harga_bibit_buah_sayur["pir"] * 1
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["pir"] * 1
                  list_bibit_buah_sayur["pir"] += 1
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif ppir == "2":
              gabung = kapasitas_tas["pir"] * 3
              if gxc >= harga_bibit_buah_sayur["pir"] * 3:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 3 bibit pir »")
                  gxc -= harga_bibit_buah_sayur["pir"] * 3
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["pir"] * 3
                  list_bibit_buah_sayur["pir"] += 3
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif ppir == "3":
              gabung = kapasitas_tas["pir"] * 5
              if gxc >= harga_bibit_buah_sayur["pir"] * 5:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 5 bibit pir »")
                  gxc -= harga_bibit_buah_sayur["pir"] * 5
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["pir"] * 5
                  list_bibit_buah_sayur["pir"] += 5
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif ppir == "x":
              print(" ")
              print(" Kembali »")
              time.sleep(0.345)
              break
            
            else:
              print(" ")
              print(" \033[31mInput salah !\033[0m")
              time.sleep(0.345)
        
        elif pbuah == "0":
          print(" ")
          wkt()
          
          while True:
            os.system("clear")
            
            print(" ")
            print(" \033[32mbibit mangga\033[0m :")
            print(" ")
            print(" ➥ Beli 1 bibit »(1)")
            print(" ➥ Beli 3 bibit »(2)")
            print(" ➥ Beli 5 bibit »(3)")
            print(" ➥ Kembali      »[x]")
            print(" ")
            print(" Pilih : ")
            pmangga = _getch()
            
            if pmangga == "1":
              gabung = kapasitas_tas["mangga"] * 1
              if gxc >= harga_bibit_buah_sayur["mangga"] * 1:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 1 bibit mamgga »")
                  gxc -= harga_bibit_buah_sayur["mangga"] * 1
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["mangga"] * 1
                  list_bibit_buah_sayur["mangga"] += 1
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif pmangga == "2":
              gabung = kapasitas_tas["mangga"] * 3
              if gxc >= harga_bibit_buah_sayur["mangga"] * 3:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 3 bibit mangga »")
                  gxc -= harga_bibit_buah_sayur["mangga"] * 3
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["mangga"] * 3
                  list_bibit_buah_sayur["mangga"] += 3
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif pmangga == "3":
              gabung = kapasitas_tas["mangga"] * 5
              if gxc >= harga_bibit_buah_sayur["mangga"] * 5:
                if tas + gabung <= 100:
                  print(" ")
                  print(" Proses membeli 5 bibit mangga »")
                  gxc -= harga_bibit_buah_sayur["mangga"] * 5
                  gxc = round(gxc, 3)
                  tas += kapasitas_tas["mangga"] * 5
                  list_bibit_buah_sayur["mangga"] += 5
                  time.sleep(1.23)
                  print(" ")
                  print(" \033[32mSukses ✓\033[0m")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" \033[31mTas penuh !\033[0m")
                  time.sleep(0.345)
              else:
                print(" ")
                print(" \033[31mKoin Gxc tidak ada !\033[0m")
                time.sleep(0.345)
            
            elif pmangga == "x":
              print(" ")
              print(" Kembali »")
              time.sleep(0.345)
              break
            
            else:
              print(" ")
              print(" \033[31mInput salah !\033[0m")
              time.sleep(0.345)
          
        elif pbuah == "x":
          print(" ")
          print(" Kembali »")
          time.sleep(0.345)
          break
        
        else:
          print(" ")
          print(" \033[31mInput salah !\033[0m")
          time.sleep(0.345)
    
    elif cmd == "4":
      print(" ")
      print(" \033[32mSegera hadir.\033[0m")
      time.sleep(0.345)
      
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
      time.sleep(0.345)

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
            
    #@
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
    print(" ➧ Untuk bagian ➟ Buah ()")
    print(" Huruf \033[32mg\033[0m untuk menanam.")
    print(" Huruf \033[32mr\033[0m untuk memanen.")
    print(" ")
    print(" Keluar [x] :")
    cmd = _getch()
    
    if cmd == "x":
      break
      
def kerajinan():
  global kayu, kayuT1, kayuT2, papan0, papan1, papan2, kursi0, kursi1, kursi2, meja0, meja1, meja2, lemari0, lemari1, lemari2, tas, exp
  
  while True:
    os.system("clear")
    
    print(" ")
    print(" \033[36mKerajinan :\033[0m")
    print(" ")
    print(" ➥ Buat \033[32mpapan\033[0m  »(1)")
    print(" ")
    print(" ➥ Buat \033[32mkursi\033[0m  »(2)")
    print(" ")
    print(" ➥ Buat \033[32mmeja\033[0m   »(3)")
    print(" ")
    print(" ➥ Buat \033[32mlemari\033[0m »(4)")
    print(" ")
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
            papan0 = round(papan0, 5)
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
            papan1 = round(papan1, 5)
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
            papan2 = round(papan2, 5)
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
              kursi0 = round(kursi0, 5)
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
              kursi1 += 1
              kursi1 = round(kursi1, 5)
              time.sleep(1.23)
              print(" ➥ \033[32mSukses ✓\033[0m")
            else:
              print(" ")
              print(" \033[31mKayu T.1 tidak ada !\033[0m")
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
              kursi2 = round(kursi2, 5)
              time.sleep(1.23)
              print(" ➥ \033[32mSukses ✓\033[0m")
            else:
              print(" ")
              print(" \033[31mKayu T.2 tidak ada !\033[0m")
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
              
    elif cmd == "3":
      
      while True:
          
        os.system("clear")
         
        print(" ")
        print(" Pilih jenis meja : ")
        print(" ")
        print(" ➥ Meja biasa \033[36m╔═╗\033[0m   »(1)")
        print("   Perlu ×4 papan biasa dan ×9 kayu T.1/2(0)")
        print(" ")
        print(" ➥ Meja T.1   \033[32m╔═╗╗\033[0m  »(2)")
        print("   Perlu x4 papan T.1 dan ×12 kayu T.1")
        print(" ")
        print(" ➥ Meja T.2   \033[31m╔═╗╗╗\033[0m »(3)")
        print("   Perlu ×4 papan T.2 dan ×36 kayu T.2")
        print(" ")
        print(" ➥ Kembali          »[x]")
        print(" ")
        print(" Pilih : ")
        meja=_getch()
         
        if meja == "1":
          if papan0 >= 4:
            if kayu >= 9:
              print(" ")
              print(" Proses membuat 033[36m╔═╗\033[0m »")
              print(" ")
              tas -= 9
              papan0 -= 4
              kayu -= 9
              exp += 25
              meja0 += 1
              meja0 = round(meja0, 5)
              time.sleep(1.23)
              print(" \033[32mSukses ✓\033[0m")
            else:
              print(" ")
              print(" \033[31mKayu T.1/2(0) !\033[0m")
              print(" ")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mPapan biasa tidak ada !\033[0m")
            print(" ")
            time.sleep(0.345)
        
        elif meja == "2":
          if papan1 >= 4:
            if kayuT1 >= 12:
              print(" ")
              print(" Proses membuat 033[32m╔═╗╗\033[0m »")
              print(" ")
              tas -= 12
              papan1 -= 4
              kayuT1 -= 12
              exp += 30
              meja1 += 1
              meja1 = round(meja1, 5)
              time.sleep(1.23)
              print(" \033[32mSukses ✓\033[0m")
            else:
              print(" ")
              print(" \033[31mKayu T.1 tidak ada !\033[0m")
              print(" ")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mPapan T.1 tidak ada !\033[0m")
            print(" ")
            time.sleep(0.345)
        
        elif meja == "3":
          if papan2 >= 4:
            if kayuT2 >= 36:
              print(" ")
              print(" Proses membuat 033[31m═╗╗╗\033[0m »")
              print(" ")
              tas -= 36
              papan2 -= 4
              kayuT2 -= 36
              exp += 35
              meja2 += 1
              meja2 = round(meja2, 5)
              time.sleep(1.23)
              print(" \033[32mSukses ✓\033[0m")
            else:
              print(" ")
              print(" \033[31mKayu T.2 tidak ada !\033[0m")
              print(" ")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mPapan T.2 tidak ada !\033[0m")
            print(" ")
            time.sleep(0.345)
        
        elif meja == "x":
          break
        
        else:
          print(" ")
          print(" \033[31mInput salah !\033[0m")
          print(" ")
          time.sleep(0.345)
               
    elif cmd == "4":
      
      while True:
        
        os.system("clear")
        
        print(" ")
        print(" Pilih jenis lemari : ")
        print(" ")
        print(" ➥ Lemari biasa \033[36m╠╣\033[0m »(1)")
        print("   Perlu ×10 papan biasa dan ×20 kayu T.1/2(0)")
        print(" ")
        print(" ➥ Lemari T.1   \033[32m╠╣\033[0m »(2)")
        print("   Perlu ×10 papan T.1 dan ×20 kayu T.1")
        print(" ")
        print(" ➥ Lemari T.2   \033[31m╠╣\033[0m »(3)")
        print("   Perlu x10 papan T.2 dan ×20 kayu T.2")
        print(" ")
        print(" ➥ Kembali           [x]")
        print(" ")
        print(" Pilih : ")
        lemari = _getch()
        
        if lemari == "1":
          if papan0 >= 10:
            if kayu >= 20:
              print(" ")
              print(" Proses membuat \033[36m╠╣\033[0m »")
              print(" ")
              tas -= 20
              papan0 -= 10
              kayu -= 20
              exp -= 40
              lemari0 += 1
              lemari0 = round(lemari0, 5)
              time.sleep(1.23)
              print(" \033[32mSukses ✓\033[0m")
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
              
        elif lemari == "2":
          if papan1 >= 10:
            if kayuT1 >= 20:
              print(" ")
              print(" Proses membuat \033[32m╠╣\033[0m »")
              print(" ")
              tas -= 20
              papan1 -= 10
              kayuT1 -= 20
              exp -= 40
              lemari1 += 1
              lemari1 = round(lemari1, 5)
              time.sleep(1.23)
              print(" \033[32mSukses ✓\033[0m")
            else:
              print(" ")
              print(" \033[31mKayu T.1 tidak ada !\033[0m")
              print(" ")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mPapan T.1 tidak ada !\033[0m")
            print(" ")
            time.sleep(0.345)
        
        elif lemari == "3":
          if papan2 >= 10:
            if kayuT2 >= 20:
              print(" ")
              print(" Proses membuat \033[36m╠╣\033[0m »")
              print(" ")
              tas -= 20
              papan2 -= 10
              kayuT2 -= 20
              exp -= 40
              lemari2 += 1
              lemari2 = round(lemari2, 5)
              time.sleep(1.23)
              print(" \033[32mSukses ✓\033[0m")
            else:
              print(" ")
              print(" \033[31mKayu T.2 tidak ada !\033[0m")
              print(" ")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mPapan T.2 tidak ada !\033[0m")
            print(" ")
            time.sleep(0.345)
        
        elif lemari == "x":
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
      print(f" \033[32mSukses! +1\033[0m {jenis}")
      print(" ")
      time.sleep(1.234)
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
    print("➥ 🐠 🎖  (ikan Juara) : ", ikan[key5])
    print(" ")
    print(" Keluar      [x]")
    print("")
    cmd = _getch()
    
    if cmd == "x":
      break
    
  
def book():
  
  os.system("python ibook.py")
  
def misi1():
  global misi, exp, gxc, gcoins, bibit, bibit2, kayu, kayuT1, kayuT2, bluebox, Game_end
  ob = misi
  ob1 = bluebox
  
  if bibit >= 20 and ob["cek.bibit1"] != "✓":
    ob["cek.bibit1"] = "✓"
    Game_end += 1
    exp += 150
    
  if bibit2 >= 20 and ob["cek.bibit2"] != "✓":
    ob["cek.bibit2"] = "✓"
    Game_end += 1
    gxc += 400
    
  if kayu >= 35 and ob["cek.kayu0"] != "✓":
    ob["cek.kayu0"] = "✓"
    Game_end += 1
    gcoins += 1000
    
  if kayuT1 >= 45 and ob["cek.kayu1"] != "✓":
    ob["cek.kayu1"] = "✓"
    Game_end += 1
    ob1["bibit2"] += 25
    
  if kayuT2 >= 55 and ob["cek.kayu2"] != "✓":
    ob["cek.kayu2"] = "✓"
    Game_end += 1
    ob1["b.stoberi"] += 10

  while True:
    os.system("clear")
    info = ""
    _1 = " Reward : \033[32m+1 GE & +150 Exp\033[0m"
    _2 = " Reward : \033[32m+1 GE & +400 Koin Gxc\033[0m"
    _3 = " Reward : \033[32m+1 GE & +1000 G-coin\033[0m"
    _4 = " Reward : \033[32m+1 GE & +25 bibit pohon T.2 »(bluebox)\033[0m"
    _5 = " Reward : \033[32m+1 GE & +10 bibit stoberi »(bluebox)\033[0m"
    
    if ob["cek.bibit1"] == "✓":
      _1 = "  \033[32mDone.\033[0m"
    else:
      _1 = " Reward : \033[32m+1 GE & +150 Exp\033[0m"
     
    if ob["cek.bibit2"] == "✓":
      _2 = "  \033[32mDone.\033[0m"
    else:
      _2 = " Reward : \033[32m+1 GE & +400 Koin Gxc\033[0m"
    
    if ob["cek.kayu0"] == "✓":
      _3 = "  \033[32mDone.\033[0m"
    else:
      _3 = " Reward : \033[32m+1 GE & +1000 G-coin\033[0m"
      
    if ob["cek.kayu1"] == "✓":
      _4 = "  \033[32mDone.\033[0m"
    else:
      _4 = " Reward : \033[32m+1 GE & +25 bibit pohon T.2 »(bluebox)\033[0m"
      
    if ob["cek.kayu2"] == "✓":
      _5 = "  \033[32mDone.\033[0m"
    else:
      _5 = " Reward : \033[32m+1 GE & +10 bibit stoberi »(bluebox)\033[0m"
      
      
    if ob["cek.bibit1"] == "✓" and ob["cek.bibit2"] == "✓" and ob["cek.kayu0"] == "✓" and ob["cek.kayu1"] == "✓" and ob["cek.kayu2"] == "✓":
      info = "\033[32mKamu berhasil menyelesaikan Misi #1 ✓\033[0m\nKeluar dan masuk kembali kepapan misi untuk misi\nselanjutnya"
    else:
      info = ""
    
    print(" ")
    print(" \033[34mM I S I #1\033[0m")
    print(" ")
    gab1 = bibit + bluebox["bibit"]
    print(f" ➥ Kumpulkan 20 bibit pohon T.1 » \033[36m{gab1}\033[0m/20 Status : \033[32m{ob["cek.bibit1"]}\033[0m")
    print(_1)
    print(" ")
    gab2 = bibit2 + bluebox["bibit2"]
    print(f" ➥ Kumpulkan 20 bibit pohon T.2 » \033[36m{gab2}\033[0m/20 Status : \033[32m{ob["cek.bibit2"]}\033[0m")
    print(_2)
    print(" ")
    gab3 = kayu + bluebox["kayu"]
    print(f" ➥ Kumpulkan 35 kayu T.1/2(0)   » \033[36m{kayu}\033[0m/35 Status : \033[32m{ob["cek.kayu0"]}\033[0m")
    print(_3)
    print(" ")
    gab4 = kayuT1 + bluebox["kayuT1"]
    print(f" ➥ Kumpulkan 45 kayu T.1        » \033[36m{kayuT1}\033[0m/45 Status : \033[32m{ob["cek.kayu1"]}\033[0m")
    print(_4)
    print(" ")
    gab5 = kayuT2 * bluebox["kayuT2"]
    print(f" ➥ Kumpulkan 55 kayu T.2        » \033[36m{kayuT2}\033[0m/55 Status : \033[32m{ob["cek.kayu2"]}\033[0m")
    print(_5)
    print(" ")
    print(" Keluar [x] : ")
    print(" ")
    print(info)
    cmd = _getch()
    
    if cmd == "x":
      break
  
def misi2():
  global misi, exp, gxc, gcoins, bluebox, Game_end, list_bibit_buah_sayur, ikan
  
  ob = misi
  ob1 = bluebox
  ob2 = list_bibit_buah_sayur
  ob3 = ikan
  key1 = "🐟 ⭐ "
  jstoberi = ob1["b.stoberi"] + ob2["stoberi"]
  jmelon = ob1["b.melon"] + ob2["melon"]
  jnanas = ob1["b.nanas"] + ob2["nanas"]
  jlemon = ob1["b.lemon"] + ob2["lemon"]
  jjeruk = ob1["b.jeruk"] + ob2["jeruk"]
  
  if jstoberi >= 50 and ob["cek.bibit.stoberi"] != "✓":
    ob["cek.bibit.stoberi"] = "✓"
    Game_end += 1
    exp += 300
    
  if jmelon >= 50 and ob["cek.bibit.melon"] != "✓":
    ob["cek.bibit.melon"] = "✓"
    Game_end += 1
    gxc += 600
    
  if jnanas >= 50 and ob["cek.bibit.nanas"] != "✓":
    ob["cek.bibit.nanas"] = "✓"
    Game_end += 1
    gcoins += 2000
    
  if jlemon >= 50 and ob["cek.bibit.lemon"] != "✓":
    ob["cek.bibit.lemon"] = "✓"
    Game_end += 1
    ob1["b.melon"] += 15
    
  if jjeruk >= 50 and ob["cek.bibit.jeruk"] != "✓":
    ob["cek.bibit.jeruk"] = "✓"
    Game_end += 1
    ob3[key1] += 10

  while True:
    os.system("clear")
    info = ""
    _1 = " Reward : \033[32m+1 GE & +300 Exp\033[0m"
    _2 = " Reward : \033[32m+1 GE & +600 Koin Gxc\033[0m"
    _3 = " Reward : \033[32m+1 GE & +2000 G-coin\033[0m"
    _4 = " Reward : \033[32m+1 GE & +15 bibit buah melon »(bluebox)\033[0m"
    _5 = " Reward : \033[32m+1 GE & +10 ikan biasa »(Hasil memancing)\033[0m"
    
    if ob["cek.bibit.stoberi"] == "✓":
      _1 = "  \033[32mDone.\033[0m"
    else:
      _1 = " Reward : \033[32m+1 GE & +300 Exp\033[0m"
     
    if ob["cek.bibit.melon"] == "✓":
      _2 = "  \033[32mDone.\033[0m"
    else:
      _2 = " Reward : \033[32m+1 GE & +600 Koin Gxc\033[0m"
    
    if ob["cek.bibit.nanas"] == "✓":
      _3 = "  \033[32mDone.\033[0m"
    else:
      _3 = " Reward : \033[32m+1 GE & +2000 G-coin\033[0m"
      
    if ob["cek.bibit.lemon"] == "✓":
      _4 = "  \033[32mDone.\033[0m"
    else:
      _4 = " Reward : \033[32m+1 GE & +15 bibit buah melon »(bluebox)\033[0m"
      
    if ob["cek.bibit.jeruk"] == "✓":
      _5 = "  \033[32mDone.\033[0m"
    else:
      _5 = " Reward : \033[32m+1 GE & +10 ikan biasa »(Hasilmemancing)\033[0m"
      
      
    if ob["cek.bibit.stoberi"] == "✓" and ob["cek.bibit.melon"] == "✓" and ob["cek.bibit.nanas"] == "✓" and ob["cek.bibit.lemon"] == "✓" and ob["cek.bibit.jeruk"] == "✓":
      info = "\033[32mKamu berhasil menyelesaikan Misi #2 ✓\033[0m\nKeluar dan masuk kembali kepapan misi untuk misi\nselanjutnya"
    else:
      info = ""
    
    print(" ")
    print(" \033[34mM I S I #2\033[0m")
    print(" ")
    print(f" ➥ Setor 50 bibit buah stoberi » \033[36m{ob2["stoberi"]}\033[0m/50 Status : \033[32m{ob["cek.bibit.stoberi"]}\033[0m")
    print(_1)
    print(" ")
    print(f" ➥ Setor 50 bibit buah melon   » \033[36m{ob2["melon"]}\033[0m/50 Status : \033[32m{ob["cek.bibit.melon"]}\033[0m")
    print(_2)
    print(" ")
    print(f" ➥ Setor 50 bibit buah nanas   » \033[36m{ob2["nanas"]}\033[0m/50 Status : \033[32m{ob["cek.bibit.nanas"]}\033[0m")
    print(_3)
    print(" ")
    print(f" ➥ Setor 50 bibit buah lemon   » \033[36m{ob2["lemon"]}\033[0m/50 Status : \033[32m{ob["cek.bibit.lemon"]}\033[0m")
    print(_4)
    print(" ")
    print(f" ➥ Setor 50 bibit buah jeruk   » \033[36m{ob2["jeruk"]}\033[0m/50 Status : \033[32m{ob["cek.bibit.jeruk"]}\033[0m")
    print(_5)
    print(" ")
    print(" Keluar [x] : ")
    print(" ")
    print(info)
    cmd = _getch()
    
    if cmd == "x":
      break

def misi3():
  while True:
    os.system("clear")
    print(" ")
    print(" \033[32mSegera hadir.\033[0m")
    print(" ")
    print(" Keluar [x] : ")
    print(" ")
    cmd = _getch()
    
    if cmd == "x":
      break

def tokoikan():
  global ikan, gxc
  
  while True:
    
    os.system("clear")
    
    print(" Selamat datang ditoko Jual/beli ikan.")
    print(" ")
    print(" ➥ Beli ikan »(1)")
    print(" ")
    print(" ➥ Jual ikan »(2)")
    print(" ")
    print(" Kembali      [x]")
    print(" ")
    print(" Pilih : ")
    cmd = _getch()
    
    if cmd == "1":
      
      while True:
        os.system("clear")
        harga_ikanbiasa = 20
        harga_ikanbesar = 30
        harga_ikansuper = 50
        harga_ikankilau = 100
        harga_ikanjuara = 1000
        print(" ")
        print(" Ikan yang tersedia untuk dibeli :")
        print(" ")
        print(" ➥ Ikan biasa »(1)")
        print(" ➥ Ikan besar »(2)")
        print(" ➥ Ikan super »(3)")
        print(" ➥ Ikan kilau »(4)")
        print(" ➥ Ikan juara »(5)")
        print(" Kembali       [x]")
        print(" ")
        print(" Pilih : ")
        beli=_getch()
        
        if beli == "1":
          
          bl_biasa = input("Masukkan jumlah ikan biasa yang ingin dibeli : ")
          
          try:
            jbiasa = int(bl_biasa)
            if jbiasa <= 0:
              print(" ")
              print(" \033[31mTidak boleh angka 0 !\033[0m")
              print(" ")
              time.sleep(0.345)
            elif gxc < jbiasa * harga_ikanbiasa:
              print(" ")
              print(" \033[31mKoin Gxc kurang !\033[0m")
              print(" ")
              time.sleep(0.345)
            else:
              print(" ")
              print(" Proses membeli ikan biasa »")
              print(" ")
              ikan["🐟 ⭐ "] += jbiasa
              gxc -= jbiasa * harga_ikanbiasa
              time.sleep(0.345)
              print(" \033[32mSukses ✓\033[0m")
              time.sleep(0.345)
              break
          except ValueError:
            print(" ")
            print("\033[33mInput salah !\033[0m")
            print(" ")
            time.sleep(0.345)
        
        elif beli == "2":
            
          bl_besar = input("Masukkan jumlah ikan besar yang ingin dibeli : ")
          
          try:
            jbesar = int(bl_besar)
            if jbesar <= 0:
              print(" ")
              print(" \033[31mTidak boleh angka 0 !\033[0m")
              print(" ")
              time.sleep(0.345)
            elif gxc < jbesar * harga_ikanbesar:
              print(" ")
              print(" \033[31mKoin Gxc kurang !\033[0m")
              print(" ")
              time.sleep(0.345)
            else:
              print(" ")
              print(" Proses membeli ikan besar »")
              print(" ")
              ikan["🐟 ✨ "] += jbesar
              gxc -= jbesar * harga_ikanbesar
              time.sleep(0.345)
              print(" \033[32mSukses ✓\033[0m")
              time.sleep(0.345)
              break
          except ValueError:
            print(" ")
            print(" \033[33mInput salah !\033[0m")
            print(" ")
            time.sleep(0.345)
        
        elif beli == "3":
          
          bl_super = input("Masukkan jumlah ikan super yang ingin dibeli : ")
          
          try:
            jsuper = int(bl_super)
            if jsuper <= 0:
              print(" ")
              print(" \033[31mTidak boleh angka 0 !\033[0m")
              print(" ")
              time.sleep(0.345)
            elif gxc < jsuper * harga_ikansuper:
              print(" ")
              print(" \033[31mKoin Gxc kurang !\033[0m")
              print(" ")
              time.sleep(0.345)
            else:
              print(" ")
              print(" Proses membeli ikan super »")
              print(" ")
              ikan["🐠 🌟 "] += jsuper
              gxc -= jsuper * harga_ikansuper
              time.sleep(0.345)
              print(" \033[32mSukses ✓\033[0m")
              time.sleep(0.345)
              break
          except ValueError:
            print(" ")
            print(" \033[33mInput salah !\033[0m")
            print(" ")
            time.sleep(0.345)
        
        elif beli == "4":
          
          bl_kilau = input("Masukkan jumlah ikan super yanh ingin dibeli : ")
          
          try:
            jkilau = int(bl_kilau)
            if jkilau <= 0:
              print(" ")
              print(" \033[31mTidak boleh angka 0 !\033[0m")
              print(" ")
              time.sleep(0.345)
            elif gxc < jkilau * harga_ikankilau:
              print(" ")
              print(" \033[31mKoin Gxc kurang !\033[0m")
              print(" ")
              time.sleep(0.345)
            else:
              print(" ")
              print(" Proses membeli ikan kilau »")
              print(" ")
              ikan["🐠 💫 "] += jkilau
              gxc -= jkilau * harga_ikankilau
              time.sleep(0.345)
              print(" \033[32mSukses ✓\033[0m")
              time.sleep(0.345)
              break
          except ValueError:
            print(" ")
            print(" \033[33mInput salah !\033[0m")
            print(" ")
            time.sleep(0.345)
        
        elif beli == "5":
          
          bl_juara = input("Masukkan jumlah ikan juara yang ingin dibeli : ")
          
          try:
            jjuara = int(bl_juara)
            if jjuara <= 0:
              print(" ")
              print(" \033[31mAngka tidak boleh 0 !\033[0m")
              print(" ")
              time.sleep(0.345)
            elif gxc < jjuara * harga_ikanjuara:
              print(" ")
              print(" \033[31mKoin Gxc kurang !\033[0m")
              print(" ")
              time.sleep(0.345)
            else:
              print(" ")
              print(" Proses membeli ikan juara »")
              print(" ")
              ikan["🐠 🎖️ "] += jjuara
              gxc -= jjuara * harga_ikanjuara
              time.sleep(0.345)
              print(" \033[32mSukses ✓\033[0m")
              time.sleep(0.345)
              break
          except ValueError:
            print(" ")
            print(" \033[33mInput salah !\033[0m")
            print(" ")
            time.sleep(0.345)
            
        elif beli == "x":
          break
      
        else:
          print(" ")
          print(" \033[31mInput salah !\033[0m")
          print(" ")
          time.sleep(0.345)
          continue
    
    elif cmd == "2":
      
      while True:
        os.system("clear")
        harga_jualbiasa = 15
        harga_jualbesar = 25
        harga_jualsuper = 45
        harga_jualkilau = 95
        harga_jualjuara = 999
        print(" ")
        print(" Ikan yang tersedia untuk dijual :")
        print(" ")
        print(" ➥ Ikan biasa »(1)")
        print(" ➥ Ikan besar »(2)")
        print(" ➥ Ikan super »(3)")
        print(" ➥ Ikan kilau »(4)")
        print(" ➥ Ikan juara »(5)")
        print(" Kembali       [x]")
        print(" ")
        print(" Pilih : ")
        jual=_getch()
        
        if jual == "1":
          
          jl_biasa = input("Masukkan jumlah ikan biasa yang ingin dijual : ")
          
          try:
            jbiasa = int(jl_biasa)
            if jbiasa <= 0:
              print(" ")
              print(" \033[31mAngka tidak boleh 0 !\033[0m")
              print(" ")
              time.sleep(0.345)
            elif ikan["🐟 ⭐ "] < jbiasa:
              print(" ")
              print(" \033[31mIkan biasa tidak ada !\033[0m")
              print(" ")
              time.sleep(0.345)
            else:
              print(" ")
              print(" Proses menjual ikan biasa »")
              print(" ")
              ikan["🐟 ⭐ "] -= jbiasa
              gxc += jbiasa * harga_jualbiasa
              time.sleep(0.345)
              print(" \033[32mSukses ✓\033[0m")
              time.sleep(0.345)
              break
          except ValueError:
            print(" ")
            print(" \033[33mInput salah !\033[0m")
            print(" ")
            time.sleep(0.345)
        
        elif jual == "2":
          
          jl_besar = input("Masukkan jumlah ikan besar yang ingin dijual : ")
          
          try:
            jbesar = int(jl_besar)
            if jbesar <= 0:
              print(" ")
              print(" \033[31mAngka tidak boleh 0 !\033[0m")
              print(" ")
              time.sleep(0.345)
            elif ikan["🐟 ✨ "] < jbesar:
              print(" ")
              print(" \033[31mIkan besar tidak ada !\033[0m")
              print(" ")
              time.sleep(0.345)
            else:
              print(" ")
              print(" Proses menjual ikan besar »")
              print(" ")
              ikan["🐟 ✨ "] -= jbesar
              gxc += jbesar * harga_jualbesar
              time.sleep(0.345)
              print(" \033[32mSukses ✓\033[0m")
              time.sleep(0.345)
              break
          except ValueError:
            print(" ")
            print(" \033[33mInput salah !\033[0m")
            print(" ")
            time.sleep(0.345)
        
        elif jual == "3":
          
          jl_super = input("Masukkan jumlah ikan super yang ingin dijual : ")
          
          try:
            jsuper = int(jl_super)
            if jsuper <= 0:
              print(" ")
              print(" \033[31mAngka tidak boleh 0 !\033[0m")
              print(" ")
              time.sleep(0.345)
            elif ikan["🐠 🌟 "] < jsuper:
              print(" ")
              print(" \033[31mIkan super tidak ada !\033[0m")
              print(" ")
              time.sleep(0.345)
            else:
              print(" ")
              print(" Proses menjual ikan super »")
              print(" ")
              ikan["🐠 🌟 "] -= jsuper
              gxc += jsuper * harga_jualsuper
              time.sleep(0.345)
              print(" \033[32mSukses ✓\033[0m")
              time.sleep(0.345)
              break
          except ValueError:
            print(" ")
            print(" \033[33mInput salah !\033[0m")
            print(" ")
            time.sleep(0.345)
        
        elif jual == "4":
          
          jl_kilau = input("Masukkan jumlah ikan kilau yang ingin dijual : ")
          
          try:
            jkilau = int(jl_kilau)
            if jkilau <= 0:
              print(" ")
              print(" \033[31mAngka tidak boleh 0 !\033[0m")
              print(" ")
              time.sleep(0.345)
            elif ikan["🐠 💫 "] < jkilau:
              print(" ")
              print(" \033[31mIkan kilau tidak ada !\033[0m")
              print(" ")
              time.sleep(0.345)
            else:
              print(" ")
              print(" Proses menjual ikan kilau »")
              print(" ")
              ikan["🐠 💫 "] -= jkilau
              gxc += jkilau * harga_jualkilau
              time.sleep(0.345)
              print(" \033[32mSukses ✓\033[0m")
              time.sleep(0.345)
              break
          except ValueError:
            print(" ")
            print(" \033[33mInput salah !\033[0m")
            print(" ")
            time.sleep(0.345) 
        
        elif jual == "5":
          
          jl_juara = input("Masukkan jumlah ikan juara yang ingin dijual : ")
          
          try:
            jjuara = int(jl_juara)
            if jjuara <= 0:
              print(" ")
              print(" \033[31mAngka tidak boleh 0 !\033[0m")
              print(" ")
              time.sleep(0.345)
            elif ikan["🐠 🎖️ "] < jjuara:
              print(" ")
              print(" \033[31mIkan juara tidak ada !\033[0m")
              print(" ")
              time.sleep(0.345)
            else:
              print(" ")
              print(" Proses menjual ikan juara »")
              print(" ")
              ikan["🐠 🎖️ "] -= jjuara
              gxc += jjuara * harga_jualjuara
              time.sleep(0.345)
              print(" \033[32mSukses ✓\033[0m")
              time.sleep(0.345)
              break
          except ValueError:
            print(" ")
            print(" \033[33mInput salah !\033[0m")
            print(" ")
            time.sleep(0.345)
        
        elif jual == "x":
          break
        
        else:
          print(" ")
          print(" \033[31mInput salah !\033[0m")
          print(" ")
          time.sleep(0.345)
            
    elif cmd == "x":
      print(" ")
      print(" Kembali »")
      print(" ")
      wkt()
      break
              
    else:
      print(" ")
      print(" \033[31mInput salah !\033[0m")
      print(" ")
      time.sleep(0.345)

def isibluebox():
  global bluebox
  
  while True:
    os.system("clear")
    
    print(" ➧ \033[36mPohon\033[0m : ")
    print(f" ➥ 🌳 T.1/2(0) : \033[32m{bluebox["kayu"]:<4}\033[0m")
    print(f" ➥ 🌳 T.1      : \033[32m{bluebox["kayuT1"]:<4}\033[0m")
    print(f" ➥ 🌲 T.2      : \033[32m{bluebox["kayuT2"]:<4}\033[0m")
    print(" Segera hadir. . .")
    print(" ")
    print(" ➧ \033[36mBibit\033[0m :")
    print(f" ➥ 🌱 Pohon T.1  : \033[32m{bluebox["bibit"]:<4}\033[0m")
    print(f" ➥ 🌱 Pohon T.2  : \033[32m{bluebox["bibit2"]:<4}\033[0m")
    print(f" ➥ 🌱 Stoberi    : \033[32m{bluebox["b.stoberi"]:<4}\033[0m")
    print(f" ➥ 🌱 Melon      : \033[32m{bluebox["b.melon"]:<4}\033[0m")
    print(f" ➥ 🌱 Nanas      : \033[32m{bluebox["b.nanas"]:<4}\033[0m")
    print(f" ➥ 🌱 Lemon      : \033[32m{bluebox["b.lemon"]:<4}\033[0m")
    print(f" ➥ 🌱 Jeruk      : \033[32m{bluebox["b.jeruk"]:<4}\033[0m")
    print(f" ➥ 🌱 Anggur     : \033[32m{bluebox["b.anggur"]:<4}\033[0m")
    print(f" ➥ 🌱 Apel merah : \033[32m{bluebox["b.apelmerah"]:<4}\033[0m")
    print(f" ➥ 🌱 Apel hijau : \033[32m{bluebox["b.apelhijau"]:<4}\033[0m")
    print(f" ➥ 🌱 Pir        : \033[32m{bluebox["b.pir"]:<4}\033[0m")
    print(f" ➥ 🌱 Mangga     : \033[32m{bluebox["b.mangga"]:<4}\033[0m")
    print(" ")
    print(" Kembali »[x]  Next »[n]")
    print(" ")
    cmd = _getch()
    
    if cmd == "x":
      break
    
    elif cmd == "n":
      while True:
        os.system("clear")
        print(" ➧ \033[36mBuah\033[0m :")
        print(f" ➥ 🍓 stoberi    : \033[32m{bluebox["buah.stoberi"]:<4}\033[0m")
        print(f" ➥ 🍈 melon      : \033[32m{bluebox["buah.melon"]:<4}\033[0m")
        print(f" ➥ 🍍 nanas      : \033[32m{bluebox["buah.nanas"]:<4}\033[0m")
        print(f" ➥ 🍋 lemon      : \033[32m{bluebox["buah.lemon"]:<4}\033[0m")
        print(f" ➥ 🍊 jeruk      : \033[32m{bluebox["buah.jeruk"]:<4}\033[0m")
        print(f" ➥ 🍇 anggur     : \033[32m{bluebox["buah.anggur"]:<4}\033[0m")
        print(f" ➥ 🍎 apel merah : \033[32m{bluebox["buah.apelmerah"]:<4}\033[0m")
        print(f" ➥ 🍏 apel hijau : \033[32m{bluebox["buah.apelhijau"]:<4}\033[0m")
        print(f" ➥ 🍐 pir        : \033[32m{bluebox["buah.pir"]:<4}\033[0m")
        print(f" ➥ 🥭 mangga     : \033[32m{bluebox["buah.mangga"]:<4}\033[0m")
        print(" ")
        print(" Kembali »[x]")
        print(" ")
        cmd = _getch()
        
        if cmd == "x":
          break
      
      
     
def loadkayu():
  global tas, kayu, gcoins, redb
  
  bonus = 10
  masukkayu = input(" Masukkan jumlah kayu T.1/2(0) yang ingin disimpan »")
  
  try:
    jkayu = int(masukkayu)
    if jkayu <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif kayu == 0:
      print(" ")
      print(" \033[31mKayu T.1/2(0) tidak ada !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bluebox["kayu"] >= kapasitas_box["kayu"]:
      print(" ")
      print(" \033[31mKapasitas kayu T.1/2(0) sudah full !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jkayu > kayu:
      print(" ")
      print(" \033[31mKayu T.1/2(0) melebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jkayu <= kapasitas_box["kayu"]:
      print(" ")
      print(" Proses memasukkan kayu T.1/2(0) »")
      tas -= jkayu * kapasitas_tas["kayu"]
      bluebox["kayu"] += jkayu
      reward = jkayu * bonus
      gcoins += reward
      kayu -= jkayu
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)
 
    
def loadkayu1():
  global tas, kayuT1, gcoins, redb
  
  bonus = 20
  masukkayu1 = input(" Masukkan jumlah kayu T.1 yang ingin disimpan »")
  
  try:
    jkayu1 = int(masukkayu1)
    if jkayu1 <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif kayuT1 == 0:
      print(" ")
      print(" \033[31mKayu T.1 tidak ada !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bluebox["kayuT1"] >= kapasitas_box["kayuT1"]:
      print(" ")
      print(" \033[31mKapasitas kayu T.1 sudah full !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jkayu1 > kayuT1:
      print(" ")
      print(" \033[31mKayu T.1 melebih batas !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jkayu1 <= kapasitas_box["kayuT1"]:
      print(" ")
      print(" Proses memasukkan kayu T.1 »")
      tas -= jkayu1 * kapasitas_tas["kayuT1"]
      bluebox["kayuT1"] += jkayu1
      reward = jkayu1 * bonus
      gcoins += reward
      kayuT1 -= jkayu1
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def loadkayu2():
  global tas, kayuT2, gcoins, redb
  
  bonus = 30
  masukkayu2 = input(" Masukkan jumlah kayu T.2 yang ingin disimpan »")
  
  try:
    jkayu2 = int(masukkayu2)
    if jkayu2 <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif kayuT2 == 0:
      print(" ")
      print(" \033[31mKayu T.2 tidak ada !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bluebox["kayuT2"] >= kapasitas_box["kayuT2"]:
      print(" ")
      print(" \033[31mKapasitas kayu T.2 sudah full !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jkayu2 > kayuT2:
      print(" ")
      print(" \033[31mKayu T.2 melebihin batas !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jkayu2 <= kapasitas_box["kayuT2"]:
      print(" ")
      print(" Proses memasukkan kayu T.2 »")
      tas -= jkayu2 * kapasitas_tas["kayuT2"]
      bluebox["kayuT2"] += jkayu2
      reward = jkayu2 * bonus
      gcoins += reward
      kayuT2 -= jkayu2
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def loadbibit():
  global tas, bibit, gcoins, redb
  
  bonus = 10
  masukbibit= input(" Masukkan jumlah bibit T.1 yang ingin disimpan »")
  
  try:
    jbibit = int(masukbibit)
    if jbibit <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bibit == 0:
      print(" ")
      print(" \033[31mBibit T.1 tidak ada !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bluebox["bibit"] >= kapasitas_box["bibit"]:
      print(" ")
      print(" \033[31mKapasitas bibit T.1 sudah full !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jbibit > bibit:
      print(" ")
      print(" \033[31mBibit T.1 melebih batas !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jbibit <= kapasitas_box["bibit"]:
      print(" ")
      print(" Proses memasukkan bibit T.1 »")
      tas -= jbibit * kapasitas_tas["bibit"]
      bluebox["bibit"] += jbibit
      reward = jbibit * bonus
      gcoins += reward
      bibit -= jbibit
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def loadbibit2():
  global tas, bibit2, gcoins, redb
  
  bonus = 10
  masukbibit2 = input(" Masukkan jumlah bibit T.2 yang ingin disimpan »")
  
  try:
    jbibit2 = int(masukbibit2)
    if jbibit2 <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bibit2 == 0:
      print(" ")
      print(" \033[31mBibit T.2 tidak ada !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bluebox["bibit2"] >= kapasitas_box["bibit2"]:
      print(" ")
      print(" \033[31mKapasitas bibit T.2 sudah full !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jbibit2 > bibit2:
      print(" ")
      print(" \033[31mBibit T.2 melebihi batas !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jbibit2 <= kapasitas_box["bibit2"]:
      print(" ")
      print(" Proses memasukkan bibit T.2 »")
      tas -= jbibit2 * kapasitas_tas["bibit2"]
      bluebox["bibit2"] += jbibit2
      reward = jbibit2 * bonus
      gcoins += reward
      bibit2 -= jbibit2
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def loadstoberi():
  global tas, gcoins, redb
  
  bonus = 10
  masukstoberi = input(" Masukkan jumlah bibit stoberi yang ingin disimpan »")
  
  try:
    jstoberi = int(masukstoberi)
    if jstoberi <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif list_bibit_buah_sayur["stoberi"] == 0:
      print(" ")
      print(" \033[31mBibit stoberi tidak ada !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bluebox["b.stoberi"] >= kapasitas_box["b.stoberi"]:
      print(" ")
      print(" \033[31mKapasitas bibit stoberi sudah full !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jstoberi > list_bibit_buah_sayur["stoberi"]:
      print(" ")
      print(" \033[31mBibit stoberi melebihi batas !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jstoberi <= kapasitas_box["b.stoberi"]:
      print(" ")
      print(" Proses memasukkan bibit stoberi »")
      tas -= jstoberi * kapasitas_tas["stoberi"]
      bluebox["b.stoberi"] += jstoberi
      reward = jstoberi * bonus
      gcoins += reward
      list_bibit_buah_sayur["stoberi"] -= jstoberi
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def loadmelon():
  global tas, gcoins, redb
  
  bonus = 10
  masukmelon = input(" Masukkan jumlah bibit melon yang ingin disimpan »")
  
  try:
    jmelon = int(masukmelon)
    if jmelon <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif list_bibit_buah_sayur["melon"] == 0:
      print(" ")
      print(" \033[31mBibit melon tidak ada !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bluebox["b.melon"] >= kapasitas_box["b.melon"]:
      print(" ")
      print(" \033[31mKapasitas bibit melon sudah full !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jmelon > list_bibit_buah_sayur["melon"]:
      print(" ")
      print(" \033[31mBibit melon melebihi batas !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jmelon <= kapasitas_box["b.melon"]:
      print(" ")
      print(" Proses memasukkan bibit melon »")
      tas -= jmelon * kapasitas_tas["melon"]
      bluebox["b.melon"] += jmelon
      reward = jmelon * bonus
      gcoins += reward
      list_bibit_buah_sayur["melon"] -= jmelon
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)
    
def loadnanas():
  global tas, gcoins, redb
  
  bonus = 10
  masuknanas = input(" Masukkan jumlah bibit stoberi yang ingin disimpan »")
  
  try:
    jnanas = int(masuknanas)
    if jnanas <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif list_bibit_buah_sayur["nanas"] == 0:
      print(" ")
      print(" \033[31mBibit nanas tidak ada !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bluebox["b.nanas"] >= kapasitas_box["b.nanas"]:
      print(" ")
      print(" \033[31mKapasitas bibit nanas sudah full !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jnanas > list_bibit_buah_sayur["nanas"]:
      print(" ")
      print(" \033[31mBibit nanas melebihi batas !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jnanas <= kapasitas_box["b.nanas"]:
      print(" ")
      print(" Proses memasukkan bibit nanas »")
      tas -= jnanas * kapasitas_tas["nanas"]
      bluebox["b.nanas"] += jnanas
      reward = jnanas * bonus
      gcoins += reward
      list_bibit_buah_sayur["nanas"] -= jnanas
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def loadlemon():
  global tas, gcoins, redb
  
  bonus = 10
  masuklemon = input(" Masukkan jumlah bibit lemon yang ingin disimpan »")
  
  try:
    jlemon = int(masuklemon)
    if jlemon <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif list_bibit_buah_sayur["lemon"] == 0:
      print(" ")
      print(" \033[31mBibit lemon tidak ada !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bluebox["b.lemon"] >= kapasitas_box["b.lemon"]:
      print(" ")
      print(" \033[31mKapasitas bibit lemon sudah full !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jlemon > list_bibit_buah_sayur["lemon"]:
      print(" ")
      print(" \033[31mBibit lemon melebihi batas !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jlemon <= kapasitas_box["b.lemon"]:
      print(" ")
      print(" Proses memasukkan bibit lemon »")
      tas -= jlemon * kapasitas_tas["lemon"]
      bluebox["b.lemon"] += jlemon
      reward = jlemon * bonus
      gcoins += reward
      list_bibit_buah_sayur["lemon"] -= jlemon
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def loadjeruk():
  global tas, gcoins, redb
  
  bonus = 10
  masukjeruk = input(" Masukkan jumlah bibit jeruk yang ingin disimpan »")
  
  try:
    jjeruk = int(masukjeruk)
    if jjeruk <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif list_bibit_buah_sayur["jeruk"] == 0:
      print(" ")
      print(" \033[31mBibit jeruk tidak ada !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bluebox["b.jeruk"] >= kapasitas_box["b.jeruk"]:
      print(" ")
      print(" \033[31mKapasitas bibit jeruk sudah full !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jjeruk > list_bibit_buah_sayur["jeruk"]:
      print(" ")
      print(" \033[31mBibit jeruk melebihi batas !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jjeruk <= kapasitas_box["b.jeruk"]:
      print(" ")
      print(" Proses memasukkan bibit jeruk »")
      tas -= jjeruk * kapasitas_tas["jeruk"]
      bluebox["b.jeruk"] += jjeruk
      reward = jjeruk * bonus
      gcoins += reward
      list_bibit_buah_sayur["jeruk"] -= jjeruk
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def loadanggur():
  global tas, gcoins, redb
  
  bonus = 25
  masukanggur = input(" Masukkan jumlah bibit anggur yang ingin disimpan »")
  
  try:
    janggur = int(masukanggur)
    if janggur <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif list_bibit_buah_sayur["anggur"] == 0:
      print(" ")
      print(" \033[31mBibit anggur tidak ada !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bluebox["b.anggur"] >= kapasitas_box["b.anggur"]:
      print(" ")
      print(" \033[31mKapasitas bibit anggur sudah full !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif janggur > list_bibit_buah_sayur["anggur"]:
      print(" ")
      print(" \033[31mBibit anggur melebihi batas !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif janggur <= kapasitas_box["b.anggur"]:
      print(" ")
      print(" Proses memasukkan bibit anggur »")
      tas -= janggur * kapasitas_tas["anggur"]
      bluebox["b.anggur"] += janggur
      reward = janggur * bonus
      gcoins += reward
      list_bibit_buah_sayur["anggur"] -= janggur
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)
  
def loadapelmerah():
  global tas, gcoins, redb
  
  bonus = 25
  masukapelmerah = input(" Masukkan jumlah bibit apel merah yang ingin disimpan »")
  
  try:
    japelmerah = int(masukapelmerah)
    if japelmerah <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif list_bibit_buah_sayur["apel_merah"] == 0:
      print(" ")
      print(" \033[31mBibit apel merah tidak ada !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bluebox["b.apelmerah"] >= kapasitas_box["b.apelmerah"]:
      print(" ")
      print(" \033[31mKapasitas bibit apel merah sudah full !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif japelmerah > list_bibit_buah_sayur["apel_merah"]:
      print(" ")
      print(" \033[31mBibit apel merah melebihi batas !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif japelmerah <= kapasitas_box["b.apelmerah"]:
      print(" ")
      print(" Proses memasukkan bibit apel merah »")
      tas -= japelmerah * kapasitas_tas["apel_merah"]
      bluebox["b.apelmerah"] += japelmerah
      reward = japelmerah * bonus
      gcoins += reward
      list_bibit_buah_sayur["apel_merah"] -= japelmerah
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)
  
def loadapelhijau():
  global tas, gcoins, redb
  
  bonus = 25
  masukapelhijau = input(" Masukkan jumlah bibit apel hijau yang ingin disimpan »")
  
  try:
    japelhijau = int(masukapelhijau)
    if japelhijau <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif list_bibit_buah_sayur["apel_hijau"] == 0:
      print(" ")
      print(" \033[31mBibit apel hijau tidak ada !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bluebox["b.apelhijau"] >= kapasitas_box["b.apelhijau"]:
      print(" ")
      print(" \033[31mKapasitas bibit apel hijau sudah full !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif japelhijau > list_bibit_buah_sayur["apel_hijau"]:
      print(" ")
      print(" \033[31mBibit apel hijau melebihi batas !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif japelhijau <= kapasitas_box["b.apelhijau"]:
      print(" ")
      print(" Proses memasukkan bibit apel hijau »")
      tas -= japelhijau * kapasitas_tas["apelhijau"]
      bluebox["b.apelhijau"] += japelhijau
      reward = japelhijau * bonus
      gcoins += reward
      list_bibit_buah_sayur["apel_hijau"] -= japelhijau
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)
  
def loadpir():
  global tas, gcoins, redb
  
  bonus = 25
  masukpir = input(" Masukkan jumlah bibit pir yang ingin disimpan »")
  
  try:
    jpir = int(masukpir)
    if jpir <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif list_bibit_buah_sayur["pir"] == 0:
      print(" ")
      print(" \033[31mBibit pir tidak ada !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bluebox["b.pir"] >= kapasitas_box["b.pir"]:
      print(" ")
      print(" \033[31mKapasitas bibit pir sudah full !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jpir > list_bibit_buah_sayur["pir"]:
      print(" ")
      print(" \033[31mBibit pir melebihi batas !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jpir <= kapasitas_box["b.pir"]:
      print(" ")
      print(" Proses memasukkan bibit pir »")
      tas -= jpir * kapasitas_tas["pir"]
      bluebox["b.pir"] += jpir
      reward = jpir * bonus
      gcoins += reward
      list_bibit_buah_sayur["pir"] -= jpir
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)
  
def loadmangga():
  global tas, gcoins, redb
  
  bonus = 25
  masukmangga = input(" Masukkan jumlah bibit mangga yang ingin disimpan »")
  
  try:
    jmangga = int(masukmangga)
    if jmangga <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif list_bibit_buah_sayur["mangga"] == 0:
      print(" ")
      print(" \033[31mBibit mangga tidak ada !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif bluebox["b.mangga"] >= kapasitas_box["b.mangga"]:
      print(" ")
      print(" \033[31mKapasitas bibit mangga sudah full !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jmangga > list_bibit_buah_sayur["mangga"]:
      print(" ")
      print(" \033[31mBibit mangga melebihi batas !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif jmangga <= kapasitas_box["b.mangga"]:
      print(" ")
      print(" Proses memasukkan bibit mangga »")
      tas -= jmangga * kapasitas_tas["mangga"]
      bluebox["b.mangga"] += jmangga
      reward = jmangga * bonus
      gcoins += reward
      list_bibit_buah_sayur["mangga"] -= jmangga
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)
    
def loadbuahstoberi():
  global tas, kayu, gcoins, redb
  
  ob = list_buah_sayur
  bonus = 25
  m_buahstoberi = input(" Masukkan jumlah buah stoberi yang ingin disimpan »")
  
  try:
    jb_stoberi = int(m_buahstoberi)
    if jb_stoberi <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif ob["stoberi"] == 0:
      print(" ")
      print(" \033[31mBuah stoberi tidak ada !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif bluebox["buah.stoberi"] >= kapasitas_box["buah.stoberi"]:
      print(" ")
      print(" \033[31mKapasitas buah stoberi sudah full !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_stoberi > ob["stoberi"]:
      print(" ")
      print(" \033[31mBuah stoberi melebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_stoberi <= kapasitas_box["buah.stoberi"]:
      print(" ")
      print(" Proses memasukkan buah stoberi »")
      tas -= jb_stoberi * kapasitas_tas["buah.stoberi"]
      bluebox["buah.stoberi"] += jb_stoberi
      reward = jb_stoberi * bonus
      gcoins += reward
      ob["stoberi"] -= jb_stoberi
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def loadbuahmelon():
  global tas, kayu, gcoins, redb
  
  ob = list_buah_sayur
  bonus = 25
  m_buahmelon = input(" Masukkan jumlah buah melon yang ingin disimpan »")
  
  try:
    jb_melon = int(m_buahmelon)
    if jb_melon <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif ob["melon"] == 0:
      print(" ")
      print(" \033[31mBuah melon tidak ada !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif bluebox["buah.melon"] >= kapasitas_box["buah.melon"]:
      print(" ")
      print(" \033[31mKapasitas buah melon sudah full !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_melon > ob["melon"]:
      print(" ")
      print(" \033[31mBuah melon melebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_melon <= kapasitas_box["buah.melon"]:
      print(" ")
      print(" Proses memasukkan buah melon »")
      tas -= jb_melon * kapasitas_tas["buah.melon"]
      bluebox["buah.melon"] += jb_melon
      reward = jb_melon * bonus
      gcoins += reward
      ob["melon"] -= jb_melon
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def loadbuahnanas():
  global tas, kayu, gcoins, redb
  
  ob = list_buah_sayur
  bonus = 25
  m_buahnanas = input(" Masukkan jumlah buah nanas yang ingin disimpan »")
  
  try:
    jb_nanas = int(m_buahnanas)
    if jb_nanas <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif ob["nanas"] == 0:
      print(" ")
      print(" \033[31mBuah nanas tidak ada !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif bluebox["buah.nanas"] >= kapasitas_box["buah.nanas"]:
      print(" ")
      print(" \033[31mKapasitas buah nanas sudah full !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_nanas > ob["nanas"]:
      print(" ")
      print(" \033[31mBuah nanas melebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_nanas <= kapasitas_box["buah.nanas"]:
      print(" ")
      print(" Proses memasukkan buah nanas »")
      tas -= jb_nanas * kapasitas_tas["buah.nanas"]
      bluebox["buah.nanas"] += jb_nanas
      reward = jb_nanas * bonus
      gcoins += reward
      ob["nanas"] -= jb_nanas
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def loadbuahlemon():
  global tas, kayu, gcoins, redb
  
  ob = list_buah_sayur
  bonus = 25
  m_buahlemon = input(" Masukkan jumlah buah lemon yang ingin disimpan »")
  
  try:
    jb_lemon = int(m_buahlemon)
    if jb_lemon <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif ob["lemon"] == 0:
      print(" ")
      print(" \033[31mBuah lemon tidak ada !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif bluebox["buah.lemon"] >= kapasitas_box["buah.lemon"]:
      print(" ")
      print(" \033[31mKapasitas buah lemon sudah full !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_lemon > ob["lemon"]:
      print(" ")
      print(" \033[31mBuah lemon melebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_lemon <= kapasitas_box["buah.lemon"]:
      print(" ")
      print(" Proses memasukkan buah lemon »")
      tas -= jb_lemon * kapasitas_tas["buah.lemon"]
      bluebox["buah.lemon"] += jb_lemon
      reward = jb_lemon * bonus
      gcoins += reward
      ob["lemon"] -= jb_lemon
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def loadbuahjeruk():
  global tas, kayu, gcoins, redb
  
  ob = list_buah_sayur
  bonus = 25
  m_buahjeruk = input(" Masukkan jumlah buah jeruk yang ingin disimpan »")
  
  try:
    jb_jeruk = int(m_buahjeruk)
    if jb_jeruk <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif ob["jeruk"] == 0:
      print(" ")
      print(" \033[31mBuah jeruk tidak ada !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif bluebox["buah.jeruk"] >= kapasitas_box["buah.jeruk"]:
      print(" ")
      print(" \033[31mKapasitas buah jeruk sudah full !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_jeruk > ob["jeruk"]:
      print(" ")
      print(" \033[31mBuah jeruk melebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_jeruk <= kapasitas_box["buah.jeruk"]:
      print(" ")
      print(" Proses memasukkan buah jeruk »")
      tas -= jb_jeruk * kapasitas_tas["buah.jeruk"]
      bluebox["buah.jeruk"] += jb_jeruk
      reward = jb_jeruk * bonus
      gcoins += reward
      ob["jeruk"] -= jb_jeruk
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
    
def loadbuahanggur():
  global tas, kayu, gcoins, redb
  
  ob = list_buah_sayur
  bonus = 25
  m_buahanggur = input(" Masukkan jumlah buah anggur yang ingin disimpan »")
  
  try:
    jb_anggur = int(m_buahanggur)
    if jb_anggur <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif ob["anggur"] == 0:
      print(" ")
      print(" \033[31mBuah anggur tidak ada !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif bluebox["buah.anggur"] >= kapasitas_box["buah.anggur"]:
      print(" ")
      print(" \033[31mKapasitas buah anggur sudah full !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_anggur > ob["anggur"]:
      print(" ")
      print(" \033[31mBuah anggur melebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_anggur <= kapasitas_box["buah.anggur"]:
      print(" ")
      print(" Proses memasukkan buah anggur »")
      tas -= jb_anggur * kapasitas_tas["buah.anggur"]
      bluebox["buah.anggur"] += jb_anggur
      reward = jb_anggur * bonus
      gcoins += reward
      ob["anggur"] -= jb_anggur
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def loadbuahapelmerah():
  global tas, kayu, gcoins, redb
  
  ob = list_buah_sayur
  bonus = 25
  m_buahapelmerah = input(" Masukkan jumlah buah apel merah yang ingin disimpan »")
  
  try:
    jb_apelmerah = int(m_buahapelmerah)
    if jb_apelmerah <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif ob["apel_merah"] == 0:
      print(" ")
      print(" \033[31mBuah apel merah tidak ada !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif bluebox["buah.apelmerah"] >= kapasitas_box["buah.apelmerah"]:
      print(" ")
      print(" \033[31mKapasitas buah apel merah sudah full !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_apelmerah > ob["apel_merah"]:
      print(" ")
      print(" \033[31mBuah apel merah melebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_apelmerah <= kapasitas_box["buah.apelmerah"]:
      print(" ")
      print(" Proses memasukkan buah apel merah »")
      tas -= jb_apelmerah * kapasitas_tas["buah.apelmerah"]
      bluebox["buah.apelmerah"] += jb_apelmerah
      reward = jb_apelmerah * bonus
      gcoins += reward
      ob["apel_merah"] -= jb_apelmerah
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def loadbuahapelhijau():
  global tas, kayu, gcoins, redb
  
  ob = list_buah_sayur
  bonus = 25
  m_buahapelhijau = input(" Masukkan jumlah buah apel hijau yang ingin disimpan »")
  
  try:
    jb_apelhijau = int(m_buahapelhijau)
    if jb_apelhijau <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif ob["apel_hijau"] == 0:
      print(" ")
      print(" \033[31mBuah apel hijau tidak ada !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif bluebox["buah.apelhijau"] >= kapasitas_box["buah.apelhijau"]:
      print(" ")
      print(" \033[31mKapasitas buah apel hijau sudah full !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_apelhijau > ob["apel_hijau"]:
      print(" ")
      print(" \033[31mBuah apel hijau melebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_apelhijau <= kapasitas_box["buah.apelhijau"]:
      print(" ")
      print(" Proses memasukkan buah apel hijau »")
      tas -= jb_apelhijau * kapasitas_tas["buah.apelhijau"]
      bluebox["buah.apelhijau"] += jb_apelhijau
      reward = jb_apelhijau * bonus
      gcoins += reward
      ob["apel_hijau"] -= jb_apelhijau
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def loadbuahpir():
  global tas, kayu, gcoins, redb
  
  ob = list_buah_sayur
  bonus = 25
  m_buahpir = input(" Masukkan jumlah buah pir yang ingin disimpan »")
  
  try:
    jb_pir = int(m_buahpir)
    if jb_pir <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif ob["pir"] == 0:
      print(" ")
      print(" \033[31mBuah pir tidak ada !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif bluebox["buah.pir"] >= kapasitas_box["buah.pir"]:
      print(" ")
      print(" \033[31mKapasitas buah pir sudah full !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_pir > ob["pir"]:
      print(" ")
      print(" \033[31mBuah pir melebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_pir <= kapasitas_box["buah.pir"]:
      print(" ")
      print(" Proses memasukkan buah pir »")
      tas -= jb_pir * kapasitas_tas["buah.pir"]
      bluebox["buah.pir"] += jb_pir
      reward = jb_pir * bonus
      gcoins += reward
      ob["pir"] -= jb_pir
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def loadbuahmangga():
  global tas, kayu, gcoins, redb
  
  ob = list_buah_sayur
  bonus = 25
  m_buahmangga = input(" Masukkan jumlah buah mangga yang ingin disimpan »")
  
  try:
    jb_mangga = int(m_buahmangga)
    if jb_mangga <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif ob["mangga"] == 0:
      print(" ")
      print(" \033[31mBuah mangga tidak ada !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif bluebox["buah.mangga"] >= kapasitas_box["buah.mangga"]:
      print(" ")
      print(" \033[31mKapasitas buah mangga sudah full !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_mangga > ob["mangga"]:
      print(" ")
      print(" \033[31mBuah mangga melebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif jb_mangga <= kapasitas_box["buah.mangga"]:
      print(" ")
      print(" Proses memasukkan buah mangga »")
      tas -= jb_mangga * kapasitas_tas["buah.mangga"]
      bluebox["buah.mangga"] += jb_mangga
      reward = jb_mangga * bonus
      gcoins += reward
      ob["mangga"] -= jb_mangga
      time.sleep(1.23)
      print(" ")
      print(f" \033[32mSukses menyimpan ✓ +{reward} Gcoins ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)

###1   
def ambilkayu():
  global tas, kayu, redb, kapasitas_tas
  
  print(" ")
  ambilkayu = input(" Masukkan jumlah kayu T.1/2(0) yang ingin diambil ? ")
  
  try:
    tlkayu = int(ambilkayu)
    totalkap = kapasitas_tas["kayu"] * tlkayu
    if tlkayu <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(1.23)
    elif bluebox["kayu"] == 0:
      print(" ")
      print(" \033[31mKayu T.1/2(0) tidak ada !\033[0m ")
      redb["y"] += 1
      time.sleep(0.345)
    elif tlkayu > bluebox["kayu"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil kayu T.1/2(0) »")
      time.sleep(0.6)
      bluebox["kayu"] -= tlkayu
      tas += tlkayu * kapasitas_tas["kayu"]
      kayu += tlkayu
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)
      
def ambilkayu1():  
  global tas, kayuT1, redb, kapasitas_tas
  
  print(" ")
  ambilkayu1 = input(" Masukkan jumlah kayu T.1 yang ingin diambil ? ")
  
  try:
    tlkayu1 = int(ambilkayu1)
    totalkap = kapasitas_tas["kayuT1"] * tlkayu1
    if tlkayu1 <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(1.23)
    elif bluebox["kayuT1"] == 0:
      print(" ")
      print(" \033[31mKayu T.1 tidak ada !\033[0m ")
      redb["y"] += 1
      time.sleep(0.345)
    elif tlkayu1 > bluebox["kayuT1"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil kayu T.1 »")
      time.sleep(0.6)
      bluebox["kayuT1"] -= tlkayu1
      tas += tlkayu1 * kapasitas_tas["kayuT1"]
      kayuT1 += tlkayu1
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)
  
def ambilkayu2():
  global tas, kayuT2, redb, kapasitas_tas
  
  print(" ")
  ambilkayu2 = input(" Masukkan jumlah kayu T.2 yang ingin diambil ? ")
  
  try:
    tlkayu2 = int(ambilkayu2)
    totalkap = kapasitas_tas["kayuT2"] * tlkayu2
    if tlkayu2 <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(1.23)
    elif bluebox["kayuT2"] == 0:
      print(" ")
      print(" \033[31mKayu T.2 tidak ada !\033[0m ")
      redb["y"] += 1
      time.sleep(0.345)
    elif tlkayu2 > bluebox["kayuT2"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil kayu T2 »")
      time.sleep(0.6)
      bluebox["kayuT2"] -= tlkayu2
      tas += tlkayu2 * kapasitas_tas["kayuT2"]
      kayuT2 += tlkayu2
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def ambilbibit():  
  global tas, bibit, redb, kapasitas_tas
  
  print(" ")
  ambilbibit = input(" Masukkan jumlah bibit T.1 yang ingin diambil ? ")
  
  try:
    tlbibit = int(ambilbibit)
    totalkap = kapasitas_tas["bibit"] * tlbibit
    if tlbibit <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(1.23)
    elif bluebox["bibit"] == 0:
      print(" ")
      print(" \033[31mBibit T.1 tidak ada !\033[0m ")
      redb["y"] += 1
      time.sleep(0.345)
    elif tlbibit > bluebox["bibit"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil bibit T.1 »")
      time.sleep(0.6)
      bluebox["bibit"] -= tlbibit
      tas += tlbibit * kapasitas_tas["bibit"]
      bibit += tlbibit
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def ambilbibit2():  
  global tas, bibit2, redb, kapasitas_tas
  
  print(" ")
  ambilbibit2 = input(" Masukkan jumlah bibit T.2 yang ingin diambil ? ")
  
  try:
    tlbibit2 = int(ambilbibit2)
    totalkap = kapasitas_tas["bibit2"] * tlbibit2
    if tlbibit2 <= 0:
      print(" ")
      print(" \033[31minvalid !\033[0m")
      redb["y"] += 1
      time.sleep(1.23)
    elif bluebox["bibit2"] == 0:
      print(" ")
      print(" \033[31mBibit T.2 tidak ada !\033[0m ")
      redb["y"] += 1
      time.sleep(0.345)
    elif tlbibit2 > bluebox["bibit2"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil bibit T.2 »")
      time.sleep(0.6)
      bluebox["bibit2"] -= tlbibit2
      tas += tlbibit2 * kapasitas_tas["bibit2"]
      bibit2 += tlbibit2
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def ambilstoberi():
  global tas, redb, list_bibit_buah_sayur, kapasitas_tas
  
  print(" ")
  ambilstoberi = input(" Masukkan jumlah bibit stoberi yang ingin diambil ? ")
  
  try:
    tlstoberi = int(ambilstoberi)
    totalkap = kapasitas_tas["stoberi"] * tlstoberi
    if tlstoberi <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(1.23)
    elif bluebox["b.stoberi"] == 0:
      print(" ")
      print(" \033[31mBibit stoberi tidak ada !\033[0m ")
      redb["y"] += 1
      time.sleep(0.345)
    elif tlstoberi > bluebox["b.stoberi"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil bibit stoberi »")
      time.sleep(0.6)
      bluebox["b.stoberi"] -= tlstoberi
      tas += tlstoberi * kapasitas_tas["stoberi"]
      list_bibit_buah_sayur["stoberi"] += tlstoberi
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def ambilmelon():
  global tas, redb, list_bibit_buah_sayur, kapasitas_tas
  
  print(" ")
  ambilmelon = input(" Masukkan jumlah bibit melon yang ingin diambil ? ")
  
  try:
    tlmelon = int(ambilmelon)
    totalkap = kapasitas_tas["melon"] * tlmelon
    if tlmelon <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(1.23)
    elif bluebox["b.melon"] == 0:
      print(" ")
      print(" \033[31mBibit melon tidak ada !\033[0m ")
      redb["y"] += 1
      time.sleep(0.345)
    elif tlmelon > bluebox["b.melon"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil bibit melon »")
      time.sleep(0.6)
      bluebox["b.melon"] -= tlmelon
      tas += tlmelon * kapasitas_tas["melon"]
      list_bibit_buah_sayur["melon"] += tlmelon
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def ambilnanas():
  global tas, redb, list_bibit_buah_sayur, kapasitas_tas
  
  print(" ")
  ambilnanas = input(" Masukkan jumlah bibit nanas yang ingin diambil ? ")
  
  try:
    tlnanas = int(ambilnanas)
    totalkap = kapasitas_tas["nanas"] * tlnanas
    if tlnanas <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(1.23)
    elif bluebox["b.nanas"] == 0:
      print(" ")
      print(" \033[31mBibit nanas tidak ada !\033[0m ")
      redb["y"] += 1
      time.sleep(0.345)
    elif tlnanas > bluebox["b.nanas"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil bibit nanas »")
      time.sleep(0.6)
      bluebox["b.nanas"] -= tlnanas
      tas += tlnanas * kapasitas_tas["nanas"]
      list_bibit_buah_sayur["nanas"] += tlnanas
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def ambillemon():
  global tas, redb, list_bibit_buah_sayur, kapasitas_tas
  
  print(" ")
  ambillemon = input(" Masukkan jumlah bibit lemon yang ingin diambil ? ")
  
  try:
    tllemon = int(ambillemon)
    totalkap = kapasitas_tas["lemon"] * tllemon
    if tllemon <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(1.23)
    elif bluebox["b.lemon"] == 0:
      print(" ")
      print(" \033[31mBibit lemon tidak ada !\033[0m ")
      redb["y"] += 1
      time.sleep(0.345)
    elif tllemon > bluebox["b.lemon"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil bibit lemon »")
      time.sleep(0.6)
      bluebox["b.lemon"] -= tllemon
      tas += tllemon * kapasitas_tas["lemon"]
      list_bibit_buah_sayur["lemon"] += tllemon
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def ambiljeruk():
  global tas, redb, list_bibit_buah_sayur, kapasitas_tas
  
  print(" ")
  ambiljeruk = input(" Masukkan jumlah bibit jeruk yang ingin diambil ? ")
  
  try:
    tljeruk = int(ambiljeruk)
    totalkap = kapasitas_tas["jeruk"] * tljeruk
    if tljeruk <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(1.23)
    elif bluebox["b.jeruk"] == 0:
      print(" ")
      print(" \033[31mBibit jeruk tidak ada !\033[0m ")
      redb["y"] += 1
      time.sleep(0.345)
    elif tljeruk > bluebox["b.jeruk"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil bibit jeruk »")
      time.sleep(0.6)
      bluebox["b.jeruk"] -= tljeruk
      tas += tljeruk * kapasitas_tas["jeruk"]
      list_bibit_buah_sayur["jeruk"] += tljeruk
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def ambilanggur():
  global tas, redb, list_bibit_buah_sayur, kapasitas_tas
  
  print(" ")
  ambilanggur = input(" Masukkan jumlah bibit anggur yang ingin diambil ? ")
  
  try:
    tlanggur = int(ambilanggur)
    totalkap = kapasitas_tas["anggur"] * tlanggur
    if tlanggur <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(1.23)
    elif bluebox["b.anggur"] == 0:
      print(" ")
      print(" \033[31mBibit anggur tidak ada !\033[0m ")
      redb["y"] += 1
      time.sleep(0.345)
    elif tlanggur > bluebox["b.anggur"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil bibit anggur »")
      time.sleep(0.6)
      bluebox["b.anggur"] -= tlanggur
      tas += tlanggur * kapasitas_tas["anggur"]
      list_bibit_buah_sayur["anggur"] += tlanggur
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def ambilapelmerah():
  global tas, redb, list_bibit_buah_sayur, kapasitas_tas
  
  print(" ")
  ambilapelmerah = input(" Masukkan jumlah bibit apel merah yang ingin diambil ? ")
  
  try:
    tlapelmerah = int(ambilapelmerah)
    totalkap = kapasitas_tas["apel_merah"] * tlapelmerah
    if tlapelmerah <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(1.23)
    elif bluebox["b.apelmerah"] == 0:
      print(" ")
      print(" \033[31mBibit apel merah tidak ada !\033[0m ")
      redb["y"] += 1
      time.sleep(0.345)
    elif tlapelmerah > bluebox["b.apelmerah"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil bibit apel merah »")
      time.sleep(0.6)
      bluebox["b.apelmerah"] -= tlapelmerah
      tas += tlapelmerah * kapasitas_tas["apel_merah"]
      list_bibit_buah_sayur["apel_merah"] += tlapelmerah
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def ambilapelhijau():
  global tas, redb, list_bibit_buah_sayur, kapasitas_tas
  
  print(" ")
  ambilapelhijau = input(" Masukkan jumlah bibit apel hijau yang ingin diambil ? ")
  
  try:
    tlapelhijau = int(ambilapelhijau)
    totalkap = kapasitas_tas["apel_hijau"] * tlapelhijau
    if tlapelhijau <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(1.23)
    elif bluebox["b.apelhijau"] == 0:
      print(" ")
      print(" \033[31mBibit apel hijau tidak ada !\033[0m ")
      redb["y"] += 1
      time.sleep(0.345)
    elif tlapelhijau > bluebox["b.apelhijau"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil bibit apel hijau »")
      time.sleep(0.6)
      bluebox["b.apelhijau"] -= tlapelhijau
      tas += tlapelhijau * kapasitas_tas["apel_hijau"]
      list_bibit_buah_sayur["apel_hijau"] += tlapelhijau
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def ambilpir():
  global tas, redb, list_bibit_buah_sayur, kapasitas_tas
  
  print(" ")
  ambilpir = input(" Masukkan jumlah bibit apel merah yang ingin diambil ? ")
  
  try:
    tlpir = int(ambilpir)
    totalkap = kapasitas_tas["pir"] * tlpir
    if tlpir <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(1.23)
    elif bluebox["b.pir"] == 0:
      print(" ")
      print(" \033[31mBibit pir tidak ada !\033[0m ")
      redb["y"] += 1
      time.sleep(0.345)
    elif tlpir > bluebox["b.pir"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil bibit pir »")
      time.sleep(0.6)
      bluebox["b.pir"] -= tlpir
      tas += tlpir * kapasitas_tas["pir"]
      list_bibit_buah_sayur["pir"] += tlpir
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def ambilmangga():
  global tas, redb, list_bibit_buah_sayur, kapasitas_tas
  
  print(" ")
  ambilmangga = input(" Masukkan jumlah bibit mangga yang ingin diambil ? ")
  
  try:
    tlmangga = int(ambilmangga)
    totalkap = kapasitas_tas["mangga"] * tlmangga
    if tlmangga <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y"] += 1
      time.sleep(1.23)
    elif bluebox["b.mangga"] == 0:
      print(" ")
      print(" \033[31mBibit mangga tidak ada !\033[0m ")
      redb["y"] += 1
      time.sleep(0.345)
    elif tlmangga > bluebox["b.mangga"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil bibit mangga »")
      time.sleep(0.6)
      bluebox["b.mangga"] -= tlmangga
      tas += tlmangga * kapasitas_tas["mangga"]
      list_bibit_buah_sayur["mangga"] += tlmangga
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y"] += 1
    time.sleep(0.345)

def ambilbuahstoberi():
  global tas, redb, list_buah_sayur, kapasitas_tas
  
  print(" ")
  ab_stoberi = input(" Masukkan jumlah buah stoberi yang ingin diambil ? ")
  
  try:
    tlb_stoberi = int(ab_stoberi)
    totalkap = kapasitas_tas["buah.stoberi"] * tlb_stoberi
    if tlb_stoberi <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(1.23)
    elif bluebox["buah.stoberi"] == 0:
      print(" ")
      print(" \033[31mBuah stoberi tidak ada !\033[0m ")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tlb_stoberi > bluebox["buah.stoberi"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil buah stoberi »")
      time.sleep(0.6)
      bluebox["buah.stoberi"] -= tlb_stoberi
      tas += tlb_stoberi * kapasitas_tas["buah.stoberi"]
      list_buah_sayur["stoberi"] += tlb_stoberi
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def ambilbuahmelon():
  global tas, redb, list_buah_sayur, kapasitas_tas
  
  print(" ")
  ab_melon = input(" Masukkan jumlah buah melon yang ingin diambil ? ")
  
  try:
    tlb_melon = int(ab_melon)
    totalkap = kapasitas_tas["buah.melon"] * tlb_melon
    if tlb_melon <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(1.23)
    elif bluebox["buah.melon"] == 0:
      print(" ")
      print(" \033[31mBuah melon tidak ada !\033[0m ")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tlb_melon > bluebox["buah.melon"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil buah melon »")
      time.sleep(0.6)
      bluebox["buah.melon"] -= tlb_melon
      tas += tlb_melon * kapasitas_tas["buah.melon"]
      list_buah_sayur["melon"] += tlb_melon
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def ambilbuahnanas():
  global tas, redb, list_buah_sayur, kapasitas_tas
  
  print(" ")
  ab_nanas = input(" Masukkan jumlah buah nanas yang ingin diambil ? ")
  
  try:
    tlb_nanas = int(ab_nanas)
    totalkap = kapasitas_tas["buah.nanas"] * tlb_nanas
    if tlb_nanas <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(1.23)
    elif bluebox["buah.nanas"] == 0:
      print(" ")
      print(" \033[31mBuah nanas tidak ada !\033[0m ")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tlb_nanas > bluebox["buah.nanas"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil buah nanas »")
      time.sleep(0.6)
      bluebox["buah.nanas"] -= tlb_nanas
      tas += tlb_nanas * kapasitas_tas["buah.nanas"]
      list_buah_sayur["nanas"] += tlb_nanas
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def ambilbuahlemon():
  global tas, redb, list_buah_sayur, kapasitas_tas
  
  print(" ")
  ab_lemon = input(" Masukkan jumlah buah lemon yang ingin diambil ? ")
  
  try:
    tlb_lemon = int(ab_lemon)
    totalkap = kapasitas_tas["buah.lemon"] * tlb_lemon
    if tlb_lemon <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(1.23)
    elif bluebox["buah.lemon"] == 0:
      print(" ")
      print(" \033[31mBuah lemon tidak ada !\033[0m ")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tlb_lemon > bluebox["buah.lemon"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil buah lemon »")
      time.sleep(0.6)
      bluebox["buah.lemon"] -= tlb_lemon
      tas += tlb_lemon * kapasitas_tas["buah.lemon"]
      list_buah_sayur["lemon"] += tlb_lemon
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def ambilbuahjeruk():
  global tas, redb, list_buah_sayur, kapasitas_tas
  
  print(" ")
  ab_jeruk = input(" Masukkan jumlah buah jeruk yang ingin diambil ? ")
  
  try:
    tlb_jeruk = int(ab_jeruk)
    totalkap = kapasitas_tas["buah.jeruk"] * tlb_jeruk
    if tlb_jeruk <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(1.23)
    elif bluebox["buah.jeruk"] == 0:
      print(" ")
      print(" \033[31mBuah jeruk tidak ada !\033[0m ")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tlb_jeruk > bluebox["buah.jeruk"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil buah jeruk »")
      time.sleep(0.6)
      bluebox["buah.jeruk"] -= tlb_jeruk
      tas += tlb_jeruk * kapasitas_tas["buah.jeruk"]
      list_buah_sayur["jeruk"] += tlb_jeruk
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def ambilbuahanggur():
  global tas, redb, list_buah_sayur, kapasitas_tas
  
  print(" ")
  ab_anggur = input(" Masukkan jumlah buah anggur yang ingin diambil ? ")
  
  try:
    tlb_anggur = int(ab_anggur)
    totalkap = kapasitas_tas["buah.anggur"] * tlb_anggur
    if tlb_anggur <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(1.23)
    elif bluebox["buah.anggur"] == 0:
      print(" ")
      print(" \033[31mBuah anggur tidak ada !\033[0m ")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tlb_anggur > bluebox["buah.anggur"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil buah anggur »")
      time.sleep(0.6)
      bluebox["buah.anggur"] -= tlb_anggur
      tas += tlb_anggur * kapasitas_tas["buah.anggur"]
      list_buah_sayur["anggur"] += tlb_anggur
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def ambilbuahapelmerah():
  global tas, redb, list_buah_sayur, kapasitas_tas
  
  print(" ")
  ab_apelmerah = input(" Masukkan jumlah buah apel merah yang ingin diambil ? ")
  
  try:
    tlb_apelmerah = int(ab_apelmerah)
    totalkap = kapasitas_tas["buah.apelmerah"] * tlb_apelmerah
    if tlb_apelmerah <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(1.23)
    elif bluebox["buah.apelmerah"] == 0:
      print(" ")
      print(" \033[31mBuah apel merah tidak ada !\033[0m ")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tlb_apelmerah > bluebox["buah.apelmerah"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil buah apel merah »")
      time.sleep(0.6)
      bluebox["buah.apelmerah"] -= tlb_apelmerah
      tas += tlb_apelmerah * kapasitas_tas["buah.apelmerah"]
      list_buah_sayur["apel_merah"] += tlb_apelmerah
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def ambilbuahapelhijau():
  global tas, redb, list_buah_sayur, kapasitas_tas
  
  print(" ")
  ab_apelhijau = input(" Masukkan jumlah buah apel hijau yang ingin diambil ? ")
  
  try:
    tlb_apelhijau = int(ab_apelhijau)
    totalkap = kapasitas_tas["buah.apelhijau"] * tlb_apelhijau
    if tlb_apelhijau <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(1.23)
    elif bluebox["buah.apelhijau"] == 0:
      print(" ")
      print(" \033[31mBuah apel hijau tidak ada !\033[0m ")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tlb_apelhijau > bluebox["buah.apelhijau"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil buah apel hijau »")
      time.sleep(0.6)
      bluebox["buah.apelhijau"] -= tlb_apelhijau
      tas += tlb_apelhijau * kapasitas_tas["buah.apelhijau"]
      list_buah_sayur["apel_hijau"] += tlb_apelhijau
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def ambilbuahpir():
  global tas, redb, list_buah_sayur, kapasitas_tas
  
  print(" ")
  ab_pir = input(" Masukkan jumlah buah pir yang ingin diambil ? ")
  
  try:
    tlb_pir = int(ab_pir)
    totalkap = kapasitas_tas["buah.pir"] * tlb_pir
    if tlb_pir <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(1.23)
    elif bluebox["buah.pir"] == 0:
      print(" ")
      print(" \033[31mBuah pir tidak ada !\033[0m ")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tlb_pir > bluebox["buah.pir"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil buah pir »")
      time.sleep(0.6)
      bluebox["buah.pir"] -= tlb_pir
      tas += tlb_pir * kapasitas_tas["buah.pir"]
      list_buah_sayur["pir"] += tlb_pir
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)
  
def ambilbuahmangga():
  global tas, redb, list_buah_sayur, kapasitas_tas
  
  print(" ")
  ab_mangga = input(" Masukkan jumlah buah mangga yang ingin diambil ? ")
  
  try:
    tlb_mangga = int(ab_mangga)
    totalkap = kapasitas_tas["buah.mangga"] * tlb_mangga
    if tlb_mangga <= 0:
      print(" ")
      print(" \033[31mInvalid !\033[0m")
      redb["y1"] += 1
      time.sleep(1.23)
    elif bluebox["buah.mangga"] == 0:
      print(" ")
      print(" \033[31mBuah mangga tidak ada !\033[0m ")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tlb_mangga > bluebox["buah.mangga"]:
      print(" ")
      print(" \033[31mmelebihi batas !\033[31m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap <= 100:
      print(" ")
      print(" Proses mengambil buah mangga »")
      time.sleep(0.6)
      bluebox["buah.mangga"] -= tlb_mangga
      tas += tlb_mangga * kapasitas_tas["buah.mangga"]
      list_buah_sayur["mangga"] += tlb_mangga
      print(" ")
      print(" \033[32mSukses ✓\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
    elif tas + totalkap > 100:
      print(" ")
      print(" \033[31mTas kamu penuh !\033[0m")
      redb["y1"] += 1
      time.sleep(0.345)
  except ValueError:
    print(" ")
    print(" \033[31mInput salah !\033[0m")
    redb["y1"] += 1
    time.sleep(0.345)

def tanambibitbuah():
  global tas, Hp, exp
  kor = (userx1, usery1)
  lhn = k_lahan
  #kor_bibit
  tn1 = tanam
  tn2 = tanam
  tn3 = tanam_bibit_buah["tanam.bibit.stoberi"]
  tn4 = tanam_bibit_buah["tanam.bibit.melon"]
  tn5 = tanam_bibit_buah["tanam.bibit.nanas"]
  tn6 = tanam_bibit_buah["tanam.bibit.lemon"]
  tn7 = tanam_bibit_buah["tanam.bibit.jeruk"]
  tn8 = tanam_bibit_buah["tanam.bibit.anggur"]
  tn9 = tanam_bibit_buah["tanam.bibit.apelmerah"]
  tn10 = tanam_bibit_buah["tanam.bibit.apelhijau"]
  tn11 = tanam_bibit_buah["tanam.bibit.pir"]
  tn12 = tanam_bibit_buah["tanam.bibit.mangga"]
  #kor_buah
  pn1 = pohon_tanam
  pn2 = pohon_tanam2
  pn3 = tanam_bibit_buah["panen.buah.stoberi"]
  pn4 = tanam_bibit_buah["panen.buah.melon"]
  pn5 = tanam_bibit_buah["panen.buah.nanas"]
  pn6 = tanam_bibit_buah["panen.buah.lemon"]
  pn7 = tanam_bibit_buah["panen.buah.jeruk"]
  pn8 = tanam_bibit_buah["panen.buah.anggur"]
  pn9 = tanam_bibit_buah["panen.buah.apelmerah"]
  pn10 = tanam_bibit_buah["panen.buah.apelhijau"]
  pn11 = tanam_bibit_buah["panen.buah.pir"]
  pn12 = tanam_bibit_buah["panen.buah.mangga"]
  
  while True:
    os.system("clear")
    print(" ")
    print(" \033[36mUntuk menanam bibit\033[0m : ")
    print(" ")
    print(" \033[32mStoberi\033[0m »(s)   \033[32mAnggur\033[0m     »(a)")
    print(" \033[32mMelon\033[0m   »(m)   \033[32mApel merah\033[0m »(1)")
    print(" \033[32mNanas\033[0m   »(n)   \033[32mApel hijau\033[0m »(2)")
    print(" \033[32mLemon\033[0m   »(l)   \033[32mPir\033[0m        »(p)")
    print(" \033[32mJeruk\033[0m   »(j)   \033[32mMangga\033[0m     »(0)")
    print(" ")
    print(" Keluar     »(x)")
    print(" ")
    cmd = _getch()
    
    if cmd == "s":
      if pos in lhn:
        if pos in tn3 or pos in pn3:
          print(" ")
          print(" \033[33mSudah ada tanaman !\033[0m")
          time.sleep(0.345)
        elif pos in tn1 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.1 !\033[0m")
          time.sleep(0.345)
        elif pos in tn2 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.2 !\033[0m")
          time.sleep(0.345)
        elif pos in tn4 or pos in pn4:
          print(" ")
          print(" \033[31mSudah ada tanaman buah melon !\033[0m")
          time.sleep(0.345)
        elif pos in tn5 or pos in pn5:
          print(" ")
          print(" \033[31mSudah ada tanaman buah nanas !\033[0m")
          time.sleep(0.345)
        elif pos in tn6 or pos in pn6:
          print(" ")
          print(" \033[31mSudah ada tanaman buah lemon !\033[0m")
          time.sleep(0.345)
        elif pos in tn7 or pos in pn7:
          print(" ")
          print(" \033[31mSudah ada tanaman buah jeruk !\033[0m")
          time.sleep(0.345)
        elif pos in tn8 or pos in pn8:
          print(" ")
          print(" \033[31mSudah ada tanaman buah anggur !\033[0m")
          time.sleep(0.345)
        elif pos in tn9 or pos in pn9:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel merah !\033[0m")
          time.sleep(0.345)
        elif pos in tn10 or pos in pn10:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel hijau !\033[0m")
          time.sleep(0.345)
        elif pos in tn11 or pos in pn11:
          print(" ")
          print(" \033[31mSudah ada tanaman buah pir !\033[0m")
          time.sleep(0.345)
        elif pos in tn12 or pos in pn12:
          print(" ")
          print(" \033[31mSudah ada tanaman buah mangga !\033[0m")
          time.sleep(0.345)
        
        elif Hp >= 2:
          if list_bibit_buah_sayur["stoberi"] >= 1:
            print(" ")
            print(" ➥ Mulai menanam bibit stoberi ")
            print(" ")
            exp += 3
            Hp -= 2
            time.sleep(1.5)
            list_bibit_buah_sayur["stoberi"] -= 1
            tas -= kapasitas_tas["stoberi"]
            print(" ")
            tanam_bibit_buah["tanam.bibit.stoberi"].add((userx1, usery1))
            print(" \033[32mSukses menanam bibit stoberi ✓\033[0m")
            time.sleep(0.3)
            tanam_bibit_buah["respawn.tanam.stoberi"][userx1, usery1] = now_stoberi + tanam_bibit_buah["waktu.tanam.stoberi"]
            break
          else:
            print(" ")
            print(" \033[31mBibit stoberi tidak ada !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          time.sleep(0.345)
         
    elif cmd == "m":
      if pos in lhn:
        if pos in tn4 or pos in pn4:
          print(" ")
          print(" \033[31mSudah ada tanaman !\033[0m")
          time.sleep(0.345)
        elif pos in tn1 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.1 !\033[0m")
          time.sleep(0.345)
        elif pos in tn2 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.2 !\033[0m")
          time.sleep(0.345)
        elif pos in tn3 or pos in pn3:
          print(" ")
          print(" \033[31mSudah ada tanaman buah stoberi !\033[0m")
          time.sleep(0.345)
        elif pos in tn5 or pos in pn5:
          print(" ")
          print(" \033[31mSudah ada tanaman buah nanas !\033[0m")
          time.sleep(0.345)
        elif pos in tn6 or pos in pn6:
          print(" ")
          print(" \033[31mSudah ada tanaman buah lemon !\033[0m")
          time.sleep(0.345)
        elif pos in tn7 or pos in pn7:
          print(" ")
          print(" \033[31mSudah ada tanaman buah jeruk !\033[0m")
          time.sleep(0.345)
        elif pos in tn8 or pos in pn8:
          print(" ")
          print(" \033[31mSudah ada tanaman buah anggur !\033[0m")
          time.sleep(0.345)
        elif pos in tn9 or pos in pn9:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel merah !\033[0m")
          time.sleep(0.345)
        elif pos in tn10 or pos in pn10:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel hijau !\033[0m")
          time.sleep(0.345)
        elif pos in tn11 or pos in pn11:
          print(" ")
          print(" \033[31mSudah ada tanaman buah pir !\033[0m")
          time.sleep(0.345)
        elif pos in tn12 or pos in pn12:
          print(" ")
          print(" \033[31mSudah ada tanaman buah mangga !\033[0m")
          time.sleep(0.345)
    
        elif Hp >= 2:
          if list_bibit_buah_sayur["melon"] >= 1:
            print(" ")
            print(" ➥ Mulai menanam bibit melon ")
            print(" ")
            exp += 3
            Hp -= 2
            time.sleep(1.5)
            list_bibit_buah_sayur["melon"] -= 1
            tas -= kapasitas_tas["melon"]
            print(" ")
            tanam_bibit_buah["tanam.bibit.melon"].add((userx1, usery1))
            print(" \033[32mSukses menanam bibit melon ✓\033[0m")
            time.sleep(0.3)
            tanam_bibit_buah["respawn.tanam.melon"][userx1, usery1] = now_melon + tanam_bibit_buah["waktu.tanam.melon"]
            break
          else:
            print(" ")
            print(" \033[31mBibit melon tidak ada !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          time.sleep(0.345)
    
    elif cmd == "n":
      if pos in lhn:
        if pos in tn5 or pos in pn5:
          print(" ")
          print(" \033[31mSudah ada tanaman !\033[0m")
          time.sleep(0.345)
        elif pos in tn1 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.1 !\033[0m")
          time.sleep(0.345)
        elif pos in tn2 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.2 !\033[0m")
          time.sleep(0.345)
        elif pos in tn3 or pos in pn3:
          print(" ")
          print(" \033[31mSudah ada tanaman buah stoberi !\033[0m")
          time.sleep(0.345)
        elif pos in tn4 or pos in pn4:
          print(" ")
          print(" \033[31mSudah ada tanaman buah melon !\033[0m")
          time.sleep(0.345)
        elif pos in tn6 or pos in pn6:
          print(" ")
          print(" \033[31mSudah ada tanaman buah lemon !\033[0m")
          time.sleep(0.345)
        elif pos in tn7 or pos in pn7:
          print(" ")
          print(" \033[31mSudah ada tanaman buah jeruk !\033[0m")
          time.sleep(0.345)
        elif pos in tn8 or pos in pn8:
          print(" ")
          print(" \033[31mSudah ada tanaman buah anggur !\033[0m")
          time.sleep(0.345)
        elif pos in tn9 or pos in pn9:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel merah !\033[0m")
          time.sleep(0.345)
        elif pos in tn10 or pos in pn10:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel hijau !\033[0m")
          time.sleep(0.345)
        elif pos in tn11 or pos in pn11:
          print(" ")
          print(" \033[31mSudah ada tanaman buah pir !\033[0m")
          time.sleep(0.345)
        elif pos in tn12 or pos in pn12:
          print(" ")
          print(" \033[31mSudah ada tanaman buah mangga !\033[0m")
          time.sleep(0.345)
        
        elif Hp >= 2:
          if list_bibit_buah_sayur["nanas"] >= 1:
            print(" ")
            print(" ➥ Mulai menanam bibit nanas ")
            print(" ")
            exp += 3
            Hp -= 2
            time.sleep(1.5)
            list_bibit_buah_sayur["nanas"] -= 1
            tas -= kapasitas_tas["nanas"]
            print(" ")
            tanam_bibit_buah["tanam.bibit.nanas"].add((userx1, usery1))
            print(" \033[32mSukses menanam bibit nanas ✓\033[0m")
            time.sleep(0.3)
            tanam_bibit_buah["respawn.tanam.nanas"][userx1, usery1] = now_nanas + tanam_bibit_buah["waktu.tanam.nanas"]
            break
          else:
            print(" ")
            print(" \033[31mBibit nanas tidak ada !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          time.sleep(0.345)
    
    elif cmd == "l":
      if pos in lhn:
        if pos in tn6 or pos in pn6:
          print(" ")
          print(" \033[31mSudah ada tanaman !\033[0m")
          time.sleep(0.345)
        elif pos in tn1 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.1 !\033[0m")
          time.sleep(0.345)
        elif pos in tn2 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.2 !\033[0m")
          time.sleep(0.345)
        elif pos in tn3 or pos in pn3:
          print(" ")
          print(" \033[31mSudah ada tanaman buah stoberi !\033[0m")
          time.sleep(0.345)
        elif pos in tn4 or pos in pn4:
          print(" ")
          print(" \033[31mSudah ada tanaman buah melon !\033[0m")
          time.sleep(0.345)
        elif pos in tn5 or pos in pn5:
          print(" ")
          print(" \033[31mSudah ada tanaman buah nanas !\033[0m")
          time.sleep(0.345)
        elif pos in tn7 or pos in pn7:
          print(" ")
          print(" \033[31mSudah ada tanaman buah jeruk !\033[0m")
          time.sleep(0.345)
        elif pos in tn8 or pos in pn8:
          print(" ")
          print(" \033[31mSudah ada tanaman buah anggur !\033[0m")
          time.sleep(0.345)
        elif pos in tn9 or pos in pn9:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel merah !\033[0m")
          time.sleep(0.345)
        elif pos in tn10 or pos in pn10:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel hijau !\033[0m")
          time.sleep(0.345)
        elif pos in tn11 or pos in pn11:
          print(" ")
          print(" \033[31mSudah ada tanaman buah pir !\033[0m")
          time.sleep(0.345)
        elif pos in tn12 or pos in pn12:
          print(" ")
          print(" \033[31mSudah ada tanaman buah mangga !\033[0m")
          time.sleep(0.345)
        
        elif Hp >= 2:
          if list_bibit_buah_sayur["lemon"] >= 1:
            print(" ")
            print(" ➥ Mulai menanam bibit lemon ")
            print(" ")
            exp += 3
            Hp -= 2
            time.sleep(1.5)
            list_bibit_buah_sayur["lemon"] -= 1
            tas -= kapasitas_tas["lemon"]
            print(" ")
            tanam_bibit_buah["tanam.bibit.lemon"].add((userx1, usery1))
            print(" \033[32mSukses menanam bibit lemon ✓\033[0m")
            time.sleep(0.3)
            tanam_bibit_buah["respawn.tanam.lemon"][userx1, usery1] = now_lemon + tanam_bibit_buah["waktu.tanam.lemon"]
            break
          else:
            print(" ")
            print(" \033[31mBibit lemon tidak ada !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          time.sleep(0.345)
    
    elif cmd == "j":
      if pos in lhn:
        if pos in tn7 or pos in pn7:
          print(" ")
          print(" \033[31mSudah ada tanaman !\033[0m")
          time.sleep(0.345)
        elif pos in tn1 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.1 !\033[0m")
          time.sleep(0.345)
        elif pos in tn2 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.2 !\033[0m")
          time.sleep(0.345)
        elif pos in tn3 or pos in pn3:
          print(" ")
          print(" \033[31mSudah ada tanaman buah stoberi !\033[0m")
          time.sleep(0.345)
        elif pos in tn4 or pos in pn4:
          print(" ")
          print(" \033[31mSudah ada tanaman buah melon !\033[0m")
          time.sleep(0.345)
        elif pos in tn5 or pos in pn5:
          print(" ")
          print(" \033[31mSudah ada tanaman buah nanas !\033[0m")
          time.sleep(0.345)
        elif pos in tn6 or pos in pn6:
          print(" ")
          print(" \033[31mSudah ada tanaman buah lemon !\033[0m")
          time.sleep(0.345)
        elif pos in tn8 or pos in pn8:
          print(" ")
          print(" \033[31mSudah ada tanaman buah anggur !\033[0m")
          time.sleep(0.345)
        elif pos in tn9 or pos in pn9:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel merah !\033[0m")
          time.sleep(0.345)
        elif pos in tn10 or pos in pn10:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel hijau !\033[0m")
          time.sleep(0.345)
        elif pos in tn11 or pos in pn11:
          print(" ")
          print(" \033[31mSudah ada tanaman buah pir !\033[0m")
          time.sleep(0.345)
        elif pos in tn12 or pos in pn12:
          print(" ")
          print(" \033[31mSudah ada tanaman buah mangga !\033[0m")
          time.sleep(0.345)
        
        elif Hp >= 2:
          if list_bibit_buah_sayur["jeruk"] >= 1:
            print(" ")
            print(" ➥ Mulai menanam bibit jeruk ")
            print(" ")
            exp += 3
            Hp -= 2
            time.sleep(1.5)
            list_bibit_buah_sayur["jeruk"] -= 1
            tas -= kapasitas_tas["jeruk"]
            print(" ")
            tanam_bibit_buah["tanam.bibit.jeruk"].add((userx1, usery1))
            print(" \033[32mSukses menanam bibit jeruk ✓\033[0m")
            time.sleep(0.3)
            tanam_bibit_buah["respawn.tanam.jeruk"][userx1, usery1] = now_jeruk + tanam_bibit_buah["waktu.tanam.jeruk"]
            break
          else:
            print(" ")
            print(" \033[31mBibit jeruk tidak ada !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          time.sleep(0.345)
    
    elif cmd == "a":
      if pos in lhn:
        if pos in tn8 or pos in pn8:
          print(" ")
          print(" \033[31mSudah ada tanaman !\033[0m")
          time.sleep(0.345)
        elif pos in tn1 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.1 !\033[0m")
          time.sleep(0.345)
        elif pos in tn2 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.2 !\033[0m")
          time.sleep(0.345)
        elif pos in tn3 or pos in pn3:
          print(" ")
          print(" \033[31mSudah ada tanaman buah stoberi !\033[0m")
          time.sleep(0.345)
        elif pos in tn4 or pos in pn4:
          print(" ")
          print(" \033[31mSudah ada tanaman buah melon !\033[0m")
          time.sleep(0.345)
        elif pos in tn5 or pos in pn5:
          print(" ")
          print(" \033[31mSudah ada tanaman buah nanas !\033[0m")
          time.sleep(0.345)
        elif pos in tn6 or pos in pn6:
          print(" ")
          print(" \033[31mSudah ada tanaman buah lemon !\033[0m")
          time.sleep(0.345)
        elif pos in tn7 or pos in pn7:
          print(" ")
          print(" \033[31mSudah ada tanaman buah jeruk !\033[0m")
          time.sleep(0.345)
        elif pos in tn9 or pos in pn9:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel merah !\033[0m")
          time.sleep(0.345)
        elif pos in tn10 or pos in pn10:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel hijau !\033[0m")
          time.sleep(0.345)
        elif pos in tn11 or pos in pn11:
          print(" ")
          print(" \033[31mSudah ada tanaman buah pir !\033[0m")
          time.sleep(0.345)
        elif pos in tn12 or pos in pn12:
          print(" ")
          print(" \033[31mSudah ada tanaman buah mangga !\033[0m")
          time.sleep(0.345)
        
        elif Hp >= 2:
          if list_bibit_buah_sayur["anggur"] >= 1:
            print(" ")
            print(" ➥ Mulai menanam bibit anggur ")
            print(" ")
            exp += 3
            Hp -= 2
            time.sleep(1.5)
            list_bibit_buah_sayur["anggur"] -= 1
            tas -= kapasitas_tas["anggur"]
            print(" ")
            tanam_bibit_buah["tanam.bibit.anggur"].add((userx1, usery1))
            print(" \033[32mSukses menanam bibit anggur ✓\033[0m")
            time.sleep(0.3)
            tanam_bibit_buah["respawn.tanam.anggur"][userx1, usery1] = now_anggur + tanam_bibit_buah["waktu.tanam.anggur"]
            break
          else:
            print(" ")
            print(" \033[31mBibit anggur tidak ada !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          time.sleep(0.345)
    
    elif cmd == "1":
      if pos in lhn:
        if pos in tn9 or pos in pn9:
          print(" ")
          print(" \033[31mSudah ada tanaman !\033[0m")
          time.sleep(0.345)
        elif pos in tn1 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.1 !\033[0m")
          time.sleep(0.345)
        elif pos in tn2 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.2 !\033[0m")
          time.sleep(0.345)
        elif pos in tn3 or pos in pn3:
          print(" ")
          print(" \033[31mSudah ada tanaman buah stoberi !\033[0m")
          time.sleep(0.345)
        elif pos in tn4 or pos in pn4:
          print(" ")
          print(" \033[31mSudah ada tanaman buah melon !\033[0m")
          time.sleep(0.345)
        elif pos in tn5 or pos in pn5:
          print(" ")
          print(" \033[31mSudah ada tanaman buah nanas !\033[0m")
          time.sleep(0.345)
        elif pos in tn6 or pos in pn6:
          print(" ")
          print(" \033[31mSudah ada tanaman buah lemon !\033[0m")
          time.sleep(0.345)
        elif pos in tn7 or pos in pn7:
          print(" ")
          print(" \033[31mSudah ada tanaman buah jeruk !\033[0m")
          time.sleep(0.345)
        elif pos in tn8 or pos in pn8:
          print(" ")
          print(" \033[31mSudah ada tanaman buah anggur !\033[0m")
          time.sleep(0.345)
        elif pos in tn10 or pos in pn10:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel hijau !\033[0m")
          time.sleep(0.345)
        elif pos in tn11 or pos in pn11:
          print(" ")
          print(" \033[31mSudah ada tanaman buah pir !\033[0m")
          time.sleep(0.345)
        elif pos in tn12 or pos in pn12:
          print(" ")
          print(" \033[31mSudah ada tanaman buah mangga !\033[0m")
          time.sleep(0.345)
        
        elif Hp >= 2:
          if list_bibit_buah_sayur["apel_merah"] >= 1:
            print(" ")
            print(" ➥ Mulai menanam bibit apel merah ")
            print(" ")
            exp += 3
            Hp -= 2
            time.sleep(1.5)
            list_bibit_buah_sayur["apel_merah"] -= 1
            tas -= kapasitas_tas["apel_merah"]
            print(" ")
            tanam_bibit_buah["tanam.bibit.apelmerah"].add((userx1, usery1))
            print(" \033[32mSukses menanam bibit apel merah ✓\033[0m")
            time.sleep(0.3)
            tanam_bibit_buah["respawn.tanam.apelmerah"][userx1, usery1] = now_apelmerah + tanam_bibit_buah["waktu.tanam.apelmerah"]
            break
          else:
            print(" ")
            print(" \033[31mBibit apel merah tidak ada !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          time.sleep(0.345)
    
    elif cmd == "2":
      if pos in lhn:
        if pos in tn10 or pos in pn10:
          print(" ")
          print(" \033[31mSudah ada tanaman !\033[0m")
          time.sleep(0.345)
        elif pos in tn1 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.1 !\033[0m")
          time.sleep(0.345)
        elif pos in tn2 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.2 !\033[0m")
          time.sleep(0.345)
        elif pos in tn3 or pos in pn3:
          print(" ")
          print(" \033[31mSudah ada tanaman buah stoberi !\033[0m")
          time.sleep(0.345)
        elif pos in tn4 or pos in pn4:
          print(" ")
          print(" \033[31mSudah ada tanaman buah melon !\033[0m")
          time.sleep(0.345)
        elif pos in tn5 or pos in pn5:
          print(" ")
          print(" \033[31mSudah ada tanaman buah nanas !\033[0m")
          time.sleep(0.345)
        elif pos in tn6 or pos in pn6:
          print(" ")
          print(" \033[31mSudah ada tanaman buah lemon !\033[0m")
          time.sleep(0.345)
        elif pos in tn7 or pos in pn7:
          print(" ")
          print(" \033[31mSudah ada tanaman buah jeruk !\033[0m")
          time.sleep(0.345)
        elif pos in tn8 or pos in pn8:
          print(" ")
          print(" \033[31mSudah ada tanaman buah anggur !\033[0m")
          time.sleep(0.345)
        elif pos in tn9 or pos in pn9:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel merah !\033[0m")
          time.sleep(0.345)
        elif pos in tn11 or pos in pn11:
          print(" ")
          print(" \033[31mSudah ada tanaman buah pir !\033[0m")
          time.sleep(0.345)
        elif pos in tn12 or pos in pn12:
          print(" ")
          print(" \033[31mSudah ada tanaman buah mangga !\033[0m")
          time.sleep(0.345)
        
        elif Hp >= 2:
          if list_bibit_buah_sayur["apel_hijau"] >= 1:
            print(" ")
            print(" ➥ Mulai menanam bibit apel hijau ")
            print(" ")
            exp += 3
            Hp -= 2
            time.sleep(1.5)
            list_bibit_buah_sayur["apel_hijau"] -= 1
            tas -= kapasitas_tas["apel_hijau"]
            print(" ")
            tanam_bibit_buah["tanam.bibit.apelhijau"].add((userx1, usery1))
            print(" \033[32mSukses menanam bibit apel hijau ✓\033[0m")
            time.sleep(0.3)
            tanam_bibit_buah["respawn.tanam.apelhijau"][userx1, usery1] = now_apelhijau + tanam_bibit_buah["waktu.tanam.apelhijau"]
            break
          else:
            print(" ")
            print(" \033[31mBibit apel hijau tidak ada !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          time.sleep(0.345)
    
    elif cmd == "p":
      if pos in lhn:
        if pos in tn11 or pos in pn11:
          print(" ")
          print(" \033[31mSudah ada tanaman !\033[0m")
          time.sleep(0.345)
        elif pos in tn1 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.1 !\033[0m")
          time.sleep(0.345)
        elif pos in tn2 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.2 !\033[0m")
          time.sleep(0.345)
        elif pos in tn3 or pos in pn3:
          print(" ")
          print(" \033[31mSudah ada tanaman buah stoberi !\033[0m")
          time.sleep(0.345)
        elif pos in tn4 or pos in pn4:
          print(" ")
          print(" \033[31mSudah ada tanaman buah melon !\033[0m")
          time.sleep(0.345)
        elif pos in tn5 or pos in pn5:
          print(" ")
          print(" \033[31mSudah ada tanaman buah nanas !\033[0m")
          time.sleep(0.345)
        elif pos in tn6 or pos in pn6:
          print(" ")
          print(" \033[31mSudah ada tanaman buah lemon !\033[0m")
          time.sleep(0.345)
        elif pos in tn7 or pos in pn7:
          print(" ")
          print(" \033[31mSudah ada tanaman buah jeruk !\033[0m")
          time.sleep(0.345)
        elif pos in tn8 or pos in pn8:
          print(" ")
          print(" \033[31mSudah ada tanaman buah anggur !\033[0m")
          time.sleep(0.345)
        elif pos in tn9 or pos in pn9:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel merah !\033[0m")
          time.sleep(0.345)
        elif pos in tn10 or pos in pn10:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel hijau !\033[0m")
          time.sleep(0.345)
        elif pos in tn12 or pos in pn12:
          print(" ")
          print(" \033[31mSudah ada tanaman buah mangga !\033[0m")
          time.sleep(0.345)
        
        elif Hp >= 2:
          if list_bibit_buah_sayur["pir"] >= 1:
            print(" ")
            print(" ➥ Mulai menanam bibit pir")
            print(" ")
            exp += 3
            Hp -= 2
            time.sleep(1.5)
            list_bibit_buah_sayur["pir"] -= 1
            tas -= kapasitas_tas["pir"]
            print(" ")
            tanam_bibit_buah["tanam.bibit.pir"].add((userx1, usery1))
            print(" \033[32mSukses menanam bibit pir ✓\033[0m")
            time.sleep(0.3)
            tanam_bibit_buah["respawn.tanam.pir"][userx1, usery1] = now_pir + tanam_bibit_buah["waktu.tanam.pir"]
            break
          else:
            print(" ")
            print(" \033[31mBibit pir tidak ada !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          time.sleep(0.345)
    
    elif cmd == "0":
      if pos in lhn:
        if pos in tn12 or pos in pn12:
          print(" ")
          print(" \033[31mSudah ada tanaman !\033[0m")
          time.sleep(0.345)
        elif pos in tn1 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.1 !\033[0m")
          time.sleep(0.345)
        elif pos in tn2 or pos in pn2:
          print(" ")
          print(" \033[31mSudah ada tumbuhan pohon T.2 !\033[0m")
          time.sleep(0.345)
        elif pos in tn3 or pos in pn3:
          print(" ")
          print(" \033[31mSudah ada tanaman buah stoberi !\033[0m")
          time.sleep(0.345)
        elif pos in tn4 or pos in pn4:
          print(" ")
          print(" \033[31mSudah ada tanaman buah melon !\033[0m")
          time.sleep(0.345)
        elif pos in tn5 or pos in pn5:
          print(" ")
          print(" \033[31mSudah ada tanaman buah nanas !\033[0m")
          time.sleep(0.345)
        elif pos in tn6 or pos in pn6:
          print(" ")
          print(" \033[31mSudah ada tanaman buah lemon !\033[0m")
          time.sleep(0.345)
        elif pos in tn7 or pos in pn7:
          print(" ")
          print(" \033[31mSudah ada tanaman buah jeruk !\033[0m")
          time.sleep(0.345)
        elif pos in tn8 or pos in pn8:
          print(" ")
          print(" \033[31mSudah ada tanaman buah anggur !\033[0m")
          time.sleep(0.345)
        elif pos in tn9 or pos in pn9:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel merah !\033[0m")
          time.sleep(0.345)
        elif pos in tn10 or pos in pn10:
          print(" ")
          print(" \033[31mSudah ada tanaman buah apel hijau !\033[0m")
          time.sleep(0.345)
        elif pos in tn11 or pos in pn11:
          print(" ")
          print(" \033[31mSudah ada tanaman buah pir !\033[0m")
          time.sleep(0.345)
        
        elif Hp >= 2:
          if list_bibit_buah_sayur["mangga"] >= 1:
            print(" ")
            print(" ➥ Mulai menanam bibit mangga")
            print(" ")
            exp += 3
            Hp -= 2
            time.sleep(1.5)
            list_bibit_buah_sayur["mangga"] -= 1
            tas -= kapasitas_tas["mangga"]
            print(" ")
            tanam_bibit_buah["tanam.bibit.mangga"].add((userx1, usery1))
            print(" \033[32mSukses menanam bibit mangga ✓\033[0m")
            time.sleep(0.3)
            tanam_bibit_buah["respawn.tanam.mangga"][userx1, usery1] = now_pir + tanam_bibit_buah["waktu.tanam.mangga"]
            break
          else:
            print(" ")
            print(" \033[31mBibit mangga tidak ada !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mIsi Energi\033[0m» ♥️  = 🍚 «")
          time.sleep(0.345)
    
    elif cmd == "x":
      break
    
    else:
      print(" ")
      print(" \033[31mInput salah !\033[0m")
      time.sleep(0.345)

def panenbibitbuah():
  global kapak, tas, exp, gxc, Hp, list_buah_sayur
  kor = (userx1, usery1)
  lhn = k_lahan
  #kor_bibit
  tn1 = tanam
  tn2 = tanam
  tn3 = tanam_bibit_buah["tanam.bibit.stoberi"]
  tn4 = tanam_bibit_buah["tanam.bibit.melon"]
  tn5 = tanam_bibit_buah["tanam.bibit.nanas"]
  tn6 = tanam_bibit_buah["tanam.bibit.lemon"]
  tn7 = tanam_bibit_buah["tanam.bibit.jeruk"]
  tn8 = tanam_bibit_buah["tanam.bibit.anggur"]
  tn9 = tanam_bibit_buah["tanam.bibit.apelmerah"]
  tn10 = tanam_bibit_buah["tanam.bibit.apelhijau"]
  tn11 = tanam_bibit_buah["tanam.bibit.pir"]
  tn12 = tanam_bibit_buah["tanam.bibit.mangga"]
  #kor_buah
  pn1 = pohon_tanam
  pn2 = pohon_tanam2
  pn3 = tanam_bibit_buah["panen.buah.stoberi"]
  pn4 = tanam_bibit_buah["panen.buah.melon"]
  pn5 = tanam_bibit_buah["panen.buah.nanas"]
  pn6 = tanam_bibit_buah["panen.buah.lemon"]
  pn7 = tanam_bibit_buah["panen.buah.jeruk"]
  pn8 = tanam_bibit_buah["panen.buah.anggur"]
  pn9 = tanam_bibit_buah["panen.buah.apelmerah"]
  pn10 = tanam_bibit_buah["panen.buah.apelhijau"]
  pn11 = tanam_bibit_buah["panen.buah.pir"]
  pn12 = tanam_bibit_buah["panen.buah.mangga"]
  
  while True:
    os.system("clear")
    
    print(" Untuk panen buah : ")
    print(" ")
    print(" \033[32mBuah stoberi\033[0m »(st)  \033[32mBuah anggur\033[0m     »(ang)")
    print(" \033[32mBuah melon\033[0m   »(ml)  \033[32mBuah apel merah\033[0m »(apm)")
    print(" \033[32mBuah nanas\033[0m   »(nns) \033[32mBuah apel hijau\033[0m »(aph)")
    print(" \033[32mBuah lemon\033[0m   »(lm)  \033[32mBuah pir\033[0m        »(pr)")
    print(" \033[32mBuah jeruk\033[0m   »(jr)  \033[32mBuah mangga\033[0m     »(mng)")
    print(" ")
    print(" Keluar       »[x]")
    print(" ")
    cmd = input(" pilih : ") 
  
    if cmd == "st":
      if pos in lhn:
        if pos in tn3:
          print(" ")
          print(" \033[31mTanaman stoberi masih muda !")
          time.sleep(0.345)
        elif pos in pn3:
          b_exp = 5
          b_gxc = 45
          muatan = kapasitas_tas["buah.stoberi"]
          if tas + muatan <= 100:
            if Hp >= 2:
              print(" ")
              print(" Memanen buah stoberi »")
              time.sleep(0.567)
              Hp -= 2
              exp += b_exp
              gxc += b_gxc
              tas += muatan
              list_buah_sayur["stoberi"] += 1
              tanam_bibit_buah["panen.buah.stoberi"].remove(pos)
              print(" ")
              print(" \033[32mSukses panen buah stoberi ✓\033[0m")
              time.sleep(0.345)
              break
            else:
              print(" ")
              print(" \033[31mTidak ada energi !\033[0m")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mTas kamu penuh !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mInvalid !\033[0m")
          time.sleep(0.345)
    
    elif cmd == "ml":
      if pos in lhn:
        if pos in tn4:
          print(" ")
          print(" \033[31mTanaman melon masih muda !")
          time.sleep(0.345)
        elif pos in pn4:
          b_exp = 5
          b_gxc = 45
          muatan = kapasitas_tas["buah.melon"]
          if tas + muatan <= 100:
            if Hp >= 2:
              print(" ")
              print(" Memanen buah melon »")
              time.sleep(0.567)
              Hp -= 2
              exp += b_exp
              gxc += b_gxc
              tas += muatan
              list_buah_sayur["melon"] += 1
              tanam_bibit_buah["panen.buah.melon"].remove(pos)
              print(" ")
              print(" \033[32mSukses panen buah melon ✓\033[0m")
              time.sleep(0.345)
              break
            else:
              print(" ")
              print(" \033[31mTidak ada energi !\033[0m")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mTas kamu penuh !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mInvalid !\033[0m")
          time.sleep(0.345)
    
    elif cmd == "nns":
      if pos in lhn:
        if pos in tn5:
          print(" ")
          print(" \033[31mTanaman nanas masih muda !")
          time.sleep(0.345)
        elif pos in pn5:
          b_exp = 5
          b_gxc = 45
          muatan = kapasitas_tas["buah.nanas"]
          if tas + muatan <= 100:
            if Hp >= 2:
              print(" ")
              print(" Memanen buah nanas »")
              time.sleep(0.567)
              Hp -= 2
              exp += b_exp
              gxc += b_gxc
              tas += muatan
              list_buah_sayur["nanas"] += 1
              tanam_bibit_buah["panen.buah.nanas"].remove(pos)
              print(" ")
              print(" \033[32mSukses panen buah nanas ✓\033[0m")
              time.sleep(0.345)
              break
            else:
              print(" ")
              print(" \033[31mTidak ada energi !\033[0m")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mTas kamu penuh !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mInvalid !\033[0m")
          time.sleep(0.345)
    
    elif cmd == "lm":
      if pos in lhn:
        if pos in tn6:
          print(" ")
          print(" \033[31mTanaman lemon masih muda !")
          time.sleep(0.345)
        elif pos in pn6:
          b_exp = 5
          b_gxc = 45
          muatan = kapasitas_tas["buah.lemon"]
          if tas + muatan <= 100:
            if Hp >= 2:
              print(" ")
              print(" Memanen buah lemon »")
              time.sleep(0.567)
              Hp -= 2
              exp += b_exp
              gxc += b_gxc
              tas += muatan
              list_buah_sayur["lemon"] += 1
              tanam_bibit_buah["panen.buah.lemon"].remove(pos)
              print(" ")
              print(" \033[32mSukses panen buah lemon ✓\033[0m")
              time.sleep(0.345)
              break
            else:
              print(" ")
              print(" \033[31mTidak ada energi !\033[0m")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mTas kamu penuh !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mInvalid !\033[0m")
          time.sleep(0.345)
    
    elif cmd == "jr":
      if pos in lhn:
        if pos in tn7:
          print(" ")
          print(" \033[31mTanaman melon masih muda !")
          time.sleep(0.345)
        elif pos in pn7:
          b_exp = 5
          b_gxc = 45
          muatan = kapasitas_tas["buah.jeruk"]
          if tas + muatan <= 100:
            if Hp >= 2:
              print(" ")
              print(" Memanen buah jeruk »")
              time.sleep(0.567)
              Hp -= 2
              exp += b_exp
              gxc += b_gxc
              tas += muatan
              list_buah_sayur["jeruk"] += 1
              tanam_bibit_buah["panen.buah.jeruk"].remove(pos)
              print(" ")
              print(" \033[32mSukses panen buah jeruk ✓\033[0m")
              time.sleep(0.345)
              break
            else:
              print(" ")
              print(" \033[31mTidak ada energi !\033[0m")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mTas kamu penuh !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mInvalid !\033[0m")
          time.sleep(0.345)
    
    elif cmd == "ang":
      if pos in lhn:
        if pos in tn8:
          print(" ")
          print(" \033[31mTanaman melon masih muda !")
          time.sleep(0.345)
        elif pos in pn8:
          b_exp = 5
          b_gxc = 45
          muatan = kapasitas_tas["buah.anggur"]
          if tas + muatan <= 100:
            if Hp >= 2:
              print(" ")
              print(" Memanen buah anggur »")
              time.sleep(0.567)
              Hp -= 2
              exp += b_exp
              gxc += b_gxc
              tas += muatan
              list_buah_sayur["anggur"] += 1
              tanam_bibit_buah["panen.buah.anggur"].remove(pos)
              print(" ")
              print(" \033[32mSukses panen buah anggur ✓\033[0m")
              time.sleep(0.345)
              break
            else:
              print(" ")
              print(" \033[31mTidak ada energi !\033[0m")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mTas kamu penuh !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mInvalid !\033[0m")
          time.sleep(0.345)
    
    elif cmd == "apm":
      if pos in lhn:
        if pos in tn9:
          print(" ")
          print(" \033[31mTanaman apel merah masih muda !")
          time.sleep(0.345)
        elif pos in pn9:
          b_exp = 5
          b_gxc = 45
          muatan = kapasitas_tas["buah.apelmerah"]
          if tas + muatan <= 100:
            if Hp >= 2:
              print(" ")
              print(" Memanen buah apel merah »")
              time.sleep(0.567)
              Hp -= 2
              exp += b_exp
              gxc += b_gxc
              tas += muatan
              list_buah_sayur["apel_merah"] += 1
              tanam_bibit_buah["panen.buah.apelmerah"].remove(pos)
              print(" ")
              print(" \033[32mSukses panen buah apel merah ✓\033[0m")
              time.sleep(0.345)
              break
            else:
              print(" ")
              print(" \033[31mTidak ada energi !\033[0m")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mTas kamu penuh !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mInvalid !\033[0m")
          time.sleep(0.345)
    
    elif cmd == "aph":
      if pos in lhn:
        if pos in tn10:
          print(" ")
          print(" \033[31mTanaman apel hijau masih muda !")
          time.sleep(0.345)
        elif pos in pn10:
          b_exp = 5
          b_gxc = 45
          muatan = kapasitas_tas["buah.apelhijau"]
          if tas + muatan <= 100:
            if Hp >= 2:
              print(" ")
              print(" Memanen buah apel hijau »")
              time.sleep(0.567)
              Hp -= 2
              exp += b_exp
              gxc += b_gxc
              tas += muatan
              list_buah_sayur["apel_hijau"] += 1
              tanam_bibit_buah["panen.buah.apelhijau"].remove(pos)
              print(" ")
              print(" \033[32mSukses panen buah apel hijau ✓\033[0m")
              time.sleep(0.345)
              break
            else:
              print(" ")
              print(" \033[31mTidak ada energi !\033[0m")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mTas kamu penuh !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mInvalid !\033[0m")
          time.sleep(0.345)
    
    elif cmd == "pr":
      if pos in lhn:
        if pos in tn11:
          print(" ")
          print(" \033[31mTanaman pir masih muda !")
          time.sleep(0.345)
        elif pos in pn11:
          b_exp = 5
          b_gxc = 45
          muatan = kapasitas_tas["buah.pir"]
          if tas + muatan <= 100:
            if Hp >= 2:
              print(" ")
              print(" Memanen buah pir »")
              time.sleep(0.567)
              Hp -= 2
              exp += b_exp
              gxc += b_gxc
              tas += muatan
              list_buah_sayur["pir"] += 1
              tanam_bibit_buah["panen.buah.pir"].remove(pos)
              print(" ")
              print(" \033[32mSukses panen buah pir ✓\033[0m")
              time.sleep(0.345)
              break
            else:
              print(" ")
              print(" \033[31mTidak ada energi !\033[0m")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mTas kamu penuh !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mInvalid !\033[0m")
          time.sleep(0.345)
    
    elif cmd == "mng":
      if pos in lhn:
        if pos in tn12:
          print(" ")
          print(" \033[31mTanaman mangga masih muda !")
          time.sleep(0.345)
        elif pos in pn12:
          b_exp = 5
          b_gxc = 45
          muatan = kapasitas_tas["buah.mangga"]
          if tas + muatan <= 100:
            if Hp >= 2:
              print(" ")
              print(" Memanen buah mangga »")
              time.sleep(0.567)
              Hp -= 2
              exp += b_exp
              gxc += b_gxc
              tas += muatan
              list_buah_sayur["mangga"] += 1
              tanam_bibit_buah["panen.buah.mangga"].remove(pos)
              print(" ")
              print(" \033[32mSukses panen buah mangga ✓\033[0m")
              time.sleep(0.345)
              break
            else:
              print(" ")
              print(" \033[31mTidak ada energi !\033[0m")
              time.sleep(0.345)
          else:
            print(" ")
            print(" \033[31mTas kamu penuh !\033[0m")
            time.sleep(0.345)
        else:
          print(" ")
          print(" \033[31mInvalid !\033[0m")
          time.sleep(0.345)
          
    elif cmd == "x":
      break
  
    else:
      print(" ")
      print(" \033[31mInput salah !\033[0m")
      time.sleep(0.345)
              

def npcmebel():
  global papan0, papan1, papan2, kursi0, kursi1,kursi2, meja0, meja1, meja2, lemari0, lemari1,lemari2, gxc, exp
  
  while True:
    
    os.system("clear")
    
    print(" ")
    print(" 🥸 : halo, saya Fred.\n  apa kamu punya barang-barang\n  mebel untuk dijual kepada ku?")
    print(" ")
    print(" Jawab : \033[32mY\033[0m jika ada, \033[31mX\033[0m tidak ada.")
    print(" ")
    cmd=_getch()
    
    if cmd == "y":
        
      while True:
        os.system("clear")
        print(" ")
        print(" 🥸 : bagus, aku senang mendengarnya.\nAku sedang membutuhkan semua barang mebel.\n 1. papan\n 2. kursi\n 3. meja\n 4. lemari")
        print(" 🥸 : Aku sangat membutuhkan itu semua.")
        print(" ")
        print(" Pilih angka dari barang yang kamu\n ingin jual. x untuk batal :")
        pilih=_getch()
        
        if pilih == "1":
          harga_papanbiasa = 20
          harga_papan1 = 60
          harga_papan2 = 90
          
          while True:
            os.system("clear")
            print(" ")
            print(" 🥸 : untuk jenis papan aku beli dengan harga berbeda.\n1. papan biasa (20 Gxc)\n2. papan T.1 (60 Gxc)\n3. papan T.2 (90 Gxc).")
            print(" ")
            print(" Pilih (1/2/3) jika tertarik.\nx untuk batal jual.")
            papan=_getch()
            
            if papan == "1":
              print(" ")
              jl_papan=input(" 🥸 : Kamu ingin jual berapa papan biasa ?")
              
              try:
                jpapan = int(jl_papan)
                if jpapan <= 0:
                  print(" ")
                  print(" 🥸 : Aku tidak suka bercanda !")
                  print(" ")
                  time.sleep(0.345)
                elif papan0 < jpapan:
                  print(" ")
                  print(" 🥸 : apa kamu coba menipu ku !")
                  print(" ")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" 🥸 : Tunggu, aku siapkan token Gxc nya.")
                  print(" ")
                  papan0 -= jpapan
                  gxc += jpapan * harga_papanbiasa
                  time.sleep(0.6)
                  print(" 🥸 : Terima kasih, ini tokennya.")
                  time.sleep(0.345)
                  break
              
              except ValueError:
                print(" ")
                print(" 🥸 : ???")
                print(" ")
                time.sleep(0.345)
                
            elif papan == "2":
              print(" ")
              jl_papan1=input(" 🥸 : Kamu ingin jual berapa papan T.1 ?")
              
              try:
                jpapan1 = int(jl_papan1)
                if jpapan1 <= 0:
                  print(" ")
                  print(" 🥸 : Aku tidak suka bercanda !")
                  print(" ")
                  time.sleep(0.345)
                elif papan1 < jpapan1:
                  print(" ")
                  print(" 🥸 : apa kamu coba menipu ku !")
                  print(" ")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" 🥸 : Tunggu, aku siapkan token Gxc nya.")
                  print(" ")
                  papan1 -= jpapan1
                  gxc += jpapan1 * harga_papan1
                  time.sleep(0.6)
                  print(" 🥸 : Terima kasih, ini tokennya.")
                  time.sleep(0.345)
                  break
              
              except ValueError:
                print(" ")
                print(" 🥸 : ???")
                print(" ")
                time.sleep(0.345)
            
            elif papan == "3":
              print(" ")
              jl_papan2 =input(" 🥸 : Kamu ingin jual berapa papan T.2 ?")
              
              try:
                jpapan2 = int(jl_papan2)
                if jpapan2 <= 0:
                  print(" ")
                  print(" 🥸 : Aku tidak suka bercanda !")
                  print(" ")
                  time.sleep(0.345)
                elif papan2 < jpapan2:
                  print(" ")
                  print(" 🥸 : apa kamu coba menipu ku !")
                  print(" ")
                  time.sleep(0.345)
                else:
                  print(" ")
                  print(" 🥸 : Tunggu, aku siapkan token Gxc nya.")
                  print(" ")
                  papan2 -= jpapan2
                  gxc += jpapan2 * harga_papan2
                  time.sleep(0.6)
                  print(" 🥸 : Terima kasih, ini tokennya.")
                  time.sleep(0.345)
                  break
              
              except ValueError:
                print(" ")
                print(" 🥸 : ???")
                print(" ")
                time.sleep(0.345)
            
            elif papan == "x":
              print(" ")
              print(" 🥸 : Ku kira kamu ingin menjual papan.\nbaiklah jika kamu belum ingin menjual.")
              print(" ")
              time.sleep(0.345)
              break
            
            else:
              print(" ")
              print(" 🥸 : ???")
              print(" ")
              time.sleep(0.345)
        
        elif pilih == "x":
          print(" ")
          print(" 🥸 : sepertinya kamu masih ragu.")
          print(" ")
          time.sleep(0.345)
          break
          
        else:
          print(" ")
          print(" 🥸 : ???")
          print(" ")
          time.sleep(0.345)
    
    elif cmd == "x":
      print(" ")
      print(" 🥸 : huft, kamu tidak jadi menjual.\ntidak apa lain waktu lagi datang kepada ku.")
      print(" ")
      time.sleep(0.345)
      break
    
    else:
      print(" ")
      print(" 🥸 : ???")
      print(" ")
      time.sleep(0.345)
      
def d_blue():
  
  bck = (0, 2)
  obk = (16, 0)
  pos= (userbx, userby)
  posc = (cacingx, cacingy)
  if pos == obk:
    kc = "\033[33mInfo 🔑 [k]\033[0m"
  elif pos != obk:
    kc = ""
  print("┌────────────┐")
  print(f"│🟦 \033[34m BlueBox\033[0m │ ✛ : \033[32m{pos}\033[0m {kc}") 
  print("└────────────┘")
  print(f"𝐆𝐄 : {Game_end}    🪓 : {kapak}   🎣 : {pancingan}   🪱 : {cacing} \033[33m{posc}\033[0m")
  infopemain()
  print("│----------------------------------------│")
  print(info)
  
  if pos == obk:
    print(" [\033[33mKunci\033[0m] Untuk akses simpan & ambil item.")
  
  if pos == bck:
    print(" [\033[31mx\033[0m] untuk keluar »")
    
  ob = masuk_isi_bluebox
  _ = ambil_isi_bluebox
  if pos == ob["_bkayu"]:
    print(f" [🌳] Pohon T.1/2(0) (\033[32m{bluebox["kayu"]}\033[0m/\033[36m{kapasitas_box["kayu"]}\033[0m)")
  elif pos == ob["_bkayu1"]:
    print(f" [🌳] Pohon T.1 (\033[32m{bluebox["kayuT1"]}\033[0m/\033[36m{kapasitas_box["kayuT1"]}\033[0m)")
  elif pos == ob["_bkayu2"]:
    print(f" [🌲] Pohon T.2 (\033[32m{bluebox["kayuT2"]}\033[0m/\033[36m{kapasitas_box["kayuT2"]}\033[0m)")
  elif pos == ob["_bbibit"]:
    print(f" [🌱] Bibit T.1 (\033[32m{bluebox["bibit"]}\033[0m/\033[36m{kapasitas_box["bibit"]}\033[0m)")
  elif pos == ob["_bbibit2"]:
    print(f" [🌱] Bibit T.2 (\033[32m{bluebox["bibit2"]}\033[0m/\033[36m{kapasitas_box["bibit2"]}\033[0m)")
  elif pos == ob["_bstoberi"]:
    print(f" [🍓] Bibit Stoberi (\033[32m{bluebox["b.stoberi"]}\033[0m/\033[36m{kapasitas_box["b.stoberi"]}\033[0m)")
  elif pos == ob["_bmelon"]:
    print(f" [🍈] Bibit Melon (\033[32m{bluebox["b.melon"]}\033[0m/\033[36m{kapasitas_box["b.melon"]}\033[0m)")
  elif pos == ob["_bnanas"]:
    print(f" [🍍] Bibit Nanas (\033[32m{bluebox["b.nanas"]}\033[0m/\033[36m{kapasitas_box["b.nanas"]}\033[0m)")
  elif pos == ob["_blemon"]:
    print(f" [🍋] Bibit Lemon (\033[32m{bluebox["b.lemon"]}\033[0m/\033[36m{kapasitas_box["b.lemon"]}\033[0m)")
  elif pos == ob["_bjeruk"]:
    print(f" [🍊] Bibit Jeruk (\033[32m{bluebox["b.jeruk"]}\033[0m/\033[36m{kapasitas_box["b.jeruk"]}\033[0m)")
  elif pos == ob["_banggur"]:
    print(f" [🍇] Bibit Anggur (\033[32m{bluebox["b.anggur"]}\033[0m/\033[36m{kapasitas_box["b.anggur"]}\033[0m)")
  elif pos == ob["_bapelmerah"]:
    print(f" [🍎] Bibit Apel merah (\033[32m{bluebox["b.apelmerah"]}\033[0m/\033[36m{kapasitas_box["b.apelmerah"]}\033[0m)")
  elif pos == ob["_bapelhijau"]:
    print(f" [🍏] Bibit Apel hijau (\033[32m{bluebox["b.apelhijau"]}\033[0m/\033[36m{kapasitas_box["b.apelhijau"]}\033[0m)")
  elif pos == ob["_bpir"]:
    print(f" [🍐] Bibit Pir (\033[32m{bluebox["b.pir"]}\033[0m/\033[36m{kapasitas_box["b.pir"]}\033[0m)")
  elif pos == ob["_bmangga"]:
    print(f" [🥭] Bibit Mangga (\033[32m{bluebox["b.mangga"]}\033[0m/\033[36m{kapasitas_box["b.mangga"]}\033[0m)")
  elif pos == _["kayu"] or pos == _["kayuT1"] or pos == _["kayuT2"] or pos == _["bibit"] or pos == _["bibit2"] or pos == _["b.stoberi"] or pos == _["b.melon"] or pos == _["b.nanas"] or pos == _["b.lemon"] or pos == _["b.jeruk"] or pos == _["b.anggur"] or pos == _["b.apelmerah"] or pos == _["b.apelhijau"] or pos == _["b.pir"] or pos == _["b.mangga"]:
    print(" [📤] \033[32mAmbil item bibit.\033[0m")
    
  elif pos == (16, 8):
    print(" [Next] \033[34mBlueBox\033[0m [m]")
    
  print("│----------------------------------------│")
  print(" ")
  for y in range(bluey):
    ln = ""
    for x in range(bluex):
      
      kor = (x, y)
    
      if kor == (userbx, userby):
        if pusing > 0:
          ln += "😵"
        else:
          ln += "😍"
      elif kor == bck:
        ln += "️🔙"
      elif kor == (redb["x"], redb["y"]):
        ln += "🔑"
      elif kor == masuk_isi_bluebox["_bkayu"]:
        ln += "🌳"
      elif kor == masuk_isi_bluebox["_bkayu1"]:
        ln += "🌳"
      elif kor == masuk_isi_bluebox["_bkayu2"]:
        ln += "🌲"
      elif kor == masuk_isi_bluebox["_bbibit"]:
        ln += "🌱"
      elif kor == masuk_isi_bluebox["_bbibit2"]:
        ln += "🌱"
      elif kor == masuk_isi_bluebox["_bstoberi"]:
        ln += "🍓"
      elif kor == masuk_isi_bluebox["_bmelon"]:
        ln += "🍈"
      elif kor == masuk_isi_bluebox["_bnanas"]:
        ln += "🍍"
      elif kor == masuk_isi_bluebox["_blemon"]:
        ln += "🍋"
      elif kor == masuk_isi_bluebox["_bjeruk"]:
        ln += "🍊"
      elif kor == masuk_isi_bluebox["_banggur"]:
        ln += "🍇"
      elif kor == masuk_isi_bluebox["_bapelmerah"]:
        ln += "🍎"
      elif kor == masuk_isi_bluebox["_bapelhijau"]:
        ln += "🍏"
      elif kor == masuk_isi_bluebox["_bpir"]:
        ln += "🍐"
      elif kor == masuk_isi_bluebox["_bmangga"]:
        ln += "🥭"
      elif kor == ambil_isi_bluebox["kayu"]:
        ln += "📤"
      elif kor == ambil_isi_bluebox["kayuT1"]:
        ln += "📤"
      elif kor == ambil_isi_bluebox["kayuT2"]:
        ln += "📤"
      elif kor == ambil_isi_bluebox["bibit"]:
        ln += "📤"
      elif kor == ambil_isi_bluebox["bibit2"]:
        ln += "📤"
      elif kor == ambil_isi_bluebox["b.stoberi"]:
        ln += "📤"
      elif kor == ambil_isi_bluebox["b.melon"]:
        ln += "📤"
      elif kor == ambil_isi_bluebox["b.nanas"]:
        ln += "📤"
      elif kor == ambil_isi_bluebox["b.lemon"]:
        ln += "📤"
      elif kor == ambil_isi_bluebox["b.jeruk"]:
        ln += "📤"
      elif kor == ambil_isi_bluebox["b.anggur"]:
        ln += "📤"
      elif kor == ambil_isi_bluebox["b.apelmerah"]:
        ln += "📤"
      elif kor == ambil_isi_bluebox["b.apelhijau"]:
        ln += "📤"
      elif kor == ambil_isi_bluebox["b.pir"]:
        ln += "📤"
      elif kor == ambil_isi_bluebox["b.mangga"]:
        ln += "📤"
      elif kor in wallblue:
        ln += "🧱"
      elif kor == (16, 8):
        ln += "➡️"
      else:
        ln += "🟨"
        
    print(ln)

def d_blue1():
    
  bck = (0, 2)
  obk = (16, 0)
  posc = (cacingx, cacingy)
  pos = (userbx1, userby1)
  ob1 = redb
  ob2 = masuk_isi_bluebox
  ob3 = ambil_isi_bluebox
  bb = bluebox
  kb = kapasitas_box
  if pos == obk:
    kc = "\033[33mInfo 🔑 [k]\033[0m"
  elif pos != obk:
    kc = ""
  print("┌────────────┐")
  print(f"│🟦 \033[34m BlueBox\033[0m │ ✛ : \033[32m{pos}\033[0m {kc}") 
  print("└────────────┘")
  print(f"𝐆𝐄 : {Game_end}    🪓 : {kapak}   🎣 : {pancingan}   🪱 : {cacing} \033[33m{posc}\033[0m")
  infopemain()
  print("│----------------------------------------│")
  print(info)
  
  if pos == obk:
    print(" [\033[33mKunci\033[0m] Untuk akses simpan & ambil item.")
  
  if pos == bck:
    print(" [\033[31mx\033[0m] untuk kembali »")
    
  elif pos == ob2["buah.stoberi"]:
    print(f" [🍓] Buah Stoberi (\033[32m{bluebox["buah.stoberi"]}\033[0m/\033[36m{kapasitas_box["buah.stoberi"]}\033[0m)")
  elif pos == ob2["buah.melon"]:
    print(f" [🍈] Buah Melon (\033[32m{bb["buah.melon"]}\033[0m/\033[36m{kb["buah.melon"]}\033[0m)")
  elif pos == ob2["buah.nanas"]:
    print(f" [🍍] Buah Nanas (\033[32m{bb["buah.nanas"]}\033[0m/\033[36m{kb["buah.nanas"]}\033[0m)")
  elif pos == ob2["buah.lemon"]:
    print(f" [🍋] Buah Lemon (\033[32m{bb["buah.lemon"]}\033[0m/\033[36m{kb["buah.lemon"]}\033[0m)")
  elif pos == ob2["buah.jeruk"]:
    print(f" [🍊] Buah Jeruk (\033[32m{bb["buah.jeruk"]}\033[0m/\033[36m{kb["buah.jeruk"]}\033[0m)")
  elif pos == ob2["buah.anggur"]:
    print(f" [🍇] Buah Anggur (\033[32m{bb["buah.anggur"]}\033[0m/\033[36m{kb["buah.anggur"]}\033[0m)")
  elif pos == ob2["buah.apelmerah"]:
    print(f" [🍎] Buah Apel merah (\033[32m{bb["buah.apelmerah"]}\033[0m/\033[36m{kb["buah.apelmerah"]}\033[0m)")
  elif pos == ob2["buah.apelhijau"]:
    print(f" [🍏] Buah Apel hijau (\033[32m{bb["buah.apelhijau"]}\033[0m/\033[36m{kb["buah.apelhijau"]}\033[0m)")
  elif pos == ob2["buah.pir"]:
    print(f" [🍐] Buah Pir (\033[32m{bb["buah.pir"]}\033[0m/\033[36m{kb["buah.pir"]}\033[0m)")
  elif pos == ob2["buah.mangga"]:
    print(f" [🥭] Buah Mangga (\033[32m{bb["buah.mangga"]}\033[0m/\033[36m{kb["buah.mangga"]}\033[0m)")
  elif pos == ob3["buah.stoberi"] or pos == ob3["buah.melon"] or pos == ob3["buah.nanas"] or pos == ob3["buah.lemon"] or pos == ob3["buah.jeruk"] or pos == ob3["buah.anggur"] or pos == ob3["buah.apelmerah"] or pos == ob3["buah.apelhijau"] or pos == ob3["buah.pir"] or pos == ob3["buah.mangga"]:
    print(" [📤] \033[32mAmbil item buah.\033[0m")
  
  
    
  print("│----------------------------------------│")
  print(" ")
  for y in range(bluey1):
    ln = ""
    for x in range(bluex1):
      kor = (x, y) 
      if kor == pos:
        if pusing > 0:
          ln += "😵"
        else:
          ln += "😍"
      elif kor == (ob1["x1"], ob1["y1"]):
        ln += "🔑"
      elif kor == ob2["buah.stoberi"]:
        ln += "🍓"
      elif kor == ob2["buah.melon"]:
        ln += "🍈"
      elif kor == ob2["buah.nanas"]:
        ln += "🍍"
      elif kor == ob2["buah.lemon"]:
        ln += "🍋"
      elif kor == ob2["buah.jeruk"]:
        ln += "🍊"
      elif kor == ob2["buah.anggur"]:
        ln += "🍇"
      elif kor == ob2["buah.apelmerah"]:
        ln += "🍎"
      elif kor == ob2["buah.apelhijau"]:
        ln += "🍏"
      elif kor == ob2["buah.pir"]:
        ln += "🍐"
      elif kor == ob2["buah.mangga"]:
        ln += "🥭"
      elif kor == ob3["buah.stoberi"]:
        ln += "📤"
      elif kor == ob3["buah.melon"]:
        ln += "📤"
      elif kor == ob3["buah.nanas"]:
        ln += "📤"
      elif kor == ob3["buah.lemon"]:
        ln += "📤"
      elif kor == ob3["buah.jeruk"]:
        ln += "📤"
      elif kor == ob3["buah.anggur"]:
        ln += "📤"
      elif kor == ob3["buah.apelmerah"]:
        ln += "📤"
      elif kor == ob3["buah.apelhijau"]:
        ln += "📤"
      elif kor == ob3["buah.pir"]:
        ln += "📤"
      elif kor == ob3["buah.mangga"]:
        ln += "📤"
      elif kor == bck:
        ln += "️🔙"
      elif kor in wallblue:
        ln += "🧱"
      else:
        ln += "🟨"
    
    print(ln)
    
def d_rbt():
  
  ob = ruang_bawah_tanah
  ob1 = pedang
  ob2 = monster
  pos = ob["userx1"], ob["usery1"]
  print(f"◎\033[32m{pos}\033[0m | 🗡 : \033[36m{pedang["pedang1"]}\033[0m | Hp : {Hp} | [i] [p]")
  
  for y in range(ob["ruangy1"]):
    ln = ""
    for x in range(ob["ruangx1"]):
        
      kor = (x, y)
      if kor == (ob["userx1"], ob["usery1"]):
        ln += "😍"
      elif kor == (19, 0):
        ln += "🪜"
      elif kor == (pedang["x1"], pedang["y1"]):
        if pedang["status1"] == True:
          ln += "[:"
        else:
          ln += "[🗡️"
      elif kor == (ob2["semut_hitam"]["x"], ob2["semut_hitam"]["y"]):
        if ob2["semut_hitam"]["status"] == True:
          ln += "::"
        else:
          ln += "🐜"
      elif kor == (ob2["nyamuk_hitam"]["x"], ob2["nyamuk_hitam"]["y"]):
        if ob2["nyamuk_hitam"]["status"] == True:
          ln += "::"
        else:
          ln += "🦟"
      elif kor == (ob2["laba2_hitam"]["x"], ob2["laba2_hitam"]["y"]):
        if ob2["laba2_hitam"]["status"] == True:
          ln += "::"
        else:
          ln += "🕷️🕸️"
      elif kor == (ob2["lalat_anomali"]["x"], ob2["lalat_anomali"]["y"]):
        if ob2["lalat_anomali"]["status"] == True:
          ln += "::"
        else:
          ln += "🪰"
      elif kor == (kunci_rbt["kunci1"]["x"], kunci_rbt["kunci1"]["y"]):
        if kunci_rbt["status1"] == True:
          ln += "::"
        else:
          ln += "🔒"
      elif kor == (ob2["2face"]["x"], ob2["2face"]["y"]):
        if ob2["2face"]["status"] == True:
          ln += "::"
        else:
          ln += "🎭"
      elif kor == (pa["semut_hitam"][0], pa["semut_hitam"][1]):
        if pos == (13, 10):
          if ob2["semut_hitam"]["status"] == False:
            ln += "!!"
          else:
            ln += "::"
        else:
          ln += "::"
      elif kor == (pa["nyamuk_hitam"][0], pa["nyamuk_hitam"][1]):
        if pos == (13, 15):
          if ob2["nyamuk_hitam"]["status"] == False:
            ln += "!!"
          else:
            ln += "::"
        else:
          ln += "::"
      elif kor == (pa["laba2_hitam"][0], pa["laba2_hitam"][1]):
        if pos == (14, 17):
          if ob2["laba2_hitam"]["status"] == False:
            ln += "!!"
          else:
            ln += "::"
        else:
          ln += "::"
      elif kor in batas_rbt:
        if pos == (13, 10):
          if ob2["semut_hitam"]["status"] == False:
            ln += "🐜"
          else:
            ln += "  "
        elif pos == (13, 15):
          if ob2["nyamuk_hitam"]["status"] == False:
            ln += "🦟"
          else:
            ln += "  "
        elif pos == (14, 17):
          if ob2["laba2_hitam"]["status"] == False:
            ln += "🕷️🕸️"
          else:
            ln += "  "
        else:
          ln += "  "
      else:
        ln += "::"
        
    print(ln)

def info_pedang():
  global pedang
  ob1 = pedang
  
  while True:
    os.system("clear")
    print(" ")
    print(" \033[32mInfo perlengkapan\033[0m ")
    print(" ")
    print(" \033[36mPedang\033[0m :")
    print(" ")
    print(" 🗡️ : ")
    print(f" Damage    : {ob1["damage1"]}")
    print(f" Hp pedang : {ob1["hp1"]}")
    print(" ")
    print(" Keluar »[x] Next »[n]")
    cmd = _getch()
    
    if cmd == "x":
      break
    
    elif cmd == "n":
      while True:
        os.system("clear")
        print(" ")
        print(" \033[32mItem yang didapat :\033[0m")
        print(" ")
        print(f" ➥ 🩹 : \033[32m{rw_rbt["plester"]}\033[0m")
        print(f" ")
        print(f" ➥  🗝️ : \033[32m{rw_rbt["kunci1"]}\033[0m")
        print(" ")
        print(f" ➥ 💊 : \033[32m{rw_rbt["pil1"]}\033[0m")
        print(" ")
        print(" Kembali »[x]")
        cmd = _getch()
        
        if cmd == "x":
          break
    
def info_musuh1():
  global monster
  ob1 = monster
  e1 = ""
  e2 = ""
  e3 = ""
  e4 = ""
  e5 = ""
  while True:
    os.system("clear")
    if ob1["semut_hitam"]["status"] == True:
      e1 = "\033[32mDikalahkan ✓\033[0m"
    if ob1["nyamuk_hitam"]["status"] == True:
      e2 = "\033[32mDikalahkan ✓\033[0m"
    if ob1["laba2_hitam"]["status"] == True:
      e3 = "\033[32mDikalahkan ✓\033[0m"
    if ob1["lalat_anomali"]["status"] == True:
      e4 = "\033[32mDikalahkan ✓\033[0m"
    if ob1["2face"]["status"] == True:
      e5 = "\033[32mDikalahkan ✓\033[0m"
      
    print(" ")
    print(" \033[32mMusuh Ruang bawah tanah : Stage 1\033[0m")
    print(" ")
    print(" Semut hitam     Laba-laba hitam")
    print(" 🐜 :            🕷️🕸️ :")
    print(f" Damage : {ob1["semut_hitam"]["damage"]}      Damage : {ob1["laba2_hitam"]["damage"]}")
    print(f" Hp     : \033[32m{ob1["semut_hitam"]["hp"]:<3}\033[0m    Hp     : \033[32m{ob1["laba2_hitam"]["hp"]:<3}\033[0m")
    print(f" {e1:<12}    {e3}")
    print(" ")
    print(" Nyamuk hitam    Lalat anomali")
    print(" 🦟 :            🪰 :")
    print(f" Damage : {ob1["nyamuk_hitam"]["damage"]}      Damage : {ob1["lalat_anomali"]["damage"]}")
    print(f" Hp     : \033[32m{ob1["nyamuk_hitam"]["hp"]:<3}\033[0m    Hp     : \033[32m{ob1["lalat_anomali"]["hp"]:<3}\033[0m")
    print(f" {e2:<12}    {e4}")
    print(" ")
    print(" \033[31m[BOSS]\033[0m: \033[36m2 Face\033[0m !")
    print(" 🎭 :")
    print(f" Damage : {ob1["2face"]["damage"]}")
    print(f" Hp : \033[32m{ob1["2face"]["hp"]}\033[0m")
    print(f" {e5}")
    print(" ")
    print(" \033[32mNote\033[0m :\n untuk menyerang monster »[m]\n dan setelah mengalahkan semua\n monster untuk merespawn semuanya kembali »[1]\n untuk heal »[h] ")
    print(" ")
    print(" Keluar »[x]")
    cmd = _getch()
    
    if cmd == "x":
      break
  
def heal():
  global rw_rbt, Hp
  
  if rw_rbt["plester"] >= 1:
    if Hp < 100:
      print(" ")
      print(" \033[32mMenggunakan plester sukses ✓\033[0m")
      time.sleep(0.456)
      Hp = 100
      rw_rbt["plester"] -= 1
    
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
  
  now_stoberi = time.time()
  for pos_stoberi in list(tanam_bibit_buah["respawn.tanam.stoberi"].keys()):
    if now_stoberi >= tanam_bibit_buah["respawn.tanam.stoberi"][pos_stoberi]:
      tanam_bibit_buah["tanam.bibit.stoberi"].remove(pos_stoberi)
      tanam_bibit_buah["panen.buah.stoberi"].add(pos_stoberi)
      del tanam_bibit_buah["respawn.tanam.stoberi"][pos_stoberi]
  
  now_melon = time.time()
  for pos_melon in list(tanam_bibit_buah["respawn.tanam.melon"].keys()):
    if now_melon >= tanam_bibit_buah["respawn.tanam.melon"][pos_melon]:
      tanam_bibit_buah["tanam.bibit.melon"].remove(pos_melon)
      tanam_bibit_buah["panen.buah.melon"].add(pos_melon)
      del tanam_bibit_buah["respawn.tanam.melon"][pos_melon]
  
  now_nanas = time.time()
  for pos_nanas in list(tanam_bibit_buah["respawn.tanam.nanas"].keys()):
    if now_nanas >= tanam_bibit_buah["respawn.tanam.nanas"][pos_nanas]:
      tanam_bibit_buah["tanam.bibit.nanas"].remove(pos_nanas)
      tanam_bibit_buah["panen.buah.nanas"].add(pos_nanas)
      del tanam_bibit_buah["respawn.tanam.nanas"][pos_nanas]
  
  now_lemon = time.time()
  for pos_lemon in list(tanam_bibit_buah["respawn.tanam.lemon"].keys()):
    if now_lemon >= tanam_bibit_buah["respawn.tanam.lemon"][pos_lemon]:
      tanam_bibit_buah["tanam.bibit.lemon"].remove(pos_lemon)
      tanam_bibit_buah["panen.buah.lemon"].add(pos_lemon)
      del tanam_bibit_buah["respawn.tanam.lemon"][pos_lemon]
      
  now_jeruk = time.time()
  for pos_jeruk in list(tanam_bibit_buah["respawn.tanam.jeruk"].keys()):
    if now_jeruk >= tanam_bibit_buah["respawn.tanam.jeruk"][pos_jeruk]:
      tanam_bibit_buah["tanam.bibit.jeruk"].remove(pos_jeruk)
      tanam_bibit_buah["panen.buah.jeruk"].add(pos_jeruk)
      del tanam_bibit_buah["respawn.tanam.jeruk"][pos_jeruk]
  
  now_anggur = time.time()
  for pos_anggur in list(tanam_bibit_buah["respawn.tanam.anggur"].keys()):
    if now_anggur >= tanam_bibit_buah["respawn.tanam.anggur"][pos_anggur]:
      tanam_bibit_buah["tanam.bibit.anggur"].remove(pos_anggur)
      tanam_bibit_buah["panen.buah.anggur"].add(pos_anggur)
      del tanam_bibit_buah["respawn.tanam.anggur"][pos_anggur]
  
  now_apelmerah = time.time()
  for pos_apelmerah in list(tanam_bibit_buah["respawn.tanam.apelmerah"].keys()):
    if now_apelmerah >= tanam_bibit_buah["respawn.tanam.apelmerah"][pos_apelmerah]:
      tanam_bibit_buah["tanam.bibit.apelmerah"].remove(pos_apelmerah)
      tanam_bibit_buah["panen.buah.apelmerah"].add(pos_apelmerah)
      del tanam_bibit_buah["respawn.tanam.apelmerah"][pos_apelmerah]
  
  now_apelhijau = time.time()
  for pos_apelhijau in list(tanam_bibit_buah["respawn.tanam.apelhijau"].keys()):
    if now_apelhijau >= tanam_bibit_buah["respawn.tanam.apelhijau"][pos_apelhijau]:
      tanam_bibit_buah["tanam.bibit.apelhijau"].remove(pos_apelhijau)
      tanam_bibit_buah["panen.buah.apelhijau"].add(pos_apelhijau)
      del tanam_bibit_buah["respawn.tanam.apelhijau"][pos_apelhijau]
  
  now_pir = time.time()
  for pos_pir in list(tanam_bibit_buah["respawn.tanam.pir"].keys()):
    if now_pir >= tanam_bibit_buah["respawn.tanam.pir"][pos_pir]:
      tanam_bibit_buah["tanam.bibit.pir"].remove(pos_pir)
      tanam_bibit_buah["panen.buah.pir"].add(pos_pir)
      del tanam_bibit_buah["respawn.tanam.pir"][pos_pir]
  
  now_mangga = time.time()
  for pos_mangga in list(tanam_bibit_buah["respawn.tanam.mangga"].keys()):
    if now_mangga >= tanam_bibit_buah["respawn.tanam.mangga"][pos_mangga]:
      tanam_bibit_buah["tanam.bibit.mangga"].remove(pos_mangga)
      tanam_bibit_buah["panen.buah.mangga"].add(pos_mangga)
      del tanam_bibit_buah["respawn.tanam.mangga"][pos_mangga]
  
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
    print("\033[32mNote\033[0m : \033[36mProgres Game » [70%]\033[0m")
    print(" ")
    print(" \033[31mGame ini tidak memiliki fitur save !\033[0m")
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
      
  elif worldpos == "portalblue":
    d_blue()
    
    cmd = _getch()
    
    oldx, oldy = userbx, userby
    roldx, roldy = redb["x"], redb["y"]
    
    pos = (userbx, userby)
    ob = (redb["x"], redb["y"])
    
    if cmd == "l":
      isibluebox()
    if cmd == "i":
      isiTas()
    if cmd == "h":
      hasilpancing()
   
    if cmd == "w" and pos == ob:
      redb["y"] -= 1
    elif cmd == "w":
      userby -= 1
        
    if cmd == "s" and pos == ob:
      redb["y"] += 1
    elif cmd == "s":
      userby += 1
        
    if cmd == "a" and pos == ob:
      redb["x"] -= 1
    elif cmd == "a":
      userbx -= 1
        
    if cmd == "d" and pos == ob:
      redb["x"] += 1
    elif cmd == "d":
      userbx += 1
    
    pos = (redb["x"], redb["y"])
    ob = wallblue
    if pos in ob:
      redb["x"], redb["y"] = roldx, roldy
      
    pos = (userbx, userby)
    ob = wallblue
    if pos in ob:
      userbx, userby = oldx, oldy
      info = " \033[33maduhhh 😵\033[0m"
      pusing = 3
    else:
      info = ""
    
    if pusing > 0:
      pusing -= 1
    
    if userbx < 0:
      userbx = 0
    elif userbx >= bluex:
      userbx = bluex -1
    if userby < 0:
      userby = 0
    elif userby >= bluey:
      userby = bluey -1
      
    if redb["x"] < 0: 
      redb["x"] = 0
    elif redb["x"] >= bluex:
      redb["x"] = bluex -1
    if redb["y"] < 0:
      redb["y"] = 0
    elif redb["y"] >= bluey:
      redb["y"] = bluey -1
      
    if cmd == "x":
      pos = (userbx, userby)
      ob = (0, 2)
      if pos == ob:
        worldpos = asal_world
    
    if cmd == "m":
      pos = (userbx, userby)
      ob = (16, 8)
      if pos == ob:
        worldpos = "portalblue1"
        
    pos = (redb["x"], redb["y"])
    ob = masuk_isi_bluebox
    if pos == ob["_bkayu"]:
      loadkayu()
    elif pos == ob["_bkayu1"]:
      loadkayu1()
    elif pos == ob["_bkayu2"]:
      loadkayu2()
    elif pos == ob["_bbibit"]:
      loadbibit()
    elif pos == ob["_bbibit2"]:
      loadbibit2()
    elif pos == ob["_bstoberi"]:
      loadstoberi()
    elif pos == ob["_bmelon"]:
      loadmelon()
    elif pos == ob["_bnanas"]:
      loadnanas()
    elif pos == ob["_blemon"]:
      loadlemon()
    elif pos == ob["_bjeruk"]:
      loadjeruk()
    elif pos == ob["_banggur"]:
      loadanggur()
    elif pos == ob["_bapelmerah"]:
      loadapelmerah()
    elif pos == ob["_bapelhijau"]:
      loadapelhijau()
    elif pos == ob["_bpir"]:
      loadpir()
    elif pos == ob["_bmangga"]:
      loadmangga()
    
    pos = (redb["x"], redb["y"])
    ob = ambil_isi_bluebox
    if pos == ob["kayu"]:
      ambilkayu()
    elif pos == ob["kayuT1"]:
      ambilkayu1()
    elif pos == ob["kayuT2"]:
      ambilkayu2()
    elif pos == ob["bibit"]:
      ambilbibit()
    elif pos == ob["bibit2"]:
      ambilbibit2()
    elif pos == ob["b.stoberi"]:
      ambilstoberi()
    elif pos == ob["b.melon"]:
      ambilmelon()
    elif pos == ob["b.nanas"]:
      ambilnanas()
    elif pos == ob["b.lemon"]:
      ambillemon()
    elif pos == ob["b.jeruk"]:
      ambiljeruk()
    elif pos == ob["b.anggur"]:
      ambilanggur()
    elif pos == ob["b.apelmerah"]:
      ambilapelmerah()
    elif pos == ob["b.apelhijau"]:
      ambilapelhijau()
    elif pos == ob["b.pir"]:
      ambilpir()
    elif pos == ob["b.mangga"]:
      ambilmangga()
  
  elif worldpos == "portalblue1":
    d_blue1()
    
    oldx, oldy = userbx1, userby1
    oldrx, oldry = redb["x1"], redb["y1"]
    
    cmd = _getch()
    
    pos = (userbx1, userby1)
    ob = (redb["x1"], redb["y1"])
    
    if cmd == "l":
      isibluebox()
    if cmd == "i":
      isiTas()
    if cmd == "h":
      hasilpancing()
    
    if cmd == "x":
      if pos == (0, 2):
        worldpos = "portalblue"
        
    
    if cmd == "w" and pos == ob:
      redb["y1"] -= 1
    elif cmd == "w":
      userby1 -= 1
      
    if cmd == "s" and pos == ob:
      redb["y1"] += 1
    elif cmd == "s":
      userby1 += 1
      
    if cmd == "a" and pos == ob:
      redb["x1"] -= 1
    elif cmd == "a":
      userbx1 -= 1
      
    if cmd == "d" and pos == ob:
      redb["x1"] += 1
    elif cmd == "d":
      userbx1 += 1
     
    if userbx1 < 0:
      userbx1 = 0
    elif userbx1 >= bluex1:
      userbx1 = bluex1 -1
    if userby1 < 0:
      userby1 = 0
    elif userby1 >= bluey1:
      userby1 = bluey1 -1
    
    if redb["x1"] < 0:
      redb["x1"] = 0
    elif redb["x1"] >= bluex1:
      redb["x1"] = bluex1 -1
    if redb["y1"] < 0:
      redb["y1"] = 0 
    elif redb["y1"] >= bluey1:
      redb["y1"] = bluey1 -1
    
    pos = (userbx1, userby1)
    ob = wallblue
    if pos in ob:
      userbx1, userby1 = oldx, oldy
      info = " \033[33maduhhh 😵\033[0m"
      pusing += 3
    else:
      info = ""
    
    if pusing > 0: 
      pusing -= 1

    pos = (redb["x1"], redb["y1"])
    ob = wallblue
    if pos in wallblue:
      redb["x1"], redb["y1"] = oldrx, oldry
    
    pos = (redb["x1"], redb["y1"])
    ob_ = masuk_isi_bluebox
    _ob = ambil_isi_bluebox
    if pos == ob_["buah.stoberi"]:
      loadbuahstoberi()
    elif pos == ob_["buah.melon"]:
      loadbuahmelon()
    elif pos == ob_["buah.nanas"]:
      loadbuahnanas()
    elif pos == ob_["buah.lemon"]:
      loadbuahlemon()
    elif pos == ob_["buah.jeruk"]:
      loadbuahjeruk()
    elif pos == ob_["buah.anggur"]:
      loadbuahanggur()
    elif pos == ob_["buah.apelmerah"]:
      loadbuahapelmerah()
    elif pos == ob_["buah.apelhijau"]:
      loadbuahapelhijau()
    elif pos == ob_["buah.pir"]:
      loadbuahpir()
    elif pos == ob_["buah.mangga"]:
      loadbuahmangga()
    elif pos == _ob["buah.stoberi"]:
      ambilbuahstoberi()
    elif pos == _ob["buah.melon"]:
      ambilbuahmelon()
    elif pos == _ob["buah.nanas"]:
      ambilbuahnanas()
    elif pos == _ob["buah.lemon"]:
      ambilbuahlemon()
    elif pos == _ob["buah.jeruk"]:
      ambilbuahjeruk()
    elif pos == _ob["buah.anggur"]:
      ambilbuahanggur()
    elif pos == _ob["buah.apelmerah"]:
      ambilbuahapelmerah()
    elif pos == _ob["buah.apelhijau"]:
      ambilbuahapelhijau()
    elif pos == _ob["buah.pir"]:
      ambilbuahpir()
    elif pos == _ob["buah.mangga"]:
      ambilbuahmangga()
  
  elif worldpos == "rbt":
    d_rbt()
    
    batas_lh = (pa["semut_hitam"][0], pa["semut_hitam"][1])
    batas_yh = (pa["nyamuk_hitam"][0], pa["nyamuk_hitam"][1])
    batas_l2b = (pa["laba2_hitam"][0], pa["laba2_hitam"][1])
    
    ob = ruang_bawah_tanah
    ob1 = monster
    pos = (ob["userx1"], ob["usery1"])
    oldx, oldy = ob["userx1"], ob["usery1"]
    back = oldx, oldy = ob["userx1"], ob["usery1"]
    cmd = _getch()
    
    uxr = "userx1"
    uyr = "usery1"
    rx = "ruangx1"
    ry = "ruangy1"
      
    if cmd == "w":
      ob[uyr] -=1
    elif cmd == "s":
      ob[uyr] += 1
    elif cmd == "a":
      ob[uxr] -= 1
    elif cmd == "d":
      ob[uxr] += 1
    
    if ob[uxr] < 0:
      ob[uxr] = 0
    elif ob[uxr] >= ob[rx]:
      ob[uxr] = ob[rx] -1
    
    if ob[uyr] < 0:
      ob[uyr] = 0
    elif ob[uyr] >= ob[ry]:
      ob[uyr] = ob[ry] -1
    
    if cmd == "i":
      info_musuh1()
    
    if cmd == "p":
      info_pedang()
    
    if cmd == "h":
      heal()
      
    if cmd == "m":
      if pos == (19, 0):
        print(" ")
        wkt()
        worldpos = "Rumah"
    
    if cmd == "1":
      if ob1["semut_hitam"]["status"] == True and ob1["nyamuk_hitam"]["status"] == True and ob1["laba2_hitam"]["status"] == True and ob1["lalat_anomali"]["status"] == True and ob1["2face"]["status"] == True and kunci_rbt["status1"] == True:
        print(" merespawn monster kembali »")
        time.sleep(28)
        ob1["semut_hitam"]["status"] = False
        ob1["semut_hitam"]["exp"] = 35
        ob1["semut_hitam"]["reward_kunci1"] = 0
        ob1["semut_hitam"]["damage"] = 0
        ob1["semut_hitam"]["plester"] = 1
        ob1["nyamuk_hitam"]["status"] = False
        ob1["nyamuk_hitam"]["exp"] = 35
        ob1["nyamuk_hitam"]["reward_kunci1"] = 0
        ob1["nyamuk_hitam"]["damage"] = 0
        ob1["nyamuk_hitam"]["plester"] = 1
        ob1["laba2_hitam"]["status"] = False
        ob1["laba2_hitam"]["exp"] = 35
        ob1["laba2_hitam"]["reward_kunci1"] = 0
        ob1["laba2_hitam"]["damage"] = 0
        ob1["laba2_hitam"]["plester"] = 1
        ob1["lalat_anomali"]["status"] = False
        ob1["lalat_anomali"]["exp"] = 35
        ob1["lalat_anomali"]["reward_kunci1"] = 0
        ob1["lalat_anomali"]["damage"] = 0
        ob1["lalat_anomali"]["plester"] = 1
        ob1["2face"]["status"] = False
        ob1["2face"]["exp"] = 70
        ob1["2face"]["plester"] = random.randint(1, 2)
        ob1["2face"]["damage"] = 25
    
    if (ob["userx1"], ob["usery1"]) in batas_rbt:
      ob["userx1"], ob["usery1"] = oldx, oldy
    
    if (ob["userx1"], ob["usery1"]) in wl_rbt:
      ob["userx1"], ob["usery1"] = oldx, oldy
    
    if cmd == "m":
      if pos == (kunci_rbt["kunci1"]["x"], kunci_rbt["kunci1"]["y"]):
        if rw_rbt["kunci1"] == kunci_rbt["need1"]:
          print(" ")
          print(" \033[32mBerhasil masuk ✓\033[0m")
          time.sleep(0.345)
          kunci_rbt["status1"] = True
          rw_rbt["kunci1"] = 0
          wl_rbt = back
        else:
          print(" ")
          print(" \033[31mKamu butuh kunci !\033[0m")
          time.sleep(0.345)
    #penghalang alur.
    
    if (ob["userx1"], ob["usery1"]) == (pa["semut_hitam"][0], pa["semut_hitam"][1]):
      if ob1["semut_hitam"]["status"] == True:
        batas_lh = back
      else:
        ob["userx1"], ob["usery1"] = oldx, oldy
    
    if (ob["userx1"], ob["usery1"]) == (pa["nyamuk_hitam"][0], pa["nyamuk_hitam"][1]):
      if ob1["nyamuk_hitam"]["status"] == True:
        batas_yh = back
      else:
        ob["userx1"], ob["usery1"] = oldx, oldy
        
    if (ob["userx1"], ob["usery1"]) == (pa["laba2_hitam"][0], pa["laba2_hitam"][1]):
      if ob1["laba2_hitam"]["status"] == True:
        batas_lb2 = back
      else:
        ob["userx1"], ob["usery1"] = oldx, oldy
    
    if cmd == "m":
      if not pedang["status1"] and pos == (pedang["x1"], pedang["y1"]):
        print(" ")
        print(" mengambil pedang »")
        time.sleep(1.23)
        pedang["pedang1"] += 1
        pedang["status1"] = True
        print(" ")
        print(" \033[32mSukses ✓\033[0m")
        time.sleep(0.345)
    
    if cmd == "t":
      if pedang["status1"] == True and pos == (pedang["x1"], pedang["y1"]):
        print(" ")
        print(" menaruh pedang »")
        time.sleep(1.23)
        pedang["pedang1"] = 0
        pedang["status1"] = False
        print(" ")
        print(" \033[32mSukses ✓\033[0m")
        time.sleep(0.345)
        
    if cmd == "m":
      if pos == (ob1["semut_hitam"]["x"], ob1["semut_hitam"]["y"]) and not ob1["semut_hitam"]["status"]:
        if pedang["pedang1"] == 1:
          if pedang["hp1"] >= 1:
            if ob1["semut_hitam"]["hp"] <= pedang["damage1"]:
              print(" ")
              print(" \033[32mKamu mulai menyerang semut hitam »\033[0m")
              time.sleep(1.23)
              ob1["semut_hitam"]["hp"] = 0
              print(" ")
              print(" \033[32mSukses membunuh ✓\033[0m")
              rw_rbt["kunci1"] += ob1["semut_hitam"]["reward_kunci1"]
              rw_rbt["plester"] += ob1["semut_hitam"]["plester"]
              pedang["damage1"] += ob1["semut_hitam"]["damage"]
              exp += ob1["semut_hitam"]["exp"]
              pedang["hp1"] -= 1
              time.sleep(0.345)
              ob1["semut_hitam"]["status"] = True
            elif Hp >= ob1["semut_hitam"]["damage"]:
              print(" ")
              print(" \033[32mKamu mulai menyerang semut hitam »\033[0m")
              print(" ")
              time.sleep(1.23)
              ob1["semut_hitam"]["hp"] -= pedang["damage1"]
              pedang["hp1"] -= 1
              print(" \033[31mSemut hitam menyerang balik »\033[0m")
              print(" ")
              time.sleep(1.23)
              Hp -= ob1["semut_hitam"]["damage"]
            elif Hp <= ob1["semut_hitam"]["damage"]:
              print(" ")
              print(" \033[32mKamu mulai menyerang semut hitam »\033[0m")
              print(" ")
              print(" \033[31mSemut hitam menyerang balik »\033[0m")
              time.sleep(1.23)
              os.system("clear")
              print(" \033[33mKamu kalah !\033[0m")
              print("    \033[31mGame over\033[0m   ")
              break
          elif pedang["hp1"] == 0:
            pedang["pedang1"] = 0
            print(" ")
            print(" Ambil pedang baru !")
            pedang["hp1"] += pedang["reloadhp"]
            pedang["status1"] = False
            time.sleep(0.345)
        
        else:
          print(" ")
          print(" ambil pedang terlebih dahulu!")
          time.sleep(0.345)
         
    if cmd == "m":
      if pos == (ob1["nyamuk_hitam"]["x"], ob1["nyamuk_hitam"]["y"]) and not ob1["nyamuk_hitam"]["status"]:
        if pedang["pedang1"] == 1:
          if pedang["hp1"] >= 1:
            if ob1["nyamuk_hitam"]["hp"] <= pedang["damage1"]:
              print(" ")
              print(" \033[32mKamu mulai menyerang nyamuk hitam »\033[0m")
              time.sleep(1.23)
              ob1["nyamuk_hitam"]["hp"] = 0
              print(" ")
              print(" \033[32mSukses membunuh ✓\033[0m")
              rw_rbt["kunci1"] += ob1["nyamuk_hitam"]["reward_kunci1"]
              rw_rbt["plester"] += ob1["nyamuk_hitam"]["plester"]
              pedang["damage1"] += ob1["nyamuk_hitam"]["damage"]
              exp += ob1["nyamuk_hitam"]["exp"]
              pedang["hp1"] -= 1
              time.sleep(0.345)
              ob1["nyamuk_hitam"]["status"] = True
            elif Hp >= ob1["nyamuk_hitam"]["damage"]:
              print(" ")
              print(" \033[32mKamu mulai menyerang nyamuk hitam »\033[0m")
              print(" ")
              time.sleep(1.23)
              ob1["nyamuk_hitam"]["hp"] -= pedang["damage1"]
              pedang["hp1"] -= 1
              print(" \033[31mNyamuk hitam menyerang balik »\033[0m")
              print(" ")
              time.sleep(1.23)
              Hp -= ob1["nyamuk_hitam"]["damage"]
            elif Hp <= ob1["nyamuk_hitam"]["damage"]:
              print(" ")
              print(" \033[32mKamu mulai menyerang nyamuk hitam »\033[0m")
              print(" ")
              print(" \033[31mNyamuk hitam menyerang balik »\033[0m")
              time.sleep(1.23)
              os.system("clear")
              print(" \033[33mKamu kalah !\033[0m")
              print("    \033[31mGame over\033[0m   ")
              break
          elif pedang["hp1"] == 0:
            pedang["pedang1"] = 0
            print(" ")
            print(" Ambil pedang baru !")
            pedang["hp1"] += pedang["reloadhp"]
            pedang["status1"] = False
            time.sleep(0.345)
            
        else:
          print(" ")
          print(" ambil pedang terlebih dahulu!")
          time.sleep(0.345)
    
    if cmd == "m":
      if pos == (ob1["laba2_hitam"]["x"], ob1["laba2_hitam"]["y"]) and not ob1["laba2_hitam"]["status"]:
        if pedang["pedang1"] == 1:
          if pedang["hp1"] >= 1:
            if ob1["laba2_hitam"]["hp"] <= pedang["damage1"]:
              print(" ")
              print(" \033[32mKamu mulai menyerang laba-laba hitam »\033[0m")
              time.sleep(1.23)
              ob1["laba2_hitam"]["hp"] = 0
              print(" ")
              print(" \033[32mSukses membunuh ✓\033[0m")
              rw_rbt["kunci1"] += ob1["laba2_hitam"]["reward_kunci1"]
              rw_rbt["plester"] += ob1["laba2_hitam"]["plester"]
              pedang["damage1"] += ob1["laba2_hitam"]["damage"]
              exp += ob1["laba2_hitam"]["exp"]
              pedang["hp1"] -= 1
              time.sleep(0.345)
              ob1["laba2_hitam"]["status"] = True
            elif Hp >= ob1["laba2_hitam"]["damage"]:
              print(" ")
              print(" \033[32mKamu mulai menyerang laba-laba hitam »\033[0m")
              print(" ")
              time.sleep(1.23)
              ob1["laba2_hitam"]["hp"] -= pedang["damage1"]
              pedang["hp1"] -= 1
              print(" \033[31mLaba-laba hitam menyerang balik »\033[0m")
              print(" ")
              time.sleep(1.23)
              Hp -= ob1["laba2_hitam"]["damage"]
            elif Hp <= ob1["laba2_hitam"]["damage"]:
              print(" ")
              print(" \033[32mKamu mulai menyerang laba-laba hitam »\033[0m")
              print(" ")
              print(" \033[31mLaba-laba hitam menyerang balik »\033[0m")
              time.sleep(1.23)
              os.system("clear")
              print(" \033[33mKamu kalah !\033[0m")
              print("    \033[31mGame over\033[0m   ")
              break
          elif pedang["hp1"] == 0:
            pedang["pedang1"] = 0
            print(" ")
            print(" Ambil pedang baru !")
            pedang["hp1"] += pedang["reloadhp"]
            pedang["status1"] = False
            time.sleep(0.345)
            
        else:
          print(" ")
          print(" ambil pedang terlebih dahulu!")
          time.sleep(0.345)
    
    if cmd == "m":
      if pos == (ob1["lalat_anomali"]["x"], ob1["lalat_anomali"]["y"]) and not ob1["lalat_anomali"]["status"]:
        if pedang["pedang1"] == 1:
          if pedang["hp1"] >= 1:
            if ob1["lalat_anomali"]["hp"] <= pedang["damage1"]:
              print(" ")
              print(" \033[32mKamu mulai menyerang lalat anomali »\033[0m")
              time.sleep(1.23)
              ob1["lalat_anomali"]["hp"] = 0
              print(" ")
              print(" \033[32mSukses membunuh ✓\033[0m")
              rw_rbt["kunci1"] += ob1["lalat_anomali"]["reward_kunci1"]
              rw_rbt["plester"] += ob1["lalat_anomali"]["plester"]
              pedang["damage1"] += ob1["lalat_anomali"]["damage"]
              exp += ob1["lalat_anomali"]["exp"]
              pedang["hp1"] -= 1
              time.sleep(0.345)
              ob1["lalat_anomali"]["status"] = True
            elif Hp >= ob1["lalat_anomali"]["damage"]:
              print(" ")
              print(" \033[32mKamu mulai menyerang lalat anomali »\033[0m")
              print(" ")
              time.sleep(1.23)
              ob1["lalat_anomali"]["hp"] -= pedang["damage1"]
              pedang["hp1"] -= 1
              print(" \033[31mLalat anomali menyerang balik »\033[0m")
              print(" ")
              time.sleep(1.23)
              Hp -= ob1["lalat_anomali"]["damage"]
            elif Hp <= ob1["lalat_anomali"]["damage"]:
              print(" ")
              print(" \033[32mKamu mulai menyerang lalat anomali »\033[0m")
              print(" ")
              print(" \033[31mLalat anomali menyerang balik »\033[0m")
              time.sleep(1.23)
              os.system("clear")
              print(" \033[33mKamu kalah !\033[0m")
              print("    \033[31mGame over\033[0m   ")
              break
          elif pedang["hp1"] == 0:
            pedang["pedang1"] = 0
            print(" ")
            print(" Ambil pedang baru !")
            pedang["hp1"] += pedang["reloadhp"]
            pedang["status1"] = False
            time.sleep(0.345)
            
        else:
          print(" ")
          print(" ambil pedang terlebih dahulu!")
          time.sleep(0.345)
          
    #BOSS1
    if cmd == "m":
      if pos == (ob1["2face"]["x"], ob1["2face"]["y"]) and not ob1["2face"]["status"]:
        if pedang["pedang1"] == 1:
          if pedang["hp1"] >= 1:
            if ob1["2face"]["hp"] <= pedang["damage1"]:
              print(" ")
              print(" \033[32mKamu mulai menyerang BOSS : 2 Face »\033[0m")
              time.sleep(1.23)
              ob1["2face"]["hp"] = 0
              print(" ")
              print(" \033[32mSukses membunuh BOSS ✓\033[0m")
              rw_rbt["pil1"] += ob1["2face"]["reward_pil1"]
              rw_rbt["plester"] += ob1["2face"]["plester"]
              exp += ob1["2face"]["exp"]
              pedang["damage1"] += ob1["2face"]["damage"]
              pedang["hp1"] -= 1
              time.sleep(0.345)
              ob1["2face"]["status"] = True
            elif Hp >= ob1["2face"]["damage"]:
              print(" ")
              print(" \033[32mKamu mulai menyerang BOSS : 2 Face »\033[0m")
              print(" ")
              time.sleep(1.23)
              ob1["2face"]["hp"] -= pedang["damage1"]
              pedang["hp1"] -= 1
              print(" \033[31mBOSS : 2 Face menyerang balik »\033[0m")
              print(" ")
              time.sleep(1.23)
              Hp -= ob1["2face"]["damage"]
            elif Hp <= ob1["2face"]["damage"]:
              print(" ")
              print(" \033[32mKamu mulai menyerang BOSS : 2 Face »\033[0m")
              print(" ")
              print(" \033[31mBOSS : 2 Face hitam menyerang balik »\033[0m")
              time.sleep(1.23)
              os.system("clear")
              print(" \033[33mKamu kalah !\033[0m")
              print("    \033[31mGame over\033[0m   ")
              break
          elif pedang["hp1"] == 0:
            pedang["pedang1"] = 0
            print(" ")
            print(" Ambil pedang baru !")
            pedang["hp1"] += pedang["reloadhp"]
            pedang["status1"] = False
            time.sleep(0.345)
            
        else:
          print(" ")
          print(" ambil pedang terlebih dahulu!")
          time.sleep(0.345)
    
    
    
  #RUMAH(HOME)
  elif worldpos == "Rumah":
    d_rumah()
    _dashboard()
    
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
    if cmd == "l":
      isibluebox()
      
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
    
    #ruang bawah tanah
    
    if cmd == "m":
      pos = (userx, usery)
      ob = (tanggax, tanggay)
      if pos == ob:
        print(" ")
        wkt()
        worldpos = "rbt"
        
    #ambil portal
    if cmd == "b":
      pos = (userx, usery)
      ob = (blue["x"], blue["y"])
      ob1 = blue["Status"]
      if worldpos == blue["world"]:
        if not ob1 and pos == ob:
          blue["x"] = userx
          blue["y"] = usery
          blue["Status"] = True
          infoblue = "🟦"
        
    #taruh portal
    if cmd == "t":
      if blue["Status"]:
        blue["Status"] = False
        blue["world"] = worldpos
        blue["x"] = userx
        blue["y"] = usery
        infoblue = ""
          
    #masuk portal     
    if cmd == "m":
      pos = (userx, usery)
      ob = (blue["x"], blue["y"])
      if worldpos == blue["world"] and pos == ob:
        asal_world = worldpos
        worldpos = "portalblue"
    
    

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
    ##Misi
    if cmd == "m":
      pos = (userx, usery)
      ob = misi
      obj = (ksuratx, ksuraty)
      if pos == obj:
        if ob["cek.bibit1"] == "✓" and ob["cek.bibit2"] == "✓" and ob["cek.kayu0"] == "✓" and ob["cek.kayu1"] == "✓" and ob["cek.kayu2"] == "✓":
          misi2()
        elif ob["cek.bibit.stoberi"] == "✓" and ob["cek.bibit.melon"] == "✓" and ob["cek.bibit.nanas"] == "✓" and ob["cek.bibit.lemon"] == "✓" and ob["cek.bibit.jeruk"] == "✓":
          misi3()
        else:
          misi1()
    
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
    
    cmd = _getch()
    
    oldx, oldy = userx1, usery1
    
    if cmd == "l":
      isibluebox()
    if cmd == "k":
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
     
    #ambil portal
    if cmd == "b":
      pos = (userx1, usery1)
      ob = (blue["x"], blue["y"])
      ob1 = blue["Status"]
      if worldpos == blue["world"]:
        if not ob1 and pos == ob:
          blue["x"] = userx1
          blue["y"] = usery1
          blue["Status"] = True
          infoblue = "🟦"
        
    #taruh portal
    elif cmd == "t":
      if blue["Status"]:
        blue["Status"] = False
        blue["world"] = worldpos
        blue["x"] = userx1
        blue["y"] = usery1
        infoblue = ""
          
    #masuk portal     
    if cmd == "m":
      pos = (userx1, usery1)
      ob = (blue["x"], blue["y"])
      if worldpos == blue["world"] and pos == ob:
        asal_world = worldpos
        worldpos = "portalblue"
        
        
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
        if pancingan <= 0:
          print(" ")
          print(" Mengambil pancingan »")
          pancingan += 50
          time.sleep(0.345)
        
    if cmd == "m":
      pos = (userx1, usery1)
      obj = (cacingx, cacingy)
      if pos == obj:
        if cacing <= 0:
          cacing += 10
          cacingx, cacingy = random.randint(0, kebunx -1), random.randint(0, kebuny -1)
    if cmd == "m":
      pos = (userx1, usery1)
      obj = pinggir_kolam
      if pos in obj:
        memancing()
    
    if cmd == "h":
      hasilpancing()
      
    #part menanam buah.
    if cmd == "g":
      pos = (userx1, usery1)
      kt = k_lahan
      if pos in kt:
        tanambibitbuah()
    #part memanen buah  
    if cmd == "r":
      pos = (userx1, usery1)
      kl = k_lahan
      if pos in kl:
        panenbibitbuah()
          
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
    if cmd == "m":
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
    if cmd == "m":
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
    
    cmd = _getch()
    
    oldx, oldy = userxp, useryp
    
    if cmd == "i":
      isiTas()
    if cmd == "l":
      isibluebox()
    
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
      
    #ambil portal
    if cmd == "b":
      pos = (userxp, useryp)
      ob = (blue["x"], blue["y"])
      ob1 = blue["Status"]
      if worldpos == blue["world"]:
        if not ob1 and pos == ob:
          blue["x"] = userxp
          blue["y"] = useryp
          blue["Status"] = True
          infoblue = "🟦"
        
    #taruh portal
    elif cmd == "t":
      if blue["Status"]:
        blue["Status"] = False
        blue["world"] = worldpos
        blue["x"] = userxp
        blue["y"] = useryp
        infoblue = ""
          
    #masuk portal     
    if cmd == "m":
      pos = (userxp, useryp)
      ob = (blue["x"], blue["y"])
      if worldpos == blue["world"] and pos == ob:
        asal_world = worldpos
        worldpos = "portalblue"
    
    
    if cmd == "m":
      pos = (userxp, useryp)
      obj = (npcmebelx, npcmebely)
      if pos == obj:
        npcmebel()
    
    
    
    pos = (userxp, useryp)
    obj1 = jendela_tokbit
    obj2 = depantokbit
    if pos in obj1 or pos in obj2:
      userxp, useryp = oldx, oldy
    
    pos = (userxp, useryp)
    obj1 = figurikan
    obj2 = pancuranikan
    if pos in obj1 or pos in obj2:
      userxp, useryp = oldx, oldy
        
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
    
    if cmd == "m":
      pos = (userxp, useryp)
      obj = Tk
      if pos in obj:
        print(" ")
        print(" Masuk ketoko jual/beli ikan »")
        print(" ")
        wkt()
        tokoikan()

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

  if Game_end == 10:
    # Broadcast game over ke semua pemain di room
    _sync_mp(game_over=True)
    os.system("clear")
    print(" ")
    print(" \033[32m╔═══════════════════════════════╗\033[0m")
    print(" \033[32m║ 🏆 KAMU MENANG! Misi selesai! ║\033[0m")
    print(" \033[32m╚═══════════════════════════════╝\033[0m")
    print(" ")
    print(" \033[32mOsot bolosot aku hebat!\033[0m")
    print(" ")
    input(" ➥ Enter untuk keluar.")
    break
