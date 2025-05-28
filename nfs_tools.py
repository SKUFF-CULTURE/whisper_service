import os
import subprocess
import logging
import shutil
import time

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

def mount_nfs_in_self(
        nfs_server_ip: str,
        nfs_path: str,
        mount_point: str = "/mnt/nfs",
        options: str = "nolock,soft,intr",
        timeout: int = 30
) -> bool:
    """
    Монтирует NFS-шару внутрь текущего Docker-контейнера

    :param nfs_server_ip: IP/hostname NFS-сервера
    :param nfs_path: Путь на NFS-сервере (например '/share/data')
    :param mount_point: Локальная точка монтирования
    :param options: Опции монтирования NFS
    :param timeout: Таймаут попыток монтирования (сек)
    :return: True если успешно, False если ошибка
    """
    try:
        # Проверяем, что мы внутри контейнера
        if not os.path.exists('/.dockerenv'):
            raise RuntimeError("Этот код должен выполняться внутри Docker-контейнера")

        # Создаем точку монтирования
        os.makedirs(mount_point, exist_ok=True)

        # Формируем команду монтирования
        mount_cmd = f"mount -t nfs -o {options} {nfs_server_ip}:{nfs_path} {mount_point}"

        # Выполняем с несколькими попытками (NFS может быть медленным)
        for attempt in range(max(1, timeout // 5)):
            try:
                subprocess.run(
                    mount_cmd,
                    shell=True,
                    check=True,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE
                )
                # Проверяем что успешно смонтировалось
                if os.path.ismount(mount_point):
                    return True
            except subprocess.CalledProcessError:
                if attempt == (timeout // 5) - 1:
                    raise
                time.sleep(5)

        return False

    except Exception as e:
        logger.error(f"Ошибка монтирования NFS: {str(e)}")
        return False

success = mount_nfs_in_self(
    nfs_server_ip="192.168.1.100",
    nfs_path="/mnt/nfs_share",
    mount_point="/mnt/nfs_share"
)