#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback

from os import path

directory = path.dirname(path.abspath(__file__))

sys.dont_write_bytecode = True

sys.path.append('{}/resources'.format(directory))
sys.path.append('{}/resources/progclasses'.format(directory))

try:
    import kivy
    from kivy.app import App
    from kivy.config import Config
    Config.set('kivy', 'keyboard_mode', 'system')
    # Config.set("kivy", "log_level", "error")
    Config.set("kivy", "log_maxfiles", "10")
    Config.set('graphics', 'width', '350')
    Config.set('graphics', 'height', '650')
except Exception:
    with open("{}/error.log".format(directory), "w") as err:
        traceback.print_exc(err)
    sys.exit(1)

__version__ = '0.3.2'


if __name__ == "__main__":
    app = None

    try:
        from prog import Prog
        app = Prog()
        app.run()
    except Exception:
        from resources.progclasses.bugreporter import BugReporter
        text_error = traceback.format_exc()
        erro = open("{}/error.log".format(directory), "w")
        erro.write(text_error)
        print(text_error)
        erro.close()

        if app:
            try:
                app.prime_screen.clear_widgets()
            except AttributeError:
                pass

        class Error(App):
            def build(self):
                win_report = BugReporter(txt_report=text_error)
                return win_report
        Error().run()
