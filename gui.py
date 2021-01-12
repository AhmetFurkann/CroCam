from custom_widgets.record_button import RecordButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.stacklayout import StackLayout
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
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.app import App

from threading import Thread

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
        self.videos_file_path = r"C:\Users\User\\"
        self.screenshot_file_path = r"C:\Users\User\\"
        self.video_name = "Video" + str(self.numbers_of_video) + ".mkv"
        self.video_path = os.path.join(self.videos_file_path, self.video_name)
        self.fps = fps
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)
        self.size_hint_x = 0.7
        self.size_hint_y = 0.7
        self.img_array = list()

    def update(self, dt):
        frame = ImageGrab.grab(bbox=(0, 0, 1366, 768))
        frame = np.array(frame)
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.buf1 = cv2.flip(self.frame, 0)
        buf = self.buf1.tostring()
        image_texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = image_texture

    def calculate_rectangle_effect(self):
        rectangle_x0 = 0
        rectangle_y0 = (1 - self.size_hint_y) * Window.size[1]

        rectangle_x1 = self.size_hint_x * Window.size[0]
        rectangle_y1 = (1 - self.size_hint_y) * Window.size[1]

        bottom_border_line = [rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1]
        self.canvas.add(Color(rgba=(0, 1, 1, 0.5)))
        self.canvas.add(Line(points=bottom_border_line, width=4, cap="square"))

    def start_record_video(self, instance):
        self.flag = True
        self.recorder_thread = Thread(target=self.record_video, args=(self.fps,), name="Recorder_Thread")
        self.recorder_thread.start()

    def record_video(self, fps):
        print("Video recording started!")
        self.fourcc = cv2.VideoWriter_fourcc('P', 'I', 'M', '1')
        self.video = cv2.VideoWriter(self.video_path, self.fourcc, 30,
                                     (1366, 768), True)
        while self.flag:
            self.video.write(self.frame)
            time.sleep(1 / fps)

    def stop_video(self, instance):
        self.numbers_of_video += 1
        self.video_name = "Video" + str(self.numbers_of_video) + ".mkv"
        self.video_path = self.videos_file_path + self.video_name
        print("Video Path: ", self.video_path)
        self.video.release()
        self.flag = False
        self.recorder_thread.join()
        print("Video has been recorded")

    def take_screenshot(self, instance):
        screenshot_name = "Screenshot" + str(self.numbers_of_screenshots) + ".jpg"
        self.screenshot_file_path = os.path.join(self.screenshot_file_path, screenshot_name)
        cv2.imwrite(self.screenshot_file_path, self.frame)
        self.numbers_of_screenshots = int(self.numbers_of_screenshots) + 1
        print("Screenshot has been taken!")
        print(self.numbers_of_screenshots)


class BackgroundLayout(StackLayout):
    def __init__(self):
        super(BackgroundLayout, self).__init__()


class ChildBackground(MDBoxLayout):
    def __init__(self):
        super(ChildBackground, self).__init__()
        self.padding[1] = 4


class CamApp(MDApp):
    def __init__(self):
        super(CamApp, self).__init__()
        self.background = BackgroundLayout()
        self.background.cols = 2

        self.right_top_child_back = ChildBackground()
        self.right_top_child_back.size_hint_x = .3
        self.right_top_child_back.size_hint_y = .7
        self.right_top_child_back.padding[2] = 5

        self.right_bottom_child_back = ChildBackground()
        self.right_top_child_back.orientation = "vertical"
        self.right_bottom_child_back.size_hint_x = 1
        self.right_bottom_child_back.size_hint_y = .3

    def build(self):
        self.capture = ImageGrab.grab(bbox=(0, 0, 1366, 768))
        self.capture = np.array(self.capture)
        self.capture = cv2.cvtColor(self.capture, cv2.COLOR_BGR2RGB)

        self.my_camera = KivyPIL(capture=self.capture, fps=30)

        video_record_button = Button(on_press=self.my_camera.start_record_video)
        video_record_button.text = "Start Recording"

        video_stop_button = Button(on_press=self.my_camera.stop_video)
        video_stop_button.size_hint_y = .4
        video_stop_button.text = "Stop Recording"

        take_screenshot = Button(on_press=self.my_camera.take_screenshot)
        take_screenshot.text = "Take A Screenshot"

        self.right_top_child_back.add_widget(take_screenshot)
        self.right_top_child_back.add_widget(video_record_button)
        self.right_top_child_back.add_widget(video_stop_button)
        self.right_bottom_child_back.add_widget(Button(text="Will Add Some Widgets"))

        self.background.add_widget(self.my_camera)
        self.background.add_widget(self.right_top_child_back)
        self.background.add_widget(self.right_bottom_child_back)
        return self.background


if __name__ == '__main__':
    CamApp().run()
