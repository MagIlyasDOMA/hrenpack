"""
Pygame utilities for game development.

Provides convenience classes and functions for Pygame,
including image handling and quit handlers.

Утилиты Pygame для разработки игр.

Предоставляет удобные классы и функции для Pygame,
включая обработку изображений и обработчики выхода.
"""

import pygame, sys


class Image:
    """
    Image loading and manipulation utility.

    Утилита для загрузки и манипуляции изображениями.

    Args:
        path: Path to image file / Путь к файлу изображения
    """

    def __init__(self, path):
        self.image = pygame.image.load(path)

    def __call__(self):
        """
        Get the loaded image surface.

        Получает загруженную поверхность изображения.

        Returns:
            pygame.Surface: Image surface / Поверхность изображения
        """
        return self.image

    def resize(self, width, height):
        """
        Resize the image.

        Изменяет размер изображения.

        Args:
            width (int): New width / Новая ширина
            height (int): New height / Новая высота

        Returns:
            pygame.Surface: Resized image surface / Измененная поверхность изображения
        """
        self.image = pygame.transform.scale(self.image, (width, height))
        return self.image

    def resize_and_convert_alpha(self, width, height):
        """
        Resize and convert image with alpha channel.

        Изменяет размер и преобразует изображение с альфа-каналом.

        Args:
            width (int): New width / Новая ширина
            height (int): New height / Новая высота

        Returns:
            pygame.Surface: Resized and converted image surface / Измененная и преобразованная поверхность
        """
        self.image = self.resize(width, height).convert_alpha()
        return self.image

    @classmethod
    def quick_resize(cls, path, width, height):
        """
        Quick resize without creating instance.

        Быстрое изменение размера без создания экземпляра.

        Args:
            path: Path to image / Путь к изображению
            width (int): New width / Новая ширина
            height (int): New height / Новая высота

        Returns:
            pygame.Surface: Resized image surface / Измененная поверхность изображения
        """
        return cls(path).resize(width, height)

    @classmethod
    def quick_resize_and_convert_alpha(cls, path, width, height):
        """
        Quick resize and convert alpha without creating instance.

        Быстрое изменение размера и преобразование альфа-канала.

        Args:
            path: Path to image / Путь к изображению
            width (int): New width / Новая ширина
            height (int): New height / Новая высота

        Returns:
            pygame.Surface: Resized and converted image surface / Измененная и преобразованная поверхность
        """
        return cls(path).resize_and_convert_alpha(width, height)


def quit():
    """
    Quit Pygame and exit the program.

    Завершает работу Pygame и выходит из программы.
    """
    pygame.quit()
    sys.exit()


def quit_if_quit(event):
    """
    Quit if event type is pygame.QUIT.

    Завершает работу, если тип события pygame.QUIT.

    Args:
        event: Pygame event / Событие Pygame
    """
    if event.type == pygame.QUIT: quit()
