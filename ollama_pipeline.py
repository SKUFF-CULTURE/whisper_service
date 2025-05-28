from llm_handler import OllamaHandler
import premade_prompts
from dotenv import load_dotenv
import logging
import time
import json
import os
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()]
)


class LlmCaller:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        try:
            load_dotenv()
            self.llm = OllamaHandler(model=os.getenv('OLLAMA_MODEL', 'mistral'))
            self.logger.info(f'Successfully initialized {self.__class__.__name__}')
        except Exception as e:
            self.logger.error(f"Got an error in pipeline init: {e}")

    @staticmethod
    def _build_prompt(artist, song, lyrics):
        return premade_prompts.PROMPT_TEMPLATE_1.format(
            artist=artist,
            song=song,
            lyrics=lyrics
        )

    def _parse_ollama_result(self, ollama_response):
        self.logger.info("Started parsing Ollama answer")

        # Найти первую подстроку, начинающуюся с фигурной скобки
        match = re.search(r'({.*})', ollama_response, re.DOTALL)
        if not match:
            raise ValueError("Не удалось найти JSON-объект в ответе")

        json_part = match.group(1)

        try:
            return json.loads(json_part)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON parsing error: {e}")

    def process_llm(self, song_name: str, song_artist: str, lyrics: list, ):

        # Отправляем Ollama данные на обработку
        self.logger.info(f'Requesting Ollama for {song_name} by {song_artist}')
        prompt = self._build_prompt(artist=song_artist, song=song_name, lyrics=lyrics)
        try:
            start_time = time.time()
            answer = self.llm.generate(prompt)
            process_time = time.time() - start_time
            self.logger.info(f"Ollama worked in {process_time:.2f}s")
            self.logger.info(f"Ollama answer: {answer}")
            parsed_json = self._parse_ollama_result(answer)
            self.logger.info(f"Parsed JSON: {parsed_json}")
            return parsed_json
        except Exception as e:
            self.logger.error(f"Got an error in Ollama request: {e}")
            return None


if __name__ == '__main__':
    pl = LlmCaller()
# pl.process_llm('Дуло', 'MORGENSHTERN', LYRICS1)
