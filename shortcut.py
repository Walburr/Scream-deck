import serial
import serial.tools.list_ports
import time
import subprocess
import threading


#I put the service file that run in the back right here 
# path : ~/.config/systemd/user/streamdeck.service 
# but u can put it wherever u whant 
# 
# 
# #
# #
##
#
#find the real file at ~/esp_deck/esp_deck.ino  && ~/esp_deck/esp_deck_2.ino

BAUD_RATE = 115200

def listen_to_port(port):
    print(f"-> Démarrage de l écoute sur {port}...")
    while True:
        try:
            ser = serial.Serial(port, BAUD_RATE, timeout=0.05)
            print(f" Connecté avec succès sur {port} !")
            while True:
                if ser.in_waiting > 0:
                    raw_data = ser.read_all().decode("utf-8", errors="ignore")
                    lines = raw_data.strip().split("\n")
                    last_vol = -1
                    last_bright = -1
                    for line in lines:
                        line = line.strip()
                        if line == "BTN_CLICK":
                            print(f"[{port}] -> Bouton : Discord")
                            subprocess.Popen(["discord"])
                        elif line.startswith("POT_VAL:"):
                            try:
                                last_vol = int(line.split(":")[1])
                            except ValueError:
                                pass
                        elif line.startswith("BRIGHT_VAL:"):
                            try:
                                last_bright = int(line.split(":")[1])
                            except ValueError:
                                pass

                    # VOLUME (best code that i made cause it really use the limite of this hyprland 4dots and not just 100⁼%)
                    if last_vol != -1:
                        vol = (last_vol / 100.0) * 1.5
                        print(f"[{port}] -> Volume : {last_vol}%")
                        subprocess.Popen(["wpctl", "set-volume", "--limit", "1.5", "@DEFAULT_AUDIO_SINK@", str(vol)])

                    # brightness(0 to 100%) ET GAMMA (100 à 25%) actually this just use the gamma i'm still workin on it
                    if last_bright != -1:
                        print(f"[{port}] -> Potentiomètre : {last_bright}%")

                        #thoose are some test not really working

                        # 1. Adjust the brightness (0 to 100%)
                        subprocess.Popen(["brightnessctl", "set", f"{last_bright}%"])

                        # 2.Gamma calcul (supposed to be min 25% to 100% plus the brightness)

                        #This part actually does not work well ngl

                        gamma_val = 0.25 + (last_bright / 100.0) * 0.75

                        # 3. Send the script to end-4 
                        cmd = f"hyprsunset -g {gamma_val:.2f} 2>/dev/null || ~/.config/hypr/hyprland/scripts/brightness.sh set {last_bright}"
                        subprocess.Popen(cmd, shell=True)

                time.sleep(0.01)
        except (serial.SerialException, OSError):
            print(f" Perte de connexion sur {port}. Reconnexion dans 2s...")
            time.sleep(2)
            break

print("=== Démarrage du contrôleur Dual-Wemos ===")
active_threads = {}
while True:
    ports = [p.device for p in serial.tools.list_ports.comports() if "USB" in p.device or "ACM" in p.device]
    for port in ports:
        if port not in active_threads or not active_threads[port].is_alive():
            t = threading.Thread(target=listen_to_port, args=(port,), daemon=True)
            t.start()
            active_threads[port] = t
    time.sleep(2)
