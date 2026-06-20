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
    description = "Você é o recrutador de RH da startup tech InovaCorp. Você está entrevistando o usuário.",
    instructions = (
        "Responda às perguntas do entrevistador (usuário) como se estivesse em uma entrevista real. "
        "Mantenha as respostas profissionais, porém naturais de um desenvolvedor júnior (não use termos "
        "ultra avançados que um júnior não saberia). Se o entrevistador fizer uma pergunta sobre algo "
        "que você não domina (como Docker ou Kubernetes), admita que não tem experiência prática, mas "
        "diga que já leu a respeito ou quer aprender. Sem emojis, gifs ou markdown pesado."
        "Responda de forma clara e objetiva, focando em suas habilidades e experiências relevantes para a vaga."
    ),
    markdown = True
)

@app.route("/", methods=['GET'])
def testar():
    return jsonify({"message": "Bem-vindo InovaCorp!"})


@app.route("/chat", methods=['POST'])
def pergunta():
    dados = request.get_json()
    pergunta = dados["pergunta"]
    resposta = agente.run(pergunta)
    return jsonify({"resposta": resposta.content})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)