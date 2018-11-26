# -*- coding: utf-8 -*-

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (StringProperty, ObjectProperty,
                             ListProperty, BooleanProperty, NumericProperty)
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import get_color_from_hex


class MyMadenButton(BoxLayout, Button):
    icon = StringProperty('')
    text = StringProperty('')
    button_color = get_color_from_hex('#f4f4f8')
    button_color_down = get_color_from_hex('#007fa9')
    text_color = get_color_from_hex('#2d525e')
    radius_button = ListProperty([dp(5)])
    shad_but = BooleanProperty(False)
    height_but = NumericProperty('60dp')
    size_x_image = NumericProperty(.6)
    events_callback = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyMadenButton, self).__init__(**kwargs)
        self.bind(size=self.setter('text_size'))
        if self.icon == "":
            self.remove_widget(self.ids.btn_img)

    def press(self, instance, id):
        """ :param instance: <kivy.graphics.instructions.Canvas> """
        instance.children[9].rgba = self.button_color_down
        Clock.schedule_once(lambda *args: self.release(instance, id), .1)

    def release(self, instance, id):
        """ :param instance: <kivy.graphics.instructions.Canvas> """
        instance.children[9].rgba = self.button_color
        self.events_callback(id)
