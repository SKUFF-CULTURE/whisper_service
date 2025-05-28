from lyrical_gpu import AudioTranscriber
from ollama_pipeline import LlmCaller
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()]
)

def run(audio_path, language, model):
    logging.info('Setting up...')
    try:
        # Setting up

        transcriber = AudioTranscriber(model)
        llm = LlmCaller()

        # Running whisper

        transcribed_data = transcriber.process(audio_path=audio_path, language=language, word_timestamps=True)
        logging.info(transcribed_data)
        logging.info('Transcription done successfully!')

        # Running LLM call
        llm_decision = llm.process_llm(song_name="<Песня загруженная пользователем>", song_artist="<пользовательсктий автор>",lyrics=transcribed_data)
        logging.info(f"Decision from Ollama: {llm_decision}")

        return 0, transcribed_data, llm_decision
    except Exception as e:
        logging.error(e)
        return 1, None, None





if __name__ == '__main__':
    run(audio_path="audio/input.wav", language="ru", model="tiny")
