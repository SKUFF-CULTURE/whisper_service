import whisper

def transcribe_audio_with_timings(audio_path):
    # Загружаем модель (можно выбрать 'tiny', 'base', 'small', 'medium', 'large')
    model = whisper.load_model("medium")  # 'base' – баланс скорости и точности

    # Расшифровываем аудио с таймингами
    result = model.transcribe(audio_path, word_timestamps=True, language='ru')

    # Возвращаем слова с временными метками
    return result["segments"]

audio_file = "audio/input.wav"
transcription = transcribe_audio_with_timings(audio_file)

for segment in transcription:
    print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")

