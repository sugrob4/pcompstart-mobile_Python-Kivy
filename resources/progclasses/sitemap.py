import re

from kivy.uix.screenmanager import Screen
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivy.properties import ObjectProperty, ListProperty

from resources.progclasses.loadback import LoadBack
from resources.scrollwid import ScrollWid
from resources.mymadenbutton import MyMadenButton
from resources.progclasses.appclass import launch_webbrowser, parse_link

from resources.progclasses.bugreporter import BugReporter


class SiteMap(Screen):
    scrollwid = ObjectProperty(None)

    loadback = ObjectProperty(None)

    geturi = ListProperty()

    def __init__(self, **kwargs):
        super(SiteMap, self).__init__(**kwargs)
        self.name = 'sitemap'

        self.add_widget(LoadBack())
        Clock.schedule_once(self.get_response, 0.5)

        self.scrollwid = ScrollWid(size_hint_y=1)

    def get_response(self, *args):
        zag = {'Content-type': 'application/x-www-form-urlencoded',
               'Accept': '*/*'}
        req = UrlRequest(
            'https://pcompstart.com/sitemap',
            on_error=self.getresponse_error,
            req_headers=zag)
        while not req.is_finished:
            req.wait(0)
        self.clear_widgets()
        res = req.result.split(
            'id="sitemap"')[1].split('<link rel="stylesheet"')[0]
        for dat in re.findall('<[^>]*>(.*)</[^>]*>', res)[2:]:
            dat = str(dat.encode("utf-8")).replace(
                '<a href="', 'https:').replace(
                "</a>", "").split('">')
            self.geturi.extend([dat])
            self.scrollwid.layout.add_widget(MyMadenButton(
                text="[size=13sp][color=#0000ff][b]" + dat[1] +
                     "[/b][/color][/size]",
                radius_button=[0],
                height_but='60dp',
                shad_but=True,
                events_callback=self.get_uri))
        self.add_widget(self.scrollwid)

    def getresponse_error(self, req, error):
        return BugReporter(txt_report=str(error))

    def get_uri(self, *args):
        a = str(args[0]).split("[b]")[1].split("[/b]")[0]
        for i in self.geturi:
            if a == i[1]:
                launch_webbrowser(i[0].split('"')[0])
