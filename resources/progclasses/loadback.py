# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.core.window import Window

from resources import programdata


class LoadBack(BoxLayout):

    load_text = StringProperty(programdata.string_lang_wait)

    load_font_size = NumericProperty("21sp")

    def __init__(self, **kwargs):
        super(LoadBack, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.pos_hint = {"top": .5}

        with self.canvas:
            Color(rgb=(1, 1, 1))
            Rectangle(size=Window.size, pos=self.pos)

        self.add_widget(Image(
            source='material/images/loadpcomp.png',
            allow_stretch=True, keep_ratio=True,
            size_hint=(None, None), size=("230dp", "130dp"),
            pos_hint={"x": .17}))

        f = FloatLayout(size_hint_y=None)
        f.add_widget(Label(
            text=self.load_text, color=(0.05, 0.32, 0.38, 1),
            size_text=(self.width, None),
            size_hint_y=None, pos=(0, dp(130)),
            bold=True, font_size=self.load_font_size, valign="bottom"))
        self.add_widget(f)
