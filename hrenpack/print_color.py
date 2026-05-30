"""
Colored terminal output utilities.

Provides functions for printing colored text in terminals using ANSI escape codes.

Утилиты для цветного вывода в терминал.

Предоставляет функции для печати цветного текста в терминалах с использованием ANSI escape кодов.
"""


class ColorsANSI:
    """ANSI color codes for terminal output."""
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'
    DICT = {
        'black': BLACK, 'red': RED, 'green': GREEN, 'yellow': YELLOW, 'blue': BLUE,
        'magenta': MAGENTA, 'cyan': CYAN, 'white': WHITE, 'reset': RESET,
        "черный": BLACK, "красный": RED, "зеленый": GREEN, "желтый": YELLOW, "синий": BLUE,
        "пурпурный": MAGENTA, "бирюзовый": CYAN, "белый": WHITE, "сброс": RESET
    }


def print_color(*values, color: str, separator: str = ' ', end: str = '\n', file=None) -> None:
    """
    Print text in specified color.

    Печатает текст указанным цветом.

    Args:
        *values: Values to print / Значения для печати
        color (str): Color name ('red', 'green', 'blue', etc.) / Название цвета
        separator (str): Separator between values, default space / Разделитель между значениями
        end (str): End character, default newline / Конечный символ
        file: Output file, default stdout / Выходной файл

    Raises:
        KeyError: If color not found / Если цвет не найден
    """
    text = separator.join(values)
    text = ColorsANSI.DICT[color] + text + '\033[0m'
    print(text, end=end, file=file)


def print_error(*values, separator: str = ' ', end: str = '\n', file=None) -> None:
    """
    Print error message in red.

    Печатает сообщение об ошибке красным цветом.

    Args:
        *values: Values to print / Значения для печати
        separator (str): Separator between values / Разделитель между значениями
        end (str): End character / Конечный символ
        file: Output file / Выходной файл
    """
    print_color(*values, color='red', separator=separator, end=end, file=file)


def print_success(*values, separator: str = ' ', end: str = '\n', file=None) -> None:
    """
    Print success message in green.

    Печатает сообщение об успехе зеленым цветом.

    Args:
        *values: Values to print / Значения для печати
        separator (str): Separator between values / Разделитель между значениями
        end (str): End character / Конечный символ
        file: Output file / Выходной файл
    """
    print_color(*values, color='green', separator=separator, end=end, file=file)


def print_warning(*values, separator: str = ' ', end: str = '\n', file=None) -> None:
    """
    Print warning message in yellow.

    Печатает предупреждение желтым цветом.

    Args:
        *values: Values to print / Значения для печати
        separator (str): Separator between values / Разделитель между значениями
        end (str): End character / Конечный символ
        file: Output file / Выходной файл
    """
    print_color(*values, color='yellow', separator=separator, end=end, file=file)


def print_info(*values, separator: str = ' ', end: str = '\n', file=None) -> None:
    """
    Print info message in blue.

    Печатает информационное сообщение синим цветом.

    Args:
        *values: Values to print / Значения для печати
        separator (str): Separator between values / Разделитель между значениями
        end (str): End character / Конечный символ
        file: Output file / Выходной файл
    """
    print_color(*values, color='blue', separator=separator, end=end, file=file)


def color_format(*values, color: str, separator: str = ' ', end: str = '') -> str:
    """
    Format text with color without printing.

    Форматирует текст с цветом без печати.

    Args:
        *values: Values to format / Значения для форматирования
        color (str): Color name / Название цвета
        separator (str): Separator between values / Разделитель между значениями
        end (str): String to append at the end / Строка для добавления в конец

    Returns:
        str: Colored formatted string / Цветная отформатированная строка
    """
    text = separator.join(values)
    text = ColorsANSI.DICT[color] + text + '\033[0m'
    text += end
    return text


def error_format(*values, separator: str = ' ', end: str = '') -> str:
    """
    Format error message in red.

    Форматирует сообщение об ошибке красным цветом.

    Args:
        *values: Values to format / Значения для форматирования
        separator (str): Separator between values / Разделитель между значениями
        end (str): String to append / Строка для добавления

    Returns:
        str: Formatted error string / Отформатированная строка ошибки
    """
    return color_format(*values, color='red', separator=separator, end=end)


def success_format(*values, separator: str = ' ', end: str = '') -> str:
    """
    Format success message in green.

    Форматирует сообщение об успехе зеленым цветом.

    Args:
        *values: Values to format / Значения для форматирования
        separator (str): Separator between values / Разделитель между значениями
        end (str): String to append / Строка для добавления

    Returns:
        str: Formatted success string / Отформатированная строка успеха
    """
    return color_format(*values, color='green', separator=separator, end=end)


def warning_format(*values, separator: str = ' ', end: str = '') -> str:
    """
    Format warning message in yellow.

    Форматирует предупреждение желтым цветом.

    Args:
        *values: Values to format / Значения для форматирования
        separator (str): Separator between values / Разделитель между значениями
        end (str): String to append / Строка для добавления

    Returns:
        str: Formatted warning string / Отформатированная строка предупреждения
    """
    return color_format(*values, color='yellow', separator=separator, end=end)


def info_format(*values, separator: str = ' ', end: str = '') -> str:
    """
    Format info message in blue.

    Форматирует информационное сообщение синим цветом.

    Args:
        *values: Values to format / Значения для форматирования
        separator (str): Separator between values / Разделитель между значениями
        end (str): String to append / Строка для добавления

    Returns:
        str: Formatted info string / Отформатированная строка информации
    """
    return color_format(*values, color='blue', separator=separator, end=end)
