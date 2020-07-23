from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random

Builder.load_file("app_5_python_mobile_app/design.kv")

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen" #manager is a property of screen, child of parent(screen), curren attribute of manager, which gets the sign up screen, widget created in kivy code.
    
    def login(self, uname, pword):
        with open("app_5_python_mobile_app/users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "Login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password"
         

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("app_5_python_mobile_app/users.json") as file:
            users =json.load(file)
        

        users[uname] = {'username': uname, 'password': pword, 'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        
        with open("app_5_python_mobile_app/users.json", "w") as file:
            json.dump(users, file)

        self.manager.current = "sign_up_screen_success"


class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Login_screen"


class LogInScreenSuccess(Screen):
    def logout(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Login_screen"

    def get_quote(self, feel):
        feel = feel.lower()
        available_feeling = glob.glob("app_5_python_mobile_app/quotes/*txt")
        
        available_feeling = [Path(filename).stem for filename in 
                            available_feeling]
        
        if feel in available_feeling:
            with open(f"app_5_python_mobile_app/quotes/{feel}.txt", encoding="utf8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()
