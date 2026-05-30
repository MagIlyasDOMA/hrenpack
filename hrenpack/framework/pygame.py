"""
Pygame utilities for game development.

Provides convenience classes and functions for Pygame,
including keyboard constants, image handling, and quit handlers.

Утилиты Pygame для разработки игр.

Предоставляет удобные классы и функции для Pygame,
включая константы клавиш, обработку изображений и обработчики выхода.
"""

import pygame, sys


class Keyboard:
    """Keyboard key constants for Pygame."""
    A = pygame.K_a
    B = pygame.K_b
    C = pygame.K_c
    D = pygame.K_d
    E = pygame.K_e
    F = pygame.K_f
    G = pygame.K_g
    H = pygame.K_h
    I = pygame.K_i
    J = pygame.K_j
    K = pygame.K_k
    L = pygame.K_l
    M = pygame.K_m
    N = pygame.K_n
    O = pygame.K_o
    P = pygame.K_p
    Q = pygame.K_q
    R = pygame.K_r
    S = pygame.K_s
    T = pygame.K_t
    U = pygame.K_u
    V = pygame.K_v
    W = pygame.K_w
    X = pygame.K_x
    Y = pygame.K_y
    Z = pygame.K_z
    SPACE = pygame.K_SPACE


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
    if event.type == pygame.QUIT:
        quit()
