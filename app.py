import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS # Necessário para Node-RED se estiver em domínio/porta diferente

# URL do endpoint público de dados IoT
EXTERNAL_API_URL = "https://callback-iot.up.railway.app/data"

app = Flask(__name__)
# Permite requisições de outras origens (CORS) durante o desenvolvimento
CORS(app) 

@app.route('/data', methods=['GET'])
def get_last_two_data_points():
    """
    GET /data: Consome o endpoint externo, retorna os 2 últimos objetos de dados.
    """
    print("Requisição GET /data recebida. Buscando dados externos...")
    try:
        # 1. Consumir dados do endpoint público
        response = requests.get(EXTERNAL_API_URL, timeout=10)
        response.raise_for_status() # Lança exceção para status de erro (4xx ou 5xx)
        
        all_data = response.json()
        
        if not isinstance(all_data, list):
            return jsonify({"error": "Dados recebidos não são uma lista."}), 500
        
        # 2. Retornar os 2 últimos objetos (slice Python)
        last_two_data = all_data[-2:]
        
        print(f"Sucesso: Retornando {len(last_two_data)} objetos de dados.")
        return jsonify(last_two_data), 200

    except requests.exceptions.RequestException as e:
        # Lidar com erros de requisição (conexão, timeout, DNS, etc.)
        print(f"Erro ao acessar a API externa: {e}")
        return jsonify({"error": "Erro ao conectar-se à API externa.", "details": str(e)}), 503
    except Exception as e:
        # Lidar com outros erros
        print(f"Ocorreu um erro inesperado: {e}")
        return jsonify({"error": "Ocorreu um erro inesperado no servidor.", "details": str(e)}), 500


@app.route('/visualize', methods=['POST'])
def post_visualize_data():
    """
    POST /visualize: Recebe dados do cliente e simula o encaminhamento
    para a aplicação de visualização (Node-RED).
    """
    if request.is_json:
        data_to_visualize = request.json
        
        # SIMULAÇÃO: Imprime os dados recebidos para comprovar o funcionamento
        print("\n--- Dados recebidos em POST /visualize (SIMULANDO ENCAMINHAMENTO) ---")
        print(data_to_visualize)
        print("----------------------------------------------------------------------\n")

        # Em um cenário real, você faria aqui um requests.post() para o Node-RED.
        
        return jsonify({"message": "Dados recebidos com sucesso e encaminhamento simulado para visualização.", "data_count": len(data_to_visualize)}), 200
    else:
        return jsonify({"error": "Conteúdo da requisição deve ser JSON."}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Executa a aplicação, acessível em http://127.0.0.1:5000/
    app.run(debug=True, host='0.0.0.0', port=port)