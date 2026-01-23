# Changelog

Все изменения в этом проекте документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/),
и проект придерживается [Семантического Версионирования](https://semver.org/).

## [Невыпущенное] / [В разработке]

### Планируется
- Миграция на Python 3.13+
- Удаление устаревших функций `Fand`, `For`, `switch_For`, `get_mime_type`

---

## [2.5.2] - 2026-01-23

### Устарело ⚠️
- Функции `Fand`, `For` и `switch_For` в `boolwork.py` объявлены устаревшими
- Функция `null` в `__init__.py` объявлена устаревшей

### Исправлено 🐛
- Оптимизирован декоратор `non_print` в `decorators.py`

---

## [2.5.1] - 2026-01-22

### Изменено 🔧
- Убраны лишние переносы строки в исходных файлах для улучшения читаемости

### Зависимости 📦
- Обновлена версия `pip-setuptools` с `>=1.1.3` на `>=1.1.4` в dev_requirements

---

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

---

## [2.4.1] - 2026-01-16

### Добавлено ✨
- Новый модуль `i18n.py` для интернационализации и локализации

### Зависимости 📦
- Добавлены `python-gettext~5.0` и `pathlike-typing` в базовые требования

---

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

---

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

---

## [2.2.2] - 2025-12-02

### Исправлено 🐛
- Убран лишний реверс списка в `framework/flask/forms/mixins.py` в методе `as_p` класса `DjangoStyleFormMixin`

---

## [2.2.1] - 2025-12-02

### Исправлено 🐛
- Исправлен баг, вызывавший ошибку в `listwork.py`

---

## [2.2.0] - 2025-12-02

### Добавлено ✨
- Добавлен пакет `flask` в `framework` для интеграции с Flask

---

## [2.1.2] - 2025-11-28 🎉

### Добавлено ✨
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

