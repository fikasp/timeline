import os, re
import subprocess
from encodings import utf_8

# Variables
year = 2025

# Path
input_path = 'b:\Prywatne\Lifebook\Timeline'

# @sup Categories
categories = {
  # @sub Atrakcje
  'Atrakcje': ['Basen', 'Centrum Nauki Kopernik', 'Festiwal Magii', 'Jaskinia Raj', 'Kopalnia soli', 'Kręgle', 'Łyżwy', 'Muzeum', 'Parada smoków', 'Park Niespodzianek', 'Smocza Jama', 'Termy', 'Turniej', 'Wawel', 'Wianki', 'Wydmy', 'Wystawa', 'Zamek', 'ZOO'],

  # @sub Góry
  'Góry': ['2013-08-24', 'Babia Góra', 'Barania Góra', 'Barnasiówka', 'Błędne Skały', 'Bystra', 'Ciecień', 'Ćwilin', 'Czarny Mniszek', 'Czerwone Wierchy', 'Czupel', 'Dolina Chochołowska', 'Dolina Goryczkowa', 'Dolina Kościeliska', 'Dolina Pięciu Stawów', 'Dolina Roztoki', 'Dolina Starorobociańska', 'Dróżki różańcowe', 'Gęsia Szyja', 'Giewont', 'Gorc', 'Goryczkowa Czuba', 'Granaty', 'Grzęda Rysów', 'Hala Łabowska', 'Hala Lipowska', 'Hala Pisana', 'Jałowiec', 'Jarząbczy Wierch', 'Jasknia Mroźna', 'Jaworzyna Krynicka', 'Kamiennik', 'Karb', 'Kasprowy Wierch', 'Kończysty Wierch', 'Kopieniec Wielki', 'Kościelec', 'Kościelisko', 'Koskowa Góra', 'Kotoń', 'Kozi Wierch', 'Koziarz', 'Krawców Wierch', 'Krzyżne', 'Kuźnice', 'Lackowa', 'Leskowiec', 'Lubań', 'Lubogoszcz', 'Lubomir', 'Luboń Wielki', 'Łysica', 'Magurki', 'Mędralowa', 'Modyń', 'Mogielica', 'Morskie Oko', 'Nosal', 'Orla Perć', 'Ornak', 'Pańska Przehybka', 'Piec', 'Pieniny', 'Pilsko', 'Plebańska Góra', 'Polana Huciska', 'Polana Michurowa', 'Polica', 'Połonica Caryńska', 'Połonina Wetlińska', 'Przehyba', 'Przełęcz', 'Przełęcze', 'Radziejowa', 'Rakoń', 'Rusinowa Polana', 'Rysy', 'Sarnie Skałki', 'Siwa Przełęcz', 'Skrzyczne', 'Śnieżka', 'Śnieżnica', 'Sokola Perć', 'Sokolica', 'Starorobociański Wierch', 'Stożek Wielki', 'Świnica', 'Świstowa Czuba', 'Szczebel', 'Szczeliniec Wielki', 'Szpiglasowy Wierch', 'Tarnica', 'Trzy Korony', 'Turbacz', 'Uklejna', 'Uklejnę', 'Wąwóz Homole', 'Wielka Racza', 'Wielka Rycerzowa', 'Wilczyce', 'Wołowiec', 'Wysoka', 'Żleb Kulczyckiego'],

  # @sub Domówki
  'Domówki': ['Ćwierćwiecze', 'DM Party', 'Dwudziestka', 'Dwunastka', 'Dziewiętnastka', 'Imprezki DM', 'Na Staszica', 'Pożegnanie pokoju', 'Spotkanie nostalgiczne', 'Starych dziejów', 'Trzydziestka', 'Urodziny Agusi', 'W domu'],

  # @sub Imprezy
  'Imprezy': ['Imieniny', 'Impreza', 'Imprezka', 'Urodziny'],

  # @sub Kawiarnie
  'Kawiarnie': ['Dziórawy Kocioł', 'Kawiarnia', 'Ministerstwo', 'Wilczy Dół'],

  # @sub Kluby
  'Kluby': ['Afera', 'Energy', 'Epsilon', 'Fashiontime', 'Gorączka', 'Pomarańcza'],

  # @sub Koncerty
  'Koncerty': ['Dyplom Karolinki', 'Filharmonia', 'Koncert', 'Organy', 'Tauron Arena', 'Zaduszki organowe'],

  # @sub Kościoły
  'Kościoły': ['Bolechowice', 'Częstochowa', 'Droga Krzyżowa', 'Jasna Góra', 'Kapucyni', 'Kościół', 'Niepokalanów', 'Pielgrzymka', 'ŚDM', 'Świątynia Opatrzności', 'Wszystkich Świętych', 'Zmartwychwstańcy'],

  # @sub Miasta
  'Miasta': ['Alwernia', 'Andrychów', 'Asyż', 'Babice', 'Barcelona', 'Będzin', 'Bełchatów', 'Biała Podlaska', 'Biała Rawska', 'Białystok', 'Biecz', 'Bielsko-Biała', 'Bieruń', 'Bobowa', 'Bochnia', 'Boguszów-Gorce', 'Brzesko', 'Brzeszcze', 'Budapeszt', 'Bukowno', 'Busko-Zdrój', 'Bydgoszcz', 'Bydlin', 'Bystrzyca Kłodzka', 'Bytom', 'Chabówka', 'Chęciny', 'Chełm', 'Chełmek', 'Chmielnik', 'Chorzów', 'Chrzanów', 'Ciechanów', 'Cieszyn', 'Ciężkowice', 'Collioure', 'Cuenca', 'Czchów', 'Czechowice-Dziedzice', 'Czechowice', 'Czeladź', 'Czorsztyn', 'Dąbrowa Górnicza', 'Dąbrowa Tarnowska', 'DąbrowaG.', 'DąbrowaT.', 'Darłowo', 'Dębica', 'Dobczyce', 'Działoszyce', 'Elbląg', 'Ełk', 'Figueres', 'Florencja', 'Frombork', 'Garwolin', 'Gdańsk', 'Gdynia', 'Giżycko', 'Gliwice', 'Głogów', 'Głogówek', 'Gniezno', 'Gorlice', 'Gorzów Wielkopolski', 'Grudziądz', 'Grybów', 'Grzybowo', 'Hel', 'Imielin', 'Inowrocław', 'Inwałd', 'Jarosław', 'Jasło', 'Jastrzębie-Zdrój', 'Jaworzno', 'Jędrzejów', 'Jelenia Góra', 'Jordanów', 'Kalisz', 'Kalwaria Zebrzydowska', 'Kamienna Góra', 'Karpacz', 'Katowice', 'Kazimierz Dolny', 'Kazimierza Wielka', 'Kędzierzyn-Koźle', 'Kęty', 'Kielce', 'Kłodzko', 'Kołobrzeg', 'Konin', 'Koszalin', 'Koszyce', 'Kowary', 'Koziegłowy', 'Kraków', 'Krosno', 'Krynica', 'Krzeszowice', 'Książ Wielki', 'Kutno', 'Lanckorona', 'Łańcut', 'Łazy', 'Lędziny', 'Legionowo', 'Legnica', 'Leszno', 'Libiąż', 'Licheń', 'Limanowa', 'Liszki', 'Łódź', 'Łomża', 'Lubin', 'Lublin', 'Madryt', 'Maków Podhalański', 'Malbork', 'Miechów', 'Międzylesie', 'Międzyzdroje', 'Mielec', 'Mielno', 'Mikołów', 'Milanówek', 'Mława', 'Monte Cassino', 'Moszna', 'Mszana Dolna', 'Muszyna', 'Myślenice', 'Mysłowice', 'Myszków', 'Neapol', 'Nidzica', 'Niedzica', 'Niepołomice', 'Nowa Ruda', 'Nowe Brzesko', 'Nowy Korczyn', 'Nowy Sącz', 'Nowy Targ', 'Nowy Wiśnicz', 'Nysa', 'Ogrodzieniec', 'Ojców', 'Oleśnica', 'Olkusz', 'Olsztyn', 'Opatowiec', 'Opoczno', 'Opole', 'Orneta', 'Ostróda', 'Ostrołęka', 'Ostrów Wielkopolski', 'Ostrowiec Świętokrzyski', 'Oświęcim', 'Otmuchów', 'Otwock', 'Pabianice', 'Pacanów', 'Paczków', 'Piaseczno', 'Piekary Śląskie', 'Piła', 'Pilica', 'Pilzno', 'Pińczów', 'Piotrków Trybunalski', 'Piwniczna', 'Płock', 'Polanica-Zdrój', 'Poręba', 'Poznań', 'Praga', 'Proszowice', 'Prudnik', 'Pruszków', 'Przemyśl', 'Przeworsk', 'Pszczyna', 'Puławy', 'Rabka', 'Racibórz', 'Racławice', 'Radłów', 'Radom', 'Radomsko', 'Radymno', 'Rimini', 'Ropczyce', 'Ruda Śląska', 'Rumia', 'Rybnik', 'Ryglice', 'Rzeszów', 'Rzym', 'San Marino', 'Sandomierz', 'Sanok', 'Saragossa', 'Sędziszów Małopolski', 'Sędziszów', 'Sępólno Krajeńskie', 'Siedlce', 'Siemianowice Śląskie', 'Siemianowice', 'Sieradz', 'Siewierz', 'Skała', 'Skalbmierz', 'Skamieniałe Miasto', 'Skarżysko-Kamienna', 'Skawina', 'Skierniewice', 'Sławków', 'Słomniki', 'Słupsk', 'Smoleń', 'Sopot', 'Sosnowiec', 'Stalowa Wola', 'Staniątki', 'Starachowice', 'Stargard', 'Starogard Gdański', 'Stary Sącz', 'Staszów', 'Stopnica', 'Sucha Beskidzka', 'Sułkowice', 'Suwałki', 'Świątniki Górne', 'Świdnica', 'Świętochłowice', 'Świnoujście', 'Szczawnica', 'Szczebrzeszyn', 'Szczecin', 'Szczekociny', 'Szczucin', 'Szczyrk', 'Szydłów', 'Tarnobrzeg', 'Tarnów', 'Tarnowskie Góry', 'Tczew', 'Tomaszów Mazowiecki', 'Toruń', 'Trzebinia', 'Tuchów', 'Tychy', 'Tylicz', 'Ustka', 'Ustroń', 'Wadowice', 'Wałbrzych', 'Walencja', 'Warszawa', 'Wejherowo', 'Wenecja', 'Wiedeń', 'Wieliczka', 'Wilamowice', 'Wisła', 'Wiślica', 'Włocławek', 'Wodzisław Śląski', 'Wojnicz', 'Wolbrom', 'Wrocław', 'Żabno', 'Zabrze', 'Zakliczyn', 'Zakopane', 'Zamość', 'Żarki', 'Zator', 'Zawiercie', 'Zduńska Wola', 'Zgierz', 'Zielona Góra', 'Złotoryja', 'Złoty Stok', 'Żnin', 'Żory', 'Żywiec'],

  # @sub Narty
  'Narty': ['Biegówki', 'Kotelnica', 'Master Ski', 'Narty'],

  # @sub Ogólne
  'Ogólne': ['Agnieszka', 'Agusia', 'Asia', 'Auto', 'Biuro', 'ŚDM Błonia', 'Gimnazjum', 'Kaśka', 'Koniec pracy', 'Konkursy', 'Kwadrat', 'Liceum', 'Natalia', 'Obrona', 'Początek związku', 'Podstawówka', 'Pokoik', 'Powiększenie biura', 'Praca', 'Prawo jazdy', 'Przedszkole', 'Przemuś', 'Rafał', 'Remont biura', 'Rodzeństwo', 'Rozdanie', 'Rozstanie', 'Sanatorium', 'Sesja', 'Sprzedaż', 'Statut', 'Studia', 'Szkoła', 'Volvo', 'Wykłady'],

  # @sub Restauracje
  'Restauracje': ['Restauracja', 'Taco Mexicano', 'Babcia Malina', 'Karczma', 'Przystanek Pierogarnia', 'Sphinx'],

  # @sub Rodzina
  'Rodzina': ['Boże narodzenie', 'Brzezinka', 'Dziadkowie', 'Dzień Dziecka', 'Grill', 'Karolinki', 'Karoliny', 'Kątscy', 'Maciejowskiej', 'Modelowie', 'Na Sądowej', 'Ognisko nad Rabą', 'Osieczany', 'Rodzina', 'U Ani', 'U Darka', 'U dziadków', 'W Brzezince', 'W Myślenicach', 'W Nowej Hucie', 'Wielkanoc', 'Wigilia', 'Wikusi', 'Załubińczu', '2013-06-30'],

  # @sub Rowery
  'Rowery': ['Rower'],

  # @sub Spacery
  'Spacery': ['Spacer', 'Dróżki Kalwaryjskie', 'Ogród Botaniczny', '2013-06-22', '2024-11-16'],

  # @sub Spektakle
  'Spektakle': ['Kino', 'Opera', 'Spektakl', 'Teatr', 'Wernisaż'],

  # @sub Uroczystości
  'Uroczystości': ['Chrzciny', 'Komunia', 'Oświadczyny', 'Pogrzeb', 'Poprawiny', 'Rocznica', 'Ślub', 'Wesele', 'Zjazd'],

  # @sub Wyjazdy
  'Wyjazdy': ['Biały Dunajec', 'Bieszczady', 'Bukowina', 'Czerwonka', 'Darłówko', 'Dźwirzyno', 'Glinka', 'Gródek', 'Grzybowo', 'Ibiza', 'Kreta', 'Krynica Morska', 'Łeba', 'Majorka', 'Międzyzdroje', 'Mielno', 'Mileżówka', 'Nocleg', 'Sarbinowo', 'Słowacki Raj', 'Sopot', 'Ustka', 'Wyjazd'],

  # @sub Znajomi
  'Znajomi': ['Adwentowe', 'Andrzejki', 'Artura', 'Aśki', 'Bal', 'Ciasteczkowe', 'Kawalerski', 'Klasowe', 'Mariusza', 'Mateusza', 'Męskie', 'Na Szubiennej', 'Nad Wisłę', 'Opłatkowe', 'Panieński', 'Planszówki', 'Podyplomowe', 'Poobozowe','Półmetek', 'Pooświadczynowe', 'Posesyjna', 'Posesyjne', 'Studniówka', 'U Anki', 'U Asi', 'U Kamila', 'U Kamili', 'U Kingi', 'U Łukasza', 'U Moniki', 'U Pawła', 'U Przemka', 'U Sebastiana', 'U Sysłów', 'U Wojtka', 'Urodzinowe', 'W biurze', 'W Brodach', 'W Krakowie', 'W Krempachach', 'W Polibudzie', 'Waldi', 'Walentynki', 'Wypad nad Wisłę', 'Znajomi'],
}

# @sup Program
print("📷 JPG to JS converter:")

# String list from categories
cat_keys = list(categories.keys())
cat_string = str(cat_keys)

# Open the output file
outputPath = os.path.join(input_path, 'index.js')
subprocess.run(['attrib', '-H', outputPath])

output = open(outputPath, 'w', encoding='utf8')

# Write header with categories
header = 'const cat = ' + cat_string + '\n\nconst data = [\n'
output.write(header)
# print(header)

# Initialize variable to keep track of the previous year
previous_year = '' 

# Traverse the directory structure
for root, dirs, files in os.walk(input_path):
  # Sort files
  files = sorted(files)
  for file in files:

    # Process jpg files only
    if file.endswith('.jpg'):

      # print(file)

      # Prepare file name
      filePath = os.path.join(root, file)
      string = file.replace('.jpg', '')

      # Separate date and event name
      if ' - ' in string:
        # Top-level file
        date, name = string.split(' - ', 1)
      else:
        continue
        # Subfolder case
        # date = os.path.basename(root).split(' - ', 1)[0]
        # name = os.path.basename(root).split(' - ', 1)[1] + '/' + string

      # Prepare category for event
      matched_category = []
      date_matched = False
      # Match categories based on patterns in file names
      for category, patterns in categories.items():
        for pattern in patterns:
          if pattern.lower() in name.lower() or pattern.lower() in date.lower():
            if re.match(r'^\d{4}-\d{2}-\d{2}$', pattern):
              matched_category = [category]
              date_matched = True
              break
            if (category not in matched_category):
              matched_category.append(category)
        if date_matched:
          break

      # Prepare years separators
      current_year = date.split('-')[0]
      if current_year != previous_year:
        header = f'// {current_year}'
        output.write(header + '\n')
        previous_year = current_year
        print(header)

      categories_string = str(matched_category)

      # Generate JavaScript object for the file
      js_obj = f"  {{date: '{date}', catg: {categories_string}, name: '{name}'}},"

      # Write the JavaScript object to the output file
      output.write(js_obj + '\n')
      
      # @sup Log
      if date.startswith(f'{year}'):
        print(js_obj)

      # print(js_obj)

# Write footer
output.write(']')

# Close the output file
output.close()

subprocess.run(['attrib', '+H', outputPath])

print('🏆 Conversion done!')
