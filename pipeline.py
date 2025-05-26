from lyrical_gpu import AudioTranscriber
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
        # Running
        transcribed_data = transcriber.process(audio_path=audio_path, language=language, word_timestamps=True)
        logging.info('Done successfully!')
        return 0
    except Exception as e:
        logging.error(e)
        return 1





if __name__ == '__main__':
    run(audio_path="audio/input.wav", language="ru", model="tiny")
