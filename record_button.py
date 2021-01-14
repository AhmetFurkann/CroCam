from kivy.properties import (BooleanProperty, NumericProperty,
                             ListProperty, ReferenceListProperty)
from kivy.graphics import Color, Ellipse, Line, InstructionGroup
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
import time
import threading

OUTLINE = 0.00000000001


class RecordButton(ButtonBehavior, Widget):
    outer_size = NumericProperty(1)
    inner_size = NumericProperty(0.5)

    outer_background_color = ListProperty([0.50, 0.50, 0.50, 1])
    inner_background_color = ListProperty([0.75, 0, 0, 1])

    outer_line_color = ListProperty([0.75, 0.75, 0.75, 1])
    inner_line_color = ListProperty([0.1, 0.1, 0.1, 1])

    outer_line_width = NumericProperty(0.005)
    inner_line_width = NumericProperty(0.01)

    _outer_line_width = NumericProperty(OUTLINE)
    _inner_line_width = NumericProperty(OUTLINE)

    _total_diameter = NumericProperty(0)
    _total_radius = NumericProperty(0)

    _outer_diameter = NumericProperty(0)
    _outer_radius = NumericProperty(0)

    _inner_diameter = NumericProperty(0)
    _inner_radius = NumericProperty(0)

    _wave_effect_colors = list()
    _wave_effect_circles = list()

    def __init__(self):
        super(RecordButton, self).__init__()
        self.waves_colors = []
        self.waves_circles = []

        self.outer_color = Color(rgba=self.outer_background_color)
        self.outer_ellipse = Ellipse(pos=((self.center_x - self._outer_radius), (self.center_y - self._outer_radius)),
                                     size=(self._outer_diameter, self._outer_diameter))

        self.out_line_color = Color(rgba=self.outer_line_color)
        self.out_line = Line(circle=(self.center_x, self.center_y, self._outer_radius - (self._outer_line_width / 2)),
                             width=self._outer_line_width)

        self.inner_color = Color(rgba=self.inner_background_color)
        self.inner_ellipse = Ellipse(pos=(self.center_x - self._inner_radius, self.center_y - self._inner_radius),
                                     size=(self._inner_diameter, self._inner_diameter))

        self.add_canvas_elements()

        # Clock.schedule_interval(self.add_wave_effect, 7)

    def add_canvas_elements(self):
        self.canvas.add(self.outer_color)
        self.canvas.add(self.outer_ellipse)

        self.canvas.add(self.out_line_color)
        self.canvas.add(self.out_line)

        self.canvas.add(self.inner_color)
        self.canvas.add(self.inner_ellipse)
        #
        # self.create_wave_effect()
        # for sep in range(len(self._wave_effect_circles)):
        #     self.canvas.add(self._wave_effect_colors[sep])
        #     self.canvas.add(self._wave_effect_circles[sep])
        # thread_1 = threading.Thread(target=self.add_wave_effect)
        # thread_1.start()

    def update_canvas_elements(self):
        self.outer_ellipse.pos = ((self.center_x - self._outer_radius), (self.center_y - self._outer_radius))
        self.outer_ellipse.size = (self._outer_diameter, self._outer_diameter)

        self.out_line.circle = (self.center_x, self.center_y, self._outer_radius - (self._outer_line_width / 2))
        self.out_line.width = self._outer_line_width

        self.inner_ellipse.pos = (self.center_x - self._inner_radius, self.center_y - self._inner_radius)
        self.inner_ellipse.size = (self._inner_diameter, self._inner_diameter)

    def update_widget(self):
        size = min(*self.size)
        self._update_outlines(size)
        self._update_circles(size)
        self.update_canvas_elements()
        # self.update_wave_effect()

    def on_pos(self, *args):
        self.update_widget()

    def on_size(self, *args):
        self.update_widget()

    def _update_circles(self, size):
        self._total_diameter = size
        self._total_radius = self._total_diameter / 2

        self._outer_diameter = (self._total_diameter - self._outer_line_width) * self.outer_size
        self._outer_radius = self._outer_diameter / 2

        self._inner_diameter = (self._total_diameter - self._inner_line_width) * self.inner_size
        self._inner_radius = self._inner_diameter / 2

    def _update_outlines(self, size):
        self._outer_line_width = self.outer_line_width * size \
            if self.outer_line_width else OUTLINE

        self._inner_line_width = self.inner_line_width * size \
            if self.inner_line_width else OUTLINE

    def create_wave_effect(self):
        rate = 0.05
        min_radius = self._inner_radius - (self._inner_line_width / 2)
        self.number_of_wave = 20
        for sep in range(self.number_of_wave):
            min_radius += 4
            color = Color()
            circle = Line(circle=(self.center_x, self.center_y, min_radius),
                          width=self._inner_line_width)
            # print("Circle: ", type(circle))

            self._wave_effect_colors.append(color)
            self._wave_effect_circles.append(circle)

            rate += 0.05

    def update_wave_effect(self):
        number_of_circles = len(self._wave_effect_circles)
        inner_min_radius = self._inner_radius - (self._inner_line_width / 2)
        outer_min_radius = self._outer_radius - (self._outer_line_width / 2)
        ratio = (outer_min_radius - inner_min_radius) / number_of_circles
        inner_min_radius -= ratio
        for sep in range(number_of_circles):
            inner_min_radius += ratio
            # self._wave_effect_colors[sep].rgba = [1, 0, 0, 1]
            self._wave_effect_circles[sep].circle = (self.center_x, self.center_y, inner_min_radius)
            self._wave_effect_circles[sep].width = self._inner_line_width
            # self._wave_effect_colors[sep].rgba = [0, 1, .0, 0.5]

    def add_wave_effect(self):

        number_of_colors = len(self._wave_effect_colors)
        rate = 1 / number_of_colors
        color_rate = 0
        for sep in range(number_of_colors):
            time.sleep(0.05)
            color_rate += rate
            print("Test: ", self._wave_effect_colors[sep])
            self._wave_effect_colors[sep].rgba = [0.5, 0, 0, color_rate]
            # self._wave_effect_colors[sep].rgba = [0, 1, .0, 0.5]
            print("RGBA: ", self._wave_effect_colors[sep].rgba)

        for sep in range(number_of_colors):
            time.sleep(0.05)
            color_rate += rate
            print("Test: ", self._wave_effect_colors[sep])
            self._wave_effect_colors[sep].rgba = [0.5, 0, 0, color_rate]
            # self._wave_effect_colors[sep].rgba = [0, 1, .0, 0.5]
            print("RGBA: ", self._wave_effect_colors[sep].rgba)

        for sep in range(number_of_colors):
            time.sleep(0.05)
            color_rate += rate
            print("Test: ", self._wave_effect_colors[sep])
            self._wave_effect_colors[sep].rgba = [0.5, 0, 0, color_rate]
            # self._wave_effect_colors[sep].rgba = [0, 1, .0, 0.5]
            print("RGBA: ", self._wave_effect_colors[sep].rgba)
