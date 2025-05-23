import whisper
import torch
from datetime import timedelta
import time
import logging
import warnings



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()]
)


class AudioTranscriber:
    def __init__(self, model):
        self.logger = logging.getLogger(self.__class__.__name__)
        try:
            warnings.filterwarnings("ignore", message="Failed to launch Triton kernels.*")
            # Проверяем доступность GPU
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.logger.info(f"Using device: {self.device.upper()}")

            # Загружаем модель
            self.model = whisper.load_model(model, device=self.device)
            self.logger.info(f"Model loaded: {model}")
        except Exception as e:
            self.logger.error(f"AudioTranscriber setup failed with {e}")

    def _transcribe(self, audio_path, language, word_timestamps):
        self.logger.info("Starting transcription...")
        try:
            options = {
                "language": language,  # Явно указываем русский язык
                "word_timestamps": word_timestamps,  # Тайминги для слов
                "task": "transcribe",  # Только транскрибация (без перевода)
                "fp16": False if self.device == "cpu" else True  # FP16 для GPU
            }

            self.logger.info(f"Working on: {audio_path}")
            result = self.model.transcribe(audio_path, **options)

            # Форматируем тайминги в читаемый вид
            segments = []
            for segment in result["segments"]:
                start = str(timedelta(seconds=round(segment['start'])))
                end = str(timedelta(seconds=round(segment['end'])))
                segments.append({
                    "start": start,
                    "end": end,
                    "text": segment['text'].strip()
                })

            return segments

        except Exception as e:
            self.logger.error(f"AudioTranscriber process failed with {e}")
            return None

    def process(self, audio_path, language, word_timestamps):
        start_time = time.time()
        transcription = self._transcribe(audio_path, language, word_timestamps)
        process_time = time.time() - start_time
        self.logger.info(f"Restoration completed in {process_time:.2f}s")
        self.logger.debug(transcription)
        return transcription


if __name__ == "__main__":
    ts = AudioTranscriber("medium")
    data = ts.process(audio_path="audio/input.wav", language="ru", word_timestamps=True)
    print(data)
