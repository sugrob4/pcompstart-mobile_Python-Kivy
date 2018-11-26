# -*- coding: utf-8 -*-

import os
import sys
import traceback

from kivy.config import ConfigParser

p = os.path.split(os.path.abspath(sys.argv[0]))[0]

select_locale = {u"Русский": "russian", "English": "english"}

# Если файл настроек отсутствует, то задаются параметры по умолчанию.
if not os.path.exists("{}/prog.ini".format(p)):
    language = u"Русский"
else:
    config = ConfigParser()
    config.read("{}/prog.ini".format(p))
    language = config.get("General", "language")
    del config

old_language = language
language = select_locale[language]

try:
    with open("{}/material/languages/{}.txt".format(p, language)) as lng:
        exec(lng.read())
except Exception:
    raise Exception(traceback.format_exc())

dict_language = {
    string_lang_on_russian: "russian",
    string_lang_on_english: "english"
}

dict_cats = {
    "userful_programs": string_lang_userful_programs,
    "advice_on_computer": string_lang_advice_on_computer,
    "user_windows": string_lang_user_windows,
    "articles_in_theme": string_lang_articles_in_theme,
    "popular_program": string_lang_popular_program,
    "other": string_lang_other
}

dict_navigations_items = [
    [string_lang_to_website,
     "atlas://material/images/navpanel/navpanel_atlas/to_website"],
    [string_lang_settings,
     "atlas://material/images/navpanel/navpanel_atlas/nav_settings"],
    [string_lang_license,
     "atlas://material/images/navpanel/navpanel_atlas/nav_license"],
    [string_lang_about,
     "atlas://material/images/navpanel/navpanel_atlas/nav_about"],
    [string_lang_exit_key,
     "atlas://material/images/navpanel/navpanel_atlas/nav_exit_prog"],
]
