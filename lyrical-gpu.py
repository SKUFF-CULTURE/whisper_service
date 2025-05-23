import whisper
import torch
from datetime import timedelta
import sys
import time


def transcribe_audio_with_timings(audio_path):
    try:
        # Проверяем доступность GPU
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Используемое устройство: {device.upper()}")

        # Загружаем модель (medium лучше для русского, но можно изменить)
        model = whisper.load_model("large", device=device)

        # Опции транскрибации
        options = {
            "language": "ru",  # Явно указываем русский язык
            "word_timestamps": True,  # Тайминги для слов
            "task": "transcribe",  # Только транскрибация (без перевода)
            "fp16": False if device == "cpu" else True  # FP16 для GPU
        }

        print(f"Начинаю обработку файла: {audio_path}")
        result = model.transcribe(audio_path, **options)

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
        print(f"Ошибка при обработке аудио: {str(e)}", file=sys.stderr)
        return None


if __name__ == "__main__":
    audio_file = "audio/final_1747866130.wav"

    # Проверка существования файла
    try:
        with open(audio_file, 'rb'):
            pass
    except FileNotFoundError:
        print(f"Файл {audio_file} не найден!", file=sys.stderr)
        sys.exit(1)

    # Запуск транскрибации
    start_time = time.time()
    transcription = transcribe_audio_with_timings(audio_file)

    process_time = time.time() - start_time
    print(f"Restoration completed in {process_time:.2f}s")


    if transcription:
        print("\nРезультат транскрибации:")
        for segment in transcription:
            print(f"[{segment['start']} - {segment['end']}] {segment['text']}")

        # Дополнительная статистика
        total_duration = sum(
            (float(timedelta.total_seconds(timedelta.strptime(s['end'], "%H:%M:%S")) -
                   float(timedelta.total_seconds(timedelta.strptime(s['start'], "%H:%M:%S")))
                   for s in transcription
                   )))
        print(f"\nОбщая длительность речи: {total_duration:.2f} секунд")
        print(f"Количество сегментов: {len(transcription)}")