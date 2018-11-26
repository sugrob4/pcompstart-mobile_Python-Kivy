#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.clipboard import Clipboard

from resources import programdata as core

root = os.path.split(os.path.abspath(sys.argv[0]))[0]

Builder.load_string('''
#: import launch_webbrowser appclass.launch_webbrowser

<BugReporter>:
    txt_traceback: txt_traceback
    canvas:
        Color:
            rgb: 0, 0.20, 0.24
        Rectangle:
            pos: self.pos
            size: root.size
    Image:
        source: root.icon_background
        size_hint: None, None
        size: dp(100), dp(150)
        pos_hint: {'x': .35, 'y': .4}
        opacity: 0.4
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        Label:
            id: title
            text: root.label_info_for_user
            text_size: self.size
            font_size: '16sp'
            halign: 'center'
            valign: 'top'
            size_hint_y: .1
        Label:
            id: subtitle
            text: root.info_for_user
            text_size: self.size
            font_size: '13sp'
            halign: 'center'
            valign: 'top'
            size_hint_y: None
        ScrollView:
            id: e_scroll
            bar_width: 10
            scroll_y: 0
            TextInput:
                id: txt_traceback
                size_hint_y: None
                height: max(e_scroll.height, self.minimum_height)
                font_size: '12sp'
                text_size: self.width, None
                background_color: 1, 1, 1, 0.07
                # text: ""
                text: root.txt_report
                foreground_color: 1, 1, 1, 1
                readonly: True
        BoxLayout:
            size_hint: 1, None
            padding: 5, 5
            height: '50dp'
            spacing: 5
            Button:
                text: 'Copy Bug'
                valign: 'middle'
                on_press: root.on_clipboard()
            Button:
                text: 'To Website'
                valign: 'middle'
                on_press: launch_webbrowser('https://pcompstart.com/contacts')
            Button:
                text: 'Close'
                valign: 'middle'
                on_press: root.on_close()
''')


class BugReporter(FloatLayout):
    txt_traceback = ObjectProperty(None)
    '''Текстовое поле для показа отслеживаемого сообщения.'''

    txt_report = StringProperty("")

    label_info_for_user = StringProperty(core.string_lang_bugreporter)

    info_for_user = StringProperty(core.string_lang_bugreporter1)

    icon_background = StringProperty(
        '{}/material/images/logo.png'.format(root)
    )

    def __init__(self, **kwargs):
        super(BugReporter, self).__init__(**kwargs)
        # self.txt_traceback.text = self.txt_report

    def on_clipboard(self, *args):
        """Функция кнопки, для копирования в буфер обмена."""
        Clipboard.copy(data=self.ids.txt_traceback.text)

    def on_close(self, *args):
        """Функция кнопки, для закрытия окна."""
        App.get_running_app().stop()
