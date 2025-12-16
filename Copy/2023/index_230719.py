import os
from encodings import utf_8

# Path
inputPath = 'B:/Prywatne/Lifebook/Timeline'
outputPath = 'B:/Prywatne/Lifebook/Timeline.js'

# Category
  # @sup Categories
categories = {
  # @sub Atrakcje
  'Atrakcje': [
    'Kręgle',
    'Łyżwy',
    'Muzeum',
    'Parada smoków',
    'Park Niespodzianek',
    'Smocza Jama',
    'Termy',
    'Wawel',
    'Wianki',
    'Wystawa',
    'ZOO',
  ],
  # @sub Góry
  'Góry': [
    'Babia Góra',
    'Barnasiówka',
    'Bystra',
    'Ciecień',
    'Czerwone Wierchy',
    'Czupel',
    'Dolina Chochołowska',
    'Dolina Pięciu Stawów',
    'Dolina Roztoki',
    'Giewont',
    'Gorc',
    'Goryczkowa Czuba',
    'Hala Łabowska',
    'Hala Lipowska',
    'Hala Pisana',
    'Jarząbczy Wierch',
    'Jasknia Mroźna',
    'Jaworzyna Krynicka',
    'Karb',
    'Kasprowy Wierch',
    'Kończysty Wierch',
    'Kościelec',
    'Kościelisko',
    'Koskowa Góra',
    'Kotoń',
    'Koziarz',
    'Krawców Wierch',
    'Krzyżne',
    'Lackowa',
    'Leskowiec',
    'Lubań',
    'Lubogoszcz',
    'Lubomir',
    'Luboń Wielki',
    'Łysica','Magurki',
    'Mędralowa',
    'Mogielica',
    'Nosal',
    'Orla Perć',
    'Ornak',
    'Piec','Pieniny',
    'Pilsko',
    'Plebańska Góra',
    'Polica',
    'Połonica Caryńska',
    'Połonina Wetlińska',
    'Przehyba',
    'Przełęcze',
    'Radziejowa',
    'Rakoń',
    'Rysy',
    'Sarnie Skałki',
    'Skrzyczne',
    'Śnieżnica',
    'Sokola Perć',
    'Sokolica',
    'Starorobociański Wierch',
    'Stożek Wielki',
    'Świnica',
    'Świstowa Czuba',
    'Szczebel',
    'Szpiglasowy Wierch',
    'Tarnica',
    'Trzy Korony',
    'Turbacz',
    'Uklejna',
    'Uklejnę',
    'Wąwóz Homole',
    'Wielka Racza' ,
    'Wielka Rycerzowa',
    'Wołowiec',
    'Wysoka',
  ],
  # @sub Domówki
  'Domówki': [
    'Ćwierćwiecze',
    'DM Party',
    'Dwudziestka',
    'Na Staszica',
    'Parapetówka',
    'Pożegnanie pokoju',
    'Spotkanie nostalgiczne',
    'Trzydziestka',
    'Urodziny Agusi',
    'W domu',
    'Wspomnienie starych dziejów',
  ],
  # @sub Imprezy
  'Imprezy': [
    'Imieniny',
    'Impreza',
    'Imprezka',
    'Urodziny'
  ],
  # @sub Kawiarnie
  'Kawiarnie': [
    'Dziórawy Kocioł',
    'Kawiarnia',
    'Ministerstwo',
    'Wilczy Dół',
  ],
  # @sub Kluby
  'Kluby': [
    'Afera',
    'Energy',
    'Epsilon',
    'Fashiontime',
    'Gorączka',
    'Pomarańcza',
  ],
  # @sub Koncerty
  'Koncerty': [
    'Dyplom Karolinki',
    'Filharmonia',
    'Koncert',
    'Organy',
    'Tauron Arena',
    'Zaduszki organowe',
  ],
  # @sub Kościoły
  'Kościoły': [
    'Częstochowa',
    'Droga Krzyżowa',
    'Kapucyni',
    'Kościół',
    'ŚDM',
    'Wszystkich Świętych',
    'Zmartwychwstańcy',
  ],
  # @sub Miasta
  'Miasta': [
    'Alwernia',
    'Andrychów',
    'Babice',
    'Barcelona',
    'Będzin',
    'Bełchatów',
    'Biała Podlaska',
    'Biała Rawska',
    'Białystok',
    'Biecz',
    'Bielsko-Biała',
    'Bieruń',
    'Bobowa',
    'Bochnia',
    'Brzesko',
    'Brzeszcze',
    'Budapeszt',
    'Bukowno',
    'Busko-Zdrój',
    'Bydgoszcz',
    'Bydlin',
    'Bytom',
    'Chabówka',
    'Chęciny',
    'Chełm',
    'Chełmek',
    'Chorzów',
    'Chrzanów',
    'Ciechanów',
    'Cieszyn',
    'Ciężkowice',
    'Collioure',
    'Cuenca',
    'Czchów',
    'Czechowice-Dziedzice',
    'Czechowice',
    'Czeladź',
    'Dąbrowa Górnicza',
    'Dąbrowa Tarnowska',
    'DąbrowaG.',
    'DąbrowaT.',
    'Darłowo',
    'Dębica',
    'Dobczyce',
    'Działoszyce',
    'Elbląg',
    'Ełk',
    'Figueres',
    'Frombork',
    'Garwolin',
    'Gdańsk',
    'Gdynia',
    'Giżycko',
    'Gliwice',
    'Głogów',
    'Głogówek',
    'Gniezno',
    'Gorlice',
    'Gorzów Wielkopolski',
    'Grudziądz',
    'Grybów',
    'Grzybowo',
    'Hel',
    'Inowrocław',
    'Inwałd','Jarosław',
    'Jasło',
    'Jastrzębie-Zdrój',
    'Jaworzno',
    'Jędrzejów',
    'Jelenia Góra',
    'Jordanów',
    'Kalisz',
    'Kalwaria Zebrzydowska',
    'Karpacz',
    'Katowice',
    'Kazimierz Dolny',
    'Kazimierza Wielka',
    'Kędzierzyn-Koźle',
    'Kęty',
    'Kielce',
    'Kłodzko',
    'Kołobrzeg',
    'Konin',
    'Koszalin',
    'Koszyce',
    'Kraków',
    'Krosno',
    'Krynica',
    'Krzeszowice',
    'Książ Wielki',
    'Kutno',
    'Lanckorona',
    'Łańcut',
    'Legionowo',
    'Legnica',
    'Leszno',
    'Libiąż',
    'Licheń',
    'Limanowa',
    'Liszki',
    'Łódź',
    'Łomża',
    'Lubin',
    'Lublin',
    'Madryt',
    'Maków Podhalański',
    'Malbork',
    'Miechów',
    'Międzylesie',
    'Międzyzdroje',
    'Mielec',
    'Mielno',
    'Mikołów',
    'Milanówek',
    'Mława',
    'Mszana Dolna',
    'Muszyna',
    'Myślenice',
    'Mysłowice',
    'Myszków',
    'Nidzica',
    'Niepołomice',
    'Nowe Brzesko',
    'Nowy Korczyn',
    'Nowy Sącz',
    'Nowy Targ',
    'Nowy Wiśnicz',
    'Nysa',
    'Ogrodzieniec',
    'Ojców',
    'Olkusz',
    'Olsztyn',
    'Opatowiec',
    'Opoczno',
    'Opole',
    'Orneta',
    'Ostrołęka',
    'Ostrów Wielkopolski',
    'Ostrowiec Świętokrzyski',
    'Oświęcim',
    'Otmuchów',
    'Otwock',
    'Pabianice',
    'Pacanów',
    'Paczków',
    'Piaseczno',
    'Piekary Śląskie',
    'Piła',
    'Pilica',
    'Pilzno',
    'Pińczów',
    'Piotrków Trybunalski',
    'Piwniczna',
    'Piwniczna',
    'Płock',
    'Poznań',
    'Praga','Proszowice',
    'Prudnik',
    'Pruszków',
    'Przemyśl',
    'Przeworsk',
    'Pszczyna',
    'Puławy',
    'Rabka',
    'Racibórz',
    'Racławice',
    'Radłów',
    'Radom',
    'Radomsko',
    'Radymno',
    'Ropczyce',
    'Ruda Śląska',
    'Rumia',
    'Rybnik',
    'Ryglice',
    'Rzeszów',
    'Sandomierz',
    'Sanok',
    'Saragossa',
    'Sędziszów Małopolski',
    'Sępólno Krajeńskie',
    'Siedlce',
    'Siemianowice Śląskie',
    'Siemianowice',
    'Sieradz',
    'Siewierz',
    'Skała',
    'Skalbmierz',
    'Skamieniałe Miasto',
    'Skarżysko-Kamienna',
    'Skawina',
    'Skierniewice',
    'Sławków',
    'Słomniki',
    'Słupsk',
    'Smoleń','Sopot',
    'Sosnowiec',
    'Stalowa Wola',
    'Staniątki',
    'Starachowice',
    'Stargard',
    'Starogard Gdański',
    'Stary Sącz',
    'Stopnica',
    'Sucha Beskidzka',
    'Sułkowice',
    'Suwałki',
    'Świątniki Górne',
    'Świdnica',
    'Świętochłowice',
    'Świnoujście',
    'Szczawnica',
    'Szczebrzeszyn',
    'Szczecin',
    'Szczekociny',
    'Szczucin',
    'Szczyrk',
    'Tarnobrzeg',
    'Tarnów',
    'Tarnowskie Góry',
    'Tczew',
    'Tomaszów Mazowiecki',
    'Tomaszów',
    'Toruń',
    'Trzebinia',
    'Tuchów',
    'Tychy',
    'Tylicz',
    'Ustka',
    'Ustroń',
    'Wadowice',
    'Wałbrzych',
    'Walencja',
    'Warszawa',
    'Wejherowo',
    'Wenecji',
    'Wiedeń',
    'Wieliczka',
    'Wiślica',
    'Włocławek',
    'Wodzisław Śląski',
    'Wodzisław',
    'Wojnicz',
    'Wolbrom',
    'Wrocław',
    'Żabno',
    'Zabrze',
    'Zakliczyn',
    'Zakopane',
    'Zamość',
    'Zator',
    'Zawiercie',
    'Zduńska Wola',
    'Zgierz',
    'Zielona Góra',
    'Złotoryja',
    'Żnin',
    'Żory',
    'Żywiec',
  ],
  # @sub Narty
  'Narty': [
    'Kotelnica',
    'Master Ski',
    'Narty',
  ],
  # @sub Ogólne
  'Ogólne': [
    'Agnieszka',
    'Auto',
    'Biuro',
    'Kaśka',
    'Koniec pracy',
    'Konkursy',
    'Obrona',
    'Pokoik',
    'Praca',
    'Rozdanie dyplomów',
    'Rozstanie',
    'Sesja',
    'Statut Kwadratu',
    'Wykłady',
    'Volvo',
  ],
  # @sub Restauracje
  'Restauracje': [
    'Restauracja',
    'Taco Mexicano',
  ],
  # @sub Rodzina
  'Rodzina': [
    'Boże narodzenie',
    'Brzezinka',
    'Dziadkowie',
    'Dzień Dziecka',
    'Grill',
    'Karolinki',
    'Karoliny',
    'Kątscy',
    'Modelowie',
    'Osieczany',
    'Rodzina',
    'U Ani',
    'W Brzezince',
    'W Nowej Hucie',
    'Wielkanoc',
    'Wigilia',
    'Wikusi',
    'Załubińczu',
  ],
  # @sub Rowery
  'Rowery': [
    'Rower',
  ],
  # @sub Spacery
  'Spacery': [
    'Spacer',
    'Ogród Botaniczny',
  ],
  # @sub Spektakle
  'Spektakle': [
    'Kino',
    'Opera',
    'Spektakl',
    'Teatr',
    'Wernisaż',
  ],
  # @sub Uroczystości
  'Uroczystości': [
    'Chrzciny',
    'Oświadczyny',
    'Pogrzeb',
    'Poprawiny',
    'Rocznica',
    'Ślub',
    'Wesele',
  ],
  # @sub Wyjazdy
  'Wyjazdy': [
    'Bieszczady',
    'Bukowina',
    'Dźwirzyno',
    'Gródek',
    'Grzybowo',
    'Ibiza',
    'Kreta',
    'Krynica Morska',
    'Łeba',
    'Majorka',
    'Międzyzdroje',
    'Mielno',
    'Mileżówka',
    'Sopot',
    'Ustka',
    'Wyjazd',
  ],
  # @sub Znajomi
  'Znajomi': [
    'Adwentowe',
    'Andrzejki',
    'Artura',
    'Bal',
    'Ciasteczkowe',
    'Kawalerski',
    'Klasowe',
    'Mariusza',
    'Mateusza',
    'Męskie',
    'Na Szubiennej',
    'Opłatkowe',
    'Panieński',
    'Planszówki',
    'Podyplomowe',
    'Pooświadczynowe',
    'Posesyjna',
    'Posesyjne',
    'U Asi',
    'U Kamila',
    'U Kamili',
    'U Kingi',
    'U Łukasza',
    'U Pawła',
    'U Przemka',
    'U Sebastiana',
    'Urodzinowe',
    'W biurze',
    'W Brodach',
    'W Krempachach',
    'W Polibudzie',
    'Walentynki',
    'Znajomi'
  ]
}

# @sup Program
# String list from categories
cat_keys = list(categories.keys())
cat_string = str(cat_keys)

# Open the output file
output = open(outputPath, 'w', encoding='utf8')

# Write header with categories
header = 'const cat = ' + cat_string + '\n\nconst data = [\n'
output.write(header)
print(header)

# Initialize variable to keep track of the previous year
previous_year = '' 

# Traverse the directory structure
for root, dirs, files in os.walk(inputPath):
  # Sort files
  files = sorted(files)
  for file in files:

    # Process jpg files only
    if file.endswith('.jpg'):

      # Prepare file name
      filePath = os.path.join(root, file)
      string = file.replace('.jpg', '')

      # Separate date and event name
      splitted_string = string.split(' - ', 1)
      if len(splitted_string) < 2:
        continue  
      date = splitted_string[0]
      name = splitted_string[1]

      # Prepare category for event
      matched_category = []
      # Match categories based on patterns in file names
      for category, patterns in categories.items():
        for pattern in patterns:
          if pattern.lower() in name.lower():
            if (category == 'Spacery' 
              or category == 'Rowery' 
              or category == 'Narty'     
              or category == matched_category):
              matched_category.clear()
            if (category not in matched_category):
              matched_category.append(category)

      # Prepare years separators
      current_year = date.split('-')[0]
      if current_year != previous_year:
        header = f'// {current_year}'
        output.write(header + '\n')
        previous_year = current_year
        print(header)

      categories_string = str(matched_category)

      # Generate JavaScript object for the file
      js_obj = f"{{date: '{date}', catg: {categories_string}, name: '{name}'}},"

      # Write the JavaScript object to the output file
      output.write(js_obj + '\n')
      
      # @sup Log
      # Print log
      if date.startswith('2009'):
        print(js_obj)

      # print(js_obj)

# Write footer
output.write(']')

# Close the output file
output.close()

print('Conversion done...')
