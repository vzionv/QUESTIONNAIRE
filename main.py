import os.path

from kivy.app import App
from kivy.graphics import Line, Color
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, ListProperty, DictProperty
from kivy.properties import ObjectProperty, ColorProperty, ReferenceListProperty, VariableListProperty
from kivy.clock import Clock
# from kivymd.toast import toast
# from kivymd.app import MDApp
# from kivymd.toast.kivytoast.kivytoast import Toast
from kivy.storage.jsonstore import JsonStore
import time
import json
from kivy import platform
from kivy.core.window import Window

Window.softinput_mode = "below_target"

from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')


if platform == "android":
    from android.storage import primary_external_storage_path
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
from kivy.uix.modalview import ModalView
from kivy.factory import Factory


class Toast(ModalView):
    message = StringProperty("")

    def __init__(self, message=None, **kwargs):
        super(Toast, self).__init__(**kwargs)
        print(message)
        if message:
            self.message = message
        else:
            self.message = ""
        Clock.schedule_once(self.dismiss_toast, 1)

    def dismiss_toast(self, dt):
        self.dismiss()


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def on_leave(self, *args):
        return None
        # print("MainScreen on leave")
        # App.get_running_app().root.ids['question_screen'].answers_check = {}


class PersonalInfoScreen(Screen):
    personal_information = {}

    def __init__(self, **kwargs):
        super(PersonalInfoScreen, self).__init__(**kwargs)
        # Clock.schedule_once(self._finish_init)

    def save_personal_information(self):
        if not self.ids.name_input.text:
            Factory.Toast("请填写姓名").open()
            return
        # if not self.ids.age_input.text:
        #     Factory.Toast("请填写年龄").open()
        # if not self.ids.height_input.text:
        #     Factory.Toast("请填写身高").open()
        # if not self.ids.weight_input.text:
        #     Factory.Toast("请填写体重").open()
        self.personal_information['name'] = self.ids.name_input.text
        self.personal_information['age'] = self.ids.age_input.text
        self.personal_information['height'] = self.ids.height_input.text
        self.personal_information['weight'] = self.ids.weight_input.text
        # print("Personal Information Saved:", self.personal_information)
        self.manager.current = 'question'



class QuestionScreen(Screen):
    question_index = NumericProperty(0)
    answers_check = DictProperty({})
#     """
# 1. 我感到心情平静*
# 2. 我感到安全*
# 3. 我是紧张的
# 4. 我感到紧张束缚
# 5. 我感到安逸*
# 6. 我感到烦乱
# 7. 我现在正在烦恼，感到这种烦恼超过了可能的不幸
# 8. 我感到满意*
# 9. 我感到害怕
# 10.我感到舒适*
# 11.我有自信心*
# 12.我觉得神经过敏
# 13.我极度紧张不安
# 14.我优柔寡断
# 15.我是轻松的*
# 16.我感到心满意足*
# 17.我是烦恼的
# 18.我感到慌乱
# 19.我感到镇定*
# 20.我感到愉快*
#
#     """
    _questions = [
        ["我感到心情平静", -1],
        ["我感到安全", -1],
        ["我是紧张的", 1],
        ["我感到紧张束缚", 1],
        ["我感到安逸", -1],
        ["我感到烦乱", 1],
        ["我现在正在烦恼，\n感到这种烦恼超过了可能的不幸", 1],
        ["我感到满意", -1],
        ["我感到害怕", 1],
        ["我感到舒适", -1],
        ["我有自信心", -1],
        ["我觉得神经过敏", 1],
        ["我极度紧张不安", 1],
        ["我优柔寡断", 1],
        ["我是轻松的", -1],
        ["我感到心满意足", -1],
        ["我是烦恼的", 1],
        ["我感到慌乱", 1],
        ["我感到镇定", -1],
        ["我感到愉快", -1],
    ]

    _answers = [
        ["    1-完全没有", "    2-有些", "    3-中等程度", "    4-非常明显"],
    ]
    questions = ListProperty(_questions)
    answers = ListProperty(_answers)
    len_questions = NumericProperty(len(_questions))
    len_answers = NumericProperty(len(_answers[0]))
    progress_string_text = StringProperty()
    question_string_text = StringProperty()
    option_0_string_text = StringProperty()
    option_1_string_text = StringProperty()
    option_2_string_text = StringProperty()
    option_3_string_text = StringProperty()

    def __init__(self, **kwargs):
        super(QuestionScreen, self).__init__(**kwargs)

        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        # self.answers_check = App.get_running_app().root.answers_check
        self.ids.check_0.bind(active=self.on_checkbox_active)
        self.ids.check_1.bind(active=self.on_checkbox_active)
        self.ids.check_2.bind(active=self.on_checkbox_active)
        self.ids.check_3.bind(active=self.on_checkbox_active)

    def on_enter(self, *args):
        # print(f"total num of questions: {len(self.questions)}")
        self.update_question()
        # print("on enter")
        self.clean_checkbox()

    def on_leave(self, *args):
        # print("on leave")
        self.question_index = 0
        # self.answers_check = {}
        self.clean_checkbox()
        # print(f"current answers: {self.answers_check}")

    def on_checkbox_active(self, checkbox, value):
        if value:
            self.answers_check[self.question_index] = int(checkbox.name)+1
        else:
            pass
        # print(f"current answers: {self.answers_check}")

    def update_question(self):
        # print(self.question_index, self.answers_check)
        self.progress_string_text = f"{self.question_index + 1}/{self.len_questions}"
        self.question_string_text = self.questions[self.question_index][0]

        self.option_0_string_text = self.answers[0][0]
        self.option_1_string_text = self.answers[0][1]
        self.option_2_string_text = self.answers[0][2]
        self.option_3_string_text = self.answers[0][3]

        if self.question_index in self.answers_check:
            self.ids[f"check_{self.answers_check[self.question_index]}"].active = True
        else:
            self.clean_checkbox()

    def clean_checkbox(self):
        # print("clean checkbox")
        for i in range(self.len_answers):
            self.ids[f"check_{i}"].active = False

    def select_option(self, index, label, args):
        # print(args)
        if label.collide_point(*label.to_local(*args[1].pos)):
            self.ids[f'check_{index}'].active = True

    def next_question(self):
        if self.question_index in self.answers_check and self.question_index < len(self.questions) - 1:
            self.question_index += 1
            self.update_question()
        elif self.question_index in self.answers_check and self.question_index == len(self.questions) - 1:
            self.manager.current = 'final'
        else:
            pass
            Factory.Toast("这一个问题还没填").open()
            # toast("hello world", True, 80, 200, 0)
            # t = Toast(duration=2.0, _md_bg_color=[0.2, 0.2, 0.2, 0.5])
            # t.label_toast.font_name = "DroidSansFallback.ttf"
            # t.toast("请先完成此项后再进入下一项")

    def previous_question(self):
        if self.question_index > 0:
            self.question_index -= 1
            self.update_question()
        else:
            self.manager.current = 'info'


class FinalScreen(Screen):
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super(FinalScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        root = App.get_running_app().root
        questions = root.ids['question_screen']._questions
        ans = root.ids['question_screen'].answers_check
        # print(ans)
        # print(questions)
        self.score = 0
        for i in range(len(questions)):
            # print((int(ans[i]))*int(questions[i][1]))
            self.score += (int(ans[i]))*int(questions[i][1])
        # self.score = sum([int(i)*j[1] for i in ans.values() for j in questions])

    def on_leave(self, *args):
        root = App.get_running_app().root
        root.ids['question_screen'].answers_check = {}
        root.ids['question_screen'].clean_checkbox()

    def save_score(self):
        root = App.get_running_app().root
        personal_information = root.ids['info_screen'].personal_information
        ans = root.ids['question_screen'].answers_check
        # print(personal_information, ans)
        merged = {}
        merged.update(personal_information)
        merged.update(ans)
        merged["total_score"] = self.score
        json_str = json.dumps(merged, indent=4, ensure_ascii=False)

        path = primary_external_storage_path()
        path = os.path.join(path, 'quest')
        if not os.path.exists(path):
            os.mkdir(path)
        file_name = f'{personal_information["name"]}_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.json'
        file_path = os.path.join(path, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)
        Factory.Toast(f"已保存至{file_name}").open()

    def return_to_main(self):
        self.score = 0
        self.manager.current = 'main'


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        # print("init checks")



class questApp(App):
    # method which will render our application
    def close_application(self):
        # closing application
        App.get_running_app().stop()
        # removing window
        Window.close()

    def build(self):
        self.icon = "icon.png"
        self.title = "焦虑评分量表"
        # self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "DeepPurple"

        self.sm = ScreenManagement()
        # Window.size = (432, 768)
        # self.sm.add_widget(MainScreen(name="main"))
        # self.sm.add_widget(PersonalInfoScreen(name="info"))
        # self.sm.add_widget(QuestionScreen(name="question"))
        # self.sm.add_widget(FinalScreen(name="final"))
        return self.sm  # 返回root控件

    def changeKeyboard(self, widget, layout):
        # print(f'Changing keyboard layout to: {layout}')
        self._keyboard = Window.request_keyboard(self._keyboard_closed, widget)

        layout_mapping = {'numeric': os.path.join('numeric.json'),
                          'alphanumeric': os.path.join('en_US.json')}

        if self._keyboard.widget:
            vkeyboard = self._keyboard.widget
            vkeyboard.layout = layout_mapping[layout]

    def _keyboard_closed(self):
        # print('My keyboard has been closed!')
        if self._keyboard:
            self._keyboard = None
            Window.release_keyboard()

if __name__ == "__main__":
    questApp().run()
