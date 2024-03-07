from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.lang import Builder
from languages import *
from googletrans import Translator
import speech_recognition as sr



class ScreenTransition(Button):
  def __init__(self, screen, direction='up', goal='home', **kwargs):
      super().__init__(**kwargs)
      self.screen = screen
      self.direction = direction
      self.goal = goal
  def on_press(self):
      self.screen.manager.transition.direction = self.direction
      self.screen.manager.current = self.goal
 
 
class MainScr(Screen):
  def __init__(self, **kwargs):
      super().__init__(**kwargs)
      vl = BoxLayout(orientation='vertical',padding=20, spacing=20)
      vl.add_widget(Label(text="Welcome to PyLator", font_size='40sp', font_name="DejaVuSans"))
      vl.add_widget(ScreenTransition(self, direction='up', goal='home', text="start", size_hint=(0.5,0.1),pos_hint={'center_x':0.5}))
      self.add_widget(vl)
      
        
class Home(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initUI()        
        
    def initUI(self):
        # Create our app widgets
        self.title = Label(text="PyLator", font_size='55sp', font_name="DejaVuSans")
        self.input_option = DropDown()
        self.output_option = DropDown()
        
        self.btn_reverse = Button(text='Reverse', on_press=self.reverse_text, size_hint=(1, 0.2), pos_hint={'center_x':0.5})
        self.btn_translate = Button(text='Translate', on_press=self.translate_text, size_hint=(0.8, 0.4), pos_hint={'center_x':0.5})
        self.btn_speak = Button(text='Speak', on_press=self.speak_and_translate, size_hint=(0.8, 0.4), pos_hint={'center_x':0.5})
        self.btn_reset = Button(text='Reset', on_press=self.clear_boxes, size_hint=(0.8, 0.4), pos_hint={'center_x':0.5})
        
        self.input_box = TextInput(hint_text='Enter text to translate',size_hint=(1, 0.8))
        self.output_box = TextInput(hint_text='Translation will appear here', readonly=True,size_hint=(1, 0.8))
        
        # Create buttons for our dropdown list
        for lang in values:
            input_btn = Button(text=lang, size_hint_y=None, height=44)
            input_btn.bind(on_release=lambda btn: self.update_button_text(self.input_button, btn.text))
            self.input_option.add_widget(input_btn)

            output_btn = Button(text=lang, size_hint_y=None, height=44)
            output_btn.bind(on_release=lambda btn: self.update_button_text(self.output_button, btn.text))
            self.output_option.add_widget(output_btn)

        self.input_button = Button(text='Select Input Language', size_hint=(0.7, 0.4), pos_hint={'center_x':0.5})
        self.input_button.bind(on_release=self.input_option.open)
        
        self.output_button = Button(text='Select Output Language', size_hint=(0.7, 0.4), pos_hint={'center_x':0.5})
        self.output_button.bind(on_release=self.output_option.open)
        
        # Adding Widgets to our Design (App Layout)
        self.master = BoxLayout()
        col1 = BoxLayout(orientation='vertical', padding=15)
        col2 = BoxLayout(orientation='vertical', padding=15)
        
        col1.add_widget(self.title)
        col1.add_widget(self.input_button)
        col1.add_widget(self.output_button)
        col1.add_widget(self.btn_translate)
        col1.add_widget(self.btn_speak)
        col1.add_widget(self.btn_reset)

        col2.add_widget(self.input_box)
        col2.add_widget(self.btn_reverse)
        col2.add_widget(self.output_box)
        
        self.master.add_widget(col1)
        self.master.add_widget(col2)
        
        self.add_widget(self.master)
    
        

    def update_button_text(self, button, text):
        button.text = text


    # By including the instance=None parameter, the methods become more versatile. They can be called without relying on an instance, making them suitable for various scenarios, such as static method calls or function references.
    def translate_text(self, instance=None):
        source_lang = self.input_button.text
        target_lang = self.output_button.text
        text = self.input_box.text

        try:
            translator = Translator()
            translated_text = translator.translate(text, src=source_lang, dest=target_lang).text
            self.output_box.text = translated_text
        except Exception as e:
            print(f"Error: {e}")
            self.output_box.text = "Error...."
    
    def speak_and_translate(self, instance=None):
        txt = self.recognize_speech()
        if txt:
            self.input_box.text = txt
            self.translate_text()

    def recognize_speech(self,instance=None):
        listener = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = listener.listen(source,timeout=5)
                text = listener.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Error requesting speech recognition results:", e)
            except Exception as e:
                print("Error recognizing speech:", e)
    

    def clear_boxes(self, instance=None):
        self.input_box.text = ''
        self.output_box.text = ''
        
    def reverse_text(self, instance=None):
        input_text = self.input_box.text
        output_text = self.output_box.text

        self.input_box.text = output_text
        self.output_box.text = input_text

        input_lang = self.input_button.text
        output_lang = self.output_button.text

        self.input_button.text = output_lang
        self.output_button.text = input_lang
 



class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScr(name="main"))
        sm.add_widget(Home(name='home'))
        return sm

if __name__ == '__main__':
    Builder.load_file('main.kv')
    MainApp().run()
