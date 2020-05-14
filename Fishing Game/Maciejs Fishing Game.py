### Wykorzystane biblioteki...
import pygame
import random

### Okno...
pygame.init()
# Wymiary okna...
window_width = 626
window_height = 417
window = pygame.display.set_mode((window_width, window_height))
# Nagłówek okna...
ikona = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/ryba ikona2.jpeg")
pygame.display.set_caption("Maciej's Fishing Game")
pygame.display.set_icon(ikona)


### Ekran startowy...
def start():

    start_background = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/starting screen.jpeg")
    window.blit(start_background, (0, 0))

# Menu...
    button_x = 225
    buttons_y = 0     # Każdy z przycisków ma y osobno (button_y_1, button_y_2, button_y_3). Zmienna buttons_y służy do regulowania wysokości wszystkich jednocześnie.
    button_width = 200
    button_height = 50

    button_color = (100, 80, 235)
    button_color_brightened = (100, 130, 235)
    button_color_outline = (250, 250, 230)
    mouse_position = pygame.mouse.get_pos()
    # print(mouse_position)
    mouse_pressed = pygame.mouse.get_pressed()

    font_type = "cooperblack"
    font_size = 25
    text_color = (255, 255, 224)

    #zmienne globalne wykorzystywane w zadaniach przycisków
    global start_screen_active
    global rozgrywka_active
    global achievements_active

# Play button_1...
    button_y_1 = 100 + buttons_y
    text_str_button_1 = "Play"

    #tło...
    pygame.draw.rect(window, button_color_outline, [button_x - 3, button_y_1 - 3, button_width + 6, button_height + 6])
    pygame.draw.rect(window, button_color, [button_x, button_y_1, button_width, button_height])
    if button_x + button_width > mouse_position[0] > button_x and button_y_1 + button_height > mouse_position[1] > button_y_1:
        pygame.draw.rect(window, button_color_brightened, [button_x, button_y_1, button_width, button_height])

    #tekst
    surface_button_1 = (pygame.font.SysFont(font_type, font_size)).render(text_str_button_1, True, text_color)
    destination_1 = surface_button_1.get_rect()
    destination_1.center = (button_x + (button_width/2), button_y_1 + (button_height/2))
    window.blit(surface_button_1, destination_1)

    #zadanie
    if mouse_pressed[0] == 1 and button_x + button_width > mouse_position[0] > button_x and button_y_1 + button_height > mouse_position[1] > button_y_1:
        start_screen_active = False
        rozgrywka_active = True




# Achievements button_2...
    button_y_2 = 180 + buttons_y
    text_str_button_2 = "Achievements"

    #tło...
    pygame.draw.rect(window, button_color_outline, [button_x - 3, button_y_2 - 3, button_width + 6, button_height + 6])
    pygame.draw.rect(window, button_color, [button_x, button_y_2, button_width, button_height])
    if button_x + button_width > mouse_position[0] > button_x and button_y_2 + button_height > mouse_position[1] > button_y_2:
        pygame.draw.rect(window, button_color_brightened, [button_x, button_y_2, button_width, button_height])

    #tekst...
    surface_button_2 = (pygame.font.SysFont(font_type, font_size)).render(text_str_button_2, True, text_color)
    destination_2 = surface_button_2.get_rect()
    destination_2.center = (button_x + (button_width/2), button_y_2 + (button_height/2))
    window.blit(surface_button_2, destination_2)

    #zadanie
    if mouse_pressed[0] == 1 and button_x + button_width > mouse_position[0] > button_x and button_y_2 + button_height > mouse_position[1] > button_y_2:
        start_screen_active = False
        achievements_active = True

# Exit button_3...
    button_y_3 = 260 + buttons_y
    text_str_button_3 = "Exit game"

    #tło...
    pygame.draw.rect(window, button_color_outline, [button_x - 3, button_y_3 - 3, button_width + 6, button_height + 6])
    pygame.draw.rect(window, button_color, [button_x, button_y_3, button_width, button_height])
    if button_x + button_width > mouse_position[0] > button_x and button_y_3 + button_height > mouse_position[1] > button_y_3:
        pygame.draw.rect(window, button_color_brightened, [button_x, button_y_3, button_width, button_height])

    #tekst...
    surface_button_3 = (pygame.font.SysFont(font_type, font_size)).render(text_str_button_3, True, text_color)
    destination_3 = surface_button_3.get_rect()
    destination_3.center = (button_x + (button_width/2), button_y_3 + (button_height/2))
    window.blit(surface_button_3, destination_3)

    #zadanie...
    if mouse_pressed[0] == 1 and button_x + button_width > mouse_position[0] > button_x and button_y_3 + button_height > mouse_position[1] > button_y_3:
        global main_loop_active
        main_loop_active = False

# start()


hooked_fish = []
# ^^ zmienna globalna funkcji ryby

fishing_float_y = 295
fishing_float_up = True
# ^^ zmienne globalne amimacji spławika


### Rozgrywka...
def rozgrywka():

    #Tło
    gameplay_background = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/staw2.jpeg")
    window.blit(gameplay_background, (0, 0))

    #Wędka
    fishing_rod_image = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/fishing rod3.png")
    fishing_rod_image = pygame.transform.scale(fishing_rod_image, (315, 300))
    window.blit(fishing_rod_image, (0, 150))

    #Próba stworzenia czasu oczekiwania na branie
    clock = pygame.time.Clock()
    max_fps = 120
    clock.tick(max_fps)

    #czas oczekiwania na branie nowej ryby w milisekundach
    # print(awaiting_time)
    #czas oczekiwania na branie w sekundach, czyli przemnożone milisekundy razy 1000
    # pygame.time.delay(awaiting_time * 100)

    seconds = round(pygame.time.get_ticks() / 1000)
    # awaiting_time = random.choice((5, 6, 7, 8, 9))
    if seconds % 12 == 0:
        #Water splash
        water_splash_image_x = 285
        water_splash_image_y = 300
        water_splash_image = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/water splash.png")
        water_splash_image = pygame.transform.scale(water_splash_image, (60, 60))
        window.blit(water_splash_image, (water_splash_image_x, water_splash_image_y))

        #Water splash sound
        water_splash_sound = pygame.mixer.Sound("C:/Users/Maciek/Pictures/Python/Fishing Game/water_splash_sound.wav")
        pygame.mixer.Sound.play(water_splash_sound)

    #Spławik
    fishing_float_x = 290
    # fishing_float_y = 295    # <- przeniesiona ponad rozgrywka() ^^
    global fishing_float_y

    fishing_float_image = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/splawik1.png")
    fishing_float_image = pygame.transform.scale(fishing_float_image, (50, 50))
    window.blit(fishing_float_image, (fishing_float_x, fishing_float_y))

    #Animacja ruchu spławika
    global fishing_float_up
    if fishing_float_up is True:
        fishing_float_y -= 1
        if fishing_float_y == 285:
            fishing_float_up = False
    elif fishing_float_up is False:
        fishing_float_y += 1
        if fishing_float_y == 295:
            fishing_float_up = True

    # #Okręgi na wodzie
    # fale_x = 290
    # fale_y = 310
    # fale_image = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/okrag1.png")
    # fale_image = pygame.transform.scale(fale_image, (50, 25))
    # window.blit(fale_image, (fale_x, fale_y))

    # # próba stworzenia wzoru rysowania kręgu na wodzie...
    # ellipse_color = (255,255,255)
    # ellipse_x = 270
    # ellipse_y = 300
    # ellipse_width = 80
    # ellipse_height = 30
    # ellipse_frame = pygame.draw.rect(window, (0,0,0), (ellipse_x, ellipse_y, ellipse_width, ellipse_height), 1)
    # pygame.draw.ellipse(window, ellipse_color, ellipse_frame)

    #Pauza
    mouse_position = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    white = (255, 255, 255)
    gray = (200, 200, 200)
    pauza_x = 580
    pauza_y = 380
    pauza_width = 10
    pauza_height = 20
    pygame.draw.rect(window, white, [pauza_x, pauza_y, pauza_width, pauza_height])
    pygame.draw.rect(window, white, [pauza_x + 15, pauza_y, pauza_width, pauza_height])
    if pauza_x < mouse_position[0] < pauza_x + 15 + pauza_width * 2 and pauza_y < mouse_position [1] < pauza_y + pauza_height:
        pygame.draw.rect(window, gray, [pauza_x, pauza_y, pauza_width, pauza_height])
        pygame.draw.rect(window, gray, [pauza_x + 15, pauza_y, pauza_width, pauza_height])

    # # Music turn ON/OFF
    # speaker_image = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/speaker_image.png")
    # # speaker_image.transform.scale(speaker_image, (20, 20))
    # window.blit(speaker_image, (540, 340))



    global start_screen_active
    global rozgrywka_active
    global komunikat_active

    if mouse_pressed[0] == 1 and pauza_x < mouse_position[0] < pauza_x + 15 + pauza_width * 2 and pauza_y < mouse_position [1] < pauza_y + pauza_height:
        rozgrywka_active = False
        start_screen_active = True
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            rozgrywka_active = False
            start_screen_active = True

    #Wyświetlenie komunikatu
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and seconds % 12 == 0:
            komunikat_active = True
            rozgrywka_active = False


            #Łowienie ryby...
            class Ryba:

                def __init__(self, name, min_size, max_size, protection_size, min_weight, max_weight, foto):
                    self.name = name
                    self.min_size = min_size
                    self.max_size = max_size
                    self.protection_size = protection_size
                    self.min_weight = min_weight
                    self.max_weight = max_weight
                    self.foto = foto

                def funkcja_ryby(self):

                    # #PRÓBA napisania uogolnionego rozkładu normalnego!!!
                    # #przybliżone wartości rozkładu normalnego: 1%, 2%, 13%, 34%, 34%, 13%, 2%, 1% = 100%.
                    # #zatem jego zakresy po wykonaniu sumowania to: 1%, 3%, 16%, 50%, 84%, 97%, 99%, 100%.
                    #
                    # proporcja_ryby = 0
                    #
                    # jednostka_z_populacji_stu = random.choice((range(1, 101)))
                    # if jednostka_z_populacji_stu == 1:
                    #     proporcja_ryby = self.max_size * 0.01
                    #     # ^^ 1%
                    # elif 1 < jednostka_z_populacji_stu <= 3:
                    #     proporcja_ryby = self.max_size * 0.03
                    #     # ^^ 2%
                    # elif 3 < jednostka_z_populacji_stu <= 16:
                    #     pass
                    #     # ^^ 13%
                    # elif 16 < jednostka_z_populacji_stu <= 50:
                    #     pass
                    #     # ^^ 34%
                    # elif 50 < jednostka_z_populacji_stu <= 84:
                    #     pass
                    #     # ^^ 34% (drugie - wykres zaczyna schodzić w dół)
                    # elif 84 < jednostka_z_populacji_stu <= 97:
                    #     pass
                    #     # ^^ 13%
                    # elif 97 < jednostka_z_populacji_stu <= 99:
                    #     pass
                    #     # ^^ 2%
                    # elif jednostka_z_populacji_stu == 100:
                    #     pass
                    #     # ^^ 1%
                    #
                    # # print(jednostka_z_populacji_stu)

                    # Wymiar
                    size = random.choice(range(self.min_size, self.max_size))

                    # Waga
                    weight_to_size_factor = self.max_weight / self.max_size
                    weight = size * weight_to_size_factor
                    if weight > self.max_weight:
                        weight = self.max_weight
                    pinch_of_randomness = random.choice((0.8, 0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15, 1.2))
                    weight = round(weight * pinch_of_randomness, 2)

                    # Wymiar ochronny
                    under_size = False
                    if size < self.protection_size:
                        under_size = True

                    # Return z funkcja_ryby()
                    return self.name, str(size), str(weight), under_size, self.foto

            # Parametry ryb do klasy Ryba()...

            # poniższym rybom doprecyzuj min_size, min_weight...
            bolen = Ryba("Boleń", 10, 99, 40, 1, 8, "bolen foto")
            brzana = Ryba("Brzana", 10, 85, 40, 1, 7, "brzana foto")
            karp = Ryba("Karp", 10, 110, 30, 1, 30, "karp foto")
            klen = Ryba("Kleń", 10, 63, 25, 1, 4, "klen foto")
            lin = Ryba("Lin", 10, 66, 25, 1, 5, "lin foto")
            lipien = Ryba("Lipień", 10, 52, 30, 1, 2, "lipien foto")
            okon = Ryba("Okoń", 10, 55, 15, 1, 3, "okon foto")
            sumik = Ryba("Sum", 10, 245, 70, 1, 102, "sum foto")
            szczupak = Ryba("Szczupak", 10, 133, 50, 1, 24, "szczupak foto")
            troc = Ryba("Troć", 10, 106, 35, 1, 15, "troc foto")

            # poniższym rybom doprecyzuj min_size, min_weight, max_weight...
            certa = Ryba("Certa", 10, 47, 30, 1, 10, "certa foto")
            glowacica = Ryba("Głowacica", 10, 118, 70, 1, 10, "glowacica foto")

            # poniższym rybom doprecyzuj min_size, max_size, min_weight, max_weight...
            jelec = Ryba("Jelec", 10, 100, 15, 1, 10, "jelec foto")
            sielawa = Ryba("Sielawa", 10, 100, 18, 1, 10, "sielawa foto")
            wzdrega = Ryba("Wzdręga", 10, 40, 15, 1, 10, "wzdrega foto")

            # uzupełnij lista_ryb o certe, glowacice, jelca, sielawe, gdy uzupełnisz ich parametry...
            lista_ryb = [bolen, brzana, karp, klen, lin, lipien, okon, sumik, szczupak, troc]

            global hooked_fish
            hooked_fish = (random.choice(lista_ryb)).funkcja_ryby()
            # print(karp.funkcja_ryby())
            # print(hooked_fish)

            # Zapis statystyk połowów do pliku notatnika
            # slownik_ryb = {"001": "Boleń", "002": "Brzana", "003": "Karp", "004": "Kleń", "005": "Lin", "006": "Lipień", "007": "Okoń", "008": "Szczupak", "009": "Sum", "010": "Troć"}
            if hooked_fish[3] is False:
                with open("C:/Users/Maciek/Pictures/Python/Fishing Game/achievements.txt", "r") as achievements_file:
                    ryby_readlines = achievements_file.readlines()

                zaktualizowany_tekst_achievements = ""

                #ujemne wartości indeksu są po to, żeby żadna linijka nie została odczytana na początku, a dopiero po spełnieniu warunku
                wymiar_line_indeks = -1
                weight_line_indeks = -1
                for indeks, line in enumerate(ryby_readlines):
                    if line[:-1] == hooked_fish[0]:
                        zaktualizowany_tekst_achievements += line
                        wymiar_line_indeks = indeks + 1
                        weight_line_indeks = indeks + 2
                        if int(ryby_readlines[wymiar_line_indeks]) < int(hooked_fish[1]):
                            zaktualizowany_tekst_achievements += hooked_fish[1] + "\n"
                        if int(ryby_readlines[wymiar_line_indeks]) >= int(hooked_fish[1]):
                            zaktualizowany_tekst_achievements += ryby_readlines[wymiar_line_indeks]
                        rounded_new_species_weight = round(float(ryby_readlines[weight_line_indeks]) + float(hooked_fish[2]), 2)
                        zaktualizowany_tekst_achievements += str(rounded_new_species_weight) + "\n"
                    if line[:-1] != hooked_fish[0] and line is not ryby_readlines[wymiar_line_indeks] and line is not ryby_readlines[weight_line_indeks]:
                        zaktualizowany_tekst_achievements += line

                # print(zaktualizowany_tekst_achievements)

                with open("C:/Users/Maciek/Pictures/Python/Fishing Game/achievements.txt", "w") as achievements_file:
                    achievements_file.write(zaktualizowany_tekst_achievements)


# rozgrywka()


### Komunikaty...
def funkcja_komunikatu():

#komunikat_1
    #kolory
    komunikat_bg_color = (200, 200, 150)
    white = (255, 255, 255)

    #tło
    pygame.draw.rect(window, komunikat_bg_color, [80, 59, 466, 337])

    #alternatywne tło wykorzystujące image png zamiast renderowania rect'u
    # komunikat_background2 = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/komunikat_background2.png")
    # komunikat_background2 = pygame.transform.scale(komunikat_background2, (466, 337))
    # window.blit(komunikat_background2, (80, 59))

    #pole tekstowe
    pygame.draw.rect(window, white, [105, 260, 420, 120])



    # #przycisk zamknij
    # pygame.draw.rect(window, (255, 0, 0), [520, 65, 20, 20])
    # #krzyżyk na "przycisku zamknij"
    # pygame.draw.line(window, white, (524, 69), (534, 79), 2)
    # pygame.draw.line(window, white, (534, 69), (524, 79), 2)

    cross_exit_button_image = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/cross_exit_button_image1.png")
    cross_exit_button_image = pygame.transform.scale(cross_exit_button_image, (20, 20))
    cross_exit_button_x = 520
    cross_exit_button_y = 65
    window.blit(cross_exit_button_image, (520, 65))

    #foto ryby
    ryba_foto = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/" + hooked_fish[4] + ".png")
    ryba_foto = pygame.transform.scale(ryba_foto, (300, 100))
    window.blit(ryba_foto, (165, 90))

    #tekst

    #tekst - nazwa gatunku ryby
    surface_komunikatu_0 = (pygame.font.SysFont("timesnewroman", 40)).render(hooked_fish[0], True, (0,0,0))
    destination_komunikatu_0 = surface_komunikatu_0.get_rect()
    destination_komunikatu_0.center = (315, 230)
    window.blit(surface_komunikatu_0, destination_komunikatu_0)


    # tekst - niewymiarowa
    fish_tekst_size_and_weight_y = 320

    if hooked_fish[3] is True:

        fish_tekst_size_and_weight_y = 290

        surface_komunikatu_2 = (pygame.font.SysFont("timesnewroman", 20)).render("Niestety jest niewymiarowa!", True, (0, 0, 0))
        destination_komunikatu_2 = surface_komunikatu_2.get_rect()
        destination_komunikatu_2.center = (315, 320)
        window.blit(surface_komunikatu_2, destination_komunikatu_2)

        surface_komunikatu_3 = (pygame.font.SysFont("timesnewroman", 20)).render("Szanujesz regulamin wędkarski i wypuszczasz ją.", True, (0, 0, 0))
        destination_komunikatu_3 = surface_komunikatu_3.get_rect()
        destination_komunikatu_3.center = (315, 350)
        window.blit(surface_komunikatu_3, destination_komunikatu_3)

    #tekst - rozmiar, waga
    surface_komunikatu_1 = (pygame.font.SysFont("timesnewroman", 20)).render("Twoja ryba mierzy " + hooked_fish[1] + " cm długości i waży " + hooked_fish[2] + " kg.", True, (0,0,0))
    destination_komunikatu_1 = surface_komunikatu_1.get_rect()
    destination_komunikatu_1.center = (315, fish_tekst_size_and_weight_y)
    window.blit(surface_komunikatu_1, destination_komunikatu_1)

    #zadanie
    mouse_position = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    global komunikat_active
    global rozgrywka_active
    if mouse_pressed[0] == 1 and cross_exit_button_x + 20 > mouse_position[0] > cross_exit_button_x and cross_exit_button_y + 20 > mouse_position[1] > cross_exit_button_y:
        komunikat_active = False
        rozgrywka_active = True
    # elif event.type == pygame.KEYDOWN:
    #     if event.key == pygame.K_ESCAPE:
    #         komunikat_active = False
    #         rozgrywka_active = True

# funkcja_komunikatu()

another_five_species = 0

def funkcja_achievements():

    with open("C:/Users/Maciek/Pictures/Python/Fishing Game/achievements.txt", "r") as achievements_file:
        achievements_readlines = achievements_file.readlines()

    #Tło
    # achievements_tabela = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/tabela_achievements.jpeg")
    # window.blit(achievements_tabela, (60, 29))
    #Tło alternatywne
    black_background = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/black_background.jpeg")
    window.blit(black_background, (60, 29))

    # achievements_bg_color = 0, 0, 0
    # pygame.draw.rect(window, achievements_bg_color, [60, 29, 516, 357])

    # Lewa strzałka do przewijania tabeli
    left_arrow = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/left_arrow1.png")
    left_arrow = pygame.transform.scale(left_arrow, (25, 25))
    left_arrow_x = 107
    left_arrow_y = 340
    window.blit(left_arrow, (left_arrow_x, left_arrow_y))

    # Prawa strzałka do przewijania tabeli
    right_arrow = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/right_arrow1.png")
    right_arrow = pygame.transform.scale(right_arrow, (25, 25))
    right_arrow_x = 508
    right_arrow_y = 340
    window.blit(right_arrow, (right_arrow_x, right_arrow_y))

    #przycisk zamknij (ten sam kod co w komunikacie)
    cross_exit_button_image = pygame.image.load("C:/Users/Maciek/Pictures/Python/Fishing Game/cross_exit_button_image1.png")
    cross_exit_button_image = pygame.transform.scale(cross_exit_button_image, (20, 20))
    cross_exit_button_x = 550
    cross_exit_button_y = 35
    window.blit(cross_exit_button_image, (cross_exit_button_x, cross_exit_button_y))

    #zadanie przycisku zamknij(skopiowane z komunikatu)
    mouse_position = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    global achievements_active
    global start_screen_active
    if mouse_pressed[0] == 1 and cross_exit_button_x + 20 > mouse_position[0] > cross_exit_button_x and cross_exit_button_y + 20 > mouse_position[1] > cross_exit_button_y:
        achievements_active = False
        start_screen_active = True

    #Parametry czcionki w tabeli achievements
    font_color = (255, 255, 255)

    #obiekt tekstowy "Player name" wyświetlany w tabeli
    surface_tekst_player = (pygame.font.SysFont("cooperblack", 20)).render(achievements_readlines[0][:-1], True, font_color)
    destination_surface_tekst_player = surface_tekst_player.get_rect()
    destination_surface_tekst_player.center = (315, 60)
    window.blit(surface_tekst_player, destination_surface_tekst_player)

    #obiekty tekstowe nazw kolumn w tabeli
    column_name = "Species     ", "Record size ", "Total weight"
    column_name_tekst_x = 185
    column_name_tekst_y = 115
    for i in range(0, 3):
        surface_tekst_column_name = (pygame.font.SysFont("cooperblack", 20)).render(column_name[i], True, font_color)
        destination_surface_tekst_column_name = surface_tekst_column_name.get_rect()
        destination_surface_tekst_column_name.center = (column_name_tekst_x, column_name_tekst_y)
        window.blit(surface_tekst_column_name, destination_surface_tekst_column_name)

        column_name_tekst_x += 150

    global another_five_species
    #obiekty tekstowe nazw gatunków w tabeli
    line_gatunek = 2 + another_five_species
    gatunek_tekst_x = 170
    gatunek_tekst_y = 152
    for i in range(1, 6):
        surface_tekst_gatunek = (pygame.font.SysFont("timesnewroman", 20)).render(achievements_readlines[line_gatunek][:-1], True, font_color)
        destination_surface_tekst_gatunek = surface_tekst_gatunek.get_rect()
        destination_surface_tekst_gatunek.center = (gatunek_tekst_x, gatunek_tekst_y)
        window.blit(surface_tekst_gatunek, destination_surface_tekst_gatunek)

        line_gatunek += 3
        gatunek_tekst_y += 40

    #obiekty tekstowe największych złowionych wymiarów danego gatunku
    line_wymiar = 3 + another_five_species
    wymiar_tekst_x = 336
    wymiar_tekst_y = 152
    for i in range(1,6):
        surface_tekst_wymiar = (pygame.font.SysFont("timesnewroman", 20)).render(achievements_readlines[line_wymiar][:-1] + " cm", True, font_color)
        destination_surface_tekst_wymiar = surface_tekst_wymiar.get_rect()
        destination_surface_tekst_wymiar.center = (wymiar_tekst_x, wymiar_tekst_y)
        window.blit(surface_tekst_wymiar, destination_surface_tekst_wymiar)

        line_wymiar += 3
        wymiar_tekst_y += 40

    #wyświetlanie łącznej wagi złowionych ryb danego gatunku
    line_weight = 4 + another_five_species
    weight_tekst_x = 486
    weight_tekst_y = 152
    for i in range(1,6):
        surface_tekst_weight = (pygame.font.SysFont("timesnewroman", 20)).render(achievements_readlines[line_weight][:-1] + " kg", True, font_color)
        destination_surface_tekst_weight = surface_tekst_weight.get_rect()
        destination_surface_tekst_weight.center = (weight_tekst_x, weight_tekst_y)
        window.blit(surface_tekst_weight, destination_surface_tekst_weight)

        line_weight += 3
        weight_tekst_y += 40

    #zabezpieczenie przed przewijaniem tabela poza zakres listy gatunków z achievements_readlines
    #dostosuj to zabezpieczenie do ilości graczy zapisanych w statystykach np. another_five_species * player name
    if another_five_species == 0:

        # pygame.draw.rect(window, (0,0,0), [right_arrow_x, right_arrow_y, 21, 20])
        if mouse_pressed[0] == 1 and right_arrow_x + 25 > mouse_position[0] > right_arrow_x and right_arrow_y + 25 > mouse_position[1] > right_arrow_y:
        # if mouse_pressed[0] == 1 and right_arrow_x < mouse_position[0] < right_arrow_x + 21 and right_arrow_y < mouse_position[1] < right_arrow_y + 20:     #<- tu już do skasowania, ale zobacz dlaczego nie chciało działać!
            another_five_species += 15

    # zabezpieczenie przed przewijaniem tabela poza zakres listy gatunków z achievements_readlines
    if another_five_species == 15:
        # pygame.draw.rect(window, (0,0,0), [107, 350, 21, 20])
        if mouse_pressed[0] == 1 and left_arrow_x + 25 > mouse_position[0] > left_arrow_x and left_arrow_y + 25 > mouse_position[1] > left_arrow_y:
            another_five_species -= 15


# funkcja_achievements()



### Main loop...
main_loop_active = True

#Funkcje podrzędne
start_screen_active = True
rozgrywka_active = False
komunikat_active = False
achievements_active = False

while main_loop_active:

    #Menu start
    if start_screen_active:
        start()
        #Muzyka...
        # pygame.mixer.music.load("C:/Users/Maciek/Pictures/Python/Fishing Game/jeffy_theme.wav")
        pygame.mixer.music.load("C:/Users/Maciek/Pictures/Python/Fishing Game/coldplay_adventure1.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()
    #Rozgrywka
    elif rozgrywka_active:
        rozgrywka()
        #muzyka w trakcie rozgrywki...
        pygame.mixer.music.unpause()
    #Komunikaty
    elif komunikat_active:
        funkcja_komunikatu()
    #Osiągnięcia
    elif achievements_active:
        funkcja_achievements()

    #Pętla wydarzeń
    for event in pygame.event.get():
        #Przycisk wyjścia z gry
        if event.type == pygame.QUIT:
            main_loop_active = False


    pygame.display.update()

pygame.quit()


### ___

