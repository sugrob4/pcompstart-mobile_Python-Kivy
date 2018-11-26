# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window

from .mymadenbutton import MyMadenButton
from .scrollwid import ScrollWid
from resources.programdata import dict_cats
from resources.progclasses.searchitem import SearchItem
from resources.progclasses.screenwin import ScreenWin
from resources.progclasses.sitemap import SiteMap


class PrimeScreen(BoxLayout):
    events_callback = ObjectProperty(None)
    # Функция обработки сигналов экрана.

    title_previous = StringProperty("")
    # Заголовок в ActionBar

    searchitem = ObjectProperty()
    '''`class` resources.progclasses.searchitem import SearchItem;
    класс поля поиска
    '''

    screenwin = ObjectProperty(None)
    '''Экран поля поиска, в него передаётся искомое слово 
    через переменную `pasttext`
    '''

    scrollwid = ObjectProperty(None)
    '''ScrollView + GridLayout'''

    def __init__(self, **kwargs):
        super(PrimeScreen, self).__init__(**kwargs)
        self.scrollwid = ScrollWid(scrollheight=Window.height // 1.43)

        # Список категорий
        for name_cat in dict_cats.fromkeys(dict_cats.items()):
            self.scrollwid.layout.add_widget(MyMadenButton(
                text=name_cat[1],
                icon="atlas://material/images/cat_img/cat_img_atlas/%s" % name_cat[0],
                size_x_image=.6,
                events_callback=self.events_callback))

        self.ids.pr_scr.add_widget(self.scrollwid)
        self.searchitem = SearchItem()
        self.add_widget(self.searchitem)
        self.searchitem.bind(evcall=self.on_evcall)

    def on_evcall(self, *args):
        self.screenwin = ScreenWin(pasttext=args[1][1].encode("utf-8"))
        if self.screenwin.name in self.ids.screen_manager.screen_names:
            if self.ids.screen_manager.current == self.screenwin.name:
                self.ids.screen_manager.switch_to(self.screenwin)
            else:
                self.ids.screen_manager.remove_widget(
                    self.ids.screen_manager.get_screen(self.screenwin.name))
                self.ids.screen_manager.add_widget(self.screenwin)
                self.ids.screen_manager.current = self.screenwin.name
        else:
            self.ids.screen_manager.add_widget(self.screenwin)
            self.ids.screen_manager.current = self.screenwin.name

    def open_sitemap(self, *args):
        if 'sitemap' in self.ids.screen_manager.screen_names:
            self.ids.screen_manager.current = 'sitemap'
        else:
            self.ids.screen_manager.add_widget(SiteMap())
            self.ids.screen_manager.current = 'sitemap'
