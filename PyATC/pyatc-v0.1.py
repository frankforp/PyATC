from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.switch import Switch
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import time
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget
import random


Builder.load_string('''
<Airplane>:
    size: 4, 4
    canvas:
        Rectangle:
            pos: self.pos
            size: self.size

<MainMenu>
    BoxLayout:
        Label:
            text: 'Kill me'
        Button:
            text: 'Go to the simulator'
            on_release: root.manager.current = 'sim_screen'
            on_release: root.manager.transition.direction = 'left'

<SimScreen>
    airplane: airplane_test

    GridLayout:
        rows: 1
        Widget:
            canvas:
                Rectangle:
                    size: 80, 4
                    pos: (self.width/100*45), (self.height/100*48)
                Rectangle:
                    size: 80, 4
                    pos: (self.width/100*45), (self.height/100*52)
                Rectangle:
                    id: limit_bar
                    size: 1, self.height
                    pos: self.width, 0
                    Color:
                        rgb: 1, 0, 1, 1
            Airplane:
                id: airplane_test
                center: self.parent.center

        BoxLayout:
            orientation: 'vertical'
            width: 220
            size_hint_x: None
            BoxLayout:
                orientation: 'vertical'
                Button:
                    text: 'Back to Menu'
                    on_release: root.manager.current = 'main_menu'
                    on_release: root.manager.transition.direction = 'right'
                Label:
                    text: ''
                Label:
                    markup: True
                    text: 'Status: [b][color=00ff00]Correct[/color][/b]'
                    id: status_label
            Label:
                text: root.banana
                markup: True
            Label:
                text: root.apple
                markup: True
            BoxLayout:
                orientation: 'horizontal'
                Label:
                    markup: True
                    text: '[b][color=ff0000]STOP[/color][/b]'
                Switch:
                    id: pause_switch
                    on_touch_up: root.pause_function()
                Label:
                    markup: True
                    text: '[b][color=00ff00]START[/color][/b]'
            BoxLayout:
                orientation: 'vertical'
                Label:
                    text: ''
                Label:
                    text: 'ATC says:'
                TextInput:
                    focus: True
                    multiline: False
                    id: input_box
                    background_color: '232453'
                    on_text_validate: root.restore_to_null_input()



''')

class MainMenu(Screen):
    pass

class Airplane(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(self.velocity) + self.pos
        print('we\'re movin\'', time.time())

class SimScreen(Screen):
    def __init__(self, **kwargs):
        super(SimScreen, self).__init__(**kwargs)
        self.input_box = self.ids['input_box']
        self.status_label = self.ids['status_label']
        self.pause_switch = self.ids['pause_switch']

    airplane = ObjectProperty(None)

    banana = '[color=ff7f50][b]DEPARTING[/b][/color]\n---------------------\nRY123 090 FL012 200kts\nAF943 340 FL015 210kts\nVG324 220 FL009 170kts'
    apple = '[color=ffff00][b]ARRIVING[/b][/color]\n---------------------\nRY123 090 FL012 200kts\nAF943 340 FL015 210kts\nVG324 220 FL009 170kts'

    def restore_to_null_input(self):
        self.input_box.text = ''
        Clock.schedule_interval(self.updateDisplay, 1 / 3)

    def pause_function(self):
        if self.pause_switch.active == False:
            self.airplane.velocity = (1.5, 2)
            Clock.schedule_interval(self.updateDisplay, 1 / 3)
        elif self.pause_switch.active == True:
            Clock.unschedule(self.updateDisplay)
        else:
            print("yo yo yo error returned")

    def updateDisplay(self, dt):
        self.airplane.move()
        if self.airplane.x < 0 or self.airplane.right > self.width: self.airplane.velocity_x *= -1
        if self.airplane.y < 0 or self.airplane.top > self.height: self.airplane.velocity_y *= -1


sm = ScreenManager()
sm.add_widget(MainMenu(name='main_menu'))
sm.add_widget(SimScreen(name='sim_screen'))

class AmyTurnMyHeadRightRoundApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    AmyTurnMyHeadRightRoundApp().run()
