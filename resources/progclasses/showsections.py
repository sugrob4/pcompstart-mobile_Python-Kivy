# -*- coding: utf-8 -*-

import os
import re

from urllib2 import HTTPError

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty, ListProperty, \
    DictProperty
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest

from resources.progclasses.databasemanager import DataBaseMnager
from resources.mymadenbutton import MyMadenButton
from resources.progclasses.loadback import LoadBack
from resources.scrollwid import ScrollWid
from resources.progclasses.appclass import parse_link, launch_webbrowser, \
    get_rootapp

from resources.progclasses.bugreporter import BugReporter


class ShowSections(Screen):

    dict_links = DictProperty({
        "userful_programs": "https://pcompstart.com/useful",
        "advice_on_computer": "https://pcompstart.com/tips",
        "user_windows": "https://pcompstart.com/windows",
        "articles_in_theme": "https://pcompstart.com/topic",
        "popular_program": "https://pcompstart.com/popular",
        "other": "https://pcompstart.com/other"})

    url = StringProperty()

    loadback = ObjectProperty(None)

    events_callback = ObjectProperty(None)

    scrollwid = ObjectProperty(None)
    '''ScrollView + GridLayout'''

    dt = ListProperty()
    '''Список для функции `get_link(self, args)`,
    с конечными значениями для создания свойства перехода по ссылке.
    '''

    vit = ListProperty()
    '''`List` базы данных  для внесения значений в БД,
     в функцие `write_response(self, *args)`. 
     И затем последующее сравнение с запросом от браузера.
    '''

    def __init__(self, **kwargs):
        super(ShowSections, self).__init__(**kwargs)

        for lnk in self.dict_links.items():
            if self.name in lnk:
                self.url = lnk[1]

        self.scrollwid = ScrollWid(size_hint_y=1)

        self.loadback = LoadBack()
        self.add_widget(self.loadback)

        if not os.path.exists('urlfiles'):
            os.mkdir('urlfiles')

        self.list_fold = os.listdir('urlfiles')

        # Подключение базы данных
        self.dbman = DataBaseMnager('urlfiles/pcomp.db')

        # Подгрузка функции проверки старниц сайта
        Clock.schedule_once(self.check_sqlpages, 0.55)

    def parse_url(self, args):
        """Разборка ссылки запроса страницы из браузера,
         для получения названия файла.
        """
        return args.split('/')[-1]

    def get_html(self, link, imag_path=None):
        """Получение ответа от браузера, с данными страниц сайта.
        """
        try:
            zagolov = {'Content-type': 'application/x-www-form-urlencoded',
                       'Accept': '*/*'}
            req = UrlRequest(link, on_error=self.gethtml_error,
                             req_headers=zagolov,
                             chunk_size=12000, timeout=self.time_out,
                             file_path=imag_path)
            while not req.is_finished:
                req.wait(0)
            return req.result.encode("utf-8")
        except HTTPError as err:
            return BugReporter(txt_report=str(err))

    def gethtml_error(self, req, error):
        return BugReporter(txt_report=str(error))

    def time_out(self, req, time):
        if req.time > 60:
            get_rootapp().prime_screen.ids.screen_manager.current = 'primescreen'

    def get_allpages(self):
        """Вытягивает и фильтрует все страницы сайта,
        из текушего `self.url`
        """
        r = self.get_html(self.url)
        res = r.split('class="pagination"')[1].split('id="right-bar"')[0]
        page = re.findall('href="?\'?([^"\'>]*)', res)
        respag = [self.url]
        i = 1
        while i < int(max(page)[-1]):
            i += 1
            respag.append(self.url + '/page={}'.format(i))
        return respag

    def parse_content(self, largs):
        """Парсинг получеенного контента,
         по заданым данным.
        """
        try:
            res = self.get_html(largs)
            res = res.split('class="conetnt-table"')[1].split(
                'class="pagination"')[0]
            return res
        except HTTPError:
            return None

    def check_sqlpages(self, *args):
        """Проверка на существование страниц в базе данных,
        и их запись/дозапись в б.д.
        """
        self.dbman.cur.execute(
            '''create table if not exists loccat (
                id integer primary key autoincrement,
                cat_type varchar(100),
                url varchar(100))''')
        var = self.dbman.query(
            "select url from loccat where cat_type='{}'".format(
                self.parse_url(self.url))).fetchall()

        '''Переменные url_pages и val,
        обработка для сравнения результатов
        '''
        respage = self.get_allpages()
        url_pages = '\n'.join(respage)
        val = '\n'.join(
            str(v) for v in var).replace("('", "").replace("',)", "")
        if not var or url_pages not in val:
            for pag in self.get_allpages():
                if pag not in val:
                    self.dbman.querymany(
                        "insert into loccat values (null, ?, ?)",
                        [(pag.split('/')[3], pag)])
            self.parse_html()
            self.load_view()
        else:
            self.write_response(
                self.parse_content(respage[-1]))
            self.load_view()

    def parse_html(self):
        """Парсинг страниц сайта по текущему,
        `self.url`.
        """
        pageurl = self.dbman.query(
            "select url from loccat where cat_type='{}'".format(
                self.url.split('/')[-1])).fetchall()
        for p in pageurl:
            self.write_response(
                self.parse_content(p[0]))

    def write_response(self, *args):
        """Запись контента полученого из запроса от браузера,
        в базу данных.
        """
        self.dbman.cur.execute(
            '''create table if not exists categories (
                id integer primary key autoincrement,
                category_type varchar(50),
                cat_title varchar(255),
                cat_imglink varchar(255),
                cat_text text,
                link_product varchar(255))''')
        resi = [a for a in args]
        result = resi[0].split('div class="key-content"')
        del result[0]
        var = self.dbman.query(
            "select cat_title from categories "
            "where category_type='{}'".format(
                self.parse_url(self.url))).fetchall()
        for v in var:
            self.vit.append(v[0])
        list_vars = {}
        for i in result:
            '''Поиск и выборка по регулярному выражению,
            всех названий статей заключёных между тегами <title></title>.
            '''
            for title in re.findall('<h3.*?><a.*?>(.+?)</a></h3>', i):
                list_vars.update({"cat_title": title})
                break

            '''Поиск по регулярному выражению, ссылок всех картинок,
            и присваивание им суффикса `https:` с начала ссылки.
            '''
            for img in re.findall('img src="?\'?([^"\'>]*)', i):
                im = 'https:{}'.format(img)
                list_vars.update({"cat_imglink": im})
                break

            '''Поиск и выборка по регулярному выражению,
            всего текста заключёного между тегами <p></p>.
            '''
            for content in re.findall('<[p][^>]*>(.+?)</[p]>', i):
                content = re.sub('<.*?>', '', content)[:200]
                con = re.sub('&.*?;', ' ', content).replace('  ', '')
                c = con.rfind(' ')
                cont = con[:c].rstrip(',') + '...'
                list_vars.update({"cat_text": cont})
                break
            '''Поиск и выборка по регулярному выражению,
             всех ссылок, ведущих на страницу с описанием
             данного компонента.
            '''
            for link in re.findall('a href="?\'?([^"\'>]*)', i):
                link = link.replace('&amp;', '&')
                link = 'https:{}'.format(link)
                list_vars.update({"link_product": link})
                break

            '''Проверка на нахождении материала в б.д.
            если нет то, запись/дозапись.
            '''
            if list_vars["cat_title"] not in self.vit:
                try:
                    self.dbman.querymany(
                        '''insert into categories values (
                            null, ?, ?, ?, ?, ?)''',
                        [(self.parse_url(self.url),
                          list_vars["cat_title"], list_vars["cat_imglink"],
                          list_vars["cat_text"], list_vars["link_product"])])
                except KeyError:
                    pass

    def load_view(self):
        """Подгрузка и вывод всего контента.
        """
        con = self.dbman.query(
            "select cat_title, cat_imglink, cat_text, link_product"
            " from categories "
            "where category_type='{}'".format(self.parse_url(self.url))
        ).fetchall()
        if not con:
            self.check_sqlpages()
        if not os.path.exists('urlfiles/urlimg'):
            os.makedirs('urlfiles/urlimg')
        for content in con:
            file_img = content[1].split('/')[-1]
            if not os.path.exists('urlfiles/urlimg/{}'.format(file_img)):
                self.get_html(
                    link=content[1],
                    imag_path='urlfiles/urlimg/{}'.format(file_img))
            self.scrollwid.layout.add_widget(MyMadenButton(
                icon='urlfiles/urlimg/{}'.format(file_img),
                size_x_image=.25,
                text="[size=13sp][color=#0000ff][b]" + content[0] +
                     "[/b][/color][/size]" + "\n" +
                     "[size=12sp][color=#000000]" + content[2] + "[/color][/size]",
                radius_button=[0],
                height_but='115dp',
                shad_but=True, events_callback=self.get_link))
        self.add_widget(self.scrollwid)
        self.remove_widget(self.loadback)
        self.dt = con
        self.dbman.__del__()

    def get_link(self, args):
        for lnk in self.dt:
            if parse_link(args) in lnk:
                launch_webbrowser(lnk[3])
