import requests
import struct
import sys

# URL do Endpoint
URL = "https://callback-iot.up.railway.app/data"

def get_iot_data():
    """Busca os dados da API e retorna o último registro."""
    try:
        print(f"[...] Buscando dados de: {URL}")
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        
        data_list = response.json()
        
        if not data_list:
            print("[!] A lista retornada pela API está vazia.")
            return None
            
        # Retorna o último dado (o mais recente)
        return data_list[-1]
    
    except requests.exceptions.RequestException as e:
        print(f"[!] Erro na conexão: {e}")
        return None

def decode_hex_payload(hex_string):
    """
    Decodifica uma string Hexadecimal de 12 bytes em 3 Floats (Little-Endian).
    Estrutura: [Temp (4B)] [Umid (4B)] [Press (4B)]
    """
    try:
        # 1. Remove prefixos '0x' se houver e limpa espaços
        clean_hex = hex_string.replace("0x", "").strip()
        
        # 2. Converte a string Hexadecimal para Bytes crus
        # Ex: "00002041" vira b'\x00\x00\x20\x41'
        payload_bytes = bytes.fromhex(clean_hex)
        
        # Verifica se temos exatamente 12 bytes
        if len(payload_bytes) != 12:
            print(f"[!] Erro: Tamanho incorreto. Esperado 12 bytes, recebido {len(payload_bytes)} bytes.")
            return None

        # 3. Desempacotamento (Unpacking)
        # '<'  = Little-Endian (padrão da maioria dos sensores/MCUs)
        # 'f'  = float (4 bytes)
        # 'fff' = 3 floats consecutivos
        temperatura, umidade, pressao = struct.unpack('<fff', payload_bytes)
        
        return {
            "temp": temperatura,
            "umid": umidade,
            "press": pressao
        }

    except Exception as e:
        print(f"[!] Erro na decodificação: {e}")
        return None

def main():
    print("--- INICIANDO DECODIFICADOR IOT ---")
    
    # 1. Obter dados da nuvem
    last_record = get_iot_data()
    
    if last_record:
        print("\n--- DADOS BRUTOS (JSON) ---")
        print(last_record)
        
        # 2. Verificar se o campo 'hexData' existe
        # OBS: Se a API não estiver enviando hexData, usaremos um mock para teste
        if 'hexData' in last_record:
            hex_data = last_record['hexData']
        else:
            print("\n[AVISO] Campo 'hexData' não encontrado no JSON.")
            print("usando um valor de teste simulado para demonstração...")
            # Exemplo: 28.7, 55.2, 1010.8 em hex little-endian
            hex_data = "6666E5419A995C42CDCC7C44"

        print(f"\nPayload Hexadecimal Recebido: {hex_data}")
        
        # 3. Decodificar
        resultado = decode_hex_payload(hex_data)
        
        if resultado:
            print("\n--- RESULTADO DA DECODIFICAÇÃO ---")
            print(f"Temperatura: {resultado['temp']:.1f} °C")
            print(f"Umidade:     {resultado['umid']:.1f} %")
            print(f"Pressão:     {resultado['press']:.1f} hPa")
            print("----------------------------------")

if __name__ == "__main__":
    main()