from kivy.graphics import Color, RoundedRectangle
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from abc import ABC, abstractmethod


class BarFactory(ABC):

    @abstractmethod
    def factory_method(self):
        pass


class BoxBarFactory(BarFactory):

    def factory_method(self):
        return BoxBar()


class GridBarFactory(BarFactory):

    def factory_method(self):
        return GridBar()


class Bar(ABC):

    @abstractmethod
    def update_background(self) -> None:
        pass

    @abstractmethod
    def adjust_widget_padding(self) -> None:
        pass


class BoxBar(BoxLayout):
    __metaclass__ = Bar
    bg_padding = ListProperty([0, 0, 0, 0])
    background_rectangle_radius = ListProperty([(0, 0), (0, 0), (0, 0), (0, 0)])

    def __init__(self):
        super(BoxBar, self).__init__()

        self.background_color = Color(rgba=[0, 0, 0, 0])
        self.bg_rectangle = RoundedRectangle(pos=self.pos, size=self.size)
        self.canvas.add(self.background_color)
        self.canvas.add(self.bg_rectangle)

        self.bind(size=self.update_background)
        self.bind(pos=self.update_background)
        self.bind(bg_padding=self.adjust_widget_padding)

    def update_background(self, *args) -> None:
        self.bg_rectangle.pos = self.pos
        self.bg_rectangle.size = self.size
        self.bg_rectangle.radius = self.background_rectangle_radius
        self.adjust_widget_padding()

    def adjust_widget_padding(self, *args) -> None:
        """If the value at index of 2 in bg_padding ListProperty is changed
                           the top padding is adjust according to its root widget."""

        """The following two code statement for the left padding of widget."""
        self.bg_rectangle.size = (self.bg_rectangle.size[0] - self.bg_padding[0], self.bg_rectangle.size[1])
        self.bg_rectangle.pos = (self.bg_rectangle.pos[0] + self.bg_padding[0], self.bg_rectangle.pos[1])

        """The following  code statement for the right padding of widget."""
        self.bg_rectangle.size = (self.bg_rectangle.size[0] - self.bg_padding[2], self.bg_rectangle.size[1])

        """The following  code statement for the top padding of widget."""
        self.bg_rectangle.size = (self.bg_rectangle.size[0], self.bg_rectangle.size[1] - self.bg_padding[1])

        """The following  code statement for the bottom padding of widget."""
        self.bg_rectangle.pos = (self.bg_rectangle.pos[0], self.bg_rectangle.pos[1] + self.bg_padding[3])


class GridBar(GridLayout):
    __metaclass__ = Bar
    bg_padding = ListProperty([0, 0, 0, 0])
    background_rectangle_radius = ListProperty([(0, 0), (0, 0), (0, 0), (0, 0)])

    def __init__(self):
        super(GridBar, self).__init__()
        self.cols = 2
        self.background_color = Color(rgba=[0, 0, 0, 0])
        self.bg_rectangle = RoundedRectangle(pos=self.pos, size=self.size)
        self.canvas.add(self.background_color)
        self.canvas.add(self.bg_rectangle)

        self.bind(size=self.update_background)
        self.bind(pos=self.update_background)
        self.bind(bg_padding=self.adjust_widget_padding)

    def update_background(self, *args) -> None:
        self.bg_rectangle.pos = self.pos
        self.bg_rectangle.size = self.size
        self.bg_rectangle.radius = self.background_rectangle_radius
        self.adjust_widget_padding()

    def adjust_widget_padding(self, *args) -> None:
        """If the value at index of 2 in bg_padding ListProperty is changed
                           the top padding is adjust according to its root widget."""

        """The following two code statement for the left padding of widget."""
        self.bg_rectangle.size = (self.bg_rectangle.size[0] - self.bg_padding[0], self.bg_rectangle.size[1])
        self.bg_rectangle.pos = (self.bg_rectangle.pos[0] + self.bg_padding[0], self.bg_rectangle.pos[1])

        """The following  code statement for the right padding of widget."""
        self.bg_rectangle.size = (self.bg_rectangle.size[0] - self.bg_padding[2], self.bg_rectangle.size[1])

        """The following  code statement for the top padding of widget."""
        self.bg_rectangle.size = (self.bg_rectangle.size[0], self.bg_rectangle.size[1] - self.bg_padding[1])

        """The following  code statement for the bottom padding of widget."""
        self.bg_rectangle.pos = (self.bg_rectangle.pos[0], self.bg_rectangle.pos[1] + self.bg_padding[3])
