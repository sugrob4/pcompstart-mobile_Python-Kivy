from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, NumericProperty
from kivy.lang import Builder

Builder.load_string('''
#: import ScrollEffect kivy.effects.scroll.ScrollEffect

<ScrollWid>:
    layout: layout
    id: e_scroll
    bar_width: dp(5)
    size_hint_y: None
    effect_cls: ScrollEffect
    height: root.doscroll_height()
    GridLayout:
        id: layout
        cols: 1
        spacing: dp(12)
        padding: dp(12), dp(12)
        size_hint_y: None
        height: max(e_scroll.height, self.minimum_height)
''')


class ScrollWid(ScrollView):

    layout = ObjectProperty(None)

    scrollheight = NumericProperty(0)

    def __init__(self, **kwargs):
        super(ScrollWid, self).__init__(**kwargs)

    def doscroll_height(self):
        if self.scrollheight == 0:
            return self.height
        else:
            return self.scrollheight
