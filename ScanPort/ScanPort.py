# OsintMx - Port Scanner Rapide et Précis
# Color Scheme: Violet, Light Blue, White
# -----------------------------------------------------------------------------------------------------------------------------------------------------------

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Color Codes
violet = "\033[95m"
light_blue = "\033[94m"
white = "\033[97m"
reset = "\033[0m"

def display_title():
    print(f"{violet}OsintMx - Port Scanner Rapide et Précis{reset}")
    print("-" * 80)

def scan_port(ip, port):
    """Scanne un port spécifique sur une adresse IP donnée."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)  # Ajuster le délai d'attente pour un scan rapide
        try:
            if s.connect_ex((ip, port)) == 0:
                return port
        except Exception:
            pass
    return None

def port_scanner(ip, start_port=1, end_port=10000, max_workers=100):
    """Scanne une plage de ports sur une adresse IP avec une barre de progression."""
    open_ports = []

    print(f"{violet}Début du scan des ports ouverts pour l'adresse IP: {light_blue}{ip}{reset}")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Génère une liste de tâches pour chaque port dans la plage
        futures = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}

        # Utilisation de tqdm pour afficher la barre de progression
        for future in tqdm(as_completed(futures), total=len(futures), desc="Scan en cours", colour="blue"):
            port = futures[future]
            result = future.result()
            if result:
                open_ports.append(result)

    return open_ports

def main():
    display_title()
    ip = input(f"{violet}[INPUT]{white} Entrez l'adresse IP à scanner -> {reset}")

    print(f"{violet}[INFO]{white} Scan rapide et précis en cours...{reset}")
    open_ports = port_scanner(ip)

    if open_ports:
        print(f"{violet}[RESULT]{white} Ports ouverts trouvés pour {light_blue}{ip}{white}: {light_blue}{', '.join(map(str, open_ports))}{reset}")
    else:
        print(f"{violet}[RESULT]{white} Aucun port ouvert trouvé pour {light_blue}{ip}{reset}")

main()
