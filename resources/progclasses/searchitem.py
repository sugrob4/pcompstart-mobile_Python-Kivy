# -*- coding: utf-8 -*-

from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.metrics import dp

from resources import programdata as core


class SearchItem(Widget):

    evcall = ObjectProperty(None)

    flot_txt = ObjectProperty(None)

    hint_text = StringProperty(core.string_enter_designation)

    def __init__(self, **kwargs):
        super(SearchItem, self).__init__(**kwargs)

        self.flot_txt = self.ids.flot_txt.__self__

        self.clear_widgets()
        self.ids.txtinpt.bind(focus=self.on_focus)

    def on_focus(self, instance, value):
        if value:
            self.ids.txtinpt.hint_text = ''
        else:
            self.ids.txtinpt.hint_text = self.hint_text

    def animfunc(self, *args):
        """Если текстовое поле за пределами границы
        окна программы то есть `self.txtinpt.x >= 350`.
        """
        if self.flot_txt.x >= Window.width:
            self.add_widget(self.flot_txt)
            with self.canvas.before:
                Color(rgba=(0, 0, 0, 0.3))
                Rectangle(size=self.parent.children[1].size,
                          pos=(self.x, self.y))
            Animation(x=dp(10), t='linear', d=0.3).start(self.flot_txt)
        else:
            anim = Animation(x=Window.width, t='linear', d=0.3)
            anim.start(self.flot_txt)
            anim.on_complete = self.animation_compl

    def animation_compl(self, args):
        self.canvas.before.clear()
        self.clear_widgets()

    def on_touch_down(self, touch):
        if self.flot_txt.x >= self.width:
            return super(SearchItem, self).on_touch_down(touch)
        elif touch.y < self.parent.children[2].y and \
                self.flot_txt.x < self.width:
            touch.grab(self)
            super(SearchItem, self).on_touch_down(touch)
            return True
        else:
            return super(SearchItem, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            for child in self.children[:]:
                if child.children[0].collide_point(*touch.pos) or \
                        child.children[1].collide_point(*touch.pos):
                    touch.ungrab(self)
                    return super(SearchItem, self).on_touch_up(touch)
                else:
                    self.animfunc()
            else:
                return super(SearchItem, self).on_touch_up(touch)

    def search(self, arg):
        if arg == '':
            return None
        self.animfunc()
        self.evcall = lambda *a: a, arg
        self.ids.txtinpt.text = ''
