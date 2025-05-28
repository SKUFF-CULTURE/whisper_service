from lyrical_gpu import AudioTranscriber
from lyrical_pipeline import LlmCaller
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

        # Running

        transcribed_data = transcriber.process(audio_path=audio_path, language=language, word_timestamps=True)
        print(transcribed_data)
        logging.info('Transcription done successfully!')
        revenue = llm.process_llm(song_name="<Песня загруженная пользователем>",song_artist="<>",lyrics=transcribed_data)
        print(revenue)






        return 0, transcribed_data
    except Exception as e:
        logging.error(e)
        return 1, None





if __name__ == '__main__':
    run(audio_path="audio/input.wav", language="ru", model="tiny")
