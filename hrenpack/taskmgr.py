"""
Process and task management utilities.

Provides functions to check, find, and kill running processes.

Утилиты для управления процессами и задачами.

Предоставляет функции для проверки, поиска и завершения запущенных процессов.
"""

import psutil, subprocess


def is_process_running(process_name):
    """
    Check if a process with given name is running.

    Проверяет, запущен ли процесс с указанным именем.

    Args:
        process_name (str): Name of the process to check / Имя процесса для проверки

    Returns:
        bool: True if process is running / True если процесс запущен
    """
    for proc in psutil.process_iter(['name']):
        try:
            # Check process name
            if proc.info['name'] == process_name:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def kill_process_if_is_running(process_name, *args, **kwargs):
    """
    Kill process if it is running.

    Завершает процесс, если он запущен.

    Args:
        process_name (str): Name of the process to kill / Имя процесса для завершения
        *args: Additional arguments for subprocess.run / Дополнительные аргументы для subprocess.run
        **kwargs: Additional keyword arguments for subprocess.run / Дополнительные ключевые аргументы
    """
    if is_process_running(process_name):
        subprocess.run(('taskkill', *args), **kwargs)
