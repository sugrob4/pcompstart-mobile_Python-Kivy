# -*- coding: utf-8 -*-

import os
import shutil

from kivy.uix.settings import InterfaceWithNoMenu, Settings, SettingOptions
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.metrics import dp, sp

from resources import programdata as c
from resources.progclasses.appclass import KIVY_DEFAULT_FONT, get_rootapp

rp = os.path.split(os.path.dirname(__file__))[0]


class SetGrid(GridLayout):
    def __init__(self, **kwargs):
        super(SetGrid, self).__init__(**kwargs)
        self.cols = 1
        self.size_hint_y = None
        self.height = dp(55)


class SetButt(Button):

    bn = StringProperty(
        'atlas://material/images/mypopup/mypopup/button_ok'.format(rp))
    '''Фон для кнопки `background_normal`.'''

    bd = StringProperty(
        'atlas://material/images/mypopup/mypopup/button_ok_shadow'.format(rp))
    '''Фон для кнопки `background_down`.'''

    def __init__(self, **kwargs):
        super(SetButt, self).__init__(**kwargs)
        self.font_name = KIVY_DEFAULT_FONT
        self.font_size = sp(16)
        self.background_normal = self.bn
        self.background_down = self.bd
        self.size_hint_y = None
        self.height = dp(45)


class ProjSettings(Settings):
    interface_cls = ObjectProperty(InterfaceWithNoMenu)

    popup = ObjectProperty(None, allownone=True)

    bg = StringProperty(
        'atlas://material/images/mypopup/mypopup/decorator'.format(rp))
    '''Фон окна `Popup`'''

    def __init__(self, **kwargs):
        super(ProjSettings, self).__init__(**kwargs)

        f = AnchorLayout(size_hint=(None, None), size=(self.x, self.y),
                         anchor_x='right', pos_hint={'y': .2},
                         padding=(dp(25), 0))
        f.add_widget(SetButt(
            text=c.string_lang_close_settings,
            size_hint=(None, None),
            size=(Window.width - dp(50), dp(40)),
            on_release=self.on_close))
        self.add_widget(f)

        SettingOptions._create_popup = self.options_popup

    def on_close(self, *args):
        self.dispatch('on_close')

    def options_popup(self, instance):
        def _set_option(button_instance):
            instance.value = button_instance.text
            popup.dismiss()

        # create the popup
        content = BoxLayout(orientation='vertical')
        self.popup = popup = Popup(
            content=content, title=c.string_lang_setting_language_title,
            size_hint=(None, None), size=(0.9 * Window.width, dp(300)),
            background=self.bg,
            title_color=[0.06, 0.20, 0.25, 1.0],
            title_align='center',
            separator_color=[0.10, 0.24, 0.29, .8])
        popup.height = len(instance.options) * dp(40) + dp(150)

        if 'but_clear' in instance.options:
            self.popup.title = c.string_want_clear_cache
            self.popup.separator_color = [1, 1, 1, 1]
            self.popup.title_size = sp(15)
            but = SetButt(
                text=c.string_lang_clean,
                on_release=self.remove_urlfiles)
            grid = SetGrid()
            grid.add_widget(but)
            content.add_widget(grid)
        else:
            # add all the options
            uid = str(self.uid)
            setbutt = SetButt()
            for option in instance.options:
                state = 'down' if option == instance.value else 'normal'
                btn = ToggleButton(
                    text=option, state=state, group=uid,
                    size_hint_y=None, height=dp(45),
                    font_name=KIVY_DEFAULT_FONT,
                    font_size=sp(16),
                    background_normal=setbutt.bn,
                    background_down=setbutt.bd, on_release=_set_option)
                grid = SetGrid()
                grid.add_widget(btn)
                content.add_widget(grid)

        # finally, add a cancel button to return on the previous panel
        btn = SetButt(
            text=c.string_lang_cancel,
            on_release=popup.dismiss)
        content.add_widget(btn)
        popup.open()

    def remove_urlfiles(self, *args):
        if os.path.exists("%s/urlfiles" % rp):
            shutil.rmtree("%s/urlfiles" % rp)
        self.popup.dismiss()
        if get_rootapp().prime_screen.ids.screen_manager.current != 'primescreen':
            get_rootapp().prime_screen.ids.screen_manager.current = 'primescreen'
            get_rootapp().prime_screen.ids.screen_manager.remove_widget(
                get_rootapp().prime_screen.ids.screen_manager.get_screen(
                    get_rootapp().prime_screen.ids.screen_manager.previous()))
