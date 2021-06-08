# coding: utf8
# FPDF version fpdf2 2.3.4.
from fpdf import FPDF
from numbers_to_words import numbers_to_words


def two_zeros_format(value):
    return "{0:.2f}".format(value)


def create_pdf_file(facture_number, date, user_data, client_data, inserted_rows, payment_form, adnotations):
    # Creating PDF file
    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()

    # Adding fonts
    pdf.add_font('Arial', '', 'arial.ttf', uni=True)
    pdf.add_font('Arial', 'B', 'arialbd.ttf', uni=True)
    pdf.set_font('Arial', 'B', 14)
    # żeby działały polskie znaki dodałem czcionkę Arial (plik "arial.ttf" w folderze "Lib\site-packages\fpdf\font")

    # Numer faktury
    pdf.cell(w=0, h=10, align="C", ln=True, txt="Numer faktury: " + facture_number)
    pdf.y -= 10

    pdf.set_font('Arial', 'B', 8)
    # Data
    pdf.multi_cell(w=0, h=4, align="R", ln=True, txt="Data wystawienia:\n" + str(date) + ", " + user_data[2])

    # Sprzedawca
    seller_cell_text = "Sprzedawca:\n"
    for info_idx, info in enumerate(user_data[:-1]):
        if info_idx == 3:
            seller_cell_text += "NIP : "
        if info_idx == 4:
            seller_cell_text += "Telefon : "
        if info_idx != 2:
            # ^^user_data[2] to miejscowość (wartość city), która w tym miejscu jest niepotrzebna
            seller_cell_text += str(info) + "\n"
    pdf.multi_cell(w=60, h=4, align="C", txt=seller_cell_text)
    pdf.y -= 16

    # Nabywca
    pdf.multi_cell(w=0, h=4, align="R", ln=True, txt="Nabywca:\n" + "".join([str(i) + "\n" for i in client_data]))
    pdf.y += 16

    # CREATING TABLE
    columns_widths_lst = [8, 60, 10, 10, 16, 25, 8, 19, 31]

    # Wrapped in a function for clarity and optional reuse in case of printing 2 factures on the same page
    def creating_table_headlines():
        # Values for table first row - text values for headlines
        columns_headlines = ['Lp.', 'Nazwa towaru lub usługi', 'Miara', 'Ilość', 'Cena\njednost.\nnetto (zł)',
                             'Wartość\ntowarów (usług)\nbez podatku (zł)', 'Vat',
                             'Kwota\npodatku (zł)', 'Wartość\ntowarów (usług)\nwraz z podatkiem (zł)']

        pdf.cell(w=columns_widths_lst[0], h=12, align="C", border=True, txt=columns_headlines[0])
        pdf.cell(w=columns_widths_lst[1], h=12, align="C", border=True, txt=columns_headlines[1])
        pdf.cell(w=columns_widths_lst[2], h=12, align="C", border=True, txt=columns_headlines[2])
        pdf.cell(w=columns_widths_lst[3], h=12, align="C", border=True, txt=columns_headlines[3])

        pdf.multi_cell(w=columns_widths_lst[4], h=4, align="C", border=True, txt=columns_headlines[4])
        pdf.y -= 12
        # ^^ this is fpdf library specific to keep multi line cells in one row

        pdf.multi_cell(w=columns_widths_lst[5], h=4, align="C", border=True, txt=columns_headlines[5])
        pdf.y -= 12

        pdf.multi_cell(w=columns_widths_lst[6], h=12, align="C", border=True, txt=columns_headlines[6])
        pdf.y -= 12

        pdf.multi_cell(w=columns_widths_lst[7], h=6, align="C", border=True, txt=columns_headlines[7])
        pdf.y -= 12

        pdf.multi_cell(w=columns_widths_lst[8], h=4, align="C", border=True, txt=columns_headlines[8], ln=True)

        # Zmiana czcionki z pogrubionej przy nagłówkach na zwykłą dla reszty tabeli
        pdf.set_font('Arial', '', 8)

    creating_table_headlines()

    # Stawka na ten moment stała - 23%, można zamienić na input z GUI jeśli byłby inne
    stawka = 23
    # Sumowanie wartości i podatku przy każdej iteracji (czyli po każdym rzędzie)
    zsumowana_wartosc = 0
    zsumowana_kwota_podatku_vat = 0
    zsumowana_wartosc_z_podatkiem = 0

    # Populacja tabeli komórkami wypełnionymi danymi z rzędów z GUI
    for coll_idx, row in enumerate(zip(inserted_rows[0], inserted_rows[1], inserted_rows[2], inserted_rows[3])):
        if row[0] == "":
            break
        pdf.cell(w=columns_widths_lst[0], h=12, align="C", border=True, txt=str(coll_idx + 1))
        pdf.cell(w=columns_widths_lst[1], h=12, align="C", border=True, txt=row[0])
        pdf.cell(w=columns_widths_lst[2], h=12, align="C", border=True, txt=row[1])
        pdf.cell(w=columns_widths_lst[3], h=12, align="C", border=True, txt=row[2])
        pdf.cell(w=columns_widths_lst[4], h=12, align="C", border=True, txt=row[3])
        wartosc = float(row[2]) * float(row[3])
        zsumowana_wartosc += wartosc
        pdf.cell(w=columns_widths_lst[5], h=12, align="C", border=True, txt=two_zeros_format(wartosc))
        pdf.cell(w=columns_widths_lst[6], h=12, align="C", border=True, txt=str(stawka) + "%")
        kwota_podatku_vat = wartosc * stawka / 100
        zsumowana_kwota_podatku_vat += kwota_podatku_vat
        pdf.cell(w=columns_widths_lst[7], h=12, align="C", border=True, txt=two_zeros_format(kwota_podatku_vat))
        wartosc_z_podatkiem = wartosc + kwota_podatku_vat
        zsumowana_wartosc_z_podatkiem += wartosc_z_podatkiem
        pdf.cell(w=columns_widths_lst[8], h=12, align="C", border=True, txt=str(two_zeros_format(wartosc_z_podatkiem)))
        # the cell under creates new line
        pdf.cell(w=1, h=12, ln=True)

    empty_cell_width = sum(columns_widths_lst[:5])

    # Zsumowane kwoty dla podatku 23%
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(w=empty_cell_width, h=12, txt="Sposób zapłaty: " + payment_form)
    pdf.cell(w=columns_widths_lst[5], h=12, align="L", txt="Zestawienie sprzedaży wg stawek podatku:")

    pdf.set_font('Arial', '', 8)
    pdf.cell(w=1, h=12, ln=True)
    if payment_form == "Gotówka":
        pdf.cell(w=empty_cell_width, h=12, txt="")
    if payment_form == "Przelew":
        pdf.cell(w=empty_cell_width, h=12, txt="Numer konta: " + user_data[-1])
    pdf.cell(w=columns_widths_lst[5], h=12, align="C", border=True, txt=two_zeros_format(zsumowana_wartosc))
    pdf.cell(w=columns_widths_lst[6], h=12, align="C", border=True, txt=str(stawka) + "%")
    pdf.cell(w=columns_widths_lst[7], h=12, align="C", border=True, txt=two_zeros_format(zsumowana_kwota_podatku_vat))
    pdf.cell(w=columns_widths_lst[8], h=12, align="C", border=True, txt=two_zeros_format(zsumowana_wartosc_z_podatkiem))
    pdf.cell(w=1, h=12, ln=True)

    # Zsumowane kwoty razem dla wszystkich stawek podatków
    pdf.set_font('Arial', 'B', 8)
    if payment_form == "Gotówka":
        pdf.cell(w=empty_cell_width, h=12, txt="")
    if payment_form == "Przelew":
        pdf.cell(w=empty_cell_width, h=12, txt="Do zapłaty: " + two_zeros_format(zsumowana_wartosc_z_podatkiem))
    pdf.cell(w=columns_widths_lst[5], h=12, align="L", txt="Razem:")
    pdf.cell(w=1, h=12, ln=True)
    if payment_form == "Gotówka":
        pdf.cell(w=empty_cell_width, h=12, txt="")
    if payment_form == "Przelew":
        pdf.cell(w=empty_cell_width, h=12, txt="Słownie: ")
    pdf.cell(w=columns_widths_lst[5], h=12, align="C", border=True, txt=two_zeros_format(zsumowana_wartosc))
    pdf.cell(w=columns_widths_lst[6], h=12, txt="")
    pdf.cell(w=columns_widths_lst[7], h=12, align="C", border=True, txt=two_zeros_format(zsumowana_kwota_podatku_vat))
    pdf.cell(w=columns_widths_lst[8], h=12, align="C", border=True, txt=two_zeros_format(zsumowana_wartosc_z_podatkiem))
    pdf.cell(w=1, h=12, ln=True)
    pdf.set_font('Arial', '', 8)
    if payment_form == "Przelew":
        pdf.cell(w=empty_cell_width, h=12, txt=numbers_to_words(float(two_zeros_format(zsumowana_wartosc_z_podatkiem))))
        pdf.cell(w=1, h=12, ln=True)

    # Adnotacje
    pdf.cell(w=empty_cell_width, h=12, txt="Adnotacje: ")
    pdf.cell(w=1, h=12, ln=True)
    pdf.cell(w=100, h=12, txt=adnotations)
    pdf.cell(w=1, h=12, ln=True)

    # Zapis pliku
    pdf.output("ostatnio_zapisana_faktura.pdf")
