# -*- coding: utf-8 -*-

from os import path

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.clock import Clock

from .databasemanager import DataBaseMnager
from resources.mymadenbutton import MyMadenButton
from resources.scrollwid import ScrollWid
from resources.progclasses.appclass import parse_link, launch_webbrowser, get_rootapp
from resources.progclasses.loadback import LoadBack

from resources import programdata as core


class ScreenWin(Screen):
    """
    class ScreenWin поиск и вывод контента на экран.
    """

    pasttext = StringProperty("")

    dbman = ObjectProperty(None)

    scrollwid = ObjectProperty(None)
    '''ScrollView + GridLayout'''

    dat = ListProperty()

    def __init__(self, **kwargs):
        super(ScreenWin, self).__init__(**kwargs)
        self.name = "screenwin"
        self.scrollwid = ScrollWid(size_hint_y=1)
        self.resp = False
        if not path.exists("urlfiles/pcomp.db"):
            self.resp = True
            self.add_widget(LoadBack(
                load_text=core.string_not_data,
                load_font_size="19sp"))
            Clock.schedule_once(self.callback, 7)
        elif len(str(self.pasttext).decode("utf-8")) < 3:
            self.resp = True
            self.add_widget(LoadBack(
                load_text=core.string_3_characters))
            Clock.schedule_once(self.callback, 4)
        else:
            self.dbman = DataBaseMnager("urlfiles/pcomp.db")
            connect = self.dbman.query(
                "select cat_title, cat_imglink, cat_text, link_product "
                " from categories ").fetchall()
            self.dat = connect
            for conc in connect:
                if str(self.pasttext).decode("utf-8").lower() in \
                        str(conc[0]).decode("utf-8").lower():
                    file_img = conc[1].split('/')[-1]
                    self.scrollwid.layout.add_widget(MyMadenButton(
                        icon='urlfiles/urlimg/{}'.format(file_img),
                        size_x_image=.25,
                        text="[size=13sp][color=#0000ff][b]" + conc[0] +
                             "[/b][/color][/size]" + "\n" +
                             "[size=12sp][color=#000000]" + conc[2] + "[/color][/size]",
                        radius_button=[0],
                        height_but='115dp',
                        shad_but=True, events_callback=self.get_link))
                    self.resp = True
            self.dbman.__del__()

        if self.resp is False:
            self.add_widget(LoadBack(
                    load_text=core.string_nothing_for_request))
            Clock.schedule_once(self.callback, 4)
        self.add_widget(self.scrollwid)

    def callback(self, *args):
        if get_rootapp().prime_screen.ids.screen_manager.current == self.name:
            get_rootapp().prime_screen.ids.screen_manager.current = 'primescreen'
        else:
            pass

    def get_link(self, args):
        for lnk in self.dat:
            if parse_link(args) in lnk:
                launch_webbrowser(lnk[3])
