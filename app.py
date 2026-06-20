#importando as bibliotecas
from flask import Flask, request, jsonify
from flask_cors import CORS
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from dotenv import load_dotenv

#Leitura da chave de API
load_dotenv()
#Criando a aplicação Flask
app = Flask(__name__)
#Habilitar o cors para permitir requisições de outros domínios
CORS(app)
#Criar agente
agente = Agent(
    model = OpenAIChat(id="gpt-4o-mini"),
    description = "Voce é um agente virtual do hotel Travesseiro Nervoso",
    instructions = "Voce reponde de forma clara e humorada, informações sobre quartos, serviços, reservas e outras dúvidas relacionadas ao hotel Travesseiro Nervoso",
    tools = ["Quarto Standbard(R$500)", "Quarto Deluxe(R$700)", "Quarto Suite Presidecial(R$1000)"],
    markdown = True
)

@app.route("/", methods=['GET'])
def testar():
    return jsonify({"message": "Bem-vindo ao agente virtual do hotel Travesseiro Nervoso!"})

@app.route("/chat", methods=['POST'])
def pergunta():
    dados = request.get_json()
    pergunta = dados["pergunta"]
    resposta = agente.run(pergunta)
    return jsonify({"resposta": resposta.content})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)