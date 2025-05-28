import os
import subprocess
import logging
import shutil

# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def check_nfs_server(nfs_mount_point="/mnt/nfs_share" ):
    logging.info(f"Searching for NFS server...")
    try:
        if os.path.ismount(nfs_mount_point):
            logging.info(f"NFS server is already available at {nfs_mount_point}")
            return True
        else:
            # Если нет, пытаемся смонтировать его (с использованием команды mount)
            logging.info(f"Mounting directory...")
            result = subprocess.run(['mount', nfs_mount_point], capture_output=True,
                                    text=True)
            if result.returncode == 0:
                logging.info(f"NFS server directory was successfully mounted.")
                return True
            else:
                logging.error(f"Error while connecting to nfs server: {result.stderr}")
                return False
    except Exception as e:
        logging.error(f"NFS server-check issue was caught: {e}")
        return False

def flush_nfs(path: str, nfs_root: str):
    try:
        # Проверка: абсолютный путь
        abs_path = os.path.abspath(path)

        # Проверка: лежит ли внутри NFS_ROOT
        if not abs_path.startswith(nfs_root):
            logger.error(f"Flushing outside of NFS is prohibited!: {abs_path}")
            return

        # Проверка: существует ли и является ли директорией
        if not os.path.isdir(abs_path):
            logger.warning(f"No such path or it is not a dir: {abs_path}")
            return

        # Удаляем рекурсивно
        shutil.rmtree(abs_path)
        logger.info(f"Successful dir flushing: {abs_path}")

    except Exception as e:
        logger.exception(f"Error while dir flushing {path}: {e}")