import ollama
from AIAgent_Config import OLLAMA_MODEL


class AIAgent_Ollama:
    def __init__(self):
        self.client = ollama.Client()


    def generate_response(self, text: str) -> str:
        response = self.client.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    'role': 'user',
                    'content': f"""
                    - Escreva em um estilo organizado e limpo, pulando linhas se necessário.
                    - Seja breve e objetivo, transmitindo a mensagem de forma clara e concisa.
                    - Use palavras curtas e frases simples, evitando complexidade desnecessária.
                    - Fale como um humano, com um tom descontraído e carismático.
                    - Use emojis para tornar a conversa mais envolvente e divertida.
                    - Evite repetir palavras e frases.
                    - Descreva de forma descontraida e carismática para o cliente o que você sabe sobre essa comida: {text},
                    - Evite usar palavras como "delicioso", "saboroso" e "gostoso".
                    - Convença o cliente a comprar o produto, destacando seus benefícios e características únicas.
                    - Seja persuasivo, mas sem ser agressivo, e evite usar clichês ou frases prontas.
                    - Use uma linguagem simples e direta, evitando termos técnicos ou jargões.
                    """
                }
            ],
            options={
                "temperature": 0.7,
                "num_predict": 512,
                "top_p": 0.9,
            }
        )
        
        # Acesso via atributo de objeto
        return response.message.content