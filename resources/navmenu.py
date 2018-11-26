# -*- coding: utf-8 -*-

from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, ListProperty
from kivy.metrics import dp

from resources.mymadenbutton import MyMadenButton


class NavMenu(GridLayout):
    events_callback = ObjectProperty(None)
    """Функция обработки событий."""
    items = ListProperty([])
    """Список названий опций, выдвигающегося меню."""

    def __init__(self, **kwargs):
        super(NavMenu, self).__init__(cols=1, spacing=dp(1), **kwargs)

        for list_item_menu in self.items:
            self.add_widget(
                MyMadenButton(
                    text=list_item_menu[0],
                    icon=list_item_menu[1],
                    size_x_image=.28,
                    radius_button=[0],
                    shad_but=True,
                    events_callback=self.events_callback))
