# Documentação da Atividade #1: Consumo e Visualização de Dados de Dispositivo IoT

Contexto: Semana 6 — Integração e visualização de dados em IoT

Objetivo: Criar uma API intermediária para consumir dados de um endpoint público e desenvolver uma aplicação web para visualizar esses dados e validar o fluxo de informações.

## 1. Análise do Endpoint Público

O endpoint https://callback-iot.up.railway.app/data retorna uma lista (array JSON) de objetos que representam medições de um dispositivo IoT ao longo do tempo.

Exemplo do formato de resposta:

{
  "temp": 25.5,
  "hum": 60,
  "light": 450,
  "timestamp": "2023-11-20T10:30:00Z"
}


## 2. Implementação da API Própria (Python Flask)

A API foi implementada utilizando o framework Flask (app.py), servindo como middleware e ponto de registro de dados.

#### 2.1 GET /data

Função: Atua como proxy. Consome o endpoint externo, filtra os dados e retorna apenas os registros mais recentes.

Método: GET

Lógica:

- Requisita dados à EXTERNAL_API_URL.

- Filtra a lista para manter apenas os 2 últimos objetos (all_data[-2:]).

- Retorna o JSON limpo para o frontend.

- Implementa CORS para permitir requisições do navegador.

#### 2.2 POST /visualize

Função: Endpoint de validação de fluxo. Recebe os dados processados pelo cliente web para confirmar o ciclo de vida da informação.

Método: POST

Lógica:

- Recebe o payload JSON enviado pelo navegador.

- Registra (imprime) os dados no terminal do servidor, comprovando o recebimento.

- Retorna confirmação de sucesso ao cliente.

## 3. Aplicação de Visualização (Cliente Web)

Em substituição a ferramentas de terceiros (como Node-RED), foi desenvolvida uma Aplicação Web Single-Page (SPA) personalizada (visualizer.html). Esta aplicação atua simultaneamente como Cliente (consumidor) e Dashboard (visualizador).

Tecnologias: HTML5, JavaScript (Vanilla), Tailwind CSS.

#### 3.1 Interface Gráfica (Dashboard)

A interface apresenta três widgets principais atualizados dinamicamente:

-  Gauge de Temperatura: Um medidor visual circular criado com CSS que altera a cor da borda (Azul/Amarelo/Vermelho) conforme a temperatura.

- Monitor de Umidade: Exibição numérica de grande formato.

- Timestamp: Data e hora da última leitura formatada para o padrão local (pt-BR).

- Log de Console: Uma área de texto que exibe, em tempo real, o status das requisições POST enviadas de volta à API.

#### 3.2 Lógica do Cliente (JavaScript)

O script embutido na página executa um ciclo autônomo a cada 5 segundos:

- Fetch Data: Executa GET em http://127.0.0.1:5000/data.

- DOM Update: Atualiza os elementos HTML com os valores recebidos.

- Data Loopback: Envia os mesmos dados via POST para http://127.0.0.1:5000/visualize.

## 4. Fluxo de Dados e Teste

O sistema opera em um ciclo contínuo orquestrado pelo navegador:

1- Navegador (visualizer.html) → Solicita dados → API Flask (GET /data).

2- API Flask → Busca dados externos → Retorna JSON filtrado → Navegador.

3- Navegador → Atualiza o Gauge e Widgets na tela.

4- Navegador → Envia dados de volta → API Flask (POST /visualize).

5- API Flask → Registra o recebimento no terminal (Log).

#### Validação de Sucesso:

- A interface gráfica exibe valores atualizados sem erros.

- O terminal da API Python exibe logs constantes de requisições POST /visualize contendo os dados corretos.