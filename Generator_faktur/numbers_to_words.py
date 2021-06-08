# Przekład liczb na kwoty słowne
def numbers_to_words(number_to_translate):
    my_dict = {1: 'jeden', 2: 'dwa', 3: 'trzy', 4: 'cztery', 5: 'pięć', 6: 'sześć',
               7: 'siedem', 8: 'osiem', 9: 'dziewięć', 10: 'dziesięć', 11: 'jedenaście',
               12: 'dwanaście', 13: 'trzynaście', 14: 'czternaście', 15: 'piętnaście',
               16: 'szesnaście', 17: 'siedemnaście', 18: 'osiemnaście', 19: 'dziewiętnaście',
               20: 'dwadzieścia', 30: 'trzydzieści', 40: 'czterdzieści', 50: 'pięćdziesiąt',
               60: 'sześćdziesiąt', 70: 'siedemdziesiąt', 80: 'osiemdziesiąt',
               90: 'dziewięćdziesiąt', 100: 'sto', 200: 'dwieście', 300: 'trzysta',
               400: 'czterysta', 500: 'pięćset', 600: 'sześćset', 700: 'siedemset',
               800: 'osiemset', 900: 'dziewięćset', 1000: 'tysiąc'}

    tens = {2: 'dwadzieścia', 3: 'trzydzieści', 4: 'czterdzieści', 5: 'pięćdziesiąt',
            6: 'sześćdziesiąt', 7: 'siedemdziesiąt', 8: 'osiemdziesiąt',
            9: 'dziewięćdziesiąt'}

    hundreds = {0: '', 1: 'sto', 2: 'dwieście', 3: 'trzysta',
                4: 'czterysta', 5: 'pięćset', 6: 'sześćset', 7: 'siedemset',
                8: 'osiemset', 9: 'dziewięćset'}

    thousands = {1: 'tysiąc', 2: 'dwa tysiące', 3: 'trzy tysiące', 4: 'cztery tysiące',
                 5: 'pięć tysięcy', 6: 'sześć tysięcy', 7: 'siedem tysięcy',
                 8: 'osiem tysięcy', 9: 'dziewięć tysięcy'}

    lst_of_dicts = [my_dict, tens, hundreds, thousands]
    result = ""
    number_to_translate = round(number_to_translate, 2)
    num, rest = str(float(number_to_translate)).split(".")
    if len(rest) == 1:
        rest += "0"
    try:
        while int(num) not in my_dict:
            if len(num) <= 0:
                return result + " " + str(rest) + "/100"
            result += lst_of_dicts[len(num) - 1][int(num[0])] + " "
            # 'Key: 0' w przypadku gdy jest liczba np. 2093.00 albo 5031.38 dodaje niepotrzebną spację
            num = num[1:]
        if int(num) in my_dict:
            result += my_dict[int(num)]
            return result + " " + str(rest) + "/100"
    except IndexError:
        return "Błąd - Nieprawidłowa liczba"
