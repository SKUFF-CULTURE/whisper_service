import requests
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()]
)

class OllamaHandler:
    def __init__(self, model):
        self.logger = logging.getLogger(self.__class__.__name__)
        try:
            load_dotenv()
            self.url = os.getenv('OLLAMA_API_URL')
            self.logger.info(f'Ollama API URL: {self.url}')
            self.headers = {'Content-Type': 'application/json'}
            self.model = model
            self.logger.info('OllamaHandler initialized!')
        except Exception as e:
            self.logger.error(f"Ollama handler init failed with {e}")

    def generate(self, prompt):
        try:
            data = {
                'model': self.model,
                'prompt': prompt,
                'stream': False
            }
            response = requests.post(self.url, headers=self.headers, json=data, stream=False)
            if response.status_code == 200:
                self.logger.info('Ollama answered successfully!.')
                return response.json()["response"]
            else:
                self.logger.warning(f"Ollama answered non 200, failed with {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Ollama handler generate failed with {e}")




