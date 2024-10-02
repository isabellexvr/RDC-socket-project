
**Objetivo:** Criar uma aplicação que permita monitorar e exibir os recursos do sistema (CPU, memória, disco, etc.) de vários computadores na rede. A aplicação consiste em um servidor central que coleta e exibe os dados enviados por clientes que estão sendo monitorados.

### Componentes Principais:

1. **Cliente de Monitoramento:**
    
    - **Função:** Coletar dados de uso de recursos do sistema local e enviar periodicamente ao servidor.
    - **Dados Coletados:**
        - Uso da CPU (percentual de uso).
        - Uso de memória (RAM) (percentual e absoluto).
        - Espaço em disco (livre e usado).
        - Outros dados relevantes (uso de rede, temperatura do CPU, etc.).
    - **Frequência de Envio:** Envia os dados coletados ao servidor em intervalos regulares (por exemplo, a cada 5 segundos).
2. **Servidor de Monitoramento:**
    
    - **Função:** Receber, armazenar e exibir os dados de uso de recursos enviados por múltiplos clientes.
    - **Funcionalidades:**
        - **Recepção de Dados:** Receber e processar os dados enviados pelos clientes.
        - **Armazenamento:** Armazenar os dados recebidos em uma estrutura adequada (pode ser em memória ou em um banco de dados).
        - **Exibição:** Exibir os dados coletados em uma interface centralizada (pode ser uma interface gráfica ou uma interface web).

### Fluxo de Trabalho:

1. **Inicialização do Cliente:**
    
    - O cliente inicia e coleta os dados de uso de recursos do sistema.
    - O cliente estabelece uma conexão com o servidor de monitoramento utilizando sockets.
    - O cliente começa a enviar os dados coletados ao servidor em intervalos regulares.
2. **Recepção de Dados pelo Servidor:**
    
    - O servidor está constantemente escutando por conexões de clientes.
    - Quando o servidor recebe os dados de um cliente, ele processa e armazena esses dados.
    - O servidor pode agrupar e organizar os dados de forma a facilitar a exibição e análise.
3. **Exibição dos Dados:**
    
    - O servidor exibe os dados de todos os clientes conectados em uma interface central.
    - A interface pode incluir gráficos e tabelas para visualizar o uso de recursos de cada cliente.
    - A interface pode oferecer funcionalidades adicionais, como filtros, ordenação e histórico de uso.

### Funcionalidades Adicionais:

- **Alertas e Notificações:** Configurar alertas que disparam notificações (e-mail, SMS, etc.) quando o uso de recursos excede um certo limite.
- **Relatórios:** Gerar relatórios periódicos sobre o uso de recursos para análise.
- **Autenticação:** Implementar autenticação para garantir que apenas clientes autorizados possam enviar dados ao servidor.
- **Escalabilidade:** Configurar o servidor para lidar com um grande número de clientes, utilizando técnicas como threads, processos ou event loops.

### Benefícios:

- **Centralização:** Monitoramento centralizado de múltiplos sistemas em uma rede.
- **Eficiência:** Detecção rápida de problemas de desempenho ou uso excessivo de recursos.
- **Análise:** Facilita a análise e otimização de recursos na rede.

### Considerações:

- **Segurança:** Proteção dos dados transmitidos entre cliente e servidor, possivelmente utilizando criptografia.
- **Robustez:** Garantir que o sistema lide bem com falhas de rede e interrupções na comunicação.
- **Desempenho:** Minimizar o impacto do cliente de monitoramento no sistema que está sendo monitorado.

Esse sistema pode ser bastante útil em ambientes corporativos ou acadêmicos para garantir que todos os recursos de TI estejam funcionando de maneira eficiente e sem sobrecarga.
