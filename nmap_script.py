import subprocess
import time
import os
import random

# Alvos a escanear
targets = ["site1.com", "site2.com"]

# User-Agents para randomização
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Firefox/102.0",
    "curl/7.85.0",
    "NmapScanner",
]

# Diretório de saída
output_dir = "nmap_results"
os.makedirs(output_dir, exist_ok=True)

# Delay entre varreduras (segundos)
delay = 8

# (Opcional) Comando base do proxy, exemplo com Tor (porta 9050 padrão)
# Usar torsocks se disponível (instalar com apt install torsocks)
use_tor = False
tor_prefix = ["torsocks"] if use_tor else []

# Função principal
def run_scan(target, user_agent):
    # Nome do arquivo de saída
    ua_safe = user_agent.replace(" ", "_").replace("/", "_").replace(";", "").replace("(", "").replace(")", "")[:40]
    output_file = f"{output_dir}/{target}_{ua_safe}.txt"

    print(f"🔍 Escaneando {target} com UA: {user_agent}")

    # Monta comando Nmap
    cmd = tor_prefix + [
        "nmap", "-p80", "--script", "http-title",
        f"--script-args=http.useragent={user_agent}",
        "-oN", output_file, target
    ]

    subprocess.run(cmd)
    print(f"📝 Resultado salvo em: {output_file}")
    print(f"⏳ Aguardando {delay} segundos...\n")
    time.sleep(delay)


# Loop de varredura
for target in targets:
    random.shuffle(user_agents)
    for ua in user_agents:
        run_scan(target, ua)

print("✅ Varredura finalizada.")
