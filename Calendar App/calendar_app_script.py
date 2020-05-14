from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.dropdown import DropDown


class Calendar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2

        self.middle_division_left = GridLayout()
        self.add_widget(self.middle_division_left)

        self.middle_division_left.cols = 7

        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for day_name in day_names:
            self.middle_division_left.add_widget((Label(text=day_name)))

        month = 31
        for day in range(1, month + 1):
            calendar_button = ToggleButton(text=str(day), background_color=[0.4, 0.7, 1, 1], on_press=self.day_pressed,
                                           group="days")
            self.middle_division_left.add_widget(calendar_button)

        self.middle_division_right = GridLayout()
        self.middle_division_right.cols = 2
        self.add_widget(self.middle_division_right)

        self.middle_division_right.add_widget(Label())
        self.middle_division_right.add_widget(Label(text="Months"))

        month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                       "November", "December"]
        for index, month_name in enumerate(month_names):
            self.middle_division_right.add_widget(ToggleButton(text=month_name, on_press=self.month_pressed,
                                                               id=str(index + 1), group="months"))

    def day_pressed(self, instance):
        print(instance.text)

    def month_pressed(self, instance):
        print(instance.text, instance.id)

        # ^^Uzupełnij o możliwość zaznaczenia roku
        # ^^Zaznaczony w interfejsie dzień i miesiąc zapisuj po kliknięciu przycisku "Add event"
        # ^^Nie każdy miesiąc musi zaczynać się od poniedziałku.

        # Dodaj kolorki do Label's:
        # self.canvas.add(Color(0.85, 0.75, 0.5, 1))
        # self.canvas.add(Rectangle(pos=self.pos))


class NewEventPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Add new event"
        self.size_hint = [0.8, 0.8]
        self.background_color = [0.9, 0.7, 0.5, 0.5]

        self.content = GridLayout(rows=2)

        self.inside_grid_text = GridLayout(rows=2)
        self.user_event = TextInput(multiline=False, size_hint_y=0.4, text="Name your event: ",
                                    background_color=[0.95, 0.85, 0.6, 1], on_touch_down=self.clear_text)

        # ^^Uzupełnij o komunkat dla użytkownika, że nie może zostawić tego pola pustego.

        self.inside_grid_text.add_widget(self.user_event)
        self.user_date = Calendar()
        self.inside_grid_text.add_widget(self.user_date)
        self.content.add_widget(self.inside_grid_text)

        self.inside_grid_btns = GridLayout(cols=2, size_hint_y=0.2)

        self.close_button = Button(text="Close", background_color=[0.9, 0, 0, 1], on_press=self.dismiss)
        self.inside_grid_btns.add_widget(self.close_button)

        self.submit_button = Button(text="Add event", background_color=[0, 0.5, 1, 1], on_press=self.add_user_event)
        self.inside_grid_btns.add_widget(self.submit_button)

        self.content.add_widget(self.inside_grid_btns)

    def add_user_event(self, instance):
        text_field_value = self.user_event.text
        if text_field_value == "Name your event: " or text_field_value == "":
            print("To pole nie może pozostać puste.")
        else:
            print(self.user_event.text)
            with open("events_db.txt", 'a') as events_db:
                events_db.write("\n" + self.user_event.text + "\n" + "01.01.0000")

    def clear_text(self, instance, touch):
        if instance.text == "Name your event: ":
            instance.text = ""


class NavBar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.size_hint_y = 0.3

        self.add_widget(Button(text="     Add \nnew event", size_hint_x=0.2, on_press=NewEventPopup().open))

        self.add_widget(Image(source="Images/violet_bg.jpg", allow_stretch=True, keep_ratio=False))

        self.settings_popup = Popup(title="Settings", content=Label(text="Choose your settings."),
                                    size_hint=[0.5, 0.5], background_color=[0.9, 0.7, 0.5, 0.5])
        self.add_widget(Button(text="Settings", size_hint_x=0.2, on_release=self.settings_popup.open))


class EventCols(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.size_hint_y = 1

        with open("events_db.txt", 'r') as events_db:
            user_data = events_db.readlines()

        event_names = ""
        event_dates = ""
        for index, line in enumerate(user_data):
            if index % 2 == 0:
                event_names += line
            if index % 2 == 1:
                event_dates += line

        self.add_widget(Label(text=event_names, halign="left"))
        self.add_widget(Label(text=event_dates))
        self.add_widget(Label(text="3"))


class Footer(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint_y = 0.1
        self.add_widget(Button(background_color=[1, 1, 1, 1], disabled=True, text="Footer"))


class MainPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 3
        self.add_widget(NavBar())
        self.add_widget(EventCols())
        self.add_widget(Footer())


class MyApp(App):
    def build(self):
        return MainPage()


if __name__ == '__main__':
    MyApp().run()
