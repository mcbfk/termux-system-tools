import os
import subprocess
import speedtest
import qrcode
import platform
import json
import signal
import sys
from datetime import datetime

class TermuxUtilities:
    def __init__(self):
        self.version = "1.0.0"
        self.running = True
        
    def signal_handler(self, sig, frame):
        """Handler para Ctrl+C"""
        print("\n\n❌ Operação interrompida pelo usuário")
        self.return_to_menu()
        
    def setup_signal_handler(self):
        """Configura o handler para Ctrl+C"""
        signal.signal(signal.SIGINT, self.signal_handler)
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_banner(self):
        banner = """
╔═══════════════════════════════════════╗
║          TERMUX UTILITIES             ║
║         Professional Suite            ║
╚═══════════════════════════════════════╝
        """
        print(banner)
    
    def wait_for_quit(self, timeout_seconds=60):
        """Espera o usuário pressionar 'q' para voltar ao menu"""
        print("\n" + "⎯" * 50)
        print(f"🚪 Aperte 'q' e depois ENTER para voltar ao menu principal")
        print(f"⏰ Ou aguarde {timeout_seconds} segundos para voltar automaticamente...")
        
        try:
            # Timeout personalizado
            import select
            import sys
            
            i, o, e = select.select([sys.stdin], [], [], timeout_seconds)
            if i:
                user_input = sys.stdin.readline().strip().lower()
                if user_input == 'q':
                    return True
            return True  # Volta automaticamente após o timeout
        except:
            return True  # Fallback se houver erro

    def check_internet_connection(self):
        """Verifica se há conexão com a internet"""
        try:
            # Tenta fazer ping para o Google
            result = subprocess.run(
                ["ping", "-c", "1", "8.8.8.8"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            return result.returncode == 0
        except:
            return False

    def return_to_menu(self):
        """Volta para o menu principal"""
        self.running = True

    def system_info(self):
        print("\n📊 [INFORMAÇÕES DO SISTEMA]")
        print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
        print("💡 Aperte CTRL+C a qualquer momento para voltar ao menu")
        print("⏰ Você tem 1 MINUTO para analisar as informações")
        print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
        
        try:
            print(f"🕐 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"⚙️  Sistema: {platform.system()} {platform.release()}")
            
            # Informações de CPU
            try:
                cpu_info = subprocess.check_output(["nproc"], text=True).strip()
                print(f"🔧 CPUs: {cpu_info} núcleos")
            except:
                try:
                    cpu_info = subprocess.check_output(["cat", "/proc/cpuinfo"], text=True)
                    cores = cpu_info.count("processor")
                    print(f"🔧 CPUs: {cores} núcleos")
                except:
                    print("🔧 CPUs: Informação não disponível")
            
            # Memória
            try:
                mem_info = subprocess.check_output(["free", "-m"], text=True)
                lines = mem_info.split('\n')
                if len(lines) > 1:
                    mem_data = lines[1].split()
                    total_mem = int(mem_data[1])
                    used_mem = int(mem_data[2])
                    if total_mem > 0:
                        mem_percent = (used_mem / total_mem) * 100
                        print(f"💾 Memória: {mem_percent:.1f}% usado ({used_mem}MB / {total_mem}MB)")
            except:
                print("💾 Memória: Informação não disponível")
            
            # Armazenamento
            try:
                disk_info = subprocess.check_output(["df", "/data/data/com.termux/files/home", "-h"], text=True)
                lines = disk_info.split('\n')
                if len(lines) > 1:
                    disk_data = lines[1].split()
                    if len(disk_data) >= 5:
                        print(f"💽 Armazenamento: {disk_data[4]} usado ({disk_data[2]} / {disk_data[1]})")
            except:
                print("💽 Armazenamento: Informação não disponível")
            
            # Bateria
            try:
                battery_info = subprocess.check_output(["termux-battery-status"], text=True)
                battery_data = json.loads(battery_info)
                battery_level = battery_data.get('percentage', 'N/A')
                status = battery_data.get('status', 'N/A')
                status_emoji = "🔋" if status == "CHARGING" else "⚡" if status == "FULL" else "🔌"
                print(f"{status_emoji} Bateria: {battery_level}% | Status: {status}")
            except:
                print("🔋 Bateria: Informação não disponível")
            
        except Exception as e:
            print(f"❌ Erro ao obter informações: {e}")
        
        return self.wait_for_quit(60)  # 60 SEGUNDOS

    def speed_test(self):
        print("\n🌐 [TESTE DE VELOCIDADE]")
        print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
        print("💡 Aperte CTRL+C a qualquer momento para cancelar e voltar ao menu")
        print("⏰ Você tem 1 MINUTO para analisar os resultados")
        print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
        
        # Primeiro verifica a conexão com a internet
        print("🔍 Verificando conexão com a internet...")
        if not self.check_internet_connection():
            print("❌ Sem conexão com a internet!")
            print("💡 Verifique sua conexão Wi-Fi ou dados móveis")
            return self.wait_for_quit(60)
        
        print("✅ Conexão detectada. Iniciando teste de velocidade...")
        
        try:
            print("⏳ Configurando teste...")
            
            # Cria instância do speedtest com timeout
            st = speedtest.Speedtest()
            st.timeout = 10  # Timeout de 10 segundos
            
            print("🌍 Procurando servidor mais próximo...")
            st.get_best_server()
            
            print("📥 Testando velocidade de download...")
            download = st.download() / 1024 / 1024  # Convertendo para Mbps
            
            print("📤 Testando velocidade de upload...")
            upload = st.upload() / 1024 / 1024  # Convertendo para Mbps
            
            ping = st.results.ping
            
            print("\n📊 RESULTADOS:")
            print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
            print(f"📥 Download: {download:.2f} Mbps")
            print(f"📤 Upload: {upload:.2f} Mbps")
            print(f"🔄 Ping: {ping:.2f} ms")
            
            # Classificação da velocidade
            if download > 100:
                print("🚀 Velocidade: EXCELENTE")
            elif download > 50:
                print("✅ Velocidade: Muito Boa")
            elif download > 25:
                print("👍 Velocidade: Boa")
            elif download > 10:
                print("⚠️  Velocidade: Regular")
            else:
                print("🐢 Velocidade: Lenta")
                
            print("\n💡 Aperte 'q' + ENTER a qualquer momento para voltar ao menu")
                
        except speedtest.SpeedtestException as e:
            print(f"❌ Erro no teste de velocidade: {str(e)}")
            print("\n🔧 Soluções possíveis:")
            print("• Verifique sua conexão com a internet")
            print("• Tente novamente em alguns segundos")
            print("• Verifique se o servidor speedtest está acessível")
            
        except KeyboardInterrupt:
            print("\n❌ Teste cancelado pelo usuário")
            return True
            
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            print("💡 Tente novamente ou verifique sua conexão")
        
        return self.wait_for_quit(60)  # 60 SEGUNDOS

    def generate_qr(self):
        print("\n📱 [GERADOR DE QR CODE]")
        print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
        print("💡 Aperte CTRL+C a qualquer momento para cancelar e voltar ao menu")
        print("⏰ Você tem 1 MINUTO após a geração do QR Code")
        print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
        
        try:
            text = input("Digite o texto/URL para o QR Code: ").strip()
            
            if not text:
                print("❌ Texto vazio! Operação cancelada.")
                return self.wait_for_quit(60)
            
            # Validação básica de URL
            if not text.startswith(('http://', 'https://')):
                if '.' in text and ' ' not in text:
                    text = 'https://' + text
            
            print("⏳ Gerando QR Code...")
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            filename = f"qrcode_{datetime.now().strftime('%H%M%S')}.png"
            img.save(filename)
            
            print(f"✅ QR Code salvo como: {filename}")
            print(f"📍 Conteúdo: {text[:50]}{'...' if len(text) > 50 else ''}")
            
            # Tentar abrir/compartilhar
            if os.path.exists(filename):
                try:
                    subprocess.run(["termux-share", filename], check=False)
                    print("📤 Abrindo opções de compartilhamento...")
                except:
                    print("💡 Use: 'termux-share' para compartilhar o arquivo manualmente")
            else:
                print("❌ Erro: QR Code não foi gerado corretamente.")
                
        except KeyboardInterrupt:
            print("\n❌ Operação cancelada pelo usuário")
            return True
        except Exception as e:
            print(f"❌ Erro ao gerar QR Code: {e}")
        
        return self.wait_for_quit(60)  # 60 SEGUNDOS

    def device_info(self):
        print("\n📱 [INFORMAÇÕES DO DISPOSITIVO]")
        print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
        print("💡 Aperte CTRL+C a qualquer momento para voltar ao menu")
        print("⏰ Você tem 1 MINUTO para analisar as informações")
        print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
        
        try:
            # Informações básicas
            model = subprocess.check_output(["getprop", "ro.product.model"], text=True).strip()
            brand = subprocess.check_output(["getprop", "ro.product.brand"], text=True).strip()
            android_version = subprocess.check_output(["getprop", "ro.build.version.release"], text=True).strip()
            sdk_version = subprocess.check_output(["getprop", "ro.build.version.sdk"], text=True).strip()
            
            print(f"📱 Dispositivo: {brand} {model}")
            print(f"🤖 Android: {android_version} (SDK: {sdk_version})")
            
            # Informações de rede
            try:
                wifi_info = subprocess.check_output(["termux-wifi-connectioninfo"], text=True, stderr=subprocess.DEVNULL)
                wifi_data = json.loads(wifi_info)
                ssid = wifi_data.get('ssid', 'Desconhecido')
                print(f"📶 Wi-Fi: {ssid}")
            except:
                print("📶 Wi-Fi: Informação não disponível")
                
        except Exception as e:
            print(f"❌ Erro ao obter informações: {e}")
        
        return self.wait_for_quit(60)  # 60 SEGUNDOS

    def update_system(self):
        print("\n🔄 [ATUALIZANDO SISTEMA]")
        print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
        print("💡 Aperte CTRL+C a qualquer momento para cancelar e voltar ao menu")
        print("⏰ Você tem 1 MINUTO para ver o resultado da atualização")
        print("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
        
        try:
            print("📦 Atualizando repositórios...")
            subprocess.run(["pkg", "update"], check=True)
            print("🔄 Atualizando pacotes...")
            subprocess.run(["pkg", "upgrade", "-y"], check=True)
            print("✅ Sistema atualizado com sucesso!")
        except KeyboardInterrupt:
            print("\n❌ Atualização cancelada pelo usuário")
            return True
        except Exception as e:
            print(f"❌ Erro na atualização: {e}")
        
        return self.wait_for_quit(60)  # 60 SEGUNDOS

    def show_menu(self):
        menu = """
🎯 MENU PRINCIPAL:

1. 📊 Informações do Sistema
2. 📱 Informações do Dispositivo  
3. 🌐 Teste de Velocidade
4. 📱 Gerar QR Code
5. 🔄 Atualizar Sistema
6. 🚪 Sair

👉 Escolha uma opção (1-6):
        """
        print(menu)

    def run(self):
        self.setup_signal_handler()
        
        while self.running:
            self.clear_screen()
            self.print_banner()
            self.show_menu()
            
            try:
                choice = input().strip()
                
                if choice == "1":
                    self.clear_screen()
                    self.print_banner()
                    self.system_info()
                elif choice == "2":
                    self.clear_screen()
                    self.print_banner()
                    self.device_info()
                elif choice == "3":
                    self.clear_screen()
                    self.print_banner()
                    self.speed_test()
                elif choice == "4":
                    self.clear_screen()
                    self.print_banner()
                    self.generate_qr()
                elif choice == "5":
                    self.clear_screen()
                    self.print_banner()
                    self.update_system()
                elif choice == "6":
                    print("\n👋 Obrigado por usar Termux Utilities!")
                    print("🌟 Contribua no GitHub!")
                    self.running = False
                else:
                    print("❌ Opção inválida! Tente novamente.")
                    input("📋 Pressione ENTER para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Obrigado por usar Termux Utilities!")
                self.running = False
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")
                input("📋 Pressione ENTER para continuar...")

if __name__ == "__main__":
    app = TermuxUtilities()
    app.run()