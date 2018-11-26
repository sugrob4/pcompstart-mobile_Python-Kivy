# -*- coding: utf-8 -*-

from kivy.animation import Animation
from kivy.properties import (NumericProperty, ObjectProperty, BooleanProperty,
                             StringProperty, OptionProperty)
from kivy.uix.stencilview import StencilView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp


class SlidePanelException(Exception):
    """
    Действует когда add_widget или remove_widget,
    вызваны не корректно в SlidePanel.
    """


class SlidePanel(StencilView):
    """Содержит два дочерних виджета боковой и главной панелей."""

    _side_panel = ObjectProperty()
    _main_panel = ObjectProperty()
    _join_image = ObjectProperty()
    """Внутрение сылки для виджетов главной, боковой панелей,
    а также изображения. `side`, `main`, `image`.
    """

    side_panel = ObjectProperty(None, allownone=True)
    """Автоматически привязывается к независимому виджету,
    и добавляется в качестве скрытой панели.
    """
    main_panel = ObjectProperty(None, allownone=True)
    """Автоматически привязывается к независимому виджету,
    и добавляется в качестве главной панели.
    """

    # Свойства, внешнего вида
    side_panel_width = NumericProperty(Window.width / 1.85)
    """Ширина скрывающейся боковой панели, по умолчанию это `200dp`."""
    separator_image = StringProperty('')
    """Путь к изображению разделителю, между
    боковой и главной панелями. Если оставить по умолчанию `''`,
    то будет градиент, от чёрного до прозрачного.
    """
    separator_image_width = NumericProperty(dp(10))
    """Ширина изображения разделителя панелей,
    по умолчанию это `10dp`.
    """

    # Свойства относящиеся к касаниям (Touch)
    touch_accept_width = NumericProperty('14dp')
    """Область слева от главной панели `class SlidePanel`,
    на которой при прикосновении будет захватываться боковая панель
    для вытягивания пальцем (либо мышкой).
    """
    _touch = ObjectProperty(None, allownone=True)
    """Текущее активное касание"""

    # Свойства анимации
    state = OptionProperty('closed', options=('open', 'closed'))
    """Указывает на одно из двух состояний виджета,
    `открыто` или `закрыто`, переключение происходит автоматически.
    Либо для анимированого перехода можно воспользоваться функцией
    anim_to_state().
    """
    anim_time = NumericProperty(0.15)
    """Время за которое боковая панель будет открываться/закрываться."""
    min_dist_to_open = NumericProperty(0.7)
    """Указывает на область скрытой панели,
    данная ширина будет определяться SlidePanel как,
    панель в открытом состонии то есть `open`.
    """
    _anim_progress = NumericProperty(0)
    """Управление состоянием позиции панели."""

    _anim_init_progress = NumericProperty(0)
    """Числовое управление `_anim_progress`,
    в функциях класса SlidePanel.
    """

    # Управление анимацией
    # _main_above = BooleanProperty(True)
    _main_above = BooleanProperty(False)
    """Доп. элемент управления функциями класса,
     а также добовляемыми виджетами в боковую панель.
    """
    side_panel_init_offset = NumericProperty(1)
    # side_panel_init_offset = NumericProperty(0.5)
    """Начальное смещение боковой панели в единицах от общей ширины,
    плавно открывает и перемещает панель до конечной позиции.
    """
    side_panel_darknes = NumericProperty(0)
    """Контролирует от прозрачного-до-чёрного,
    боковую панель в закрытом состоянии.
    Должно быть между 0 (не прозрачно)
    и 1 (от прозрачного до конкретно чёрного)
    """
    side_panel_opacity = NumericProperty(1)
    """Контролирует прозрачность боковой панели в закрытом состоянии.
    Должно быть между 0 прозрачно, и 1 не прозрачно.
    """
    # main_panel_final_offset = NumericProperty(0.5)
    main_panel_final_offset = NumericProperty(0.7)
    """Финальное смещение главной панели,
    (вправо от нормального положения),
    в единицах от ширины боковой панели"""
    main_panel_darknes = NumericProperty(0.5)
    """Контролирует интенсивность цвета главной панели,
     от прозрачного-до-чёрного, когда боковая панель в открытом
     состоянии. Должно быть между 0 (обесцвеченно) и
     1 (до конкретно чёрного).
     """
    events_callback = ObjectProperty(None)
    """Функция обработки сигналов экрана."""

    def __init__(self, **kwargs):
        super(SlidePanel, self).__init__(**kwargs)
        Clock.schedule_once(self.on__main_above, 0)

    def on__main_above(self, *args):
        newval = self._main_above
        main_panel = self._main_panel
        side_panel = self._side_panel
        self.canvas.remove(main_panel.canvas)
        self.canvas.remove(side_panel.canvas)
        if newval:
            self.canvas.insert(0, main_panel.canvas)
            self.canvas.insert(0, side_panel.canvas)
        else:
            self.canvas.insert(0, side_panel.canvas)
            self.canvas.insert(0, main_panel.canvas)

    def toggle_main_above(self, *args):
        if self._main_above:
            self._main_above = False
        else:
            self._main_above = True

    def add_widget(self, widget, index=0, canvas=None):
        if len(self.children) == 0:
            super(SlidePanel, self).add_widget(widget)
            self._side_panel = widget
        elif len(self.children) == 1:
            super(SlidePanel, self).add_widget(widget)
            self._main_panel = widget
        elif len(self.children) == 2:
            super(SlidePanel, self).add_widget(widget)
            self._join_image = widget
        elif self.side_panel is None:
            self._side_panel.add_widget(widget)
            self.side_panel = widget
        elif self.main_panel is None:
            self._main_panel.add_widget(widget)
            self.main_panel = widget
        else:
            raise SlidePanelException(
                'Невозможно добавить более двух виджетов'
                ' непосредственно в SlidePanel')

    def remove_widget(self, widget):
        if widget is self.side_panel:
            self._side_panel.remove_widget(widget)
            self.side_panel = None
        elif widget is self.main_panel:
            self._main_panel.remove_widget(widget)
            self.main_panel = None
        else:
            raise SlidePanelException(
                'Виджет не является боковой или главной панелью,'
                ' невозможно удалить его.'
            )

    def set_side_panel(self, widget):
        """Удаляет существующие виджеты боковой панели и заменяет их на
         аргумент `widget`.
        """
        # Очищение существующих элементов боковой панели
        if len(self._side_panel.children) > 0:
            for child in self._side_panel.children:
                self._side_panel.remove(child)
        # Назначение новой боковой панели
        self._side_panel.add_widget(widget)
        self.side_panel = widget

    def set_main_panel(self, widget):
        """Удаляет существующие виджеты главной панели и заменяет их на
         аргумент `widget`.
        """
        # Очищение существующих элементов главной панели
        if len(self._main_panel.children) > 0:
            for child in self._main_panel.children:
                self._main_panel.remove(child)
        # Назначение новой главной панели
        self._main_panel.add_widget(widget)
        self.main_panel = widget

    def on__anim_progress(self, *args):
        if self._anim_progress > 1:
            self._anim_progress = 1
        elif self._anim_progress < 0:
            self._anim_progress = 0
        elif self._anim_progress >= 1:
            self.state = 'open'
        elif self._anim_progress <= 0:
            self.state = 'closed'

    def on_state(self, *args):
        Animation.cancel_all(self)
        if self.state == 'open':
            self._anim_progress = 1
        else:
            self._anim_progress = 0

    def anim_to_state(self, state):
        """Время открытия или закрытия берёт из self.anim_time,
        положение должно быть `open` либо `closed`.
        """
        if state == 'open':
            anim = Animation(
                _anim_progress=1, duration=self.anim_time,
                transition='linear')
            anim.start(self)
        elif state == 'closed':
            anim = Animation(
                _anim_progress=0, d=self.anim_time, t='linear'
            )
            anim.start(self)
        else:
            raise SlidePanelException(
                'Некорректное получение состояния, '
                'должно быть что-то одно `open` или `closed`.'
            )

    def toggle_state(self, animate=True):
        """Переключение из закрытого в открытое и наоборот,
        с анимированием или просто со скачком.
        """
        if self.state == 'open':
            if animate:
                self.anim_to_state('closed')
            else:
                self.state = 'closed'
        elif self.state == 'closed':
            if animate:
                self.anim_to_state('open')
            else:
                self.state = 'open'

    def on_touch_down(self, touch):
        col_self = self.collide_point(*touch.pos)
        col_side = self._side_panel.collide_point(*touch.pos)
        col_main = self._main_panel.collide_point(*touch.pos)

        if self._anim_progress < 0.001:  # т.е. закрыто
            valid_region = (self.x <=
                            touch.x <=
                            (self.x + self.touch_accept_width))
            if not valid_region:
                self._main_panel.on_touch_down(touch)
                return False
        else:
            if col_side and not self._main_above:
                self._side_panel.on_touch_down(touch)
                return False
            valid_region = (self._main_panel.x <=
                            touch.x <=
                            (self._main_panel.x + self._main_panel.width))
            if not valid_region:
                if self._main_above:
                    if col_main:
                        self._main_panel.on_touch_down(touch)
                    elif col_side:
                        self._side_panel.on_touch_down(touch)
                else:
                    if col_side:
                        self._side_panel.on_touch_down(touch)
                    elif col_main:
                        self._main_panel.on_touch_down(touch)
                return False
        Animation.cancel_all(self)
        self._anim_init_progress = self._anim_progress
        self._touch = touch
        touch.ud['type'] = self.state
        touch.ud['panels_jiggled'] = False
        """Если пользователь переместил панель назад либо вперёд,
            то не используется значение по умолчанию,
            и отменяется сенсорный режим.
        """
        touch.grab(self)
        return True

    def on_touch_move(self, touch):
        if touch is self._touch:
            dx = touch.x - touch.ox
            self._anim_progress = max(
                0, min(self._anim_init_progress +
                       (dx / self.side_panel_width), 1))
            if self._anim_progress < 0.975:
                touch.ud['panels_jiggled'] = True
        else:
            super(SlidePanel, self).on_touch_move(touch)
            return

    def on_touch_up(self, touch):
        if touch is self._touch:
            self._touch = None
            init_state = touch.ud['type']
            touch.ungrab(self)
            jiggled = touch.ud['panels_jiggled']
            if init_state == 'open' and not jiggled:
                if self._anim_progress >= 0.975:
                    self.anim_to_state('closed')
                else:
                    self._anim_relax()
            else:
                self._anim_relax()
        else:
            super(SlidePanel, self).on_touch_up(touch)
            return

    def _anim_relax(self):
        """Анимирует до открытой или закрытой позиции,
            в зависимости от того какие данные были переданы в
            self.min_dist_to_open
        """
        if self._anim_progress > self.min_dist_to_open:
            self.anim_to_state('open')
        else:
            self.anim_to_state('closed')

    def _choose_image(self, *args):
        """Выбирает какая картинка будет показываться в качестве
            разделителя между основной и боковой панелями.
            На основании _main_above.
        """
        if self.separator_image:
            return self.separator_image
        if self._main_above:
            return 'atlas://material/images/navpanel/' \
                   'navpanel_atlas/gradient_rtol'
        else:
            return 'atlas://material/images/navpanel/' \
                   'navpanel_atlas/gradient_ltor'
