# -*- coding: utf-8 -*-

import os

from kivy.uix.popup import Popup
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import (ObjectProperty, StringProperty, DictProperty,
                             ListProperty, OptionProperty, NumericProperty)
from kivy.clock import Clock

from .appclass import KIVY_DEFAULT_FONT

root = os.path.split(__file__)[0]
root = root if root != '' else os.getcwd()


def _pass(*args):
    pass


class MyPopup(Popup):
    events_callback = ObjectProperty(_pass)
    '''Пользовательская функция обработки событий окна.'''

    answer_callback = ObjectProperty(_pass)
    '''Встроеная функция обработки событий окна.'''

    progress_callback = ObjectProperty(None)
    '''Функция, вызываемая при старте окна прогресса.'''

    background = StringProperty(
        'atlas://material/images/mypopup/mypopup/decorator'.format(root))
    '''Декоратор окна.'''

    separator_color = ListProperty([0.10, 0.24, 0.29, .8])
    '''Цвет линии-разделителя окна.'''

    title_align = OptionProperty('center')
    '''Выравнивание заголовка окна.'''

    title_color = ListProperty([0.06, 0.20, 0.25, 1.0])
    '''Цвет заголовка окна.'''

    title_size = NumericProperty('15sp')
    '''Размер заголовка окна.'''

    background_image_buttons = DictProperty({
        0: 'atlas://material/images/mypopup/mypopup/button_ok'.format(root),
        1: 'atlas://material/images/mypopup/mypopup/button_no'.format(root),
        2: 'atlas://material/images/mypopup/mypopup/button_cancel'.format(root)
    })
    '''Обычные кнопки, в неактивном состоянии, `No Active`.'''

    background_image_shadows = DictProperty({
        0: 'atlas://material/images/mypopup/mypopup/button_ok_shadow'.format(root),
        1: 'atlas://material/images/mypopup/mypopup/button_no_shadow'.format(root),
        2: 'atlas://material/images/mypopup/mypopup/button_cancel_shadow'.format(root)
    })
    '''Кнопки в нажатом состоянии, `Active`.'''

    base_font_size = NumericProperty('17sp')
    '''Размер шрифта окна.'''

    base_font_name = StringProperty(KIVY_DEFAULT_FONT)
    '''Имя шрифта окна.'''

    base_text_color = ListProperty([0.10, 0.24, 0.29, 1.0])
    '''Цвет текста окна программы.'''

    size_height_window = NumericProperty('220dp')
    '''Высота окна MyPopup, по умолчанию равна `220dp`'''

    mypopup_label_height = NumericProperty('120dp')
    '''Высота текста окна MyPopup, по умолчанию равна `120dp`'''

    def __init__(self, **kwargs):
        super(MyPopup, self).__init__(**kwargs)
        self.box_buttons_select = BoxLayout(
            size_hint_y=None, height=dp(40), spacing=dp(20))
        self.box_root = self.ids.box_root
        self.box_content = self.ids.box_content

        self.message = None

    def show(self, text='Text message', text_button_ok=None,
             text_button_no=None, text_button_cancel=None,
             auto_dismiss=True):

        def create_button(name_button, background_image_normal,
                          background_image_down):
            self.box_buttons_select.add_widget(Button(
                id=name_button, text=name_button,
                background_normal=background_image_normal,
                background_down=background_image_down,
                font_size=sp(17),
                on_release=self._answer_user
            ))
            return True

        for i, name_button in enumerate([
                text_button_ok, text_button_no, text_button_cancel]):
            if name_button:
                create_button(
                    name_button,
                    self.background_image_buttons[i],
                    self.background_image_shadows[i])

        self.message = Label(
            text=text, size_hint_y=None, markup=True,
            height=self.mypopup_label_height,
            text_size=(self.width, None),
            halign='center',
            padding_x=dp(10),
            on_ref_press=self.answer_callback,
            font_size=self.base_font_size,
            font_name=self.base_font_name,
            color=self.base_text_color)
        self.box_content.add_widget(self.message)

        # self.box_root.add_widget(Widget())
        self.box_root.add_widget(self.box_buttons_select)

        self.auto_dismiss = auto_dismiss
        self.open()

        if callable(self.progress_callback):
            Clock.schedule_once(self.progress_callback, 0)
        return self

    def _answer_user(self, *args):
        """Вызывается при нажатии управляющих кнопок."""
        self.answer_callback(args[0].text)
        self.dismiss()
