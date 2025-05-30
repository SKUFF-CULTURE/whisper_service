from dotenv import load_dotenv
import os

load_dotenv()
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")

KAFKA_TOPICS = {
    "nettools": "app.main.nettools",
    "audio_raw": "app.main.audio_raw",
    "audio_buffed": "app.main.audio_buffed",
    "audio_recognised": "app.main.audio_recognised",
    "audio_processed": "app.main.audio_processed",
}

KAFKA_CONSUMER_GROUPS = {
    # Group for net producers
    "nettools_group": "app.nettools.group",
    "audio_voicefixers_group": "app.main.audio.voicefixers.group",
    "audio_recognisers_group": "app.main.audio.recognisers.group",
    "audio_compositors_group": "app.main.audio.compositors.group",
}

ACTOR_GRACE_PERIOD = 20

NFS_MOUNT_POINT = os.getenv("NFS_MOUNT_POINT", "/mnt/nfs_share/")

NFS_IP = os.getenv("NFS_IP", "172.30.26.251")