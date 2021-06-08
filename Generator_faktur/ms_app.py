# Python version 3.8 (64-bit)
# built-in libraries
from tkinter import *
from tkinter import messagebox
import sqlite3
from datetime import date
import codecs
import os.path
# custom libraries
from numbers_to_words import numbers_to_words
from xml_file_matrix import new_xml_file_content
from ms_fpdf_printing import create_pdf_file, two_zeros_format


todays_date = date.today()

# ACCESSING DATABASE...
# Checking if database is accessed for the first time
data_base_exists = False
if os.path.isfile('faktury.db'):
    data_base_exists = True

# Połączenie z bazą danych
connection = sqlite3.connect('faktury.db')
cursor = connection.cursor()


def create_db_tables():
    cursor.execute('''CREATE TABLE users
                   (name TEXT, address TEXT, city TEXT, nip INTEGER, phone INTEGER, item_name TEXT, item_measure TEXT, account_number TEXT)''')
    cursor.execute('INSERT INTO users VALUES ("", "", "", "", "", "", "", "")')
    # ^^Przy tworzeniu bazy danych dodaje pusty rząd, bo GUI nie może przyjmować wartości None

    cursor.execute('''CREATE TABLE clients
                   (client_name TEXT, client_address TEXT, client_nip INTEGER, client_phone INTEGER, client_email TEXT)''')

    cursor.execute('''CREATE TABLE sales
                   (sequence_number TEXT, client_name TEXT, client_address TEXT,
                    client_nip INTEGER, date TEXT, netto REAL, vat REAL, payment TEXT)''')

    cursor.execute('''CREATE TABLE sold_items
                   (item_name TEXT, quantity INTEGER, netto REAL, vat REAL, sale_sequence_number TEXT)''')


# Jeśli przed włączeniem programu baza danych nie istniała to odpali się funkcja tworząca wszystkie potrzebne tabele
if not data_base_exists:
    create_db_tables()

cursor.execute('SELECT * FROM users')
current_user_data = cursor.fetchone()
# ^^Jest tylko jeden rząd w tej tabeli z danymi użytkownika, więc można użyć *

# GUI
# Root and it's configuration
window = Tk()
window.title("Generator Faktur")
window.geometry("1000x700")

# Widgets
user_data_label = Label(window, pady=8, text=("Sprzedawca:\n" + current_user_data[0] + "\n Adres: "
                                              + current_user_data[1] + "\n NIP: " + str(current_user_data[3])
                                              + "\n Telefon: " + str(current_user_data[4])))
user_data_label.grid(row=0, column=0)


# Okno edycji danych sprzedawcy
def edit_seller_data():
    # Otworzenie okna rejestracji danych sprzedawcy
    register_window = Toplevel(window)
    register_window.title("Generator Faktur - Edytuj dane sprzedawcy")

    Label(register_window,
          text="Wypełnij poniższe pola danymi swojej firmy,\nktóre chcesz przedstawiać na swoich fakturach", pady=5,
          fg="white", bg="#026dba", font=('Arial', 12)).pack(ipadx=40)

    Label(register_window, text="Nazwa firmy: *").pack()
    company_name = Entry(register_window, width=40)
    company_name.pack(pady=5)

    Label(register_window, text="Adres firmy: *").pack()
    company_address = Entry(register_window, width=40)
    company_address.pack(pady=5)

    Label(register_window, text="Miejscowość: *").pack()
    company_city = Entry(register_window, width=40)
    company_city.pack(pady=5)

    Label(register_window, text="NIP: *").pack()
    company_nip = Entry(register_window, width=40)
    company_nip.pack(pady=5)

    Label(register_window, text="Telefon: *").pack()
    company_phone = Entry(register_window, width=40)
    company_phone.pack(pady=5)

    Label(register_window, text="Domyślna nazwa towaru: ").pack()
    company_default_item = Entry(register_window, width=40)
    company_default_item.pack(pady=5)

    Label(register_window, text="Domyślna miara towaru: ").pack()
    company_default_measure = Entry(register_window, width=40)
    company_default_measure.pack(pady=5)

    Label(register_window, text="Numer konta: ").pack()
    company_account_number = Entry(register_window, width=40)
    company_account_number.pack(pady=5)

    # Póki co zmiana stawki niepotrzebna, ale w razie rozbudowy programu można dodać
    # Label(register_window, text="Stawka vat: ").pack()
    # default_vat_value = StringVar(register_window)
    # default_vat_value.set("23%")
    # company_default_vat = OptionMenu(register_window, default_vat_value, "8%", "5%")
    # company_default_vat.pack()

    Label(register_window, text="* Wypełnienie pól oznaczonych gwiazdkami\n"
                                "jest konieczne do poprawnego wypełniania faktur.", font=('Arial', 8)).pack()

    # Lista pól z danymi rejestracji
    entries_lst = [company_name, company_address, company_city, company_nip, company_phone,
                   company_default_item, company_default_measure, company_account_number]
    # Wypełnienie pól aktualnymi danymi użytkownika/sprzedawcy z bazy danych
    for entry_obj, value in zip(entries_lst, current_user_data):
        entry_obj.insert(0, str(value))

    def verify_registration_data():
        # Zebranie danych z pól rejestracji jako str
        entries_values_lst = [i.get() for i in entries_lst]
        # Aktualizacja bazy danych
        cursor.execute("DELETE FROM users")
        # ^^w tej tabeli zawsze ma być tylko jeden rząd, więc można skasować jej całą zawartość
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", entries_values_lst)
        connection.commit()
        register_window.destroy()
        messagebox.showinfo("Sukces!", "Dane zostały zapisane."
                                       "\nZmiany będą widoczne po ponownym uruchomieniu programu.")

    Button(register_window, text="Zapisz", font=('Arial', 14), fg="white", bg="#318c1f",
           command=verify_registration_data).pack(pady=20)


Button(window, text="Edytuj dane sprzedawcy", command=edit_seller_data).grid(row=1, column=0)

# Numer faktury
sequence_number_frame = Frame(window)
new_sequence_number_label = Label(sequence_number_frame, text="Faktura Nr", font=('Courier', 25))
new_sequence_number_label.pack()
new_sequence_number_entry = Entry(sequence_number_frame, width=10, font=('Courier', 25), justify="center")
new_sequence_number_entry.pack()

sequence_number_frame.grid(row=0, column=1)

date_label = Label(window, padx=20, font=('Arial', 12), text="Miejscowość: " + current_user_data[2]
                                                             + "\nData wystawienia faktury: " + str(todays_date))
date_label.grid(row=0, column=2)

client_role_label = Label(window, font=('Arial', 14), text="      Nabywca:")
client_role_label.grid(row=1, column=1, sticky="w")


# Otwieranie okna wyszukiwania klientów
def find_client():
    # Tworzenie okna i jego konfiguracja
    client_window = Toplevel(window)
    client_window.geometry("1100x500")
    client_window.title("Generator Faktur - Znajdź klienta")
    client_window.resizable(False, False)

    # Pasek wyszukiwania klientów
    search_bar = Entry(client_window, width=38, font=('Arial', 18))
    search_bar.grid(row=0, column=0, columnspan=3, sticky="w", padx=20, pady=20)

    def select_client(chosen_client_table_row):
        # Oczyszczenie zawartości pól po ewentaulnych poprzednich klientach
        client_name_entry.delete(0, 'end')
        client_address_entry.delete(0, 'end')
        client_nip_entry.delete(0, 'end')
        # Uzupełnienie pól nowo wybranymi danymi klienta
        client_name_entry.insert(0, chosen_client_table_row[0])
        client_address_entry.insert(0, chosen_client_table_row[1])
        client_nip_entry.insert(0, chosen_client_table_row[2])
        # Zamknięcie okna
        client_window.destroy()

    def remove_client_data(chosen_client_nip):
        if messagebox.askokcancel(title="Usuwanie klienta", message="Czy na pewno chcesz usunąć tego klienta?"):
            cursor.execute('DELETE FROM clients WHERE client_nip =?', (chosen_client_nip,))
            connection.commit()
            client_window.destroy()
            messagebox.showinfo(title="Sukces!", message="Wybrany klient został usunięty.")

    # Wyszukaj klientów
    def search_clients_table():
        # Wyczyszenie wyświetlacza z ewentualnych poprzednio wyświetlanych rezultatów
        clients_inside_frame.destroy()
        create_displayer()
        # Pobranie treści z pola wyszukiwania i znalazenie dopasowań w bazie danych
        searching_clue = "%" + search_bar.get() + "%"
        cursor.execute('SELECT * FROM clients WHERE client_name LIKE ? OR client_address LIKE ? OR client_nip LIKE ? '
                       'OR client_email LIKE ? ORDER BY client_name', (searching_clue, searching_clue,
                                                                       searching_clue, searching_clue, ))
        rows_to_show = cursor.fetchall()
        # Wyświetlenie znalezionych dopasowań
        for row_to_show_idx, row_to_show in enumerate(rows_to_show):
            Label(clients_inside_frame, text=row_to_show[0]).grid(row=row_to_show_idx + 1, column=0)
            Label(clients_inside_frame, text=row_to_show[1]).grid(row=row_to_show_idx + 1, column=1)
            Label(clients_inside_frame, text=row_to_show[2]).grid(row=row_to_show_idx + 1, column=2)
            Label(clients_inside_frame, text=row_to_show[3]).grid(row=row_to_show_idx + 1, column=3)
            Label(clients_inside_frame, text=row_to_show[4]).grid(row=row_to_show_idx + 1, column=4)
            Button(clients_inside_frame, text="Wybierz", bg="#026dba", fg="white", command=lambda x=row_to_show: select_client(x)).grid(row=row_to_show_idx + 1, column=5)
            Button(clients_inside_frame, text="Usuń", bg="#990000", fg="white", command=lambda x=row_to_show[2]: remove_client_data(x)).grid(row=row_to_show_idx + 1, column=6)

    search_bar_action_button = Button(client_window, text=" Wyszukaj ", font=('Arial', 12), command=search_clients_table, fg="white", bg="#575c56")
    search_bar_action_button.grid(row=0, column=2, sticky="e")

    # Po kliknięciu przycisku otwiera okno, które po wpisaniu danych dodaje nowego klienta do bazy danych
    def add_new_client():
        # Tworzenie okna
        new_client_window = Toplevel(window)
        new_client_window.geometry("580x400")
        new_client_window.title("Generator Faktur - Dodaj nowego klienta")

        # Headline
        Label(new_client_window, font=('Arial', 18), text="Dodawanie nowego klienta").grid(row=0, column=1, padx=10, pady=10)
        # Nazwa
        Label(new_client_window, font=('Arial', 14), text="Nazwa: ").grid(row=1, column=0, padx=10, pady=10)
        new_client_name_entry = Entry(new_client_window, width=30, font=('Arial', 19))
        new_client_name_entry.grid(row=1, column=1)
        # Adres
        Label(new_client_window, font=('Arial', 14), text="Adres: ").grid(row=2, column=0, padx=10, pady=10)
        new_client_address_entry = Entry(new_client_window, width=30, font=('Arial', 19))
        new_client_address_entry.grid(row=2, column=1)
        # NIP
        Label(new_client_window, font=('Arial', 14), text="NIP: ").grid(row=3, column=0, padx=10, pady=10)
        new_client_nip_entry = Entry(new_client_window, width=30, font=('Arial', 19))
        new_client_nip_entry.grid(row=3, column=1)
        # Telefon
        Label(new_client_window, font=('Arial', 14), text="Telefon* : ").grid(row=4, column=0, padx=10, pady=10)
        new_client_phone_entry = Entry(new_client_window, width=30, font=('Arial', 19))
        new_client_phone_entry.grid(row=4, column=1)
        # E-mail
        Label(new_client_window, font=('Arial', 14), text="E-mail* : ").grid(row=5, column=0, padx=10, pady=10)
        new_client_email_entry = Entry(new_client_window, width=30, font=('Arial', 19))
        new_client_email_entry.grid(row=5, column=1)
        # Adnotacja
        Label(new_client_window, text="* Dodawanie telefonu oraz e-mail'u jest opcjonalne").grid(row=6, column=1, sticky="w")

        # Anuluj - zamknij okno dodawania nowego klienta
        Button(new_client_window, text="Anuluj", font=('Arial', 14), fg="white", bg="#575c56", command=new_client_window.destroy).grid(row=7, column=1, padx=60, pady=20, sticky="w")

        # Zapisz - dodaj dane klienta do bazy danych
        def save_client_data():
            # Zamiana inputu użytkownika na format 10-cio cyfrowy
            nip_to_save = "".join([digit for digit in new_client_nip_entry.get() if digit.isdigit()])

            # Zebranie danych z form wypełnionych przez użytkownika
            new_client_data_tuple = (new_client_name_entry.get(), new_client_address_entry.get(),
                                     nip_to_save, new_client_phone_entry.get(), new_client_email_entry.get(), )

            # Weryfikacja treści wprowadzonych przez użytkownika
            if len(new_client_data_tuple[0]) < 1 or len(new_client_data_tuple[0]) > 200:
                messagebox.showwarning(title="Błędna Nazwa", message="Przekroczono limit znaków.")
            elif len(new_client_data_tuple[1]) < 1 or len(new_client_data_tuple[1]) > 200:
                messagebox.showwarning(title="Błędny Adres", message="Przekroczono limit znaków.")
            elif len(nip_to_save) != 10:
                messagebox.showwarning(title="Błędny NIP", message="Wpisany przez Ciebie NIP jest niepoprawny.")
            elif len(new_client_data_tuple[3]) > 20:
                messagebox.showwarning(title="Błędny numer telefonu", message="Przekroczono limit znaków.")
            else:
                # Dodawanie danych klienta do bazy SQL
                cursor.execute('INSERT INTO clients VALUES (?, ?, ?, ?, ?)', new_client_data_tuple)
                connection.commit()
                messagebox.showinfo(title="Sukces!", message="Nowy klient został zapisany.")
                new_client_window.destroy()

        Button(new_client_window, text="Zapisz", font=('Arial', 14), fg="white", bg="#026dba", command=save_client_data).grid(row=7, column=1, padx=60, pady=20, sticky="e")

    # Przycisk otwiera okno nowego klienta
    add_new_client_button = Button(client_window, text=" Dodaj nowego + ", font=('Arial', 12), command=add_new_client, fg="white", bg="#318c1f")
    add_new_client_button.grid(row=0, column=3, padx=80)

    # Wyświetlacz wyników wyszukiwania klientów
    def create_displayer():
        clients_lst_frame = Frame(client_window)
        clients_lst_frame.grid(row=2, column=0, columnspan=5, sticky="w")

        # Scrollbar & canvas
        clients_lst_canvas = Canvas(clients_lst_frame, width=1080, height=400)
        clients_scroll = Scrollbar(clients_lst_frame, orient="vertical", command=clients_lst_canvas.yview)
        global clients_inside_frame
        clients_inside_frame = Frame(clients_lst_canvas)
        clients_lst_canvas.configure(yscrollcommand=clients_scroll.set)
        clients_lst_canvas.grid(row=2, column=0)
        clients_scroll.grid(row=2, column=8, sticky="NS")
        clients_inside_frame.bind("<Configure>",
                                  lambda e: clients_lst_canvas.configure(scrollregion=clients_lst_canvas.bbox("all")))
        clients_lst_canvas.create_window((0, 0), window=clients_inside_frame, anchor="nw")

        # Nagłówki kolumn
        Label(clients_inside_frame, text="Nazwa", bg="#9900cc", fg="white", width=25, height=2, font=('Arial', 12)).grid(row=0, column=0)
        Label(clients_inside_frame, text="Adres", bg="#9900cc", fg="white", width=25, height=2, font=('Arial', 12)).grid(row=0, column=1)
        Label(clients_inside_frame, text="NIP", bg="#9900cc", fg="white", width=15, height=2, font=('Arial', 12)).grid(row=0, column=2)
        Label(clients_inside_frame, text="Telefon", bg="#9900cc", fg="white", width=15, height=2, font=('Arial', 12)).grid(row=0, column=3)
        Label(clients_inside_frame, text="E-mail", bg="#9900cc", fg="white", width=25, height=2, font=('Arial', 12)).grid(row=0, column=4)

    create_displayer()


search_client_button = Button(window, text="Wyszukaj klienta", command=find_client)
search_client_button.grid(row=3, column=0, sticky="w", padx=35)


def delete_facture(seq_num, browse_factures_window_obj):
    if messagebox.askyesno(title="Usuń wybraną fakture", message="Czy na pewno chcesz usunąć fakture o numerze "
                                                                 + str(seq_num) + " ?"):
        cursor.execute('DELETE FROM sales WHERE sequence_number =?', (seq_num, ))
        connection.commit()
        # Zamyka przeglądarkę faktur
        browse_factures_window_obj.destroy()


def browse_factures():
    browse_factures_window = Toplevel(window)
    # browse_factures_window.geometry("580x400")
    browse_factures_window.title("Generator Faktur - Przeglądaj faktury")
    factures_search_bar = Entry(browse_factures_window, width=25, font=('Arial', 18))
    factures_search_bar.grid(row=0, column=0, sticky="w", padx=20, pady=20)

    default_month_value = StringVar(browse_factures_window)
    default_month_value.set("Miesiąc")
    month_menu = OptionMenu(browse_factures_window, default_month_value, "Styczeń", "Luty", "Marzec", "Kwiecień", "Maj",
                            "Czerwiec", "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień")
    month_menu.grid(row=0, column=2)

    default_year_value = StringVar(browse_factures_window)
    default_year_value.set("Rok")
    year_menu = OptionMenu(browse_factures_window, default_year_value, "2020", "2021", "2022", "2023", "2024", "2025",
                                                                       "2026", "2027", "2028", "2029", "2030", "2031")
    year_menu.grid(row=0, column=3)

    month_dict = {"Styczeń": "01", "Luty": "02", "Marzec": "03", "Kwiecień": "04", "Maj": "05", "Czerwiec": "06",
                  "Lipiec": "07", "Sierpień": "08", "Wrzesień": "09", "Październik": "10", "Listopad": "11",
                  "Grudzień": "12", "Miesiąc": ""}

    # Pole do wyświetlania faktur
    factures_frame = Frame(browse_factures_window)
    factures_frame.grid(row=2, column=0, columnspan=4)

    def display_factures():
        # Scrollbar & canvas
        factures_canvas = Canvas(factures_frame, width=950, height=500)
        factures_scroll = Scrollbar(factures_frame, orient="vertical", command=factures_canvas.yview)
        factures_inside_frame = Frame(factures_canvas)
        factures_canvas.configure(yscrollcommand=factures_scroll.set)
        factures_canvas.grid(row=2, column=0)
        factures_scroll.grid(row=2, column=8, sticky="NS")
        factures_inside_frame.bind("<Configure>",
                                   lambda e: factures_canvas.configure(scrollregion=factures_canvas.bbox("all")))
        factures_canvas.create_window((0, 0), window=factures_inside_frame, anchor="nw")

        # Nagłówki kolumn
        Label(factures_inside_frame, text="Numer\nfaktury", font="Arial 10 bold", width=10).grid(row=1, column=0,
                                                                                                 padx=5)
        Label(factures_inside_frame, text="Nazwa", font="Arial 10 bold", width=10).grid(row=1, column=1, padx=5)
        Label(factures_inside_frame, text="Adres", font="Arial 10 bold", width=10).grid(row=1, column=2, padx=5)
        Label(factures_inside_frame, text="NIP", font="Arial 10 bold", width=10).grid(row=1, column=3, padx=5)
        Label(factures_inside_frame, text="Data", font="Arial 10 bold", width=10).grid(row=1, column=4, padx=5)
        Label(factures_inside_frame, text="NETTO", font="Arial 10 bold", width=10).grid(row=1, column=5, padx=5)
        Label(factures_inside_frame, text="VAT", font="Arial 10 bold", width=10).grid(row=1, column=6, padx=5)
        Label(factures_inside_frame, text="Forma\npłatności", font="Arial 10 bold", width=10).grid(row=1, column=7,
                                                                                                   padx=5)

        # Pobieranie i obróbka inputu z pól Miesiąc i Rok
        chosen_factures_month = month_dict[default_month_value.get()]
        chosen_factures_year = default_year_value.get()
        if chosen_factures_year == "Rok":
            chosen_factures_year = ""
        date_range_to_search = "%" + chosen_factures_year + "-" + chosen_factures_month + "%"
        # Pobranie treści z pola wyszukiwania i znalazenie dopasowań w bazie danych
        searching_facture_clue = "%" + factures_search_bar.get() + "%"
        cursor.execute('SELECT * FROM sales WHERE (sequence_number LIKE ? OR client_name LIKE ? OR client_nip LIKE ?) '
                       'AND date LIKE ? ORDER BY date', (searching_facture_clue, searching_facture_clue,
                                                         searching_facture_clue, date_range_to_search, ))
        factures_to_show = cursor.fetchall()
        # Wyświetlanie faktur
        for facture_idx, facture in enumerate(factures_to_show):
            facture_idx += 2
            # ^^Wyświetlanie faktur zaczyna się od 2-go rzędu gridu, dltego trzeba dodać 2 do indeksu faktury
            for facture_column_idx in range(len(facture)):
                Label(factures_inside_frame, text=facture[facture_column_idx]).grid(row=facture_idx, column=facture_column_idx, padx=5)
            delete_facture_button = Button(factures_inside_frame, text="Usuń", fg="white", bg="#990000",
                                           command=lambda x=facture[0], y=browse_factures_window: delete_facture(x, y))
            delete_facture_button.grid(row=facture_idx, column=8, padx=10)

    factures_search_bar_action_button = Button(browse_factures_window, text="Wyszukaj", command=display_factures,
                                               fg="white", bg="#575c56", font=('Arial', 12))
    factures_search_bar_action_button.grid(row=0, column=1)


browse_factures_button = Button(window, text="Przeglądaj faktury", command=browse_factures)
browse_factures_button.grid(row=4, column=0, sticky="w", padx=35)

# Nazwa klienta
client_name_label = Label(window, font=('Arial', 14), text="Imię i nazwisko lub nazwa: ")
client_name_label.grid(row=2, column=0, sticky="e")
client_name_entry = Entry(window, width=40, font=('Arial', 19))
client_name_entry.grid(row=2, column=1, columnspan=2)

# Adres klienta
client_name_label = Label(window, font=('Arial', 14), text="Adres: ")
client_name_label.grid(row=3, column=0, sticky="e")
client_address_entry = Entry(window, width=40, font=('Arial', 19))
client_address_entry.grid(row=3, column=1, columnspan=2)

# NIP klienta
client_name_label = Label(window, font=('Arial', 14), text="NIP: ")
client_name_label.grid(row=4, column=0, sticky="e")
client_nip_entry = Entry(window, width=40, font=('Arial', 19))
client_nip_entry.grid(row=4, column=1, columnspan=2)

# Lista zakupów
sold_items_frame = Frame(window, padx=20, pady=15)

labels_lst = ['Lp.', 'Nazwa (rodzaj) towaru lub usługi\n(zakres wykonanych usług)',
              'Miara', 'Ilość', 'Cena\njednostkowa\nbez podatku (zł)',
              'Wartość\ntowarów (usług)\nbez podatku (zł)', 'Stawka\npodatku (%)',
              'Kwota\npodatku (zł)', 'Wartość\ntowarów (usług)\nwraz z podatkiem (zł)']

for idx, col_name in enumerate(labels_lst):
    sold_items_label = Label(sold_items_frame, text=col_name)
    sold_items_label.grid(row=0, column=idx)

# Listy obiektów Entry dla ułatwienia wypełniania ich wartościami
sold_items_lp_lst = []
sold_items_nazwa_lst = []
sold_items_miara_lst = []
sold_items_ilosc_lst = []
sold_items_cena_lst = []
sold_items_wartosc_lst = []
sold_items_stawka_lst = []
sold_items_kwota_podatku_lst = []
sold_items_cena_wartosc_z_podatkiem_lst = []


# Trzeba pomnożyć ilość przez cenę jednostkową, żeby wyszła "wartość"
def count_total():
    # Automatycznie wprowadzany numer faktury
    current_year = (str(todays_date.year) + "-%",)
    cursor.execute('SELECT COUNT(*) FROM sales WHERE date LIKE ?', current_year)
    yearly_factures_count = cursor.fetchone()
    new_sequence_number = str(yearly_factures_count[0] + 1) + "/F/" + str(todays_date.year)[-2:]
    new_sequence_number_entry.delete(0, 'end')
    new_sequence_number_entry.insert(0, new_sequence_number)

    added_value_23 = 0
    added_tax = 0
    for price_idx, price in enumerate(sold_items_cena_lst):
        # Jeśli ilość nie zostanie wpisana, domyślnie wstawi wartość 1
        amount = sold_items_ilosc_lst[price_idx].get()
        if amount == "":
            amount = 1
        # Jeśli cena nie zostanie wpisana, nie będzie sprawdzał późniejszych pól
        the_price = price.get()
        if the_price == "":
            break

        value = two_zeros_format(float(amount) * float(the_price))
        added_value_23 += float(value)

        # Automatyczne wypełnianie wartości w kolumnach
        sold_items_lp_lst[price_idx].delete(0, 'end')  # <-usuwa poprzednią wartość jeśli została wpisana
        sold_items_lp_lst[price_idx].insert(0, str(price_idx + 1))

        sold_items_nazwa_lst[price_idx].delete(0, 'end')
        sold_items_nazwa_lst[price_idx].insert(0, current_user_data[5])

        sold_items_miara_lst[price_idx].delete(0, 'end')
        sold_items_miara_lst[price_idx].insert(0, current_user_data[6])

        sold_items_wartosc_lst[price_idx].delete(0, 'end')
        sold_items_wartosc_lst[price_idx].insert(0, value)

        sold_items_stawka_lst[price_idx].delete(0, 'end')
        sold_items_stawka_lst[price_idx].insert(0, "23")

        tax_amount = two_zeros_format(float(value) * 0.23)
        added_tax += float(tax_amount)
        sold_items_kwota_podatku_lst[price_idx].delete(0, 'end')
        sold_items_kwota_podatku_lst[price_idx].insert(0, str(tax_amount))

        value_with_tax = two_zeros_format(float(value) + float(tax_amount))
        sold_items_cena_wartosc_z_podatkiem_lst[price_idx].delete(0, 'end')
        sold_items_cena_wartosc_z_podatkiem_lst[price_idx].insert(0, value_with_tax)

        wartosc_23.delete(0, 'end')
        wartosc_23.insert(0, two_zeros_format(added_value_23))
        wartosc_razem.delete(0, 'end')
        wartosc_razem.insert(0, two_zeros_format(added_value_23))  # <-tu wstawiamy tą samą wartość, bo wszystkie pola mają stawkę 23

        kwota_podatku_23.delete(0, 'end')
        kwota_podatku_23.insert(0, str(round(added_tax, 2)))
        kwota_podatku_razem.delete(0, 'end')
        kwota_podatku_razem.insert(0, str(round(added_tax, 2)))

        added_value_with_tax = float(added_value_23) + float(added_tax)
        wartosc_z_podatkiem_23.delete(0, 'end')
        wartosc_z_podatkiem_23.insert(0, two_zeros_format(added_value_with_tax))
        wartosc_z_podatkiem_razem.delete(0, 'end')
        wartosc_z_podatkiem_razem.insert(0, two_zeros_format(added_value_with_tax))

        # Wyświetlanie danych do przelwu jeśli został wybrany jako forma płatności
        if default_payment.get() == "Przelew":
            payment_account_label = Label(payment_frame, text="Nr konta:")
            payment_account_label.grid(row=1, column=0)
            nr_konta = current_user_data[7]
            payment_account_entry = Label(payment_frame, text=nr_konta, padx=payment_data_entry_padx)
            payment_account_entry.grid(row=1, column=1, columnspan=2, sticky=W)

            payment_amount_label = Label(payment_frame, text="Do zapłaty: ")
            payment_amount_label.grid(row=2, column=0)
            payment_amount_entry = Entry(payment_frame, width=payment_data_entry_width)
            payment_amount_entry.grid(row=2, column=1, columnspan=2, padx=payment_data_entry_padx)

            payment_written_label = Label(payment_frame, text="Słownie: ")
            payment_written_label.grid(row=3, column=0)
            payment_written_entry = Entry(payment_frame, width=payment_data_entry_width)
            payment_written_entry.grid(row=3, column=1, columnspan=2)

            payment_amount_entry.delete(0, 'end')
            payment_amount_entry.insert(0, two_zeros_format(added_value_with_tax))
            payment_written_entry.delete(0, 'end')
            payment_written_entry.insert(0, numbers_to_words(float(two_zeros_format(added_value_with_tax))))


for row in range(1, 10):
    sold_items_lp = Entry(sold_items_frame, width=5, justify="center")
    sold_items_lp.grid(row=row, column=0)
    sold_items_lp_lst.append(sold_items_lp)

    sold_items_nazwa = Entry(sold_items_frame, width=40, justify="center")
    sold_items_nazwa.grid(row=row, column=1)
    sold_items_nazwa_lst.append(sold_items_nazwa)

    sold_items_miara = Entry(sold_items_frame, width=10, justify="center")
    sold_items_miara.grid(row=row, column=2)
    sold_items_miara_lst.append(sold_items_miara)

    sold_items_ilosc = Entry(sold_items_frame, width=10, justify="center")
    sold_items_ilosc.grid(row=row, column=3)
    sold_items_ilosc_lst.append(sold_items_ilosc)

    sold_items_cena = Entry(sold_items_frame, width=18, justify="center")
    sold_items_cena.grid(row=row, column=4)
    sold_items_cena_lst.append(sold_items_cena)

    sold_items_wartosc = Entry(sold_items_frame, width=18, justify="center")
    sold_items_wartosc.grid(row=row, column=5)
    sold_items_wartosc_lst.append(sold_items_wartosc)

    sold_items_stawka = Entry(sold_items_frame, width=15, justify="center")
    sold_items_stawka.grid(row=row, column=6)
    sold_items_stawka_lst.append(sold_items_stawka)

    sold_items_kwota_podatku = Entry(sold_items_frame, width=18, justify="center")
    sold_items_kwota_podatku.grid(row=row, column=7)
    sold_items_kwota_podatku_lst.append(sold_items_kwota_podatku)

    sold_items_cena_wartosc_z_podatkiem = Entry(sold_items_frame, width=20, justify="center")
    sold_items_cena_wartosc_z_podatkiem.grid(row=row, column=8)
    sold_items_cena_wartosc_z_podatkiem_lst.append(sold_items_cena_wartosc_z_podatkiem)

    if row == 1:
        sold_items_stawka.insert(0, "23")
        sold_items_lp.insert(0, "1")

sold_items_frame.grid(row=5, column=0, columnspan=3)

# Dane do zapłaty
payment_frame = Frame(window)
payment_data_entry_width = 60
payment_data_entry_padx = 30

payment_label = Label(payment_frame, text="Sposób zapłaty: ")
payment_label.grid(row=0, column=0)
default_payment = StringVar(payment_frame)
default_payment.set("Gotówka")
payment_menu = OptionMenu(payment_frame, default_payment, "Gotówka", "Przelew")
payment_menu.grid(row=0, column=1)
payment_time_label = Label(payment_frame, text="Termin zapłaty: 14 dni")
payment_time_label.grid(row=0, column=2)

# Zestawienie sprzedaży według stawek podatku
zestawienie_label = Label(payment_frame, text="Zestawienie sprzedaży wg stawek podatku:")
zestawienie_label.grid(row=0, column=3, columnspan=4, sticky="w")

wartosc_entry_width = 18
wartosc_23 = Entry(payment_frame, width=wartosc_entry_width)
wartosc_23.grid(row=1, column=3)

stawki_procentowe = [23, ]
# ^^ można dodać do listy stawki o wartościach [8, 5, 0, zw] ale póki co jest to zbędne
for row_idx, stawka in enumerate(stawki_procentowe):
    if type(stawka) is int:
        stawka = str(stawka) + "%"

    wartosc_stawka = Label(payment_frame, text=stawka, width=13)
    wartosc_stawka.grid(row=row_idx+1, column=4)

kwota_podatku_entry_width = 18
kwota_podatku_23 = Entry(payment_frame, width=kwota_podatku_entry_width)
kwota_podatku_23.grid(row=1, column=5)

wartosc_z_podatkiem_entry_width = 20
wartosc_z_podatkiem_23 = Entry(payment_frame, width=wartosc_z_podatkiem_entry_width)
wartosc_z_podatkiem_23.grid(row=1, column=6)

# Pusty label, żeby nie przesuwało kolumn w lewo, gdy znikają dane z przelewu
empty_fill_label = Label(payment_frame, width=payment_data_entry_width)
empty_fill_label.grid(row=2, column=1, columnspan=2)

# Razem
total_amount_label = Label(payment_frame, text="Razem: ")
total_amount_label.grid(row=2, column=3, columnspan=4, sticky="w")

wartosc_razem = Entry(payment_frame, width=wartosc_entry_width)
wartosc_razem.grid(row=3, column=3)

kwota_podatku_razem = Entry(payment_frame, width=kwota_podatku_entry_width)
kwota_podatku_razem.grid(row=3, column=5)

wartosc_z_podatkiem_razem = Entry(payment_frame, width=wartosc_z_podatkiem_entry_width)
wartosc_z_podatkiem_razem.grid(row=3, column=6)

payment_frame.grid(row=6, column=0, columnspan=3)

# Adnotacje
adnotations_label = Label(window, text="Adnotacje: ")
adnotations_label.grid(row=7, column=0, columnspan=1)
adnotations_entry = Entry(window, width=50)
adnotations_entry.grid(row=8, column=0, ipady=20)

# Obliczanie sprzedaży
calculate_btn = Button(window, text="Oblicz sprzedaż", command=count_total)
calculate_btn.grid(row=7, column=1, pady=10)


# Zapis przeliczonej faktury w bazie danych
def save_facture():
    desired_values = [new_sequence_number_entry.get(), client_name_entry.get(), client_address_entry.get(),
                      client_nip_entry.get(), str(todays_date), wartosc_razem.get(), kwota_podatku_razem.get(),
                      default_payment.get()]

    # Numer faktury musi być unikatowy
    cursor.execute('SELECT sequence_number FROM sales WHERE sequence_number =?', (desired_values[0], ))
    if cursor.fetchone() is not None:
        messagebox.showwarning(title="Powtórzenie numeru faktury", message="Podany numer faktury już istnieje, "
                                                                           "zmień go na właściwy.")

    correct = True
    for value in desired_values:
        if value == "":
            correct = False
    if not correct:
        messagebox.showwarning(title="Niepełne dane", message="Uzupełnij wszystkie niezbędne dane w fakturze.")
    if correct:
        cursor.execute('INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?, ?)', desired_values)
        connection.commit()
        if messagebox.askyesno(title="Sukces!", message="Faktura została zapisana.\nCzy chcesz ją wydrukować?"):
            print("drukowanie w toku")
            current_client_data = [client_name_entry.get(), client_address_entry.get(), "NIP:" + client_nip_entry.get()]
            input_rows_values = [sold_items_nazwa_lst, sold_items_miara_lst, sold_items_ilosc_lst, sold_items_cena_lst]
            # Przekształcenie list obiektów w listy wartości za pomocą metody "tk.Entry().get()"
            input_rows_values = [[i.get() for i in lst] for lst in input_rows_values]
            create_pdf_file(new_sequence_number_entry.get(), todays_date, current_user_data[:-3]
                            + (current_user_data[7], ), current_client_data, input_rows_values, default_payment.get(),
                            adnotations_entry.get())

            # Drukowanie faktury
            def print_out_facture():
                filename = "ostatnio_zapisana_faktura.pdf"
                try:
                    # Potrzebne są 2 wydruki, więc powtarzam komendę
                    os.startfile(filename, "print")
                    os.startfile(filename, "print")
                    # ^^ Do poprawnego wydruku potrzebny jest AdobeReader jako domyślna przeglądarka plików PDF
                except OSError:
                    # Samo otwieranie pliku pdf w domyślnym programie:
                    os.system(filename)
                    messagebox.showinfo(title="Brak Adobe Reader",
                                        message="Do poprawnego automatycznego druku powinien zostać zainstalowany "
                                                "Adobe Reader jako domyślna przeglądarka plików PDF. Możesz go pobrać"
                                                "ze strony: get.adobe.com/pl/reader/")
                    # Błąd wyskakuje przy próbie wydruku pliku typu .pdf. Pliki typu .txt działają normalnie.
                    # OSError: [WinError 1155] Z określonym plikiem nie skojarzono dla tej operacji
                    # żadnej aplikacji: 'ostatnio_zapisana_faktura.pdf'

            print_out_facture()


save_facture_btn = Button(window, text="Zapisz fakturę", command=save_facture)
save_facture_btn.grid(row=8, column=1, sticky="w")

year_lst_start = 2020


# Tworzenie pliku XML
def create_new_xml_file(chosen_month_idx, chosen_year_idx):
    # Przekształcenie indeksów miesiąca i roku w stringi do SQL query
    chosen_month = str(chosen_month_idx + 1)
    if len(chosen_month) == 1:
        chosen_month = "0" + chosen_month
    chosen_year = str(chosen_year_idx + year_lst_start)

    # Select all sales made in selected month from SQL db
    chosen_period = (chosen_year + "-" + chosen_month + "-" + "%", )
    cursor.execute('SELECT * FROM sales WHERE date LIKE ? ORDER BY sequence_number', chosen_period)
    monthly_sales = cursor.fetchall()
    # ^^Jeśli ta lista będzie zawierać minimum jeden wpis, utworzony zostanie plik xml
    if len(monthly_sales) <= 0:
        messagebox.showwarning(title="Operacja przerwana",
                               message="W wybranym miesiącu nie ma jeszcze zapisanych żadnych faktur.")
    if len(monthly_sales) > 0:
        # Concatenating data from db with XML file syntax
        new_file_sale_section = ""
        podstawa_opodatkowania = 0
        podatek_nalezny = 0
        for sale_idx, sale in enumerate(monthly_sales):
            sale_text = "\n<SprzedazWiersz>"
            sale_text += "\n\t<LpSprzedazy>" + str(sale_idx + 1) + "</LpSprzedazy>"
            sale_text += "\n\t<NrKontrahenta>" + str(sale[3]) + "</NrKontrahenta>"
            sale_text += "\n\t<NazwaKontrahenta>" + sale[1] + "</NazwaKontrahenta>"
            sale_text += "\n\t<DataWystawienia>" + sale[4] + "</DataWystawienia>"
            sale_text += "\n\t<DowodSprzedazy>" + sale[0] + "</DowodSprzedazy>"
            sale_text += "\n\t<K_19>" + str(sale[5]) + "</K_19>"
            sale_text += "\n\t<K_20>" + str(sale[6]) + "</K_20>"
            podstawa_opodatkowania += sale[5]
            podatek_nalezny += sale[6]
            sale_text += "\n</SprzedazWiersz>"
            new_file_sale_section += sale_text
        new_file_sale_section += "<SprzedazCtrl>\n\t<LiczbaWierszySprzedazy>" + str(len(monthly_sales)) \
                                 + "</LiczbaWierszySprzedazy>\n\t<PodatekNalezny>" + str(podatek_nalezny) \
                                 + "</PodatekNalezny>\n</SprzedazCtrl>"
        k19_and_k20 = [round(podstawa_opodatkowania), round(podatek_nalezny)]
        # ^^tutaj zwykłe zaokrąglanie zamiast funkcji two_zeros_format, bo rubryki K19 i K20 są zaokrąglane do złotówek

        new_xml_file_name = chosen_year + "-" + chosen_month + "-JPK_V7M.xml"
        with codecs.open("XML_files/" + new_xml_file_name, "w", 'utf-8') as xml_file_matrix:
            xml_file_matrix.write(new_xml_file_content(chosen_year, chosen_month, new_file_sale_section, k19_and_k20))
        messagebox.showinfo(title="Sukces!", message="Plik XML został zapisany i jest gotowy do wysłania.")


def xml_file_menu():
    xml_file_menu_window = Toplevel(window)
    xml_file_menu_window.title("Generator Faktur - Tworzenie pliku XML")

    instruction_label = Label(xml_file_menu_window, fg="white", bg="#026dba", font=('Arial', 12),
                              text='Zaznacz miesiąc i rok za który chcesz wygenerować plik,'
                                   '\na następnie kliknij przycisk "Utwórz plik XML"')
    instruction_label.grid(row=0, column=0, columnspan=2, ipadx=40, pady=20)

    month_label = Label(xml_file_menu_window, text="Miesiąc", font=('Arial', 12))
    month_label.grid(row=1, column=0)
    month_to_choose = Listbox(xml_file_menu_window, height=12, exportselection=0)
    month_to_choose.grid(row=2, column=0)
    months_lst = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec", "Sierpień",
                  "Wrzesień", "Październik", "Listopad", "Grudzień"]
    for month_idx in range(12):
        month_to_choose.insert(month_idx + 1, months_lst[month_idx])

    year_label = Label(xml_file_menu_window, text="Rok", font=('Arial', 12))
    year_label.grid(row=1, column=1)
    year_to_choose = Listbox(xml_file_menu_window, height=12, exportselection=0)
    year_to_choose.grid(row=2, column=1)
    for year_idx in range(51):  # <- za 50 lat można zwiększyć ten zakres opcji ;)
        year_to_choose.insert(year_idx + 1, year_idx + year_lst_start)

    def create_xml_file_button_command():
        if month_to_choose.curselection() == () or year_to_choose.curselection() == ():
            messagebox.showwarning(title="Niepełna data", message="Zaznacz okres w obu kolumnach.")
            xml_file_menu_window.destroy()
        else:
            create_new_xml_file(month_to_choose.curselection()[0], year_to_choose.curselection()[0])
            xml_file_menu_window.destroy()

    create_xml_file_button = Button(xml_file_menu_window, text="Utwórz plik XML", fg="white", bg="#318c1f",
                                    command=create_xml_file_button_command)
    create_xml_file_button.grid(row=3, column=0, columnspan=2, pady=20)


open_xml_file_menu_button = Button(window, text="Wygeneruj plik XML", command=xml_file_menu)
open_xml_file_menu_button.grid(row=8, column=1, sticky="e")

# Podpis
signature_label = Label(window, text="Podpis wystawcy faktury: ")
signature_label.grid(row=7, column=2)
signature_entry = Entry(window, width=50, state='disabled')
signature_entry.grid(row=8, column=2, ipady=20)


# Zamyka połączenie z bazą danych, a następnie cały program
def close_program():
    connection.close()
    window.destroy()


window.protocol("WM_DELETE_WINDOW", close_program)
window.mainloop()
