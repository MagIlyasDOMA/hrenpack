# Hrenpack v2.1.2
# Copyright (c) 2024-2025, Маг Ильяс DOMA (MagIlyasDOMA)
# Licensed under MIT (https://github.com/MagIlyasDOMA/hrenpack/blob/main/LICENSE)

from kivy.uix.scrollview import ScrollView as KivyScrollView


class ScrollView(KivyScrollView):
    def __init__(self, parent=None, child=None, do_scroll_x: bool = False, **kwargs):
        super().__init__(do_scroll_x=do_scroll_x, **kwargs)
        if parent is not None:
            parent.add_widget(self)
        if child is not None:
            self.add_widget(child)
