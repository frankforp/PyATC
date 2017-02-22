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
import math


Builder.load_string('''
<Airplane>:
    size: 4, 4
    canvas:
        Color:
            rgba: 1, 0, 0, 1
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        text: 'PL123'
        pos: root.pos

<MainMenu>
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: '[i][color=ffff00]PyATC[sub] Version 1[/sub][/color][/i]'
            font_size:70
            markup: True
        Button:
            text: '[b][size=20]Start Session[/size][/b] - Starts a session under certain parameters'
            markup: True
            on_release: root.manager.current = 'sim_screen'
            on_release: root.manager.transition.direction = 'left'
        Button:
            text: '[b][size=20]Training[/size][/b] - Access to tutorials and practice air field'
            markup: True
            on_release: root.manager.current = 'sim_screen'
            on_release: root.manager.transition.direction = 'left'
        Button:
            text: '[b][size=20]Details[/size][/b] - Extra information about the project and its goals'
            markup: True
            on_release: root.manager.current = 'sim_screen'
            on_release: root.manager.transition.direction = 'left'

<SimScreen>
    airplanes: planes_widget
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
            id: planes_widget

        BoxLayout:
            orientation: 'vertical'
            width: 250
            size_hint_x: None
            BoxLayout:
                orientation: 'vertical'
                Button:
                    text: 'Back to Menu'
                    on_release: root.manager.current = 'main_menu'
                    on_release: root.manager.transition.direction = 'right'
                Button:
                    text: 'Test Creation'
                    on_release: root.plane_creation_test()
                Label:
                    markup: True
                    text: 'Status: [b][color=00ff00]Correct[/color][/b]'
                    id: status_label
            Label:
                text: '[color=ff7f50][b]ARRIVING[/b][/color]'
                markup: True
            Label:
                text: 'no arriving flights'
                markup: True
                id: departing
            BoxLayout:
                orientation: 'horizontal'
                Label:
                    markup: True
                    text: '[b][color=ff0000]RESET[/color][/b]'
                Switch:
                    id: pause_switch
                    on_touch_up: root.start_function()
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
                    on_text_validate: root.text_validation()
''')

class MainMenu(Screen):
    pass

class Airplane(Widget):
    angle = NumericProperty(0)
    speed = NumericProperty(1)

    def move(self, dt):
        velocity = (math.sin(self.angle) * self.speed, math.cos(self.angle) * self.speed)
        self.pos = (Vector(velocity) * dt) + self.pos

class SimScreen(Screen):

    airplane = ObjectProperty(None)
    banana = '[color=ff7f50][b]DEPARTING[/b][/color]\n---------------------\nRY123 090 FL012 200kts\nAF943 340 FL015 210kts\nVG324 220 FL009 170kts'
    apple = '[color=ffff00][b]ARRIVING[/b][/color]\n---------------------\nPL123 090 FL012 200kts'

    def __init__(self, **kwargs):
        super(SimScreen, self).__init__(**kwargs)
        self.input_box = self.ids['input_box']
        self.status_label = self.ids['status_label']
        self.pause_switch = self.ids['pause_switch']
        self.departing = self.ids['departing']
        self.plane_referenced = ''
        self.plane_instruction = ''
        self.plane_instrucion_value = ''

    def text_validation(self):
        #Clock.unschedule(self.updateDisplay)
        # split user input into different parts (plane being spoken to, instruction given and value of instruction)
        self.plane_referenced = self.input_box.text[:5]
        self.plane_instruction = self.input_box.text[6:9]
        self.plane_instrucion_value = self.input_box.text[10:13]
        self.input_box.text = ''
        Clock.schedule_interval(self.updateDisplay, 1 / 3)


    def start_function(self):
        if self.pause_switch.active == False:
            #self.airplane.velocity = (2, 2)
            #self.airplane.pos = (0, 0)
            Clock.schedule_interval(self.updateDisplay, 1 / 3)
        elif self.pause_switch.active == True:
            Clock.unschedule(self.updateDisplay)
        else:
            pass

    def plane_creation_test(self):
        # create aircrafts
        airplane = Airplane()
        airplane.angle = math.pi / 2
        airplane.speed = 2

        self.airplanes.add_widget(airplane)

    def updateDisplay(self, dt):
        self.status_label.text = 'Status: [b][color=00ff00]Correct[/color][/b]'
        #self.departing.text = 'PL123 ' + str(self.airplane.speed) + str(self.airplane.angle)
        #self.airplane.move()
        planes = (c for c in self.airplanes.children if isinstance(c, Airplane))
        for plane in planes:
            plane.move(dt)
        # move around
        if self.plane_referenced == "PL123" and self.plane_instruction == "FHE":
            #self.airplane.angle = int(self.plane_instrucion_value) * math.pi / 180
            self.status_label.text = 'Status: [b][color=0000ff]Copied[/color][/b]'
            self.plane_referenced = ''

        if self.plane_referenced == "PL123" and self.plane_instruction == "SPE":
            #self.airplane.speed = int(self.plane_instrucion_value)
            self.status_label.text = 'Status: [b][color=0000ff]Copied[/color][/b]'
            self.plane_referenced = ''

        # collide variables
        #if self.airplane.x < 0 or self.airplane.right > self.width - 250 or self.airplane.y < 0 or self.airplane.top > self.height:
        #    self.status_label.text = 'Status: [b][color=ff0000]Aircraft left radar[/color][/b]'
        #    Clock.unschedule(self.updateDisplay)
        #    self.pause_switch.disabled = True

# screen after screen of data
sm = ScreenManager()
sm.add_widget(MainMenu(name='main_menu'))
sm.add_widget(SimScreen(name='sim_screen'))

class AmyTurnMyHeadRightRoundApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    AmyTurnMyHeadRightRoundApp().run()
