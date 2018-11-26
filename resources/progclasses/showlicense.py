# -*- coding: utf-8 -*-

import os
import webbrowser
import codecs

from kivy.clock import Clock
from kivy.uix.rst import RstDocument
from kivy.uix.modalview import ModalView
from kivy.effects.scroll import ScrollEffect
from kivy.core.window import Window
from kivy.metrics import dp

from .mypopup import MyPopup
from resources import programdata as basis


class ShowLicense(object):
    def show_license(self, *args):
        def choice_language_license(*args):
            if len(args) > 1:  # выбраны ссылки в тексте
                click_link = args[1]
                webbrowser.open(click_link)
            else:
                on_language = args[0]
                progress = MyPopup(
                    title=basis.string_lang_title).show(
                    text=basis.string_lang_wait)
                Clock.schedule_once(
                    lambda *args: show_license(progress, on_language), 0.3)

        def show_license(progress, on_language):
            path_to_license = '{}/license/license_{}.rst'.format(
                os.getcwd(), basis.dict_language[on_language])

            if not os.path.exists(path_to_license):
                MyPopup(title=basis.string_lang_title).show(
                    text=basis.string_lang_not_license,
                    text_button_ok=basis.string_lang_yes)
                progress.dismiss()

            text_license = codecs.open(path_to_license, 'r', 'utf-8').read()
            view = ModalView(
                size_hint=(None, None),
                size=(Window.width - dp(30), Window.height - dp(70)))
            view.add_widget(RstDocument(
                text=text_license, effect_cls=ScrollEffect))
            view.open()
            progress.dismiss()

        MyPopup(
            title=basis.string_lang_title,
            answer_callback=choice_language_license).show(
            text=basis.string_lang_prev_license,
            text_button_ok=basis.string_lang_on_russian,
            text_button_no=basis.string_lang_on_english)
