###Wykorzystywane biblioteki...
import requests
from bs4 import BeautifulSoup as bs
import tkinter as tk
import os

###Słownik kodów postaci...
all_champions_dic_str = {"Aatrox":"266","Ahri":"103","Akali":"84","Alistar":"12","Amumu":"32","Anivia":"34","Annie":"1","Ashe":"22","AurelionSol":"136","Azir":"268","Bard":"432","Blitzcrank":"53","Brand":"63","Braum":"201","Caitlyn":"51","Camille":"164","Cassiopeia":"69","ChoGath":"31","Corki":"42","Darius":"122","Diana":"131","DrMundo":"36","Draven":"119","Ekko":"245","Elise":"60","Evelynn":"28","Ezreal":"81","Fiddlesticks":"9","Fiora":"114","Fizz":"105","Galio":"3","Gangplank":"41","Garen":"86","Gnar":"150","Gragas":"79","Graves":"104","Hecarim":"120","Heimerdinger":"74","Illaoi":"420","Irelia":"39","Ivern":"427","Janna":"40","JarvanIV":"59","Jax":"24","Jayce":"126","Jhin":"202","Jinx":"222","Kalista":"429","Karma":"43","Karthus":"30","Kassadin":"38","Katarina":"55","Kayle":"10","Kayn":"141","Kennen":"85","KhaZix":"121","Kindred":"203","Kled":"240","KogMaw":"96","LeBlanc":"7","LeeSin":"64","Leona":"89","Lissandra":"127","Lucian":"236","Lulu":"117","Lux":"99","Malphite":"54","Malzahar":"90","Maokai":"57","MasterYi":"11","MissFortune":"21","Mordekaiser":"82","Morgana":"25","Nami":"267","Nasus":"75","Nautilus":"111","Nidalee":"76","Nocturne":"56","Nunu":"20","Olaf":"2","Orianna":"61","Ornn":"516","Pantheon":"80","Poppy":"78","Quinn":"133","Rakan":"497","Rammus":"33","RekSai":"421","Renekton":"58","Rengar":"107","Riven":"92","Rumble":"68","Ryze":"13","Sejuani":"113","Shaco":"35","Shen":"98","Shyvana":"102","Singed":"27","Sion":"14","Sivir":"15","Skarner":"72","Sona":"37","Soraka":"16","Swain":"50","Syndra":"134","TahmKench":"223","Taliyah":"163","Talon":"91","Taric":"44","Teemo":"17","Thresh":"412","Tristana":"18","Trundle":"48","Tryndamere":"23","TwistedFate":"4","Twitch":"29","Udyr":"77","Urgot":"6","Varus":"110","Vayne":"67","Veigar":"45","VelKoz":"161","Vi":"254","Viktor":"112","Vladimir":"8","Volibear":"106","Warwick":"19","Wukong":"62","Xayah":"498","Xerath":"101","XinZhao":"5","Yasuo":"157","Yorick":"83","Zac":"154","Zed":"238","Ziggs":"115","Zilean":"26","Zoe":"142","Zyra":"143","Kaisa":"145","Pyke":"555","Sylas":"517", "Neeko":"518"}
all_champions_dic_str_reversed = {"266":"Aatrox","103":"Ahri","84":"Akali","12":"Alistar","32":"Amumu","34":"Anivia","1":"Annie","22":"Ashe","136":"AurelionSol","268":"Azir","432":"Bard","53":"Blitzcrank","63":"Brand","201":"Braum","51":"Caitlyn","164":"Camille","69":"Cassiopeia","31":"ChoGath","42":"Corki","122":"Darius","131":"Diana","36":"DrMundo","119":"Draven","245":"Ekko","60":"Elise","28":"Evelynn","81":"Ezreal","9":"Fiddlesticks","114":"Fiora","105":"Fizz","3":"Galio","41":"Gangplank","86":"Garen","150":"Gnar","79":"Gragas","104":"Graves","120":"Hecarim","74":"Heimerdinger","420":"Illaoi","39":"Irelia","427":"Ivern","40":"Janna","59":"JarvanIV","24":"Jax","126":"Jayce","202":"Jhin","222":"Jinx","429":"Kalista","43":"Karma","30":"Karthus","38":"Kassadin","55":"Katarina","10":"Kayle","141":"Kayn","85":"Kennen","121":"KhaZix","203":"Kindred","240":"Kled","96":"KogMaw","7":"LeBlanc","64":"LeeSin","89":"Leona","127":"Lissandra","236":"Lucian","117":"Lulu","99":"Lux","54":"Malphite","90":"Malzahar","57":"Maokai","11":"MasterYi","21":"MissFortune","82":"Mordekaiser","25":"Morgana","267":"Nami","75":"Nasus","111":"Nautilus","76":"Nidalee","56":"Nocturne","20":"Nunu","2":"Olaf","61":"Orianna","516":"Ornn","80":"Pantheon","78":"Poppy","133":"Quinn","497":"Rakan","33":"Rammus","421":"RekSai","58":"Renekton","107":"Rengar","92":"Riven","68":"Rumble","13":"Ryze","113":"Sejuani","35":"Shaco","98":"Shen","102":"Shyvana","27":"Singed","14":"Sion","15":"Sivir","72":"Skarner","37":"Sona","16":"Soraka","50":"Swain","134":"Syndra","223":"TahmKench","163":"Taliyah","91":"Talon","44":"Taric","17":"Teemo","412":"Thresh","18":"Tristana","48":"Trundle","23":"Tryndamere","4":"TwistedFate","29":"Twitch","77":"Udyr","6":"Urgot","110":"Varus","67":"Vayne","45":"Veigar","161":"VelKoz","254":"Vi","112":"Viktor","8":"Vladimir","106":"Volibear","19":"Warwick","62":"Wukong","498":"Xayah","101":"Xerath","5":"XinZhao","157":"Yasuo","83":"Yorick","154":"Zac","238":"Zed","115":"Ziggs","26":"Zilean","142":"Zoe","143":"Zyra","145":"Kaisa","555":"Pyke","517":"Sylas", "518":"Neeko"}
#^^brakuje Yummi i może kogoś z najnowszych postaci jeszcze.

###Funkcja zawierająca wszystkie inne funkcje służące określaniu statystyk, która jest wywoływana po kliknięciu przycisku "Research".
def almighty_function():
    try:
        ###Funkcja określająca obecne pliki w folderze logów LOL'a...
        def log_files_function():
            path = "C:/Program Files/Riot Games/League of Legends/Logs/LeagueClient Logs/"
            league_client = []
            league_client_ux = []
            # r=root, d=directories, f = files
            for r, d, f in os.walk(path):
                for file_name in f:
                    if "LeagueClient.log" in file_name:
                        league_client.append(os.path.join(r, file_name))
                    elif "LeagueClientUx.log" in file_name:
                        league_client_ux.append(os.path.join(r, file_name))
            return league_client[-1], league_client_ux[-1], league_client_ux[-2], league_client_ux[-3]
        #^^tu możesz zmieniać numery porządkowe tych plików - żeby zmienić na aktualne (na bieżąco) ustaw na -1, -1, -2, -3.

        log_files_function()
        # print(log_files_function())

        ###Automatyczne otwieranie pliku LeagueClient... Jeśli jest to otwieranie automatyczne to zmutuj poniższe otwieranie.
        try:
            with open(log_files_function()[0]) as clientlog:
                client = clientlog.readlines()
        except:
            "Komunikat o błędzie - automatyczny LeagueClient..."

        ###Ręczne otwieranie pliku z deklarowanymi postaciami...
        # # Aktualne nazwy plików logu gry clienta League of Legends do ręcznego otwierania...
        # LeagueClient_file_name = "2019-10-03T17-17-14_7444_LeagueClient"
        # LeagueClientUx_file_name = "2019-10-03T17-17-20_4780_LeagueClientUx"

        # try:
        #     with open("C:/Program Files/Riot Games/League of Legends/Logs/LeagueClient Logs/{}.log".format(LeagueClient_file_name)) as clientlog:
        #         client = clientlog.readlines()
        # except:
        #     print('Uaktualnij nazwę najświeższego pliku "LeagueClient" z folderu "/Riot Games/League of Legends/Logs/LeagueClient Logs/" i wszystko będzie działało poprawnie :)')


        ###Wyszukanie z pliku tekstowego logu Clienta championId, rozkodowanie ich za pomocą słownika na nazwy i utworzenie z nich listy...
        def funkcja0():
            lista_kodow_postaci0 = ""
            in_game_champions = ""
            for line in client:
                if line.find(""","championId":""") > 0:
                    linijka_podzielona = line.split(""","championId":""")
                    for fragment in linijka_podzielona[1:]:
                        lista_kodow_postaci0 += fragment[0:3] + " "
            lista_kodow_postaci1 = lista_kodow_postaci0.replace(",", "")
            lista_kodow_postaci2 = lista_kodow_postaci1.replace('"', "")
            lista_kodow_postaci3 = list(lista_kodow_postaci2.split(" "))
            # print(lista_kodow_postaci3[-11:-1])
            for liczba in lista_kodow_postaci3[-31:-1]:
                if liczba in all_champions_dic_str_reversed:
                    in_game_champions += all_champions_dic_str_reversed[liczba] + "&"
            # return in_game_champions
            aktywne_postacie = list(in_game_champions.split("&"))
            return aktywne_postacie[:-1]

        bany_postaci = funkcja0()[:9]
        kolejnosc_wyboru_postaci = funkcja0()[-20:-10]
        zlokowane_postacie = funkcja0()[-10:]
        my_team_champions = funkcja0()[-10:-5]
        # print("Bany: " + str(bany_postaci))
        # print("Kolejność wyboru: " + str(kolejnosc_wyboru_postaci))
        # print("Zlokowane postacie: " + str(zlokowane_postacie))
        # print("W mojej drużynie są: " + str(my_team_champions))

        ###Automatyczne otwieranie plików LeagueClientUx i określanie, który z nich zawiera potrzebne nam informacje...

        def ux_log_files_function():
            #otwiera kolejne najświeższe pliki z końcówką LeagueClientUx.log i sprawdza czy jest w nich zawarta fraza "summonerId"...
            with open(log_files_function()[1]) as clientUxlog1:
                ux_names1 = clientUxlog1.readlines()
            for line in ux_names1:
                if line.find("summonerId") > 0:
                    return ux_names1

            with open(log_files_function()[2]) as clientUxlog2:
                ux_names2 = clientUxlog2.readlines()
            for line in ux_names2:
                if line.find("summonerId") > 0:
                    return ux_names2

            with open(log_files_function()[3]) as clientUxlog2:
                ux_names3 = clientUxlog2.readlines()
            for line in ux_names3:
                if line.find("summonerId") > 0:
                    return ux_names3


        Ux_names = ux_log_files_function()

        ###Ręczne otwieranie pliku z nazwami graczy... Zmutuj to, jeśli automatyczne otwieranie powyżej jest aktywne
        # try:
        #     with open("C:/Program Files/Riot Games/League of Legends/Logs/LeagueClient Logs/{}.log".format(LeagueClientUx_file_name)) as clientUxlog:
        #         Ux_names = clientUxlog.readlines()
        # except:
        #     print('Uaktualnij nazwę najświeższego pliku "LeagueClientUx" z folderu "/Riot Games/League of Legends/Logs/LeagueClient Logs/" i wszystko będzie działało poprawnie :)')

        ###Wyszukanie z pliku tekstowego LeagueClientUx.log nicków graczy z własnej drużyny i utworzenie z nich listy...
        # *Jakby coś w przyszłości Riot coś zmienił i przestało działać, to można wyszukać summonerId i dopasować jako zgodność pomiędzy plikami LeagueClient i LeagueClientUx.
        def funkcja_names():
            displayed_names_str = ""
            for line in Ux_names:
                if line.find(''',"displayName":"''') > 0:
                    # print(line[line.find(''',"displayName":"''') + 16:])
                    for znak in line[line.find(''',"displayName":"''') + 16:]:
                        if znak == '"':
                            displayed_names_str += "&"
                            break  #tu zatrzymaj for loop najniższego rzędu
                        # if znak != '"':
                        displayed_names_str += znak
            return displayed_names_str
            # displayed_names_lista = list(displayed_names_str.split("&"))
            # return displayed_names_lista[:-1]
        player_names = funkcja_names()
        # print(player_names)
        # ^^ tu jako string rozdzielone znakiem "&"

        player_names_lista = list(player_names.split("&"))
        # print(player_names_lista[:-1])
        # ^^ tu jako lista


        ###Link do eune.op.gg na podstawie zmiennej player_names, czyli nicków graczy...
        my_team = player_names.replace("&", "%2C", 5)
        my_team_link = "https://eune.op.gg/multi/query=" + my_team
        my_team_link_nospace = my_team_link.replace(" ", "")
        # print(my_team_link_nospace)


        ###Informacje ze strony op.gg z wykorzystaniem biblioteki requests...
        page_opgg = requests.get(my_team_link_nospace)
        soup_opgg = bs(page_opgg.content, "html.parser")


        ###Funkcja do zestawienia nick'u gracza z właściwymi statystykami do deklarowanej postaci...
        def funkcja_stat_opgg():
            statistics_list = []
            summonername_str = ""
            for summonername_html in soup_opgg.find_all(class_="SummonerName"):
                summonername_str += summonername_html.get_text() + "&"
            summonername_order = summonername_str.split("&")[:-1]
            # print(summonername_order)

            stat_blocks = soup_opgg.find_all(class_="MultiSearchResultRowContent")
            champion_indeks = 0
            for player in player_names_lista[:-1]:
                block_indeks = summonername_order.index(player)
                tier_block = stat_blocks[block_indeks].find(class_="TierRank")
                statistics_list.append("Player name: " + player + " \n")

                general_winratio_html = tier_block.find(class_="WinRatio")
                if general_winratio_html is not None:
                    general_winratio = general_winratio_html.get_text()
                    statistics_list.append("General winratio: " + general_winratio + " \n")

                tier_rank_html = tier_block.find(class_="TierRank")
                if tier_rank_html is not None:
                    tier_rank = tier_rank_html.get_text().replace("\t", "")
                    division_end_indeks = tier_rank.find("(")
                    division = tier_rank[:division_end_indeks].replace("\n", "")
                    statistics_list.append("Division: " + division + " \n\nIn a season: \n")

                    champion_block = stat_blocks[block_indeks].find(class_="MostChampionStats tabItems")
                    champion_name_count = 0
                    never_played = 0
                    champion_html_all = champion_block.find_all(class_="ChampionName")
                    if champion_html_all is not None:
                        for champion_html in champion_html_all:
                            champion = champion_html.get_text()
                            if champion == my_team_champions[champion_indeks]:
                                game_count_html = champion_block.find_all(class_="GameCount Cell")[champion_name_count]
                                game_count_text = game_count_html.get_text().replace("\t", "")
                                game_count = game_count_text.replace("\n", "")
                                statistics_list.append(my_team_champions[champion_indeks] + " ranked played: " + game_count + " \n")
                                never_played += int(game_count)

                                winratio_html_cell = champion_block.find_all(class_="WinRatio Cell")[champion_name_count]
                                winratio_html = winratio_html_cell.findChild()
                                winratio = winratio_html.get_text()
                                statistics_list.append(my_team_champions[champion_indeks] + " winrate: " + winratio + " \n")
                                KDA_html_cell = champion_block.find_all(class_="KDA Cell")[champion_name_count]
                                KDA_html = KDA_html_cell.findChild()
                                KDA = KDA_html.get_text()
                                statistics_list.append(my_team_champions[champion_indeks] + " KDA: " + KDA + " \n\n")
                            champion_name_count += 1
                        if never_played == 0:
                            statistics_list.append(my_team_champions[champion_indeks] + " ranked played: 0 \n")
                        statistics_list.append("_____________________________________________________________________________\n\n")
                        champion_indeks += 1
                else:
                    statistics_list.append("Brak informacji o graczu: " + player + " ")
            return "".join(statistics_list)


        # funkcja_stat_opgg()
        # print(funkcja_stat_opgg())

        ###Wydruk statystyk w GUI...
        def stat_activation_function():
            # Aktywacja funkcji przycisku - wyświetlanie statystyk...
            text1 = tk.Text(window, width=77, height=19, font="arial", bd=0)
            text1.place(x=70, y=125)
            text1.insert(tk.INSERT, funkcja_stat_opgg())
            # text1.insert(tk.INSERT, funkcja_stat_opgg())
            text1.config(state="disabled")

            # Scrollbar...
            scrollbar_text1 = tk.Scrollbar(window, command=text1.yview)
            scrollbar_text1.place(x=765, y=65, height=424)
            # scrollbar_text1.config(command=text1.yview)  #<- można zamienić label na entry


        stat_activation_function()
    except:
        error_label = tk.Label(window, text="Oops! Something went wrong :( \nPlease try again later. \n\nPerhaps wait until all players lock their champions.", font="arial", justify="left")
        error_label.place(x=70, y=125)


###Graphical User Interface (GUI)...
window = tk.Tk()
window.title("Lol Bot v 1.0")
window_height = 640
window_width = 800
window.resizable(width=False, height=True)

canvas = tk.Canvas(window, height=window_height, width=window_width)
canvas.pack()

# Obraz w tle...
background_image = tk.PhotoImage(file="kingred background2.png")
background_label = tk.Label(window, image=background_image, bg="darkgray")
background_label.place(relwidth=1, relheight=1)

# Fragment błękitnego tła jako dekoracja...
background_element_label = tk.Label(window, height=28, width=80, bg="#6981bb", font="arial")
background_element_label.place(x=40, y=65)

# Instrukcja dla użytkownika...
informacja_label = tk.Label(window, height=2, width=80, text='''Click "Research" button when all players lock their champions.''', bg="#6981bb", fg="white", font="arial")
informacja_label.place(x=40, y=65)

# Białe tło dla wyświetlanych statystyk...
label_player1 = tk.Label(window, bg="white", fg="black", width=80, height=21, font="arial", justify="left")
label_player1.place(x=40, y=105)

# Przycisk do wciśnięcia po zlokowaniu wszystkich championów...
button_play = tk.Button(window, width=10, height=2, text="Research", bg="#208fbf", activebackground="#16546f", fg="white", activeforeground="white",  font="arial")
button_play.place(x=640, y=506)
button_play.config(command=almighty_function)

window.mainloop()


#Notatki, możliwe ulepszenia: ->
# a) urozmaicenie webscrapingu - może dodaj ilość wygranych i przegranych z rzędu (win/lose streak)
# b) dopisz warunki, które powiadomią użytkownika czy lepiej grać czy zdodgować
# c) zapisać program z rozszerzeniem .exe i dać graczom do wypróbowania
# d) spróbuj znaleźć fragment logu w LeagueClient lub LeagueClientUx, który stanowi przesłankę o zakończeniu procesu wybierania postaci przez graczy, bo wtedy można zwrócić użytkownikowi informacje, żeby poczekał aż wszyscy zatwierdzą swój wybór.
# e) popraw czytelność kodu, żeby był zdatny do użycia jako open source code. Np. zamień magic numbers na zmienne, dodaj komentarze wyjaśniające itp.
# f) dodaj if statements, żeby w funkcja_stat_opgg w przypadku, gdy stronie na op.gg nie ma zawartości tier_block lub champion_block wyświetlałą wszystkie informacje
# g) może dostosuj też do trybu gry blind pick, bo w sumie wystarczy banów nie uwzględniać i patrzeć na ostatnie pozycje championid
# h) nazwy graczy mogą niekiedy zawierać obce znaki (np. ruskie), co uniemożliwia wygenerowanie właściwego linku w op.gg dlatego musisz zrobić warunkowe przyjmowanie nazw graczy lub inny język tłumaczenia inputu
# i) zrób alternatywną wersję językową interfejsu




