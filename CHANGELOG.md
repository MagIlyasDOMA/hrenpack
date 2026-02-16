<a id="clen"></a>
# Changelog
[Changelog на русском](#clru)

All changes in this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [3.0.0-beta.2] - 2026-02-16
### Breaking changes ⚠️
- Removed `framework/Pyside6/templates.py` module
- Changed `setup.py` to `pyproject.toml`
- Completely reworked the `is_object` function in `type_define.py`
- Reworked `dev_*` extras under `pyproject.toml`

### Added ✨
- Added `screen.py` and `styles.py` modules to `framework/Pyside6`
- Added the `exclude_nones` function to `kwargswork.py`

### Fixed 🐛
- Removed import of non-existent decorator in `__init__.py`

## [3.0.0-beta.1] - 2026-02-11
First beta version of hrenpack 3.0.0

### Breaking changes ⚠️
- Minimum Python version is now 3.13+
- Removed `null`, `show_help`, and `get_resource` functions in `__init__.py`
- Removed `Fand`, `For`, and `switch_For` functions in `boolwork.py`
- Removed `get_mime_type` function in `cmd.py`
- Removed `list_to_str`, `is_first`, and `is_last` functions in `strwork.py`
- Removed `deprecated` decorator in `decorators.py`
- Removed `system.py` module
- Removed `Converter` subclass in `ConfigurationFile` class `filework/__init__.py`

---

## [2.5.9] - 2026-02-10
### Fixed 🐛
- Corrected version in `__init__.py`

## [2.5.8] - 2026-02-10
### Added
- Added extras [django], [pyside6], [kivy], [pygame], [dev_django], [dev_pyside6], [dev_kivy], [dev_pygame], and [full]

### Changed
- Removed the `dataclass` decorator from the `Keyboard` class in `framework/pygame.py`

## [2.5.7] - 2026-02-02
### Fixed 🐛
- Fixed [dev] extras

## [2.5.6] - 2026-02-02
### Deprecated ⚠️
- The functions `show_help` and `get_resource` in `__init__.py` are deprecated
- The functions `list_to_str`, `is_first`, and `is_last` in `strwork.py` are deprecated
- The `system.py` module is deprecated

### Changed 🔧
- Added "This function will be removed in version 3.0.0" to the deprecation warning text

### Fixed 🐛
- Removed unnecessary imports
- Removed use of deprecated functions


## [2.5.5] - 2026-02-01
### Fixed 🐛
- Fixed imports in `cmd.py`

## [2.5.4] - 2026-02-01
### Deprecated ⚠️
- The `deprecated` decorator in `decorators.py` has been deprecated

### Fixed 🐛
- Optimized the `for_in` function in `boolwork.py`
- Fixed deprecation from the `@deprecated` decorator to `warnings.warn`

## [2.5.3] - 2026-01-31
### Changed 🔧
- Enhanced setup.py with development workflow improvements

### Dependencies 📦
- Development workflow improvements for better pip/setuptools integration


## [2.5.2] - 2026-01-23
### Deprecated ⚠️
- Functions `Fand`, `For` and `switch_For` in `boolwork.py` are now deprecated
- Function `null` in `__init__.py` is now deprecated

### Fixed 🐛
- Optimized the `non_print` decorator in `decorators.py`


## [2.5.1] - 2026-01-22
### Changed 🔧
- Removed unnecessary line breaks in source files for better readability

### Dependencies 📦
- Updated `pip-setuptools` version from `>=1.1.3` to `>=1.1.4` in dev_requirements


## [2.5.0] - 2026-01-21
### Added ✨
- New module `argparse_plus.py` with enhanced command-line argument parsing
- Module `iterwork.py` for working with iterators and generators
- Decorator `superonlymethod` in `encapsulation.py` for methods for false method overriding
- Function `empty_function(*args, **kwargs)` in `functionwork.py` as a universal stub

### Fixed 🐛
- Fixed bugs in `encapsulation.py` and `listwork.py`
- Python 3.14 compatibility issues

### Dependencies 📦
- Added development extras:
  - `[dev]`, `[dev_base]`, `[dev_image]`, `[dev_flask]`
  - `[dev_filetype]`, `[dev_all]`, `[dev_full]`


## [2.4.1] - 2026-01-16
### Added ✨
- New module `i18n.py` for internationalization and localization

### Dependencies 📦
- Added `python-gettext~5.0` and `pathlike-typing` to base requirements


## [2.4.0] - 2026-01-15
### Added ✨
- Decorator `deprecated` in `decorators.py` (fully works on Python 3.13+)
- New module `filetype.py` for file type detection

### Removed 🗑️
- Constant `RGB` removed from `constants.py` module

### Deprecated ⚠️
- Function `get_mime_type` in `cmd.py` is now deprecated (use `filetype` instead)

### Dependencies 📦
- `filetype` module removed from base requirements
- Added `[filetype]` extra for optional installation


## [2.3.0] - 2026-01-01
### Changed 🔧
- Removed copyright notices from file headers to reduce package size

### Added ✨
- Function `subfactorial` in `algebra.py` for calculating subfactorials
- Class `TupleDict` in `classes.py` for pseudo-dictionaries (lists with two-element tuples)
- New modules `framework/django/db.py` and `framework/django/urls.py`
- Function `create_logout_view_with_next()` in `framework/django/views.py`
- Module `ipwork.py` for working with IP addresses

### Updated 🔄
- Changed form class to `UserCreationForm` in `RegistrationView` (`framework/django/views.py`)


## [2.2.2] - 2025-12-02
### Fixed 🐛
- Removed unnecessary list reversal in `framework/flask/forms/mixins.py` in `as_p` method of `DjangoStyleFormMixin` class


## [2.2.1] - 2025-12-02
### Fixed 🐛
- Fixed bug causing an error in `listwork.py`


## [2.2.0] - 2025-12-02
### Added ✨
- Added `flask` package to `framework` for Flask integration


## [2.1.2] - 2025-11-28 🎉
First stable version of `hrenpack`!

### 📦 Package Contents
#### Core Modules:
- **Core**: `__init__`, `algebra`, `boolwork`, `charset`, `classes`
- **System**: `clipboard_work`, `cmd`, `windows_registry`
- **Utilities**: `constants`, `decorators`, `functionwork`, `hashwork`
- **Data Processing**: `strwork`, `slugwork`, `listwork`, `numwork`
- **Network & Interface**: `network`, `resolution`, `print_color`
- **Types & Management**: `type_define`, `typings`, `taskmgr`, `encapsulation`, `kwargswork`

#### Sublibraries:
- `custom_methods` - additional methods for existing objects
- `filework` - file and filesystem operations
- `framework` - integrations with popular frameworks:
  - `Pyside6` - Qt applications
  - `Kivy` - cross-platform mobile applications
  - `Django` - web framework
  - `pygame` - game development
  - `tkinter` - standard GUI

### ⚙️ Requirements
#### Core:
- **Python**: 3.10+
- **Django**: 5.2+ (for `framework/django/` modules)
- **Flask**: 3.1.2+ (for `framework/flask/` modules)

#### Installation:
```shell
# Basic installation
pip install hrenpack

# With additional features
pip install hrenpack[filetype]
pip install hrenpack[dev]
```

Full list of dependencies available in [requirements files](https://github.com/MagIlyasDOMA/hrenpack/tree/main/requirements)

---

## [1.0.0 - 2.1.1] - Unstable Versions
#### Note
These versions were unstable and are not recommended for installation.

Use version 2.1.2 or higher for production environments.

---

<a id="clru"></a>
# Changelog
[Changelog in English](#clen)

Все изменения в этом проекте документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/),
и проект придерживается [Семантического Версионирования](https://semver.org/).

## [3.0.0-beta.2] - 2026-02-16
### Критические изменения ⚠️
- Удален модуль `framework/Pyside6/templates.py`
- `setup.py` изменен на `pyproject.toml`
- Полностью переработана функция `is_object` в `type_define.py`
- Переработаны экстра `dev_*` под `pyproject.toml`

### Добавлено ✨
- Добавлены модули `screen.py` и `styles.py` в `framework/Pyside6`
- Добавлена функция `exclude_nones` в `kwargswork.py`

### Исправлено 🐛
- Убран импорт несуществующего декоратора в `__init__.py`

## [3.0.0-beta.1] - 2026-02-11
Первая бета-версия hrenpack 3.0.0

### Критические изменения ⚠️
- Минимальная версия Python теперь 3.13+
- Удалены функции `null`, `show_help` и `get_resource` в `__init__.py`
- Удалены функции `Fand`, `For` и `switch_For` в `boolwork.py`
- Удалена функция `get_mime_type` в `cmd.py`
- Удалены функции `list_to_str`, `is_first` и `is_last` в `strwork.py`
- Удален декоратор `deprecated` в `decorators.py`
- Удален модуль `system.py`
- Удален подкласс `Converter` в классе `ConfigurationFile` в `filework/__init__.py`

---

## [2.5.9] - 2026-02-10
### Исправлено 🐛
- Исправлена версия в `__init__.py`

## [2.5.8] - 2026-02-10
### Добавлено ✨
- Добавлены экстра [django], [pyside6], [kivy], [pygame], [dev_django], [dev_pyside6], [dev_kivy], [dev_pygame] и [full]

### Изменено 🔧
- Убран декоратор `dataclass` из класса `Keyboard` в `framework/pygame.py` 

## [2.5.7] - 2026-02-02
### Исправлено 🐛
- Исправлены экстра [dev]

## [2.5.6] - 2026-02-02
### Устарело ⚠️
- Функции `show_help`, `get_resource`, в `__init__.py` объявлены устаревшими
- Функции `list_to_str`, `is_first`, `is_last` в `strwork.py` объявлены устаревшими
- Модуль `system.py` объявлен устаревшим

### Изменено 🔧
- В текст предупреждений устаревания добавлено "This function will be removed in version 3.0.0"

### Исправлено 🐛
- Убраны лишние импорты
- Убрано использование устаревших функций

## [2.5.5] - 2026-02-01
### Исправлено 🐛
- Исправлены импорты в `cmd.py`

## [2.5.4] - 2026-02-01
### Устарело ⚠️
- Декоратор `deprecated` в `decorators.py` объявлен устаревшим

### Исправлено 🐛
- Оптимизирована функция `for_in` в `boolwork.py`
- Исправлено устаревание с декоратора `@deprecated` на `warnings.warn`

## [2.5.3] - 2026-01-31
### Изменено 🔧
- Улучшен setup.py с улучшениями рабочего процесса разработки

### Зависимости 📦
- Улучшения рабочего процесса разработки для лучшей интеграции с pip/setuptools


## [2.5.2] - 2026-01-23
### Устарело ⚠️
- Функции `Fand`, `For` и `switch_For` в `boolwork.py` объявлены устаревшими
- Функция `null` в `__init__.py` объявлена устаревшей

### Исправлено 🐛
- Оптимизирован декоратор `non_print` в `decorators.py`


## [2.5.1] - 2026-01-22
### Изменено 🔧
- Убраны лишние переносы строки в исходных файлах для улучшения читаемости

### Зависимости 📦
- Обновлена версия `pip-setuptools` с `>=1.1.3` на `>=1.1.4` в dev_requirements


## [2.5.0] - 2026-01-21
### Добавлено ✨
- Новый модуль `argparse_plus.py` с расширенным парсингом аргументов командной строки
- Модуль `iterwork.py` для работы с итераторами и генераторами
- Декоратор `superonlymethod` в `encapsulation.py` для методов для ложного переопределения методов
- Функция `empty_function(*args, **kwargs)` в `functionwork.py` как универсальная заглушка

### Исправлено 🐛
- Исправлены баги в `encapsulation.py` и `listwork.py`
- Проблемы совместимости с Python 3.14

### Зависимости 📦
- Добавлены extras для разработки:
  - `[dev]`, `[dev_base]`, `[dev_image]`, `[dev_flask]`
  - `[dev_filetype]`, `[dev_all]`, `[dev_full]`


## [2.4.1] - 2026-01-16
### Добавлено ✨
- Новый модуль `i18n.py` для интернационализации и локализации

### Зависимости 📦
- Добавлены `python-gettext~5.0` и `pathlike-typing` в базовые требования


## [2.4.0] - 2026-01-15
### Добавлено ✨
- Декоратор `deprecated` в `decorators.py` (полностью работает на Python 3.13+)
- Новый модуль `filetype.py` для определения типов файлов

### Удалено 🗑️
- Константа `RGB` из модуля `constants.py`

### Устарело ⚠️
- Функция `get_mime_type` в `cmd.py` объявлена устаревшей (используйте `filetype`)

### Зависимости 📦
- Модуль `filetype` удален из базовых requirements
- Добавлен экстра `[filetype]` для опциональной установки


## [2.3.0] - 2026-01-01
### Изменено 🔧
- Убраны копирайты из начала файлов для уменьшения размера пакета

### Добавлено ✨
- Функция `subfactorial` в `algebra.py` для вычисления субфакториалов
- Класс `TupleDict` в `classes.py` для псевдословарей (списков с кортежами из двух элементов)
- Новые модули `framework/django/db.py` и `framework/django/urls.py`
- Функция `create_logout_view_with_next()` в `framework/django/views.py`
- Модуль `ipwork.py` для работы с IP-адресами

### Обновлено 🔄
- Изменен класс формы на `UserCreationForm` в представлении `RegistrationView` (`framework/django/views.py`)


## [2.2.2] - 2025-12-02
### Исправлено 🐛
- Убран лишний реверс списка в `framework/flask/forms/mixins.py` в методе `as_p` класса `DjangoStyleFormMixin`


## [2.2.1] - 2025-12-02
### Исправлено 🐛
- Исправлен баг, вызывавший ошибку в `listwork.py`


## [2.2.0] - 2025-12-02
### Добавлено ✨
- Добавлен пакет `flask` в `framework` для интеграции с Flask


## [2.1.2] - 2025-11-28 🎉
Первая стабильная версия `hrenpack`!

### 📦 Содержание пакета
#### Основные модули:
- **Ядро**: `__init__`, `algebra`, `boolwork`, `charset`, `classes`
- **Системные**: `clipboard_work`, `cmd`, `windows_registry`
- **Утилиты**: `constants`, `decorators`, `functionwork`, `hashwork`
- **Работа с данными**: `strwork`, `slugwork`, `listwork`, `numwork`
- **Сеть и интерфейс**: `network`, `resolution`, `print_color`
- **Типы и управление**: `type_define`, `typings`, `taskmgr`, `encapsulation`, `kwargswork`

#### Подбиблиотеки:
- `custom_methods` - дополнительные методы для существующих объектов
- `filework` - работа с файлами и файловыми системами
- `framework` - интеграции с популярными фреймворками:
  - `Pyside6` - Qt-приложения
  - `Kivy` - кроссплатформенные мобильные приложения
  - `Django` - веб-фреймворк
  - `pygame` - разработка игр
  - `tkinter` - стандартный GUI

### ⚙️ Требования
#### Основные:
- **Python**: 3.10+
- **Django**: 5.2+ (для модулей `framework/django/`)
- **Flask**: 3.1.2+ (для модулей `framework/flask/`)

#### Установка:
```shell
# Базовая установка
pip install hrenpack

# С дополнительными возможностями
pip install hrenpack[filetype]
pip install hrenpack[dev]
```

Полный список зависимостей доступен в [файлах requirements](https://github.com/MagIlyasDOMA/hrenpack/tree/main/requirements)

---

## [1.0.0 - 2.1.1] - Нестабильные версии
### Примечание
Данные версии были нестабильными и не рекомендуются к установке.

Используйте версию 2.1.2 или выше для production-окружений.
