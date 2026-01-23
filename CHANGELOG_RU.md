# Changelog

Все изменения в этом проекте документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/),
и проект придерживается [Семантического Версионирования](https://semver.org/).

## [2.5.2] - 23.01.2026
- Функции `Fand`, `For` и `switch_For` объявлены устаревшими
- Исправления багов

## [2.5.1] - 22.01.2026
- Убраны лишние переносы строки в файлах
- В dev_requirements `pip-setuptools>=1.1.3` изменен на `pip-setuptools>=1.1.4`

## [2.5.0] - 21.01.2026
- Добавлен модули `argparse_plus.py` и `iterwork.py`
- Исправлены баги в `encapsulation.py` и `listwork.py`
- Добавлен декоратор `superonlymethod` в `encapsulation.py`
- Добавлена функция `empty_function(*args, **kwargs)` в `functionwork.py`
- Добавлены экстра `[dev]`, `[dev_base]`, `[dev_image]`, `[dev_flask]`, `[dev_filetype]`, `[dev_all]`, `[dev_full`

## [2.4.1] - 16.01.2026
- Добавлен модуль `i18n.py`
- В базовые requirements добавлены `python-gettext~5.0` и `pathlike-typing`

## [2.4.0] - 15.01.2026
- Добавлен декоратор `deprecated` в `decorators.py` (полностью работает на Python 3.13+)
- Добавлен модуль `filetype.py`
- Удалена константа `RGB` из модуля `constants.py`
- Функция `get_mime_type` в `cmd.py` объявлена устаревшей 
- Модуль `filetype` удален из базовых requirements
- Добавлен экстра `[filetype]`

## [2.3.0] - 01.01.2026
- Убраны копирайты из начала файлов
- Добавлена функция `subfactorial` в `algebra.py`
- Добавлен класс `TupleDict` в `classes.py`
- Добавлены модули `framework/django/db.py` и `framework/django/urls.py`
- Добавлена функция `create_logout_view_with_next()` в файл `framework/django/views.py`
- Изменен класс формы на `UserCreationForm` в представлении `RegistrationView` (`framework/django/views.py`)
- Добавлен модуль `ipwork.py`

## [2.2.2] - 02.12.2025
- Убран лишний реверс списка в `framework/flask/forms/mixins.py` в методе `as_p` класса `DjangoStyleFormMixin`

## [2.2.1] - 02.12.2025
- Исправлен баг, вызывавший ошибку в `listwork.py` 

## [2.2.0] - 02.12.2025
- Добавлен пакет `flask` в `framework`

## [2.1.2] - 28.11.2025
Первая стабильная версия `hrenpack`

### Установка
```shell
pip install hrenpack
```

### Пакет содержит модули:
- `__init__` - основные функции и функции, которые не могут быть отнесены ни к одной категории
- `algebra` - работа с алгебраическими выражениями
- `boolwork` - работа с булевыми значениями
- `charset` - работа с кодировками файлов
- `classes` - классы
- `clipboard_work` - работа с буфером обмена
- `cmd` - работа с инструментами ОС
- `constants` - разные полезные константы 
- `date_and_time_work` - работа со значениями даты и времени
- `decorators` - декораторы
- `functionwork` - работа с функциями
- `hashwork` - работа с хешированием
- `encapsulation` - полноценная инкапсуляция
- `kwargswork` - работа с **kwargs
- `listwork` - работа со списками, кортежами и словарями
- `network` - работа с интернетом
- `numwork` - работа с числами
- `python` - работа с импортами python
- `print_color` - цветная консоль. Может работать не во всех консолях
- `resolution` - определение разрешения экрана
- `slugwork` - работа со slug, т. е. с строками, которые соответствуют правилам
- `strwork` - работа со строками
- `taskmgr` - работа с задачами
- `type_define` - определение, относятся ли данные к определнному типу, или нет
- `typings` - тайпингами
- `windows_registry` - работа с реестром Windows

### Помимо пакетов, в hrenpack есть несколько подбиблиотек:
- `custom_methods` - дополнительные методы для уже существующих объектов
- `filework` - работа с файлами
- `framework` - дополнительные функции для уже существующих библиотек и фреймворков:
  - `Pyside6`
  - `Kivy`
  - `Django`
  - `pygame`
  - `tkinter`

### Требования
- Python 3.10+
- Django 5.2+
- Flask 3.1.2+

#### Другие требования указаны в [файлах requirements]()


## [1.0.0 - 2.1.1] - нестабильные версии
Данные версии нестабильны и не рекомендуются к установке
