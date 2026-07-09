#!/usr/bin/env python3
"""
████████╗███████╗██████╗ ███╗   ███╗██╗   ██╗██╗  ██╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║   ██║╚██╗██╔╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║ ╚███╔╝
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║ ██╔██╗
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝██╔╝ ██╗
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝
 ██████╗██╗  ██╗ █████╗ ████████╗
██╔════╝██║  ██║██╔══██╗╚══██╔══╝
██║     ███████║███████║   ██║
██║     ██╔══██║██╔══██║   ██║
╚██████╗██║  ██║██║  ██║   ██║
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝

[ Online Chat via MQTT — paho.mqtt.client ]
"""

import paho.mqtt.client as mqtt
import json
import sys
import os
import time
import random
import signal
from datetime import datetime

# ─────────────────────────────────────────────────────
#  Detect paho-mqtt version — fix DeprecationWarning
#  Use hasattr check instead of __version__ (not always present)
# ─────────────────────────────────────────────────────
PAHO_V2 = hasattr(mqtt, "CallbackAPIVersion")  # True on paho-mqtt >= 2.0

try:
    from importlib.metadata import version as _pkg_ver
    PAHO_VERSION_STR = _pkg_ver("paho-mqtt")
except Exception:
    PAHO_VERSION_STR = "2.x" if PAHO_V2 else "1.x"

# ─────────────────────────────────────────────────────
#  ANSI COLORS
# ─────────────────────────────────────────────────────
class C:
    RESET      = "\033[0m"
    BOLD       = "\033[1m"
    DIM        = "\033[2m"
    NEON       = "\033[38;2;57;255;20m"      # bright neon green
    LIME       = "\033[38;2;127;255;0m"
    OWN        = "\033[38;2;180;255;80m"     # own messages
    SYSTEM     = "\033[38;2;184;160;0m"      # amber system
    TIME       = "\033[38;2;80;160;80m"      # dim timestamp
    BORDER     = "\033[38;2;57;255;20m"
    ERROR      = "\033[38;2;255;60;60m"
    STATUS     = "\033[38;2;100;200;100m"

    # Accent colors for usernames (cycle by hash)
    ACCENTS = [
        "\033[38;2;255;107;107m",   # red
        "\033[38;2;255;217;61m",    # yellow
        "\033[38;2;107;180;255m",   # blue
        "\033[38;2;255;107;255m",   # purple
        "\033[38;2;107;255;255m",   # cyan
        "\033[38;2;255;160;50m",    # orange
    ]

def user_color(name: str) -> str:
    return C.ACCENTS[hash(name) % len(C.ACCENTS)]

# ─────────────────────────────────────────────────────
#  BROKER LIST  (tries each in order)
# ─────────────────────────────────────────────────────
BROKERS = [
    ("broker.hivemq.com",      1883),
    ("test.mosquitto.org",     1883),
    ("broker.emqx.io",         1883),
    ("mqtt.eclipseprojects.io", 1883),
]

TOPIC_PREFIX = "termuxchat"
KEEPALIVE    = 60

# ─────────────────────────────────────────────────────
#  GLOBAL STATE
# ─────────────────────────────────────────────────────
state = {
    "username":    "",
    "channel":     "general",
    "connected":   False,
    "running":     True,
    "users_seen":  set(),
    "broker_host": BROKERS[0][0],
    "broker_port": BROKERS[0][1],
}

client: mqtt.Client = None

# ─────────────────────────────────────────────────────
#  PRINT HELPERS
# ─────────────────────────────────────────────────────
def now() -> str:
    return datetime.now().strftime("%H:%M:%S")

def clear():
    os.system("clear")

def _write(line: str):
    sys.stdout.write("\r" + line + "\n")
    sys.stdout.flush()

def print_system(msg: str):
    _write(f"{C.TIME}[{now()}]{C.RESET} {C.SYSTEM}* {msg}{C.RESET}")
    _prompt()

def print_chat(username: str, text: str, is_own=False):
    color = C.OWN if is_own else user_color(username)
    _write(f"{C.TIME}[{now()}]{C.RESET} {color}{C.BOLD}<{username}>{C.RESET} {color if is_own else ''}{text}{C.RESET}")
    _prompt()

def print_error(msg: str):
    _write(f"{C.ERROR}[ERR]{C.RESET} {msg}")
    _prompt()

def _prompt():
    ch   = state["channel"]
    user = state["username"]
    dot  = f"{C.NEON}●{C.RESET}" if state["connected"] else f"{C.ERROR}○{C.RESET}"
    sys.stdout.write(
        f"{C.DIM}┌[{C.NEON}{user}{C.DIM}@{C.NEON}#{ch}{C.DIM}] {dot}\n"
        f"└─{C.RESET}{C.NEON}${C.RESET} "
    )
    sys.stdout.flush()

def print_border():
    print(f"{C.BORDER}{'─'*52}{C.RESET}")

# ─────────────────────────────────────────────────────
#  MQTT PUBLISH HELPERS
# ─────────────────────────────────────────────────────
def _topic() -> str:
    return f"{TOPIC_PREFIX}/{state['channel']}"

def _publish(payload: dict):
    if not state["connected"] or client is None:
        return
    try:
        msg = json.dumps(payload)
        client.publish(_topic(), msg, qos=1)
    except Exception:
        pass

def _presence(ptype: str):
    _publish({"type": ptype, "username": state["username"], "timestamp": int(time.time())})

def send_message(text: str):
    if not state["connected"]:
        print_error("Not connected. Try /reconnect")
        return
    _publish({
        "type":      "message",
        "username":  state["username"],
        "text":      text,
        "timestamp": int(time.time()),
    })

def join_channel(new_ch: str):
    _presence("leave")
    client.unsubscribe(_topic())
    state["channel"] = new_ch
    state["users_seen"].clear()
    client.subscribe(_topic())
    _presence("join")
    print_system(f"Switched to #{new_ch}")

# ─────────────────────────────────────────────────────
#  MQTT CALLBACKS  (compatible with paho v1 AND v2)
# ─────────────────────────────────────────────────────
def _on_connect_v1(client, userdata, flags, rc):
    if rc == 0:
        state["connected"] = True
        client.subscribe(_topic())
        print_system(f"Connected to {state['broker_host']} — #{state['channel']}")
        _presence("join")
    else:
        print_error(f"Connect failed rc={rc}  (trying next broker...)")

def _on_connect_v2(client, userdata, connect_flags, reason_code, properties):
    # In paho v2, reason_code is a ReasonCode object; 0 = success
    rc = reason_code if isinstance(reason_code, int) else reason_code.value
    _on_connect_v1(client, userdata, connect_flags, rc)

def _on_disconnect_v1(client, userdata, rc):
    state["connected"] = False
    if rc != 0:
        print_system(f"Disconnected (rc={rc}) — will reconnect automatically...")

def _on_disconnect_v2(client, userdata, disconnect_flags, reason_code, properties):
    rc = reason_code if isinstance(reason_code, int) else reason_code.value
    _on_disconnect_v1(client, userdata, rc)

def _on_message(client, userdata, msg):
    try:
        payload  = json.loads(msg.payload.decode("utf-8"))
        mtype    = payload.get("type", "message")
        username = payload.get("username", "???")
        text     = payload.get("text", "")

        if mtype == "message":
            state["users_seen"].add(username)
            print_chat(username, text, is_own=(username == state["username"]))

        elif mtype == "join":
            state["users_seen"].add(username)
            if username != state["username"]:
                print_system(f"{username} joined #{state['channel']}")

        elif mtype == "leave":
            if username != state["username"]:
                print_system(f"{username} left #{state['channel']}")
    except Exception:
        pass

# ─────────────────────────────────────────────────────
#  BUILD CLIENT
# ─────────────────────────────────────────────────────
def build_client(host: str, port: int) -> mqtt.Client:
    client_id = f"tc_{state['username']}_{random.randint(1000, 9999)}"

    if PAHO_V2:
        # paho-mqtt >= 2.0 — use VERSION2 API to suppress DeprecationWarning
        c = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=client_id,
            protocol=mqtt.MQTTv311,
        )
        c.on_connect    = _on_connect_v2
        c.on_disconnect = _on_disconnect_v2
    else:
        # paho-mqtt < 2.0 — classic API
        c = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311)
        c.on_connect    = _on_connect_v1
        c.on_disconnect = _on_disconnect_v1

    c.on_message = _on_message

    # auto-reconnect settings
    c.reconnect_delay_set(min_delay=2, max_delay=30)
    return c

# ─────────────────────────────────────────────────────
#  BROKER CONNECTION  (try each broker in list)
# ─────────────────────────────────────────────────────
def connect_best_broker() -> mqtt.Client:
    global client
    for host, port in BROKERS:
        print(f"  {C.STATUS}>{C.RESET} Trying {host}:{port} ...", end=" ", flush=True)
        c = build_client(host, port)
        try:
            c.connect(host, port, KEEPALIVE)
            c.loop_start()
            # wait up to 4 s for on_connect
            deadline = time.time() + 4
            while not state["connected"] and time.time() < deadline:
                time.sleep(0.1)
            if state["connected"]:
                print(f"{C.NEON}OK{C.RESET}")
                state["broker_host"] = host
                state["broker_port"] = port
                client = c
                return c
            else:
                print(f"{C.ERROR}timeout{C.RESET}")
                c.loop_stop()
                c.disconnect()
        except Exception as e:
            print(f"{C.ERROR}failed ({e}){C.RESET}")
            try:
                c.loop_stop()
            except Exception:
                pass

    return None  # all brokers failed

# ─────────────────────────────────────────────────────
#  COMMANDS
# ─────────────────────────────────────────────────────
HELP = f"""
{C.BORDER}┌{'─'*46}┐{C.RESET}
{C.BORDER}│{C.RESET}  {C.NEON}AVAILABLE COMMANDS{C.RESET}                            {C.BORDER}│{C.RESET}
{C.BORDER}├{'─'*46}┤{C.RESET}
{C.BORDER}│{C.RESET}  {C.ACCENTS[2]}/join #channel{C.RESET}   switch channel              {C.BORDER}│{C.RESET}
{C.BORDER}│{C.RESET}  {C.ACCENTS[2]}/nick newname{C.RESET}    change nickname             {C.BORDER}│{C.RESET}
{C.BORDER}│{C.RESET}  {C.ACCENTS[2]}/users{C.RESET}           list users seen             {C.BORDER}│{C.RESET}
{C.BORDER}│{C.RESET}  {C.ACCENTS[2]}/info{C.RESET}            connection info             {C.BORDER}│{C.RESET}
{C.BORDER}│{C.RESET}  {C.ACCENTS[2]}/reconnect{C.RESET}       reconnect to broker         {C.BORDER}│{C.RESET}
{C.BORDER}│{C.RESET}  {C.ACCENTS[2]}/clear{C.RESET}           clear screen                {C.BORDER}│{C.RESET}
{C.BORDER}│{C.RESET}  {C.ACCENTS[2]}/quit  /exit{C.RESET}     leave chat                  {C.BORDER}│{C.RESET}
{C.BORDER}│{C.RESET}  {C.ACCENTS[2]}/help{C.RESET}            show this help              {C.BORDER}│{C.RESET}
{C.BORDER}└{'─'*46}┘{C.RESET}
"""

def handle_command(raw: str) -> bool:
    parts = raw.strip().split(maxsplit=1)
    cmd   = parts[0].lower()
    arg   = parts[1].strip() if len(parts) > 1 else ""

    if cmd in ("/quit", "/exit", "/q"):
        _presence("leave")
        print_system("Disconnecting... Goodbye!")
        state["running"] = False
        return True

    if cmd == "/help":
        print(HELP)
        return True

    if cmd == "/clear":
        clear()
        _header()
        return True

    if cmd == "/join":
        ch = arg.lstrip("#").strip()
        if not ch:
            print_error("Usage: /join #channel")
        else:
            join_channel(ch)
        return True

    if cmd == "/nick":
        nick = arg.strip()
        if not nick:
            print_error("Usage: /nick newname")
        elif len(nick) > 20:
            print_error("Max 20 chars")
        else:
            old = state["username"]
            _presence("leave")
            state["username"] = nick
            _presence("join")
            print_system(f"Now known as {nick} (was: {old})")
        return True

    if cmd == "/users":
        users = sorted(state["users_seen"])
        print_system("Users seen: " + (", ".join(users) if users else "(none yet)"))
        return True

    if cmd == "/info":
        st = f"{C.NEON}ONLINE{C.RESET}" if state["connected"] else f"{C.ERROR}OFFLINE{C.RESET}"
        print(f"\n{C.BORDER}{'─'*46}{C.RESET}")
        print(f"  {C.ACCENTS[2]}Broker  :{C.RESET} {state['broker_host']}:{state['broker_port']}")
        print(f"  {C.ACCENTS[2]}Channel :{C.RESET} #{state['channel']}")
        print(f"  {C.ACCENTS[2]}Username:{C.RESET} {state['username']}")
        print(f"  {C.ACCENTS[2]}Status  :{C.RESET} {st}")
        print(f"  {C.ACCENTS[2]}paho ver:{C.RESET} {PAHO_VERSION_STR}  (api={'v2' if PAHO_V2 else 'v1'})")
        print(f"{C.BORDER}{'─'*46}{C.RESET}\n")
        return True

    if cmd == "/reconnect":
        print_system("Reconnecting...")
        try:
            client.reconnect()
        except Exception as e:
            print_error(f"Reconnect failed: {e}")
        return True

    return False

# ─────────────────────────────────────────────────────
#  UI HELPERS
# ─────────────────────────────────────────────────────
BANNER = f"""
{C.NEON}{C.BOLD}
 ████████╗███████╗██████╗ ███╗   ███╗██╗   ██╗██╗  ██╗
 ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║   ██║╚██╗██╔╝
    ██║   █████╗  ██████╔╝██╔████╔██║██║   ██║ ╚███╔╝
    ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║ ██╔██╗
    ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝██╔╝ ██╗
    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝{C.RESET}
{C.LIME}{C.BOLD}        ██████╗██╗  ██╗ █████╗ ████████╗
       ██╔════╝██║  ██║██╔══██╗╚══██╔══╝
       ██║     ███████║███████║   ██║
       ██║     ██╔══██║██╔══██║   ██║
       ╚██████╗██║  ██║██║  ██║   ██║
        ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝{C.RESET}
"""

def _header():
    print(f"{C.BORDER}╔{'═'*50}╗{C.RESET}")
    print(f"{C.BORDER}║{C.RESET}{'TERMUX CHAT  — paho.mqtt.client'.center(50)}{C.BORDER}║{C.RESET}")
    print(f"{C.BORDER}╚{'═'*50}╝{C.RESET}")
    print(f"{C.DIM}  /help for commands{C.RESET}\n")

def boot_sequence():
    clear()
    print(BANNER)
    steps = [
        "Initializing paho.mqtt.client...",
        f"Callback API: {'VERSION2 (v2)' if PAHO_V2 else 'VERSION1 (v1)'}",
        "Loading pixel interface...",
        "Ready.",
    ]
    for s in steps:
        print(f"  {C.NEON}>{C.RESET} {s}")
        time.sleep(0.2)
    print()

def get_login() -> tuple:
    print(f"  {C.BORDER}┌{'─'*40}┐{C.RESET}")
    print(f"  {C.BORDER}│{C.RESET}  {C.NEON}LOGIN{C.RESET}                                  {C.BORDER}│{C.RESET}")
    print(f"  {C.BORDER}└{'─'*40}┘{C.RESET}\n")

    while True:
        sys.stdout.write(f"  {C.NEON}username{C.RESET} > ")
        sys.stdout.flush()
        username = input().strip()
        if 1 <= len(username) <= 20:
            break
        print(f"  {C.ERROR}Must be 1-20 chars.{C.RESET}")

    sys.stdout.write(f"  {C.NEON}channel {C.RESET} > {C.DIM}(default: general){C.RESET}  ")
    sys.stdout.flush()
    channel = input().strip().lstrip("#") or "general"
    print()
    return username, channel

# ─────────────────────────────────────────────────────
#  SIGNAL HANDLER
# ─────────────────────────────────────────────────────
def _shutdown(sig, frame):
    state["running"] = False
    try:
        _presence("leave")
        client.loop_stop()
        client.disconnect()
    except Exception:
        pass
    print(f"\n{C.SYSTEM}Bye!{C.RESET}\n")
    sys.exit(0)

# ─────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────
def main():
    signal.signal(signal.SIGINT,  _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    boot_sequence()
    username, channel = get_login()
    state["username"] = username
    state["channel"]  = channel

    print(f"  {C.STATUS}Connecting (paho-mqtt {PAHO_VERSION_STR})...{C.RESET}")
    c = connect_best_broker()

    if c is None:
        print(f"\n  {C.ERROR}All brokers unreachable.{C.RESET}")
        print(f"  {C.DIM}Check your internet connection in Termux:{C.RESET}")
        print(f"  {C.NEON}  ping broker.hivemq.com{C.RESET}")
        sys.exit(1)

    clear()
    _header()
    print(f"{C.SYSTEM}  Welcome {username}! Connected to #{channel}{C.RESET}")
    print(f"{C.DIM}  Type a message and Enter to send. /help for commands.{C.RESET}\n")
    print_border()
    print()
    _prompt()

    while state["running"]:
        try:
            raw = input()
        except (EOFError, KeyboardInterrupt):
            break

        raw = raw.strip()
        if not raw:
            _prompt()
            continue

        if raw.startswith("/"):
            handled = handle_command(raw)
            if not handled:
                print_error(f"Unknown command '{raw.split()[0]}' — type /help")
        else:
            send_message(raw)

        if state["running"]:
            _prompt()

    # cleanup
    try:
        _presence("leave")
        client.loop_stop()
        client.disconnect()
    except Exception:
        pass
    print(f"\n{C.SYSTEM}Disconnected. Goodbye!{C.RESET}\n")

if __name__ == "__main__":
    main()
