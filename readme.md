# Termux Utilities 🚀

Um conjunto de ferramentas úteis e scripts Python desenvolvidos para o Termux (Android) que fornecem informações do sistema, testes de rede, geração de QR codes e muito mais.

## 📋 Funcionalidades

### 🖥️ System Info
- **Informações do Sistema**: Data/hora, versão do Android, modelo do dispositivo
- **Monitoramento de Recursos**: Uso de memória, armazenamento e CPU (quando disponível)
- **Status da Bateria**: Nível da bateria e status de carregamento
- **Informações de Rede**: Interfaces de rede e conectividade

### 🌐 Network Tools
- **Teste de Velocidade**: Medição de download, upload e ping
- **Teste de Conectividade**: Verificação de acesso a sites populares
- **Informações de IP**: Detalhes das interfaces de rede

### 🔧 Utilities
- **Gerador de QR Code**: Cria QR codes a partir de texto/URLs
- **Gerenciador de Arquivos**: Navegação básica no sistema de arquivos
- **Comandos Úteis**: Acesso rápido a utilitários do Termux

## 🛠️ Instalação

### Pré-requisitos
```bash
pkg update && pkg upgrade
pkg install python