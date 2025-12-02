# Hrenpack v2.2.2
# Copyright (c) 2024-2025, Маг Ильяс DOMA (MagIlyasDOMA)
# Licensed under MIT (https://github.com/MagIlyasDOMA/hrenpack/blob/main/LICENSE)

from hrenpack.classes import DataClass

file_dialog_templates = DataClass(images="Изображения (*.jpg *.jpeg *.png *.tif *.tiff)", all="Все файлы (*)",
                                  txt="Текстовый документ (*.txt)", srt="Субтитры SRT (*.srt)")