# -*- coding: utf-8 -*-

import os

from kivy.app import App
from kivy.core.text import LabelBase

r = os.getcwd()

KIVY_FONTS = [{
    'name': 'Roboto',
    'fn_regular': 'material/fonts/Roboto-Regular.ttf'.format(r),
    'fn_bold': 'material/fonts/Roboto-Bold.ttf'.format(r),
    'fn_italic': 'material/fonts/Roboto-Italic.ttf'.format(r)
}]

for font in KIVY_FONTS:
    LabelBase.register(**font)

KIVY_DEFAULT_FONT = 'Roboto'


def launch_webbrowser(url):
    import webbrowser
    webbrowser.open(url)


def parse_link(*args):
    res = str(*args).split('[b]')
    res = res[1].split('[/b]')
    return res[0]


def get_rootapp():
    return App.get_running_app()
