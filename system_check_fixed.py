import os
import subprocess
import speedtest
import qrcode
import platform
from datetime import datetime

def system_info():
    print("\n[+] Informações do Sistema Termux")
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Sistema: {platform.system()} {platform.release()}")
    
    # Informações de CPU alternativas
    try:
        # Tenta obter informações da CPU via comandos do Termux
        cpu_info = subprocess.check_output(["cat", "/proc/cpuinfo"], text=True, stderr=subprocess.DEVNULL)
        cores = cpu_info.count("processor")
        print(f"CPUs: {cores} núcleos")
    except:
        print("CPUs: Informação não disponível")
    
    # Informações de memória via comandos do Termux
    try:
        mem_info = subprocess.check_output(["free", "-m"], text=True)
        lines = mem_info.split('\n')
        if len(lines) > 1:
            mem_data = lines[1].split()
            total_mem = int(mem_data[1])
            used_mem = int(mem_data[2])
            if total_mem > 0:
                mem_percent = (used_mem / total_mem) * 100
                print(f"Memória: {mem_percent:.1f}% usado ({used_mem}MB / {total_mem}MB)")
    except:
        print("Memória: Informação não disponível")
    
    # Informações de armazenamento
    try:
        disk_info = subprocess.check_output(["df", "/data/data/com.termux/files/home", "-h"], text=True)
        lines = disk_info.split('\n')
        if len(lines) > 1:
            disk_data = lines[1].split()
            if len(disk_data) >= 5:
                print(f"Armazenamento: {disk_data[4]} usado ({disk_data[2]} / {disk_data[1]})")
    except:
        try:
            # Fallback para psutil se disponível
            import psutil
            disk = psutil.disk_usage('/')
            print(f"Armazenamento: {disk.percent}% usado ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)")
        except:
            print("Armazenamento: Informação não disponível")
    
    # Informações da bateria
    try:
        battery_info = subprocess.check_output(["termux-battery-status"], text=True)
        if "percentage" in battery_info:
            import json
            battery_data = json.loads(battery_info)
            print(f"Bateria: {battery_data.get('percentage', 'N/A')}%")
            print(f"Status: {battery_data.get('status', 'N/A')}")
    except:
        print("Bateria: Informação não disponível")

def speed_test():
    try:
        print("\n[+] Testando velocidade da internet...")
        st = speedtest.Speedtest()
        st.get_best_server()
        
        print("Testando download...")
        download = st.download() / 1024 / 1024
        
        print("Testando upload...")
        upload = st.upload() / 1024 / 1024
        
        print(f"\nResultados:")
        print(f"Download: {download:.2f} Mbps")
        print(f"Upload: {upload:.2f} Mbps")
        print(f"Ping: {st.results.ping:.2f} ms")
        
    except Exception as e:
        print(f"Erro no teste de velocidade: {e}")
        print("Verifique sua conexão com a internet")

def generate_qr():
    try:
        text = input("\nDigite o texto/URL para o QR Code: ")
        if not text.strip():
            print("Texto vazio! Operação cancelada.")
            return
            
        qr = qrcode.make(text)
        filename = "qrcode_termux.png"
        qr.save(filename)
        print(f"QR Code salvo como '{filename}'")
        
        # Tenta abrir com app disponível
        if os.path.exists(filename):
            print("Tentando abrir o QR Code...")
            os.system(f"termux-share {filename}")
        else:
            print("Erro: QR Code não foi gerado corretamente.")
            
    except Exception as e:
        print(f"Erro ao gerar QR Code: {e}")

def device_info():
    print("\n[+] Informações do Dispositivo")
    try:
        # Modelo do dispositivo
        model = subprocess.check_output(["getprop", "ro.product.model"], text=True).strip()
        brand = subprocess.check_output(["getprop", "ro.product.brand"], text=True).strip()
        android_version = subprocess.check_output(["getprop", "ro.build.version.release"], text=True).strip()
        
        print(f"Dispositivo: {brand} {model}")
        print(f"Android: {android_version}")
        
        # Resolução da tela (se disponível)
        try:
            display_info = subprocess.check_output(["termux-wallpaper", "-h"], text=True, stderr=subprocess.DEVNULL)
            print("Wallpaper: Suportado")
        except:
            print("Wallpaper: Não suportado")
            
    except Exception as e:
        print(f"Informações limitadas: {e}")

def main():
    print("=" * 50)
    print("      TERMUX SYSTEM UTILITIES")
    print("=" * 50)
    
    while True:
        print("\n--- Menu Principal ---")
        print("1. Informações do Sistema")
        print("2. Informações do Dispositivo")
        print("3. Teste de Velocidade da Internet")
        print("4. Gerar QR Code")
        print("5. Sair")
        
        choice = input("\nEscolha uma opção (1-5): ").strip()
        
        if choice == "1":
            system_info()
        elif choice == "2":
            device_info()
        elif choice == "3":
            speed_test()
        elif choice == "4":
            generate_qr()
        elif choice == "5":
            print("\nObrigado por usar Termux Utilities! 👋")
            break
        else:
            print("Opção inválida! Tente novamente.")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()
EOF