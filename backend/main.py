from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time # Apenas para simular o tempo de processamento da IA

# --- Modelo de Dados com Pydantic ---
# Define a estrutura do JSON que a API espera receber no corpo da requisição.
# FastAPI usa isso para validar os dados automaticamente. Se o frontend enviar
# algo diferente, a API retornará um erro claro.
class EmailRequest(BaseModel):
    text: str

# --- Instância da Aplicação FastAPI ---
app = FastAPI(
    title="AutoU Email Classifier API",
    description="Uma API para classificar e-mails e sugerir respostas usando IA.",
    version="1.0.0"
)

# --- Configuração do CORS ---
# Permissões para que seu frontend React (rodando em outra porta/endereço)
# possa se comunicar com esta API.
origins = [
    "http://localhost:5173", # Endereço padrão do Vite (React) em desenvolvimento
    # Adicione aqui a URL do seu frontend quando fizer o deploy
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Endpoints da API ---

@app.get("/")
def read_root():
    """Endpoint raiz para verificar se a API está online."""
    return {"status": "online", "message": "Bem-vindo à API da AutoU!"}


@app.post("/process-email")
def process_email(request: EmailRequest):
    """
    Recebe o texto de um e-mail, classifica-o e sugere uma resposta.
    """
    email_text = request.text
    
    print(f"Recebido e-mail para processamento: '{email_text[:50]}...'")

    # --- LÓGICA DA INTELIGÊNCIA ARTIFICIAL (PLACEHOLDER) ---
    # Aqui é onde você fará a chamada para a API do Hugging Face ou OpenAI.
    # Por enquanto, vamos simular o comportamento.
    
    # Simula um tempo de espera, como se estivesse processando na IA
    time.sleep(2) 

    # Lógica de simulação: se o e-mail contém palavras como "ajuda" ou "problema",
    # considera-se produtivo. Caso contrário, improdutivo.
    if any(keyword in email_text.lower() for keyword in ["ajuda", "problema", "suporte", "dúvida"]):
        category = "Produtivo"
        suggested_response = (
            "Olá! Agradecemos o seu contato. "
            "Recebemos sua solicitação e nossa equipe irá analisá-la em breve. "
            "Entraremos em contato assim que tivermos uma atualização."
        )
    else:
        category = "Improdutivo"
        suggested_response = (
            "Olá! Agradecemos pela sua mensagem. Tenha um ótimo dia!"
        )
    # --- FIM DA LÓGICA DA IA (PLACEHOLDER) ---
    
    print(f"E-mail classificado como: {category}")

    return {
        "category": category,
        "suggested_response": suggested_response
    }
