import logging
import json
import time
import os
from dotenv import load_dotenv
from kafka_tools import KafkaMessageConsumer, KafkaMessageProducer
from config import KAFKA_TOPICS, KAFKA_CONSUMER_GROUPS, ACTOR_GRACE_PERIOD, NFS_MOUNT_POINT
import pipeline
import nfs_tools

# Настроим логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NAME = "SERVICE_RECOGNISER"
load_dotenv()

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "tiny")

if WHISPER_MODEL == "tiny":
    logger.warning(f"Using model tiny for whisper likely to env parse fail or test run!")

# Получаем топик и группу
topic = KAFKA_TOPICS.get("audio_buffed")
group = KAFKA_CONSUMER_GROUPS.get("audio_recognisers_group")

# Инициализируем Kafka consumer
consumer = KafkaMessageConsumer(topic=topic, group=group)

# Инициализируем Kafka producer
producer_topic = KAFKA_TOPICS.get("audio_recognised")
producer = KafkaMessageProducer(topic=producer_topic)


def serve(key, value):
    logger.info(f"{NAME}| ✴️ Got kafka message with key: {key}!")
    try:
        data = json.loads(value)
        pipeline_uuid = data.get("uuid")
        final_path = data.get("final_path")
        vocals_path = data.get("vocals_path")

        logger.info(f"Continuing pipeline with uuid: {pipeline_uuid}...")
        logger.info(f"Calling pipeline on {vocals_path}...")

        pipeline_error_flag, lyrics, llm_decision = pipeline.run(audio_path=vocals_path, model="heavy-v2",
                                                                 language="ru")

        if pipeline_error_flag is False:
            logger.info(f"Pipeline {pipeline_uuid} ended successfully!")
        else:
            logger.error(f"Pipeline {pipeline_uuid} encountered internal errors!")

        message = json.dumps({
            "uuid": pipeline_uuid,
            "final_path": final_path,
            "lyrics": lyrics,
            "llm_decision": llm_decision
        })

        logger.info(f"⏩ Producer is sending message to {producer_topic}")
        producer.send_message(key=key, value=message)

        pipeline_dir = os.path.dirname(final_path)
        #logger.info(f"🧻 As full pipeline is done, now cleaning nfs dir: {pipeline_dir}")

        #nfs_tools.flush_nfs(pipeline_dir, NFS_MOUNT_POINT)

        logger.info(f"🚀 Work cycle on {pipeline_uuid} done!")

    except json.JSONDecodeError as e:
        logger.error(f"{NAME} | ❌ JSON decoding error: {e}")
    except Exception as e:
        logger.error(f"{NAME} | ❌ Error processing message: {e}")


if __name__ == "__main__":
    logger.info(f"{NAME} | ⏳ Sleeping for {ACTOR_GRACE_PERIOD} seconds...")
    time.sleep(ACTOR_GRACE_PERIOD)
    logger.info("Running external health-checks...")
    if not nfs_tools.check_nfs_server(NFS_MOUNT_POINT):
        logger.warning("NFS server is not available! Crucial functionality likely to be unavailable.")
    else:
        logger.info("NFS server is available!")
    try:
        logger.info(f"{NAME} | 🔄 Starting Kafka consumer...")
        consumer.consume_messages(serve)
    except Exception as e:
        logger.error(f"{NAME} | ❌ Error in Kafka consumer: {e}")
    finally:
        logger.info(f"{NAME} | 🛑 Stopping Kafka consumer...")
        consumer.close()  # Закрываем consumer корректно
        producer.flush()
