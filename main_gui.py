from record_button import RecordButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.stacklayout import StackLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget
from kivy.properties import ListProperty

from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.graphics.texture import Texture

from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.app import App

from threading import Thread
from bar import *

from PIL import ImageGrab
import numpy as np
import time
import cv2
import os


class KivyPIL(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyPIL, self).__init__(**kwargs)
        self.numbers_of_screenshots = 0
        self.numbers_of_video = 0
        self.videos_file_path = os.getcwd()
        self.screenshot_file_path = os.getcwd()
        self.video_name = "Video" + str(self.numbers_of_video) + ".mkv"
        self.record_flag = False
        # self.screenshot_name = "Screenshot" + str(self.numbers_of_screenshots) + ".jpg"
        self.video_path = os.path.join(self.videos_file_path, self.video_name)

        # self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        self.fps = fps
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)
        self.size_hint_x = 0.7
        self.size_hint_y = 0.7
        self.img_array = list()
        # self.calculate_rectangle_effect()

    def update(self, dt):
        frame = ImageGrab.grab(bbox=(0, 0, 1366, 768))
        frame = np.array(frame)
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # frame = cv2.resize(frame, dsize=(int(Window.size[0]), int(Window.size[1])),
        #                    interpolation=cv2.INTER_CUBIC)
        # convert it to texture
        self.buf1 = cv2.flip(self.frame, 0)
        buf = self.buf1.tostring()
        # print("Lenght Of The Frame: ", len(buf))
        image_texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.texture = image_texture

    def calculate_rectangle_effect(self):
        rectangle_x0 = 0
        rectangle_y0 = (1 - self.size_hint_y) * Window.size[1]

        rectangle_x1 = self.size_hint_x * Window.size[0]
        rectangle_y1 = (1 - self.size_hint_y) * Window.size[1]

        bottom_border_line = [rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1]
        self.canvas.add(Color(rgba=(0, 1, 1, 0.5)))
        self.canvas.add(Line(points=bottom_border_line, width=4, cap="square"))

    def start_record_video(self, instance, video_format):
        print("Video_Format: ", video_format)

        if self.record_flag == False:
            self.recorder_thread = Thread(target=self.start_recording, args=(self.fps, video_format),
                                          name="Recorder_Thread")
            self.recorder_thread.start()
            self.record_flag = True
        else:
            self.stop_recording(video_format)
            self.record_flag = False

    def start_recording(self, fps, format_argument):
        print("Video recording started!")
        self.flag = True
        if format_argument == "mkv":
            video_format = "PIM1"
        elif format_argument == "mp4":
            video_format = "mp4v"
        elif format_argument == "avi":
            video_format = "FMP4"
        self.fourcc = cv2.VideoWriter_fourcc(*video_format)
        self.video = cv2.VideoWriter(self.video_path, self.fourcc, 30,
                                     (1366, 768), True)
        while self.flag:
            self.video.write(self.frame)
            time.sleep(1 / fps)

    def stop_recording(self, video_format):
        self.video_name = "Video" + str(self.numbers_of_video) + "." + video_format
        self.video_path = self.videos_file_path + self.video_name
        print("Video Path: ", self.video_path)
        self.flag = False
        self.video.release()
        self.numbers_of_video += 1
        self.recorder_thread.join()
        print("Video has been recorded")

    def take_screenshot(self, instance):
        screenshot_name = "Screenshot" + str(self.numbers_of_screenshots) + ".jpg"
        self.screenshot_file_path = os.path.join(self.screenshot_file_path, screenshot_name)
        cv2.imwrite(self.screenshot_file_path, self.frame)
        self.numbers_of_screenshots = int(self.numbers_of_screenshots) + 1
        print("Screenshot has been taken!")
        print(self.numbers_of_screenshots)


class BackgroundLayout(MDStackLayout):
    def __init__(self):
        super(BackgroundLayout, self).__init__()


class ChildBackground(MDBoxLayout):
    def __init__(self):
        super(ChildBackground, self).__init__()
        self.padding[1] = 4


class PropertiesToolBar(BoxLayout):
    def __init__(self):
        super(PropertiesToolBar, self).__init__()
        self.orientation = "vertical"
        self.padding = [0, 0, 0, 0]
        self.spacing = 5

        self.background_color = Color(rgba=[.45, .45, .45, 0.9])
        self.background_rectangle = RoundedRectangle(pos=self.pos, size=self.size)
        self.background_rectangle.radius = [(12, 12), (12, 12), (12, 12), (12, 12)]

        self.label = MDLabel()
        self.label.text = "Properties"
        self.label.halign = "center"
        self.label.color = [0.9, 0.9, 0.9, 1]

        # self.label2 = MDLabel()
        # self.label2.text = "Properties"
        # self.label2.halign = "center"
        # self.label2.color = [0.9, 0.9, 0.9, 1]

        self.toolbar = SingleBar()
        self.toolbar.size_hint_y = 0.1
        self.toolbar.background_rectangle_radius = [(12, 12), (12, 12), (0, 0), (0, 0)]
        self.toolbar.add_widget(self.label)

        self.second_bar = SingleBar()
        self.second_bar.orientation = "vertical"
        self.second_bar.bg_padding = [5, 5, 5, 5]
        self.dropdown_item = CustomDropDownItem()

        self.video_format_label = MDLabel()
        self.video_format_label.text = "Video Format"
        self.video_format_label.halign = "center"

        self.inside_bar = GridBarFactory().factory_method()

        self.dropdown_screen = Screen()
        self.dropdown_screen.add_widget(self.dropdown_item)

        self.inside_bar.size_hint_y = .2
        self.inside_bar.pos_hint = {"top": 1}
        self.inside_bar.add_widget(self.video_format_label)
        self.inside_bar.add_widget(self.dropdown_screen)

        self.record_button = RecordButton()
        self.screenshot_button = RecordButton()
        self.screenshot_button.inner_background_color = [0, 0, 0, 0]
        self.screenshot_button.outer_line_width = 0.05

        self.buttons_layout = BoxLayout()
        self.buttons_layout.padding = [23, 23, 23, 23]
        self.buttons_layout.spacing = 40
        # self.buttons_layout.size_hint_y = .2

        # self.buttons_layout.padding = [0, 100, 0, 0]
        self.buttons_layout.add_widget(self.record_button)
        self.buttons_layout.add_widget(self.screenshot_button)
        self.second_bar.add_widget(self.inside_bar)
        self.second_bar.add_widget(self.buttons_layout)

        self.add_widget(self.toolbar)
        self.add_widget(self.second_bar)
        self.canvas.add(self.background_color)
        self.canvas.add(self.background_rectangle)

        self.bind(size=self.update_background)
        self.bind(pos=self.update_background)

    def update_background(self, *args):
        self.background_rectangle.pos = self.pos
        self.background_rectangle.size = self.size
        self.background_color.rgba = [0.20, 0.20, 0.20, 0.5]


class SingleBar(MDBoxLayout):
    bg_padding = ListProperty([0, 0, 0, 0])
    background_rectangle_radius = ListProperty([(0, 0), (0, 0), (0, 0), (0, 0)])

    def __init__(self):
        super(SingleBar, self).__init__()
        self.background_color = Color(rgba=[.3, .3, .3, 1])
        self.bg_rectangle = RoundedRectangle(pos=self.pos, size=self.size)
        self.canvas.add(self.background_color)
        self.canvas.add(self.bg_rectangle)

        self.bind(size=self.update_background)
        self.bind(pos=self.update_background)
        self.bind(bg_padding=self.apply_background_padding)

    def update_background(self, *args):
        self.bg_rectangle.pos = self.pos
        self.bg_rectangle.size = self.size
        self.bg_rectangle.radius = self.background_rectangle_radius
        self.apply_background_padding()

    def apply_background_padding(self, *args):
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


class CustomDropDownItem(MDDropDownItem):

    def __init__(self):
        super(CustomDropDownItem, self).__init__()
        self.pos_hint = {"center_x": .5, "center_y": .5}
        # self.pos_hint = {"center_y": .5}
        menu_items = [{"icon": "git", "text": f"MP4"},
                      {"icon": "git", "text": f"AVI"},
                      {"icon": "git", "text": f"MKV"}]
        self.menu = MDDropdownMenu(
            caller=self,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.text = menu_items[0]["text"]
        self.current_item = self.text
        self.menu.bind(on_release=self.set_new_item)
        self.bind(pos=self.update_the_location)

    def on_release(self):
        self.menu.open()

    def set_new_item(self, instance_menu, instance_menu_item):
        self.set_item(instance_menu_item.text)
        print("Current Item: ", self.current_item)
        self.menu.dismiss()

    def update_the_location(self, *args):
        self.pos_hint = {"center_x": .5, "center_y": .5}


class CamApp(MDApp):
    def __init__(self):
        super(CamApp, self).__init__()
        self.background = BackgroundLayout()
        self.background.md_bg_color = [0.55, 0.55, 0.55, 1]
        self.background.cols = 2

        # self.left_top_child_back = ChildBackground()
        # self.left_top_child_back.size_hint_x = None
        # self.left_top_child_back.width = 708
        # self.left_top_child_back.size_hint_y = None
        # self.left_top_child_back.height = 400

        self.right_top_child_back = ChildBackground()
        self.right_top_child_back.size_hint_x = .3
        self.right_top_child_back.size_hint_y = .7
        self.right_top_child_back.padding[2] = 5

        self.right_bottom_child_back = ChildBackground()
        self.right_top_child_back.orientation = "vertical"
        self.right_bottom_child_back.size_hint_x = 1
        self.right_bottom_child_back.size_hint_y = .3

        self.properties_section = PropertiesToolBar()

        # self.left_bottom_child_back = ChildBackground()

        # self.left_bottom_child_back.add_widget(Button(text="Left Bottom"))

    def build(self):
        self.capture = ImageGrab.grab(bbox=(0, 0, 1366, 768))
        self.capture = np.array(self.capture)
        self.capture = cv2.cvtColor(self.capture, cv2.COLOR_BGR2RGB)

        self.my_camera = KivyPIL(capture=self.capture, fps=30)

        # video_record_button = Button(on_press=self.my_camera.start_record_video)
        # Todo: Reorganize the Layout
        # video_record_button = RecordButton()
        # video_record_button.text = "Start Recording"

        # video_stop_button = Button(on_press=self.my_camera.stop_video)
        # video_stop_button.size_hint_y = .4
        # video_stop_button.text = "Stop Recording"
        self.properties_section.record_button.bind(on_press=lambda instance: self.my_camera.start_record_video(instance,
                                                                                                               self.properties_section.dropdown_item.current_item.lower()))

        take_screenshot = Button(on_press=self.my_camera.take_screenshot)
        take_screenshot.text = "Take A Screenshot"

        # option_caption = MDLabel()
        # option_caption.text = "Properties"
        # option_caption.font_style = "Caption"

        # self.right_top_child_back.add_widget(take_screenshot)
        # self.right_top_child_back.add_widget(video_record_button)
        self.right_top_child_back.add_widget(self.properties_section)
        # self.right_top_child_back.add_widget(video_stop_button)
        self.right_bottom_child_back.add_widget(Button(text="Will Add Some Widgets"))

        # self.left_top_child_back.add_widget(self.my_camera)
        # self.background.add_widget(self.left_top_child_back)
        self.background.add_widget(self.my_camera)
        self.background.add_widget(self.right_top_child_back)
        # self.background.add_widget(self.left_bottom_child_back)
        self.background.add_widget(self.right_bottom_child_back)
        return self.background

    # def on_stop(self):
    #     #without this, app waill not exit even if the window is closed
    #     self.capture.release()


if __name__ == '__main__':
    CamApp().run()
