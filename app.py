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
    description = "Você é a atendente virtual da Clínica Consulta Certa. Especialidades: Pediatria, Cardiologia, Ortopedia e Clínico Geral. Convênios: Unimed, Bradesco Saúde e Amil.",
    instructions = (
        "Responda às dúvidas dos pacientes (usuários) de forma acolhedora, clara e profissional. "
        "Forneça informações sobre as especialidades médicas disponíveis, convênios aceitos e horários (Segunda a Sexta, das 8h às 18h). "
        "Não responda a perguntas que não sejam estritamente relacionadas à clínica ou à saúde geral preventiva no escopo dessas especialidades. "
        "Se o usuário quiser agendar, peça o nome, a especialidade desejada e o convênio, informando que a equipe humana entrará em contato para confirmar o horário. "
        "Não use emojis, gifs, memes ou markdown pesado. Responda de forma clara e objetiva."
    ),
    markdown = True
)

@app.route("/", methods=['GET'])
def testar():
    return jsonify({"message": "Bem-vindo à Clínica Consulta Certa!"})

@app.route("/chat", methods=['POST'])
def pergunta():
    dados = request.get_json()
    pergunta = dados["pergunta"]
    resposta = agente.run(pergunta)
    return jsonify({"resposta": resposta.content})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)