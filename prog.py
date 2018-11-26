# -*- coding: utf-8 -*-

import os
import sys

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.utils import platform

from resources.primescreen import PrimeScreen
from resources import programdata as core
from resources.progclasses.slide_panel import SlidePanel
from resources.navmenu import NavMenu
from resources.progclasses.showlicense import ShowLicense
from resources.progclasses.mypopup import MyPopup
from resources.projsettings import ProjSettings
from resources.progclasses.appclass import launch_webbrowser
from resources.progclasses.showsections import ShowSections


class Prog(App):
    prime_screen = ObjectProperty(None)
    '''`prime_screen` is a class `resources.primescreen.PrimeScreen`.'''

    settings_cls = ProjSettings

    def __init__(self, **kwargs):
        super(Prog, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.events_program)

        self.core = core
        self.load_all_kvfiles()
        self.name_program = core.string_lang_title
        self.slide_panel = SlidePanel(events_callback=self.events_program)
        self.open_dialog = False  # открыто диалоговое окно
        self.cats = []

    def build(self):
        self.title = self.name_program
        self.icon = 'material/images/logo.png'
        self.use_kivy_settings = False
        self.load_config().read('{}/prog.ini'.format(self.directory))

        self.prime_screen = PrimeScreen(
            title_previous=self.name_program,
            events_callback=self.events_program)

        navpanel = NavMenu(
            items=core.dict_navigations_items,
            events_callback=self.events_program)

        self.slide_panel.add_widget(navpanel)
        self.slide_panel.add_widget(self.prime_screen)
        return self.slide_panel

    def build_config(self, config):
        config.setdefaults("General", {"language": u"Русский"})
        config.setdefaults("Clear_section", {
            "clear_key": ""})

    def build_settings(self, settings):
        with open('material/profiles/general.json',
                  'r') as settings_json:
            settings.add_json_panel(
                core.string_lang_settings + ' ' + self.name_program,
                self.config,
                data=settings_json.read().format(
                    language=core.string_lang_setting_language,
                    title=core.string_lang_setting_language_title,
                    desc=core.string_lang_setting_language_desc,
                    russian=core.string_lang_setting_language_russian,
                    english=core.string_lang_setting_language_english,
                    additional_options=core.string_additional_options,
                    clear_cache=core.string_clear_cache,
                    desc_clear_cache=core.string_clear_cache_program))

    def get_application_config(self,
                               defaultpath='{}/prog.ini'.format(core.p)):
        if platform == 'android':
            defaultpath = '{}/prog.ini'.format(self.directory)
        elif platform == 'ios':
            defaultpath = '{}/prog.ini'.format(self.directory)
        else:
            return super(Prog, self).get_application_config(
                defaultpath='{}/prog.ini'.format(self.directory))

    def events_program(self, *args):
        """Обработка событий программы."""

        if len(args) == 2:  # нажата ссылка
            event = args[1].encode("utf-8")
        else:   # нажата кнопка программы
            try:
                _args = args[0]
                event = _args if isinstance(_args, str) else str(_args) if \
                    isinstance(_args, dict) else _args.id
            except AttributeError:  # нажата кнопка девайса
                event = args[1]

        for a in core.dict_cats.items():
            self.cats.append(a[1])

        if event == "slide_panel" or \
                self.slide_panel.state == "open" and event in (1001, 27):
            self.slide_panel.toggle_state()
        elif event == core.string_lang_to_website:
            launch_webbrowser("https://pcompstart.com")
        elif event == core.string_lang_exit_key:
            self.exit_program()
        elif event in (1001, 27):
            self.back_screen(event)
        elif event == core.string_lang_license:
            ShowLicense().show_license()
        elif event == core.string_lang_settings:
            self.open_settings()
        elif event == core.string_lang_about:
            self.view_about()
        elif event in self.cats:
            for res in core.dict_cats.items():
                if event in res:
                    res = res[0]
                    self.show_screens(res)
        return True

    def show_screens(self, res):
        if res in self.prime_screen.ids.screen_manager.screen_names:
            self.prime_screen.ids.screen_manager.current = res
        else:
            self.prime_screen.ids.screen_manager.add_widget(
                ShowSections(name=res))
            self.prime_screen.ids.screen_manager.current = res

    def back_screen(self, event):
        """Менеджер экранов. Нажата BackKey на главном экране."""
        if self.prime_screen.searchitem.flot_txt.x < Window.width \
                and event in (1001, 27):
            self.prime_screen.searchitem.animfunc()
            return None

        if self.prime_screen.ids.screen_manager.current == "primescreen":
            if event in (1001, 27):
                self.exit_program()
            return
        else:
            self.prime_screen.ids.screen_manager.current = \
                self.prime_screen.ids.screen_manager.previous()
            self.prime_screen.ids.screen_manager.current = 'primescreen'

    def load_all_kvfiles(self):
        directory_kv_files = 'resources/kv/'
        for kv_files in os.listdir(directory_kv_files):
            with open(directory_kv_files + kv_files, 'r') as f:
                Builder.load_string(f.read())

    def exit_program(self, *args):
        def dismiss(*args):
            self.open_dialog = False

        def answer_callback(answer):
            if answer == core.string_lang_yes:
                sys.exit(0)
            dismiss()

        if not self.open_dialog:
            MyPopup(answer_callback=answer_callback, on_dismiss=dismiss,
                    title=self.name_program).show(
                text=core.string_lang_exit,
                text_button_ok=core.string_lang_yes,
                text_button_no=core.string_lang_no)
            self.open_dialog = True

    def on_start(self):
        pass

    def on_pause(self):
        """Ставит приложение на 'паузу' при выхоже из него.
        В противном случае запускает программу по заново"""
        return True

    def on_resume(self):
        pass

    def on_stop(self):
        pass

    def on_config_change(self, config, section, key, value):
        """Вызывается при выборе одного из пункта настроек программы."""

        if key == 'language':
            if not os.path.exists(
                    '{}/material/languages/{}.txt'.format(
                        self.directory, core.select_locale[value])):
                MyPopup(title=self.name_program).show(
                    text=core.string_lang_not_locale.format(
                        core.select_locale[value]),
                    text_button_no=core.strin_lang_on_close)
                config.set(section, key, core.old_language)
                config.write()
                self.close_settings()

    def view_about(self):
        MyPopup(base_text_color=[0, 0, 0, 1],
                base_font_size='14sp',
                size_height_window='400dp',
                mypopup_label_height='320dp',
                title=core.string_lang_title
                ).show(text=core.string_lang_about_text,
                       text_button_cancel=core.strin_lang_on_close)
