<a id="clen"></a>
# Changelog
[Changelog на русском](#clru)

All changes in this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [3.1.1] - 2026-08-27
### ⚠️ Breaking changes
- Changed the minimum Python version to 3.11, as Python 3.10 does not support certain features.

## [3.1.0] - 2026-06-25
### ✨ Added
- Added the `hot_mode` parameter to the `hrenpack.filework.ConfigurationFile` class

### 🗑️ Removed
- Removed deprecated private API

## [3.0.0] - 2026-05-30
### ⚠️ Breaking Changes
- **Removed modules and classes**:
  - Removed the `hrenpack/boolwork.py` module and all its functions (`booltest`, `str_to_bool`, `bool_list_count`, `for_in`, `equals_all`).
  - Removed the `hrenpack/no_default.py` module. `undefined` from the `undefined-python` package is now used instead of `no_default`.
  - Removed the `PackageIsDebug` class and the `package_is_debug` function from `hrenpack/cmd.py`.
  - Removed the `AndroidPath` class and the `android_path` function from `hrenpack/cmd.py`.
  - Removed the `FileNameInfo` dataclass from `hrenpack/cmd.py`.
  - Removed the `AbstractClass` class and the `protectedmethod`/`privatemethod` functions from `hrenpack/encapsulation.py`.
  - Removed the `hrenpack/framework/kivy` module.
  - Removed the `hrenpack/framework/tkinter.py` module.
  - Removed the entire `hrenpack/custom_methods` module.
  - Removed the `hrenpack/filework/source_code.py` module.
- **API Changes**:
  - `hrenpack/__init__.py`: Removed imports of `range_plus`, `Class`, `split_list`. The `bincode_generator` function renamed its parameter `isInt` to `is_int`.
  - `hrenpack.cmd.create_file_exist`: Removed the `return_filename_and_path` parameter and `FileNameInfo`. The function now only returns a `str` (the new path).
  - `hrenpack.encapsulation`: The `getattrs` function lost its `is_tuple` parameter.
  - `hrenpack.filework.TextFile`: Removed the `comment_decorator` decorator and the `delete` method.
  - `hrenpack.filework.SRTSubtitleFile`: Removed the `extension_check` function.
  - `hrenpack.listwork`: Removed functions `_is_tuple`, `listsearch`, `antienter`, `antienter_plus`, `keys_dict_equals`, `str_to_list_one`, `in_number_series`, `in_numbers`, `dict_to_list`, `multi_pop`, `if_dict_key`, `split_list_enter/space/tab`, `ab_reverse`, `multi_reverse`, `dict_keys_values`, `remove_all`, `list_to_list`, and others. Many functions now only return a `list` (without the `is_tuple` option).
  - `hrenpack.listwork.get_from_dict`: Removed the `is_tuple` parameter.
  - `hrenpack.strwork`: Removed functions `tuple_to_str`, `zap_list`, `if_empty_str`, `search_and_edit`, `enter_fix`, `unspace_multi`.
  - `hrenpack.strwork.words_to_letters`: Removed the `is_tuple` parameter.
  - `hrenpack.type_define`: Removed the `TypeEdit` class.

### ✨ Added
- **Documentation and Comments**:
  - Added extensive documentation (docstrings) in both Russian and English for almost all functions and classes across various modules (algebra, argparse_plus, charset, classes, cmd, date_and_time_work, decorators, descriptors, emailwork, encapsulation, filework, flask, mixins, network, numwork, print_color, python, resolution, security, strwork, typings, and others).

### 🔧 Changed
- **General Code Improvements**: Major refactoring aimed at unifying style and removing deprecated constructs.
- **`hrenpack.cmd` module**: Improved path handling on Windows.
- The minimum version is now Python 3.10

### 🐛 Fixed
- **`hrenpack.cmd.get_filename`**: Fixed handling of paths with backslashes.
- **`hrenpack.cmd.get_path_without_filename`**: Fixed path building logic.
- **`hrenpack.listwork.merging_dictionaries`**: Fixed merging logic (now correctly merges *dicts).
- **`hrenpack.listwork.dict_enumerate`**: Rewritten as a generator instead of creating a list in memory.

### 🗑️ Removed
- Removed commented-out code blocks in `hrenpack/__init__.py`, `classes.py`, `cmd.py`.
- Removed the `hrenpack/resources/` folder.
- Removed unused imports in many modules.

## [3.0.0-beta.5] - 2026-04-12
### 🐛 Fixed
- Fixed a bug in `CachedProperty.is_cached` (`hrenpack/descriptors.py`) that was causing a `KeyError`.

## [3.0.0-beta.4] - 2026-04-12
### ⚠️ Breaking Changes
- **Removed `TransposedList` class** from `hrenpack.classes` module. If you used this class in your projects, your code will break. You need to find an alternative or stop using it.
- **Removed automatic Django integration loading** from `hrenpack/__init__.py`. Previously, when Django was installed, the `hrenpack.framework.django.apps` module was automatically imported. This no longer happens, and developers must explicitly import the necessary Django submodules.
- **Changed `Environment.setdefault` behavior**: Added a new `local_global` parameter, and the logic for working with local data has been changed. The method no longer uses `setdefault` for `local_data` in the old way.
- **Changed signatures of path handling functions** (`get_filename`, `get_extension`, etc.) in `hrenpack/cmd.py`. They now accept `PathLike` instead of `str`. This may break code passing other types without explicit conversion to string.
- **Removed `Category` and `MenuElement` classes** from `hrenpack/framework/django/__init__.py`. Exports of these classes have been removed, which will break code that relied on them.

### ✨ Added (New Features)
- **New module `hrenpack.emailwork`**: Added full-featured email support.
  - `ServerConfig` class for storing server configuration.
  - `MailClient` class for IMAP connections (POP and SMTP are stubbed for now).
  - `LocalFileFinder` class and nested `Message` class for parsing and searching local `.eml` files.
- **New module `hrenpack.descriptors`**: Added a set of useful class descriptors:
  - `Constant`, `ObjectConstant` (creating constants and lazy objects).
  - `TypedDescriptor`, `Boolean`, `PathLikeDescriptor` (typed attributes).
  - `CachedProperty`, `UncacheProperty` (property caching).
- **New classes in `hrenpack.classes`**:
  - `EmptyClass`: a class that returns `None` for any attribute request.
  - `NonStrictDict`: a dictionary that returns a default value (instead of raising `KeyError`) when accessing a missing key.
- **New functions in `hrenpack.classes.DictObject`**: The object now supports the dictionary interface (`__getitem__`, `__setitem__`, `__delitem__`).
- **New functions in `hrenpack.cmd`**:
  - `get_max_path_length()`: get the maximum path length for the current OS.
  - `is_path_valid()`: validate path for length, forbidden characters, and names.
- **New module `hrenpack.security`**: `HTMLSanitizer` class for cleaning HTML from dangerous tags (scripts, iframes), events (onclick), and CSS properties.
- **New module `hrenpack.python`**: Classes for lazy importing (`LazyImporter`, `LazyImportedObject`).
- **New functions in `hrenpack.framework.django`**:
  - `sanitize_html_and_mark_safe()`: for safely outputting HTML in templates.
  - `JsonResponse` class (inherits from Django's JsonResponse) with proper Cyrillic support and a `.data` property.
  - New lookup for Django ORM: `DirnameLookup` (folder path checking).
- **New utilities**:
  - `hrenpack.numwork.randcolor()`: generate random HEX color.
  - `hrenpack.strwork.strip_quotes()`: remove quotes from string edges.
  - `hrenpack.listwork.two_tuples_to_dict()`, `values_keys()`, `getitem_plus`, `setitem_plus`: extended functions for working with dictionaries and nested structures.

### 🔧 Changed
- **`Environment` class**:
  - Refactored `load` method: now uses internal `_dotenv_values` method for local loading.
  - `setdefault` method now raises a `Warning` when arguments mismatch and changed key existence checking logic.
  - Class moved within the file, removed extra blank lines.
- **`frozendict` class**: Added hashing support (`__hash__`).
- **`hrenpack.encapsulation` module**:
  - Removed `SafeInheritance` and `SafeMeta` classes (likely unused or problematic).
  - Added new functions: `getattr_strict`, `getattr_plus` (access to nested attributes/keys), `check_type` (type validation), `get_own_attributes`, `DescriptorsFinder`.
- **`TextFile` class** in `hrenpack/filework/__init__.py`:
  - Constructor signature simplified, removed `extension`/`extensions` parameters.
  - Added `create_file_if_not_exists` flag (defaults to `True`).
- **`download_file` function** in `hrenpack/network.py`: added streaming support (`stream=True`) for progress bar display.
- **`hrenpack.windows_registry` module**:
  - Completely rewritten: added `RegistryManager` class, new exceptions.
  - Removed old wrapper functions (`remove_registry_keys`, `remove_registry_values`).
- **Typing** (`hrenpack/typings.py`): Added new types: `JsonData`, `HttpMethod`, `GetterFunc`, `SetterFunc`.

### 🐛 Fixed
- **`current_timezone` function** (`hrenpack/date_and_time_work.py`): Changed signature to keyword argument `raw_data` (instead of `to_string`), making usage more explicit and clear.
- **`get_timezone_offset` function** (`hrenpack/date_and_time_work.py`): Added function to get timezone offset in hours (previously missing or broken).
- **`hrenpack/framework/django` module**: Removed "dead" and commented imports, improved `base_template_name` handling (added `None` check).

### 📦 Dependencies
- **Added new dependencies** to `requirements.txt`:
  - `typeguard` (used for type checking in descriptors).
  - `undefined-python>=1.1.0` (used for `no_default`).
  - `zoneinfo` (added import in `date_and_time_work`).

### 🗑️ Removed
- Completely removed the commented-out giant `DateTime` class from `date_and_time_work.py`.
- Removed `hrenpack/framework/django/_undb_compat.py` file (added to `.gitignore`).
- Removed old file extension checking logic from `TextFile`.
- Removed `fb2` folder from resources.

### Other
- **Encoding**: Fixed or updated file headers (e.g., `__init__.py`).
- **Structure**: `hrenpack/framework/django/db.py` module turned into `hrenpack/framework/django/db/` package with `fields` and `lookup` submodules.
- **Exceptions**: Added `convert_exception_to_str` function in `hrenpack/exceptions.py` for pretty error printing.

## [3.0.0-beta.3] - 2026-02-27
### Breaking Changes ⚠️
- Removed classes `stl`, `DictionaryWithExtendedFunctionality`, `MatrixCore`, `DataClass`, `PreEmptyDataClass`, `EmptyDataClass`, `Color`, `NoneType`, `TupleDict` in `classes.py`
- Removed functions `emptydataclass` and `dicta_to_dataclasses` in `classes.py`
- Removed the `add_comment` method and `comment_letter` attribute in the `filework.TextFile` class
- Removed methods `edit_section_if_not_none` and `edit_if_not_none` in the `filework.ConfigurationFile` class
- Removed functions `hex_to_dec`, `dec_to_hex`, `dec_to_oct`, `oct_to_dec` in `numwork.py`
- Removed the `Number` class in `numwork.py`
- Removed `dev_*` extras, except `dev`, `dev_all`, `dev_full`

### Added ✨
- Added classes `DictObject` and `Environment` in `classes.py`
- Added function `current_timezone` in `date_and_time_work.py`
- Added modules `exceptions.py`, `framework/Pyside6/mixins.py`, `framework/django/typings.py`
- Added typing `EnvDict` in `typings.py`
- Added extra [email]
- Added dependencies `pyqtcli>=0.1.1` to extra [pyside6]
- Added dependencies `argparse-typing>=0.2.0`, `pytz`, `tzlocal`

### Changed 🔧
- Added `force` argument to the `copy` method of the `filework.TextFile` class
- Optimized constant `file_dialog_templates` in `framework/Pyside6/variables.py`
- Optimized function `merging_dictionaries` in `listwork.py`
- Optimized functions `moreless` and `pifs` in `numwork.py`
- Optimized function `search_and_edit` in `strwork.py`

### Fixed 🐛
- Fixed bugs in the `ConfigurationFile` class in `filework/__init__.py`

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

## [2.5.10] - 2026-02-16
### Deprecated ⚠️
- The classes `stl`, `DictionaryWithExtendedFunctionality`, `MatrixCore`, `DataClass`, `PreEmptyDataClass`, `EmptyDataClass`, `Color`, `NoneType`, and `TupleDict` in `classes.py` are deprecated
- The functions `dicts_to_dataclasses` and `emptydataclass` in `classes.py` are deprecated
- The function `dec_to_hex` and the class `Number` in `numwork.py` are deprecated

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

## [3.1.1] - 2026-08-27
### ⚠️ Критические изменения
- Изменена минимальная версия Python на 3.11, так как Python 3.10 не поддерживает некоторые функции

## [3.1.0] - 2026-06-25
### ✨ Добавлено
- Добавлен параметр `hot_mode` в класс `hrenpack.filework.ConfigurationFile`

### 🗑️ Удалено
- Удален устаревший приватный API

## [3.0.0] - 2026-05-30
### ⚠️ Критические изменения
- **Удалены модули и классы**:
  - Удален модуль `hrenpack/boolwork.py` и все его функции (`booltest`, `str_to_bool`, `bool_list_count`, `for_in`, `equals_all`).
  - Удален модуль `hrenpack/no_default.py`. Вместо `no_default` теперь используется `undefined` из пакета `undefined-python`.
  - Удален класс `PackageIsDebug` и функция `package_is_debug` в `hrenpack/cmd.py`
  - Удален класс `AndroidPath` и функция `android_path` в `hrenpack/cmd.py`.
  - Удален класс `FileNameInfo` dataclass в `hrenpack/cmd.py`.
  - Удалены классы `AbstractClass` и функция `protectedmethod`/`privatemethod` в `hrenpack/encapsulation.py`.
  - Удален модуль `hrenpack/framework/kivy` .
  - Удален модуль `hrenpack/framework/tkinter.py`.
  - Удален модуль `hrenpack/custom_methods` (целиком).
  - Удален модуль `hrenapck/filework/source_code.py`
- **Изменения в API**:
  - `hrenpack/__init__.py`: Удалены импорты `range_plus`, `Class`, `split_list`. Функция `bincode_generator` переименовала параметр `isInt` в `is_int`.
  - `hrenpack.cmd.create_file_exist`: Удалены параметры `return_filename_and_path` и `FileNameInfo`. Функция теперь возвращает только `str` (новый путь).
  - `hrenpack.encapsulation`: Функция `getattrs` потеряла параметр `is_tuple`.
  - `hrenpack.filework.TextFile`: Удален декоратор `comment_decorator` и метод `delete`.
  - `hrenpack.filework.SRTSubtitleFile`: Удалена функция `extension_check`.
  - `hrenpack.listwork`: Удалены функции `_is_tuple`, `listsearch`, `antienter`, `antienter_plus`, `keys_dict_equals`, `str_to_list_one`, `in_number_series`, `in_numbers`, `dict_to_list`, `multi_pop`, `if_dict_key`, `split_list_enter/space/tab`, `ab_reverse`, `multi_reverse`, `dict_keys_values`, `remove_all`, `list_to_list` и другие. Многие функции теперь возвращают только `list` (без опции `is_tuple`).
  - `hrenpack.listwork.get_from_dict`: Удален параметр `is_tuple`.
  - `hrenpack.strwork`: Удалены функции `tuple_to_str`, `zap_list`, `if_empty_str`, `search_and_edit`, `enter_fix`, `unspace_multi`.
  - `hrenpack.strwork.words_to_letters`: Удален параметр `is_tuple`.
  - `hrenpack.type_define`: Удален класс `TypeEdit`.

### ✨ Добавлено
- **Документация и комментарии**:
  - Добавлена обширная документация (docstring) на русском и английском практически для всех функций и классов во всех модулях (algebra, argparse_plus, charset, classes, cmd, date_and_time_work, decorators, descriptors, emailwork, encapsulation, filework, flask, mixins, network, numwork, print_color, python, resolution, security, strwork, typings и др.).

### 🔧 Изменено
- **Общее улучшение кода**: Массовый рефакторинг с целью унификации стиля и удаления устаревших конструкций.
- **Модуль `hrenpack.cmd`**: Улучшена обработка путей на Windows.
- Минимальная версия теперь Python 3.10

### 🐛 Исправлено
- **`hrenpack.cmd.get_filename`**: Исправлена обработка путей с обратными слешами.
- **`hrenpack.cmd.get_path_without_filename`**: Исправлена логика сборки пути.
- **`hrenpack.listwork.merging_dictionaries`**: Исправлена логика слияния (теперь корректно объединяет *dicts).
- **`hrenpack.listwork.dict_enumerate`**: Переписан как генератор вместо создания списка в памяти.

### 🗑️ Удалено
- Удалены закомментированные блоки кода в `hrenpack/__init__.py`, `classes.py`, `cmd.py`.
- Удалена папка `hrenpack/resources/`.
- Удалены неиспользуемые импорты во многих модулях.

## [3.0.0-beta.5] - 2026-04-12
### 🐛 Исправлено
- Исправлен баг в `CachedProperty.is_cached` (`hrenpack/descriptors.py`), вызывавший `KeyError`.  

## [3.0.0-beta.4] - 2026-04-12
### ⚠️ Критические изменения
- **Удален класс `TransposedList`** из модуля `hrenpack.classes`. Если вы использовали этот класс в своих проектах, код сломается. Необходимо найти альтернативу или отказаться от его использования.
- **Удалена автоматическая загрузка интеграции с Django** из `hrenpack/__init__.py`. Ранее, при установленном Django, автоматически импортировался модуль `hrenpack.framework.django.apps`. Теперь этого не происходит, и разработчику нужно явно импортировать необходимые подмодули Django.
- **Изменено поведение `Environment.setdefault`**: добавлен новый параметр `local_global`, а логика работы с локальными данными изменена. Метод больше не использует `setdefault` для `local_data` в старом виде.
- **Изменены сигнатуры функций работы с путями** (`get_filename`, `get_extension` и др.) в `hrenpack/cmd.py`. Теперь они принимают `PathLike` вместо `str`. Это может сломать код, передающий другие типы без явного приведения к строке.
- **Удалены классы `Category` и `MenuElement`** из `hrenpack/framework/django/__init__.py`. Экспорты этих классов удалены, что сломает код, который на них полагался.

### ✨ Добавлено
- **Новый модуль `hrenpack.emailwork`**: Добавлена полноценная поддержка работы с электронной почтой.
  - Класс `ServerConfig` для хранения конфигурации сервера.
  - Класс `MailClient` для подключения по IMAP (POP и SMTP пока заготовлены).
  - Класс `LocalFileFinder` и вложенный класс `Message` для парсинга и поиска по локальным `.eml` файлам.
- **Новый модуль `hrenpack.descriptors`**: Добавлен набор полезных дескрипторов для классов:
  - `Constant`, `ObjectConstant` (создание констант и ленивых объектов).
  - `TypedDescriptor`, `Boolean`, `PathLikeDescriptor` (типизированные атрибуты).
  - `CachedProperty`, `UncacheProperty` (кэширование свойств).
- **Новые классы в `hrenpack.classes`**:
  - `EmptyClass`: класс, который на любой запрос атрибута возвращает `None`.
  - `NonStrictDict`: словарь, который возвращает значение по умолчанию (а не ошибку `KeyError`) при обращении к отсутствующему ключу.
- **Новые функции в `hrenpack.classes.DictObject`**: Теперь объект поддерживает интерфейс словаря (`__getitem__`, `__setitem__`, `__delitem__`).
- **Новые функции в `hrenpack.cmd`**:
  - `get_max_path_length()`: получение максимальной длины пути для текущей ОС.
  - `is_path_valid()`: валидация пути на длину, запрещенные символы и имена.
- **Новый модуль `hrenpack.security`**: Класс `HTMLSanitizer` для очистки HTML от опасных тегов (скрипты, iframe), событий (onclick) и CSS-свойств.
- **Новый модуль `hrenpack.python`**: Классы для ленивого импорта (`LazyImporter`, `LazyImportedObject`).
- **Новые функции в `hrenpack.framework.django`**:
  - `sanitize_html_and_mark_safe()`: для безопасного вывода HTML в шаблонах.
  - Класс `JsonResponse` (наследник Django JsonResponse) с корректной работой с кириллицей и свойством `.data`.
  - Новый `lookup` для Django ORM: `DirnameLookup` (проверка пути к папке).
- **Новые утилиты**:
  - `hrenpack.numwork.randcolor()`: генерация случайного HEX-цвета.
  - `hrenpack.strwork.strip_quotes()`: удаление кавычек по краям строки.
  - `hrenpack.listwork.two_tuples_to_dict()`, `values_keys()`, `getitem_plus`, `setitem_plus`: расширенные функции работы со словарями и вложенными структурами.

### 🔧 Изменено
- **Класс `Environment`**:
  - Рефакторинг метода `load`: теперь для локальной загрузки используется внутренний метод `_dotenv_values`.
  - Метод `setdefault` теперь кидает `Warning` при несоответствии аргументов и изменена логика проверки наличия ключа.
  - Класс перемещен в файле, удалены лишние пустые строки.
- **Класс `frozendict`**: Добавлена поддержка хэширования (`__hash__`).
- **Модуль `hrenpack.encapsulation`**:
  - Удалены классы `SafeInheritance` и `SafeMeta` (вероятно, не использовались или были проблемными).
  - Добавлены новые функции: `getattr_strict`, `getattr_plus` (доступ к вложенным атрибутам/ключам), `check_type` (валидация типов), `get_own_attributes`, `DescriptorsFinder`.
- **Класс `TextFile`** в `hrenpack/filework/__init__.py`:
  - Сигнатура конструктора упрощена, удалены параметры `extension`/`extensions`.
  - Добавлен флаг `create_file_if_not_exists` (по умолчанию `True`).
- **Функция `download_file`** в `hrenpack/network.py`: добавлена поддержка потоковой загрузки (`stream=True`) для отображения прогресс-бара.
- **Модуль `hrenpack.windows_registry`**:
  - Полностью переработан: добавлен класс `RegistryManager`, новые исключения.
  - Удалены старые функции-обертки (`remove_registry_keys`, `remove_registry_values`).
- **Типизация** (`hrenpack/typings.py`): Добавлены новые типы: `JsonData`, `HttpMethod`, `GetterFunc`, `SetterFunc`.

### 🐛 Исправлено
- **Функция `current_timezone`** (`hrenpack/date_and_time_work.py`): Изменена сигнатура на ключевой аргумент `raw_data` (вместо `to_string`), что делает использование более явным и понятным.
- **Функция `get_timezone_offset`** (`hrenpack/date_and_time_work.py`): Добавлена функция для получения смещения временной зоны в часах (раньше ее не было, либо она была сломана).
- **Модуль `hrenpack/framework/django`**: Удалены "мертвые" и закомментированные импорты, улучшена обработка `base_template_name` (добавлена проверка на `None`).

### 📦 Зависимости
- **Добавлены новые зависимости** в `requirements.txt`:
  - `typeguard` (используется для проверки типов в дескрипторах).
  - `undefined-python>=1.1.0` (используется для `no_default`).
  - `zoneinfo` (добавлен импорт в `date_and_time_work`).

### 🗑️ Удалено
- Полностью удален закомментированный гигантский класс `DateTime` из `date_and_time_work.py`.
- Удален файл `hrenpack/framework/django/_undb_compat.py` (добавлен в `.gitignore`).
- Удалена старая логика проверки расширений файлов из `TextFile`.
- Удалена папка `fb2` из ресурсов.

### Прочее
- **Кодировка**: Исправлены или обновлены заголовки файлов (например, `__init__.py`).
- **Структура**: Модуль `hrenpack/framework/django/db.py` превращен в пакет `hrenpack/framework/django/db/` с подмодулями `fields` и `lookup`.
- **Исключения**: В `hrenpack/exceptions.py` добавлена функция `convert_exception_to_str` для красивой распечатки ошибок.

## [3.0.0-beta.3] - 2026-02-27
### Критические изменения ⚠️
- Удалены классы `stl`, `DictionaryWithExtendedFunctionality`, `MatrixCore`, `DataClass`, `PreEmptyDataClass`, `EmptyDataClass`, `Color`, `NoneType`, `TupleDict` в `classes.py`
- Удалены функции `emptydataclass` и `dicta_to_dataclasses` в `classes.py`
- Удалены метод `add_comment` и атрибут `comment_letter` в классе `filework.TextFile`
- Удалены методы `edit_section_if_not_none` и `edit_if_not_none` в классе `filework.ConfigurationFile`
- Удалены функции `hex_to_dec`, `dec_to_hex`, `dec_to_oct`, `oct_to_dec` в `numwork.py
- Удален класс `Number` в `numwork.py
- Удалены `dev_*` экстра, кроме `dev`, `dev_all`, `dev_full`

### Добавлено ✨
- Добавлены классы `DictObject` и `Environment` в `classes.py`
- Добавлена функция `current_timezone` в `date_and_time_work.py`
- Добавлены модули `exceptions.py`, `framework/Pyside6/mixins.py`, `framework/django/typings.py`
- Добавлен typing `EnvDict` в `typings.py`
- Добавлен экстра [email]
- Добавлены зависимости `pyqtcli>=0.1.1` в экстра [pyside6]
- Добавлены зависимости `argparse-typing>=0.2.0`, `pytz`, `tzlocal`

### Изменено 🔧
- Добавлен аргумент `force` в метод `copy` класса `filework.TextFile`
- Оптимизирована константа `file_dialog_templates` в `framework/Pyside6/variables.py`
- Оптимизирована функция `merging_dictionaries` в `listwork.py`
- Оптимизированы функции `moreless` и `pifs` в `numwork.py`
- Оптимизирована функция `search_and_edit` в `strwork.py`

### Исправлено 🐛
- Исправлены баги в классе `ConfigurationFile` в `filework/__init__.py`


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

## [2.5.10] - 2026-02-16
### Устарело ⚠️
- Классы `stl`, `DictionaryWithExtendedFunctionality`, `MatrixCore`, `DataClass` `PreEmptyDataClass`, `EmptyDataClass`, `Color`, `NoneType` и `TupleDict` в `classes.py` объявлены устаревшими
- Функции `dicts_to_dataclasses` и `emptydataclass` в `classes.py` объявлены устаревшими
- Функция `dec_to_hex` и класс `Number` в `numwork.py` объявлены устаревшими

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
