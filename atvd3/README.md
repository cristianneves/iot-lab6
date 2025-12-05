# Documentação da Atividade #3: Decodificação de Payload Binário IoT

Contexto: Semana 6 — Manipulação de dados de baixo nível e Endianness.
Objetivo: Desenvolver um script em Python capaz de consumir dados de uma API, identificar payloads hexadecimais codificados e transformá-los em valores legíveis (ponto flutuante) utilizando a biblioteca struct.

## 1. O Desafio Técnico

Dispositivos IoT, como o ESP32, frequentemente enviam dados em formato binário (Hexadecimal) para economizar banda, em vez de JSON texto. O desafio consiste em pegar uma sequência de bytes "ininteligível" e reconstruir os números originais.

#### Cenário da Atividade:

Protocolo: HTTP/REST.

- Formato esperado: String Hexadecimal de 12 bytes (24 caracteres).

- Estrutura do Payload:

   - Bytes 0-3: Temperatura (Float)

   - Bytes 4-7: Umidade (Float)

   - Bytes 8-11: Pressão (Float)

- Arquitetura: Little-Endian (padrão Intel/ESP32).

## 2. Solução Implementada (decoder.py)

O script foi desenvolvido em Python focando na biblioteca nativa struct, que permite a interpretação de dados binários como estruturas da linguagem C.

### 2.1 Fluxo de Execução

1- Conexão: O script realiza um GET no endpoint https://callback-iot.up.railway.app/data.

2- Verificação: Analisa se o JSON retornado contém a chave hexData.

   - Nota: Como a API atual retorna o JSON já decodificado, o script implementa um fallback (mock) com uma string hexadecimal de teste para validar a lógica de decodificação exigida na atividade.

3- Conversão: Transforma a string Hex (ex: CDCC7C44) em bytes crus (b'\xcd\xcc|D').

4- Desempacotamento (Unpacking): Utiliza a máscara <fff.

## 2.2 Entendendo a Máscara <fff

A linha crucial do código é:

temperatura, umidade, pressao = struct.unpack('<fff', payload_bytes)


< (Little-Endian): Indica que o byte menos significativo vem primeiro. Isso é crucial. Se usássemos > (Big-Endian), o valor 1011.2 seria lido como um número totalmente errado (algo na casa de $10^{-35}$).

f (Float): Indica que cada bloco de dados tem 4 bytes (32 bits), seguindo o padrão IEEE 754 de precisão simples.

fff: Indica que existem três números float consecutivos na sequência de bytes.

## 3. Exemplo Prático de Decodificação

Durante a execução, utilizamos o seguinte payload de teste:
Hex: 6666E5419A995C42CDCC7C44

O processo de conversão realizado pelo script foi:

1- Bloco 1 (Temperatura): 66 66 E5 41

   - Invertendo (Little-Endian): 0x41E56666

   - Conversão IEEE 754: 28.7 °C

2- Bloco 2 (Umidade): 9A 99 5C 42

   - Invertendo (Little-Endian): 0x425C999A

   - Conversão IEEE 754: 55.2 %

3- Bloco 3 (Pressão): CD CC 7C 44

   - Invertendo (Little-Endian): 0x447CCCCD

   - Conversão IEEE 754: 1011.2 hPa

## 4. Evidência de Funcionamento

### Saída do Terminal:

--- INICIANDO DECODIFICADOR IOT ---
[...] Buscando dados de: [https://callback-iot.up.railway.app/data](https://callback-iot.up.railway.app/data)

--- DADOS BRUTOS (JSON) ---
{'device': '42A6DA', 'timestamp': '...', 'temperature': 29.79, ...}

[AVISO] Campo 'hexData' não encontrado no JSON.
usando um valor de teste simulado para demonstração...

Payload Hexadecimal Recebido: 6666E5419A995C42CDCC7C44

--- RESULTADO DA DECODIFICAÇÃO ---
Temperatura: 28.7 °C
Umidade:     55.2 %
Pressão:     1011.2 hPa
----------------------------------


Isso comprova que o sistema é capaz de reconstruir com precisão os dados físicos a partir de uma transmissão binária otimizada.