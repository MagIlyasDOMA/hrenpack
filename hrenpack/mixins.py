# Hrenpack v2.0.0
# Copyright (c) 2024-2025, Маг Ильяс DOMA (MagIlyasDOMA)
# Licensed under MIT (https://github.com/MagIlyasDOMA/hrenpack/blob/main/LICENSE)

class SlotsReadMixin:
    def __getitem__(self, item):
        if item in self.__slots__:
            return getattr(self, item)
        raise KeyError(item)


class SlotsMixin(SlotsReadMixin):
    def __setitem__(self, key, value):
        setattr(self, key, value)
