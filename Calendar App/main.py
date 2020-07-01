from datetime import datetime
import calendar
import sqlite3
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.dropdown import DropDown

# Połączenie z bazą danych SQLite 
conn = sqlite3.connect('calendar_app_db.db')
c = conn.cursor()

c.execute("SELECT Theme_Color FROM user_settings")
chosen_theme_color = c.fetchone()[0]

# Zmienne globalne
chosen_day = "0"
chosen_month_id = "0"
chosen_year = "0"

event_cols_object = GridLayout()
footer_object = GridLayout()

current_row_number = 0


class Calendar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = 2

        self.middle_division_up = GridLayout(cols=2, size_hint_y=0.2)
        self.add_widget(self.middle_division_up)

        self.middle_division_down = GridLayout(cols=7)
        self.add_widget(self.middle_division_down)

        month_scroll = DropDown()

        month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                       "November", "December"]
        for index, month_name in enumerate(month_names):
            month_scroll.add_widget(ToggleButton(text=month_name, on_press=self.month_pressed, size_hint_y=None,
                                                 id=str(index + 1), group="months"))
        self.middle_division_up.add_widget(Button(on_release=lambda x: month_scroll.open(x), text="Month", font_size=17,
                                                  size_hint_y=0.3, background_color=[0.4, 0.7, 1, 1]))

        scroll_layout = GridLayout(cols=1)
        year_scroll = DropDown()
        current_year = datetime.today().year
        amount_of_year_buttons = 100
        for i in range(amount_of_year_buttons):
            year_scroll.add_widget(ToggleButton(text=str(current_year + i), size_hint_y=None,
                                                on_press=self.year_pressed, group="years"))
            # ^^przyciski z wypisanymi latami
        scroll_layout.add_widget(Button(on_release=lambda x: year_scroll.open(x), text="Year", font_size=17,
                                        background_color=[0.4, 0.7, 1, 1]))
        # ^^przycisk scroll drop
        self.middle_division_up.add_widget(scroll_layout)

    def day_pressed(self, instance):
        global chosen_day
        chosen_day = instance.text
        # print(instance.text)

    def month_pressed(self, instance):
        global chosen_month_id
        chosen_month_id = instance.id
        # print(instance.text, instance.id)

        if chosen_month_id != "0" and chosen_year != "0":
            self.display_days(instance)

    def year_pressed(self, instance):
        global chosen_year
        chosen_year = instance.text

        if chosen_month_id != "0" and chosen_year != "0":
            self.display_days(instance)

    def display_days(self, instance):
        self.middle_division_down.clear_widgets()

        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for day_name in day_names:
            self.middle_division_down.add_widget((Label(text=day_name)))

        which_weekday = datetime(int(chosen_year), int(chosen_month_id), 1).weekday()  # <- który to dzień tygodniu [0:6]
        for day_id in range(which_weekday):
            self.middle_division_down.add_widget(Label())

        days_amount = calendar.monthrange(int(chosen_year), int(chosen_month_id))[1]  # <- ilość dni w danym miesiącu
        for day in range(1, days_amount + 1):
            calendar_button = ToggleButton(text=str(day), background_color=[0.4, 0.7, 1, 1], on_press=self.day_pressed,
                                           group="days")
            self.middle_division_down.add_widget(calendar_button)


class NewEventPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Add new event"
        self.size_hint = [0.8, 0.8]
        self.background_color = [0.9, 0.7, 0.5, 0.5]

        # Font size of Text_input, Close i Add event buttons
        the_font_size = 17

        self.content = GridLayout(rows=2)

        self.inside_grid_text = GridLayout(rows=2)
        char_limit = 30  # <- the maximum amount of characetrs user can enter into the Text Field
        self.user_event = TextInput(multiline=False, size_hint_y=0.3, text="Name your event: ", font_size=the_font_size,
                                    background_color=[0.95, 0.85, 0.67, 1], on_touch_down=self.clear_text,
                                    input_filter=lambda text, from_undo: text[:char_limit - len(self.user_event.text)])

        self.inside_grid_text.add_widget(self.user_event)
        self.user_date = Calendar()
        self.inside_grid_text.add_widget(self.user_date)
        self.content.add_widget(self.inside_grid_text)

        self.inside_grid_btns = GridLayout(cols=2, size_hint_y=0.15)

        self.close_button = Button(text="Close", background_color=[1, 0.2, 0.2, 1], on_press=self.dismiss,
                                   font_size=the_font_size,)
        self.inside_grid_btns.add_widget(self.close_button)

        self.submit_button = Button(text="Add event", background_color=[0.5, 1, 0.2, 1], on_press=self.add_user_event,
                                    font_size=the_font_size,)
        self.inside_grid_btns.add_widget(self.submit_button)

        self.content.add_widget(self.inside_grid_btns)

    def add_user_event(self, instance):
        text_field_value = self.user_event.text
        if text_field_value == "Name your event: " or text_field_value == "":
            self.no_blank_field(instance)
        else:
            # Dodanie "0" przed cyframi pojedynczych dni i miesięcy (potrzebne do późniejszego sortowania dat z SQL)
            the_month = chosen_month_id
            if len(chosen_month_id) == 1:
                the_month = "0" + chosen_month_id

            the_day = chosen_day
            if len(chosen_day) == 1:
                the_day = "0" + chosen_day

            whole_date = chosen_year + "-" + the_month + "-" + the_day
            if len(whole_date) < 10:
                whole_date = "-"

            self.event_added_info(instance)

            # Nadawanie indeksów kolejnym wpisom do bazy danych
            c.execute("SELECT MAX(idx) FROM user_events")  # <- zaznacza największą wartość w kolumnie idx'ów
            last_idx = c.fetchone()[0]

            new_idx = 0  # <- ta wartość zostanie nadpisana przez następne 4 linijki
            if last_idx is None:  # <- gdy last_idx wynosi None nie można do niego dodawać, a tabela jest obecnie pusta
                new_idx = 1  # <- gdy tabela jest pusta, indeks pierwszego wpisu będzie wynosił 1
            elif last_idx is not None:
                new_idx = last_idx + 1  # <- wcześniejsze zaznaczenie +1 daje nowy indeks o największej wartości

            # Zapisywanie nowego wpisu w bazie danych
            new_event_name = self.user_event.text
            new_event_date = whole_date
            new_insertion_time = str(datetime.now())
            c.execute("INSERT INTO user_events (idx, event_name, event_date, insertion_time) VALUES(?, ?, ?, ?)",
                      (new_idx, new_event_name, new_event_date, new_insertion_time))
            conn.commit()

            global event_cols_object
            event_cols_object.clear_widgets()
            event_cols_object.add_widget(EventCols3())

    def clear_text(self, instance, touch):
        if instance.text == "Name your event: ":
            instance.text = ""

    def no_blank_field(self, instance):
        reminder_layout = GridLayout(cols=1)
        reminder_layout.add_widget(Label(text="Please name your event."))
        reminder = Popup(content=reminder_layout, title="Text field can not be blank.", size_hint=[0.4, 0.4])
        btn_ok = Button(text="Ok", on_press=reminder.dismiss, size_hint_y=0.5)
        reminder_layout.add_widget(btn_ok)
        reminder.open()

    def event_added_info(self, instance):
        info_layout = GridLayout(cols=1)
        info_layout.add_widget(Label(text="Event added."))
        info_popup = Popup(content=info_layout, title="Success!", size_hint=[0.4, 0.4])
        btn_ok = Button(text="Ok", on_release=info_popup.dismiss, size_hint_y=0.5, on_press=self.dismiss)
        info_layout.add_widget(btn_ok)
        info_popup.open()


class NavBar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.size_hint_y = 0.2

        self.plus_popup = NewEventPopup()
        self.plus_btn = Button(size_hint_x=0.2, on_release=self.plus_popup.open,
                               background_normal="Images/plus_sign2_" + chosen_theme_color + ".jpg")
        self.add_widget(self.plus_btn)

        # self.theme_view_image = Button(text="Calendar App", disabled=True, font_size=20, font_name="Impact",
        #                                background_disabled_normal="Images/theme_" + chosen_theme_color + ".jpg")
        self.theme_view_image = Image(source="Images/theme_" + chosen_theme_color + ".jpg", allow_stretch=True, keep_ratio=False)
        self.add_widget(self.theme_view_image)

        # Zawartość popup'u związanaego z przyciskiem "Settings"
        settings_popup_content = GridLayout(rows=4)
        settings_popup_content.add_widget(Label(text="Choose visual theme :", size_hint_y=0.3))
        buttons_layout = GridLayout(rows=1, size_hint_y=0.7)
        # Przyciski kolorów motywu
        buttons_layout.add_widget(ToggleButton(text="Violet", background_color=[1, 0, 1, 1], on_press=self.change_theme, group="theme_color"))
        buttons_layout.add_widget(ToggleButton(text="Blue", background_color=[0, 0, 1, 1], on_press=self.change_theme, group="theme_color"))
        buttons_layout.add_widget(ToggleButton(text="Orange", background_color=[1, 0.6, 0, 1], on_press=self.change_theme,group="theme_color"))
        # Dodatkowe kolory
        # buttons_layout.add_widget(ToggleButton(text="Green", background_color=[0, 1, 0, 1], on_press=self.change_theme, group="theme_color"))
        # buttons_layout.add_widget(ToggleButton(text="Red", background_color=[1, 0, 0, 1], on_press=self.change_theme, group="theme_color"))
        # buttons_layout.add_widget(ToggleButton(text="Yellow", background_color=[1, 1, 0, 1], on_press=self.change_theme, group="theme_color"))
        settings_popup_content.add_widget(buttons_layout)

        # Okno ustawień
        self.settings_popup = Popup(title="Settings", content=settings_popup_content,
                                    size_hint=[0.5, 0.8], background_color=[0.9, 0.7, 0.5, 0.5])

        settings_popup_content.add_widget(Label(text="Sort:", size_hint_y=0.3))
        sort_by_columns_layout = GridLayout(rows=5)
        sort_by_columns_layout.add_widget(ToggleButton(text="By addition time", group="sorters", on_press=self.actualize_sorting))
        sort_by_columns_layout.add_widget(ToggleButton(text="Alphabetically", group="sorters", on_press=self.actualize_sorting))
        sort_by_columns_layout.add_widget(ToggleButton(text="By date", group="sorters", on_press=self.actualize_sorting))
        sort_by_columns_layout.add_widget(Label())
        sort_by_columns_layout.add_widget(Button(text="Close", background_color=[1, 0.2, 0.2, 1], on_press=self.settings_popup.dismiss))
        settings_popup_content.add_widget(sort_by_columns_layout)

        self.settings_btn = Button(size_hint_x=0.2, on_release=self.settings_popup.open,
                                   background_normal="Images/settings_icon1_" + chosen_theme_color + ".jpg")
        self.add_widget(self.settings_btn)

    def change_theme(self, instance):
        plus_image = "Images/plus_sign2_" + instance.text + ".jpg"
        self.plus_btn.background_normal = plus_image

        settings_image = "Images/settings_icon1_" + instance.text + ".jpg"
        self.settings_btn.background_normal = settings_image

        theme_image = "Images/theme_" + instance.text + ".jpg"
        self.theme_view_image.source = theme_image
        # ^^poszukaj w google fajnych obrazków do środka navbar'u

        c.execute("UPDATE user_settings SET Theme_Color = ?", (instance.text,))
        conn.commit()

        global chosen_theme_color
        chosen_theme_color = instance.text

        event_cols_object.clear_widgets()
        event_cols_object.add_widget(EventCols3())

        footer_object.clear_widgets()
        footer_object.add_widget(Footer())

    def actualize_sorting(self, instance):
        c.execute("UPDATE user_settings SET Sorting = ?", (instance.text,))
        conn.commit()

        event_cols_object.clear_widgets()
        event_cols_object.add_widget(EventCols3())


class EventCols3(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 4
        self.rows = 6

        # Parametry nagłówków
        headlines_y = 0.15
        headlines_bg = "Images/headlines_" + chosen_theme_color + ".jpg"
        headlines_font_size = 20  # <- dostosuj fon_sizes, żeby pasowały na docelowym ekranie telefonu

        # Parametry rzędów z wyświetlanymi eventami
        rows_y = 0.2
        rows_font_size = 17
        delete_col_x = 0.2
        event_col_x = 0.5
        date_col_x = 0.5
        daysleft_col_x = 0.2

        # Nagłówki kolumn
        self.add_widget(Button(text="Delete", size_hint_x=delete_col_x, size_hint_y=headlines_y, disabled=True,
                               background_disabled_normal=headlines_bg, font_size=headlines_font_size))
        self.add_widget(Button(text="Event Name", size_hint_x=event_col_x, size_hint_y=headlines_y, disabled=True,
                               background_disabled_normal=headlines_bg, font_size=headlines_font_size))
        self.add_widget(Button(text="Date", size_hint_x=date_col_x, size_hint_y=headlines_y, disabled=True,
                               background_disabled_normal=headlines_bg, font_size=headlines_font_size))
        self.add_widget(Button(text="Days left", size_hint_x=daysleft_col_x, size_hint_y=headlines_y, disabled=True,
                               background_disabled_normal=headlines_bg, font_size=headlines_font_size))

        # Wyświetlana zawartość kolumn
        self.amount_of_displayed_rows = self.rows - 1  # <- -1, bo jeden rząd zajmują nagłówki

        # Wybrany sposób sortowania wyśtwietlanych eventów
        c.execute("SELECT Sorting FROM user_settings")
        chosen_sorting = c.fetchone()[0]

        displayed_data = []
        if chosen_sorting == "By addition time":
            c.execute("SELECT * FROM user_events LIMIT ? OFFSET ?", (self.amount_of_displayed_rows, current_row_number))
            displayed_data = c.fetchall()
        elif chosen_sorting == "Alphabetically":
            c.execute("SELECT * FROM user_events ORDER BY LOWER(event_name) LIMIT ? OFFSET ?",
                      (self.amount_of_displayed_rows, current_row_number))
            displayed_data = c.fetchall()
        elif chosen_sorting == "By date":
            c.execute("SELECT * FROM user_events ORDER BY DATE(event_date) LIMIT ? OFFSET ?",
                      (self.amount_of_displayed_rows, current_row_number))
            displayed_data = c.fetchall()
            # zadbaj o kosmetykę (ładniejsze czcionki, tła itp.)
            # Zobacz czy jest wystarczająca liczba komentarzy

        for row in displayed_data:
            self.add_widget(Button(id=str(row[0]), on_press=self.delete_row, size_hint_x=delete_col_x,
                                   size_hint_y=rows_y, background_normal='Images/trash_can_icon4.png'))
            self.add_widget(Label(text=str(row[1]), size_hint_x=event_col_x, size_hint_y=rows_y, font_size=rows_font_size))

            saved_date = ""
            desired_date_format = "-"
            if row[2] != "-":
                saved_date = datetime.strptime(row[2], "%Y-%m-%d")  # <- date object created from a string
                desired_date_format = saved_date.strftime("%d - %m - %Y")  # <- tu możesz zmienić format wyświetlania
            self.add_widget(Label(text=desired_date_format, size_hint_x=date_col_x, size_hint_y=rows_y, font_size=rows_font_size))

            time_left = "-"
            if row[2] != "-":
                time_left = (saved_date - datetime.now()).days
            self.add_widget(Label(text=str(time_left), size_hint_x=daysleft_col_x, size_hint_y=rows_y, font_size=rows_font_size))

        if len(displayed_data) < self.rows - 1:
            amount_of_labels = self.rows - 1 - len(displayed_data)
            for i in range(amount_of_labels):
                self.add_widget(Label(size_hint_x=delete_col_x, size_hint_y=rows_y))
                self.add_widget(Label(size_hint_x=event_col_x, size_hint_y=rows_y))
                self.add_widget(Label(size_hint_x=date_col_x, size_hint_y=rows_y))
                self.add_widget(Label(size_hint_x=daysleft_col_x, size_hint_y=rows_y))

    def delete_row(self, instance):
        c.execute("DELETE FROM user_events WHERE idx = (?)", (int(instance.id),))
        conn.commit()

        event_cols_object.clear_widgets()
        event_cols_object.add_widget(EventCols3())


class Footer(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.size_hint_y = 0.1

        # Przyciski do scrolowania wyświetlanych eventów
        self.add_widget(Button(id="btn_page_up", on_press=self.scroll_page, background_normal="Images/page_up_" + chosen_theme_color + ".jpg"))
        self.add_widget(Button(id="btn_one_up", on_press=self.scroll_page, background_normal="Images/one_up_" + chosen_theme_color + ".jpg"))
        self.add_widget(Button(id="btn_one_down", on_press=self.scroll_page, background_normal="Images/one_down_" + chosen_theme_color + ".jpg"))
        self.add_widget(Button(id="btn_page_down", on_press=self.scroll_page, background_normal="Images/page_down_" + chosen_theme_color + ".jpg"))

    # Funkcja scrolowania eventów. Wykorzystuje OFFSET do ustalenia pozycji rzędu
    def scroll_page(self, instance):
        global current_row_number

        the_limit = EventCols3().amount_of_displayed_rows

        c.execute("SELECT COUNT(*) FROM user_events")
        amount_of_events = c.fetchone()[0]

        if current_row_number >= 0:
            if instance.id == "btn_one_up":
                current_row_number -= 1
                if current_row_number < 0:  # <- ten warunek służy do ograniczenia nadmiernego przewijania
                    current_row_number = 0

            elif instance.id == "btn_page_up":
                current_row_number -= the_limit
                if current_row_number < 0:
                    current_row_number = 0

        if current_row_number < amount_of_events:
            if instance.id == "btn_one_down":
                current_row_number += 1
                if current_row_number > amount_of_events:
                    current_row_number = amount_of_events

            elif instance.id == "btn_page_down":
                current_row_number += the_limit
                if current_row_number > amount_of_events:
                    current_row_number = amount_of_events

        global event_cols_object
        event_cols_object.clear_widgets()
        event_cols_object.add_widget(EventCols3())


class MainPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 3

        self.add_widget(NavBar())

        global event_cols_object
        event_cols_object = EventCols3()  # <- ta zmienna utworzona w celu aktualizacji z zewnątrz
        self.add_widget(event_cols_object)

        global footer_object
        footer_object = Footer()
        self.add_widget(footer_object)


class MyApp(App):
    title = "The Maciej Calendar"

    def build(self):
        return MainPage()


if __name__ == '__main__':
    MyApp().run()

    c.close()
    conn.close()
