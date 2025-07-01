import os, re
import subprocess
import unicodedata
from pathlib import Path
from PIL.ExifTags import TAGS
from PIL import Image
# pip install pillow

YEAR = 2021

# @sup Config

categories = {
  # @sub Atrakcje
  'Atrakcje': ['Basen', 'Centrum Nauki Kopernik', 'Festiwal Magii', 'Jaskinia Raj', 'Kopalnia soli', 'Kręgle', 'Łyżwy', 'Muzeum', 'Parada smoków', 'Park Niespodzianek', 'Smocza Jama', 'Terma', 'Termy', 'Turniej', 'Wawel', 'Wianki', 'Wydmy', 'Wystawa', 'Zamek', 'ZOO'],

  # @sub Gastronomia
  'Gastronomia': ['Kawiarnia','Restauracja', 'Babcia Malina', 'Karczma', 'Przystanek Pierogarnia', 'Sphinx'],

  # @sub Góry
  'Góry': ['2013-08-24', 'Babia Góra', 'Barania Góra', 'Barnasiówka', 'Błędne Skały', 'Bystra', 'Ciecień', 'Ćwilin', 'Czarny Mniszek', 'Czerwone Wierchy', 'Czupel', 'Dolina Chochołowska', 'Dolina Goryczkowa', 'Dolina Kościeliska', 'Dolina Pięciu Stawów', 'Dolina Roztoki', 'Dolina Starorobociańska', 'Dróżki różańcowe', 'Gęsia Szyja', 'Giewont', 'Gorc', 'Goryczkowa Czuba', 'Granaty', 'Grzęda Rysów', 'Hala Łabowska', 'Hala Lipowska', 'Hala Pisana', 'Jałowiec', 'Jarząbczy Wierch', 'Jasknia Mroźna', 'Jaworzyna Krynicka', 'Kamiennik', 'Karb', 'Kasprowy Wierch', 'Kończysty Wierch', 'Kopieniec Wielki', 'Kościelec', 'Kościelisko', 'Koskowa Góra', 'Kotoń', 'Kozi Wierch', 'Koziarz', 'Krawców Wierch', 'Krzyżne', 'Kuźnice', 'Lackowa', 'Leskowiec', 'Lubań', 'Lubogoszcz', 'Lubomir', 'Luboń Wielki', 'Łysica', 'Magurki', 'Mędralowa', 'Modyń', 'Mogielica', 'Morskie Oko', 'Nosal', 'Orla Perć', 'Ornak', 'Pańska Przehybka', 'Piec', 'Pieniny', 'Pilsko', 'Plebańska Góra', 'Polana Huciska', 'Polana Michurowa', 'Polica', 'Połonica Caryńska', 'Połonina Wetlińska', 'Przehyba', 'Przełęcz', 'Przełęcze', 'Pusta Wielka','Radziejowa', 'Rakoń', 'Rusinowa Polana', 'Rysy', 'Sarnie Skałki', 'Siwa Przełęcz', 'Skrzyczne', 'Śnieżka', 'Śnieżnica', 'Sokola Perć', 'Sokolica', 'Starorobociański Wierch', 'Stożek Wielki', 'Świnica', 'Świstowa Czuba', 'Szczebel', 'Szczeliniec Wielki', 'Szpiglasowy Wierch', 'Tarnica', 'Trzy Korony', 'Turbacz', 'Uklejna', 'Uklejnę', 'Wąwóz Homole', 'Wielka Racza', 'Wielka Rycerzowa', 'Wilczyce', 'Wołowiec', 'Wysoka', 'Żleb Kulczyckiego'],

  # @sub Domówki
  'Domówki': ['Ćwierćwiecze', 'DM Party', 'Dwudziestka', 'Dwunastka', 'Dziewiętnastka', 'Imprezki DM', 'Na Staszica', 'Pożegnanie pokoju', 'Spotkanie nostalgiczne', 'Starych dziejów', 'Trzydziestka', 'Urodziny Agusi', 'W domu'],

  # @sub Koncerty
  'Koncerty': ['Dyplom Karolinki', 'Filharmonia', 'Koncert', 'Organy', 'Tauron Arena', 'Zaduszki organowe'],

  # @sub Kościoły
  'Kościoły': ['Bolechowice', 'Częstochowa', 'Droga Krzyżowa', 'Jasna Góra', 'Kapucyni', 'Kościół', 'Niepokalanów', 'Pielgrzymka', 'ŚDM', 'Świątynia Opatrzności', 'Wszystkich Świętych', 'Zmartwychwstańcy'],

  # @sub Miasta
  'Miasta': ['Alwernia', 'Andrychów', 'Asyż', 'Babice', 'Barcelona', 'Będzin', 'Bełchatów', 'Biała Podlaska', 'Biała Rawska', 'Białystok', 'Biecz', 'Bielsko-Biała', 'Bieruń', 'Bobowa', 'Bochnia', 'Boguszów-Gorce', 'Brzesko', 'Brzeszcze', 'Budapeszt', 'Bukowno', 'Busko-Zdrój', 'Bydgoszcz', 'Bydlin', 'Bystrzyca Kłodzka', 'Bytom', 'Chabówka', 'Chęciny', 'Chełm', 'Chełmek', 'Chmielnik', 'Chorzów', 'Chrzanów', 'Ciechanów', 'Cieszyn', 'Ciężkowice', 'Collioure', 'Cuenca', 'Czchów', 'Czechowice-Dziedzice', 'Czechowice', 'Czeladź', 'Czorsztyn', 'Dąbrowa Górnicza', 'Dąbrowa Tarnowska', 'DąbrowaG.', 'DąbrowaT.', 'Darłowo', 'Dębica', 'Dobczyce', 'Działoszyce', 'Elbląg', 'Ełk', 'Figueres', 'Florencja', 'Frombork', 'Garwolin', 'Gdańsk', 'Gdynia', 'Giżycko', 'Gliwice', 'Głogów', 'Głogówek', 'Gniezno', 'Gorlice', 'Gorzów Wielkopolski', 'Grudziądz', 'Grybów', 'Grzybowo', 'Hel', 'Imielin', 'Inowrocław', 'Inwałd', 'Jarosław', 'Jasło', 'Jastrzębie-Zdrój', 'Jaworzno', 'Jędrzejów', 'Jelenia Góra', 'Jordanów', 'Kalisz', 'Kalwaria Zebrzydowska', 'Kamienna Góra', 'Karpacz', 'Katowice', 'Kazimierz Dolny', 'Kazimierza Wielka', 'Kędzierzyn-Koźle', 'Kęty', 'Kielce', 'Kłodzko', 'Kołobrzeg', 'Konin', 'Koszalin', 'Koszyce', 'Kowary', 'Koziegłowy', 'Kraków', 'Krosno', 'Krynica', 'Krzeszowice', 'Książ Wielki', 'Kutno', 'Lanckorona', 'Łańcut', 'Łazy', 'Lędziny', 'Legionowo', 'Legnica', 'Leszno', 'Libiąż', 'Licheń', 'Limanowa', 'Liszki', 'Łódź', 'Łomża', 'Lubin', 'Lublin', 'Madryt', 'Maków Podhalański', 'Malbork', 'Miechów', 'Międzylesie', 'Międzyzdroje', 'Mielec', 'Mielno', 'Mikołów', 'Milanówek', 'Mława', 'Monte Cassino', 'Moszna', 'Mszana Dolna', 'Muszyna', 'Myślenice', 'Mysłowice', 'Myszków', 'Neapol', 'Nidzica', 'Niedzica', 'Niepołomice', 'Nowa Ruda', 'Nowe Brzesko', 'Nowy Korczyn', 'Nowy Sącz', 'Nowy Targ', 'Nowy Wiśnicz', 'Nysa', 'Ogrodzieniec', 'Ojców', 'Oleśnica', 'Olkusz', 'Olsztyn', 'Opatowiec', 'Opoczno', 'Opole', 'Orneta', 'Ostróda', 'Ostrołęka', 'Ostrów Wielkopolski', 'Ostrowiec Świętokrzyski', 'Oświęcim', 'Otmuchów', 'Otwock', 'Pabianice', 'Pacanów', 'Paczków', 'Piaseczno', 'Piekary Śląskie', 'Piła', 'Pilica', 'Pińczów', 'Piotrków Trybunalski', 'Piwniczna', 'Płock', 'Polanica-Zdrój', 'Poręba', 'Poznań', 'Praga', 'Proszowice', 'Prudnik', 'Pruszków', 'Przemyśl', 'Przeworsk', 'Pszczyna', 'Puławy', 'Rabka', 'Racibórz', 'Racławice', 'Radłów', 'Radom', 'Radomsko', 'Radymno', 'Rimini', 'Ropczyce', 'Ruda Śląska', 'Rumia', 'Rybnik', 'Ryglice', 'Rzeszów', 'San Marino', 'Sandomierz', 'Sanok', 'Saragossa', 'Sędziszów Małopolski', 'Sędziszów', 'Sępólno Krajeńskie', 'Siedlce', 'Siemianowice Śląskie', 'Siemianowice', 'Sieradz', 'Siewierz', 'Skała', 'Skalbmierz', 'Skamieniałe Miasto', 'Skarżysko-Kamienna', 'Skawina', 'Skierniewice', 'Sławków', 'Słomniki', 'Słupsk', 'Smoleń', 'Sopot', 'Sosnowiec', 'Stalowa Wola', 'Staniątki', 'Starachowice', 'Stargard', 'Starogard Gdański', 'Stary Sącz', 'Staszów', 'Stopnica', 'Sucha Beskidzka', 'Sułkowice', 'Suwałki', 'Świątniki Górne', 'Świdnica', 'Świętochłowice', 'Świnoujście', 'Szczawnica', 'Szczebrzeszyn', 'Szczecin', 'Szczekociny', 'Szczucin', 'Szczyrk', 'Szydłów', 'Tarnobrzeg', 'Tarnów', 'Tarnowskie Góry', 'Tczew', 'Tomaszów Mazowiecki', 'Toruń', 'Trzebinia', 'Tuchów', 'Tychy', 'Tylicz', 'Ustka', 'Ustroń', 'Wadowice', 'Wałbrzych', 'Walencja', 'Warszawa', 'Wejherowo', 'Wenecja', 'Wiedeń', 'Wieliczka', 'Wilamowice', 'Wisła', 'Wiślica', 'Włocławek', 'Wodzisław Śląski', 'Wojnicz', 'Wolbrom', 'Wrocław', 'Żabno', 'Zabrze', 'Zakliczyn', 'Zakopane', 'Zamość', 'Żarki', 'Zator', 'Zawiercie', 'Zduńska Wola', 'Zgierz', 'Zielona Góra', 'Złotoryja', 'Złoty Stok', 'Żnin', 'Żory', 'Żywiec'],

  # @sub Narty
  'Narty': ['Biegówki', 'Kotelnica', 'Master Ski', 'Narty'],

  # @sub Ogólne
  'Ogólne': ['Agnieszka', 'Agusia', 'Asia', 'Auto', 'Biuro', 'ŚDM Błonia', 'Gimnazjum', 'Kaśka', 'Koniec pracy', 'Konkursy', 'Kwadrat', 'Liceum', 'Natalia', 'Obrona', 'Początek związku', 'Podstawówka', 'Pokoik', 'Powiększenie biura', 'Praca', 'Prawo jazdy', 'Przedszkole', 'Przemuś', 'Rafał', 'Remont','Rodzeństwo', 'Rozdanie', 'Rozstanie', 'Sanatorium', 'Sesja', 'Sprzedaż', 'Statut', 'Studia', 'Szkoła', 'Volvo', 'Wykłady'],

  # @sub Rodzina
  'Rodzina': ['Boże narodzenie', 'Brzezinka', 'Dziadkowie', 'Dzień Dziecka', 'Grill', 'Karolinki', 'Karoliny', 'Kątscy', 'Maciejowskiej', 'Modelowie', 'Na Sądowej', 'Ognisko nad Rabą', 'Osieczany', 'Rodzina', 'Święcenie pokarmów', 'U Ani', 'U Darka', 'U dziadków', 'W Brzezince', 'W Myślenicach', 'W Nowej Hucie', 'Wielkanoc', 'Wigilia', 'Wikusi', 'Załubińczu'],

  # @sub Rowery
  'Rowery': ['Rower'],

  # @sub Spacery
  'Spacery': ['Spacer'],

  # @sub Spektakle
  'Spektakle': ['Kino', 'Opera', 'Spektakl', 'Teatr', 'Wernisaż'],

  # @sub Uroczystości
  'Uroczystości': ['Chrzciny', 'Komunia', 'Oświadczyny', 'Pogrzeb', 'Poprawiny', 'Rocznica', 'Ślub', 'Wesele', 'Zjazd'],

  # @sub Wyjazdy
  'Wyjazdy': ['Biały Dunajec', 'Bieszczady', 'Bukowina', 'Czerwonka', 'Darłówko', 'Dźwirzyno', 'Glinka', 'Gródek', 'Grzybowo', 'Ibiza', 'Kreta', 'Krępachy', 'Krynica Morska', 'Łeba', 'Majorka', 'Międzyzdroje', 'Mielno', 'Mileżówka', 'Nocleg', 'Podróż', 'Sarbinowo', 'Słowacki Raj', 'Sopot', 'Ustka', 'Wyjazd'],

  # @sub Znajomi
  'Znajomi': ['Adwentowe', 'Andrzejki', 'Artura', 'Aśki', 'Bal', 'Ciasteczkowe', 'Kawalerski', 'Klasowe', 'Mariusza', 'Mateusza', 'Męskie', 'Na Szubiennej', 'Nad Wisłę', 'Opłatkowe', 'Panieński', 'Planszówki', 'Podyplomowe', 'Poobozowe','Półmetek', 'Pooświadczynowe', 'Posesyjna', 'Posesyjne', 'Studniówka', 'U Anki', 'U Asi', 'U Kamila', 'U Kamili', 'U Kingi', 'U Łukasza', 'U Moniki', 'U Pawła', 'U Przemka', 'U Sebastiana', 'U Sysłów', 'U Wojtka', 'Urodzinowe', 'W biurze', 'W Brodach', 'W Krakowie', 'W Krempachach', 'W Polibudzie', 'Waldi', 'Walentynki', 'Wypad nad Wisłę', 'Znajomi'],
}

# @sup Program
print("📷 JPG to JS converter:")

# Category keys
cat_keys = list(categories.keys())

# Set input and output paths
input_path = Path(__file__).parent.resolve()
outputPath = input_path / 'index.js'

# Remove hidden attribute from output file if it exists
subprocess.run(['attrib', '-H', outputPath])

# Open output file for writing with UTF-8 encoding
output = open(outputPath, 'w', encoding='utf8')

# Write initial JS header: category keys and start of data array
output.write(f"const cat = {cat_keys}\n\nconst data = [\n")

# Keep track of last processed year to insert year separators
previous_year = '' 

# Normalize filenames
def normalize_filename(s):
  """Normalize filename by removing accents and converting to lowercase."""
  nfkd = unicodedata.normalize('NFKD', s)
  return ''.join([c for c in nfkd if not unicodedata.combining(c)]).lower()

# Get exif tags
def get_tags(path):
  """
  Extract XPKeywords tags from image EXIF metadata.
  Returns list of tags split by semicolon, or empty list if none found.
  """
  try:
    with Image.open(path) as img:
      exif_data = img._getexif()
      if not exif_data:
        return []

      for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag == 'XPKeywords':
          if isinstance(value, bytes):
            decoded = value.decode('utf-16le', errors='ignore').strip('\x00')
          else:
            decoded = ''.join(chr(c) for c in value).strip('\x00')
          # Split tags by semicolon and strip whitespace
          return [t.strip() for t in decoded.split(';') if t.strip()]
  except Exception as e:
    print(f"EXIF error in '{path}': {e}")
  return []

# Gather all .jpg files and sort
all_files = list(input_path.rglob('*.jpg'))
sorted_files = sorted(all_files, key=lambda f: normalize_filename(f.name))

for file in sorted_files:
  # Prepare filename without extension
  base_name = file.stem

  # Skip files without the expected ' - '
  if ' - ' not in base_name:
    continue
  
  # Separate date and event name
  date, name = base_name.split(' - ', 1)

  # Find categories matched by filename patterns
  matched_category = []
  date_matched = False

  # Match categories based on patterns in file names
  for category, patterns in categories.items():
    for pattern in patterns:
      if pattern.lower() in name.lower() or pattern.lower() in date.lower():
        # If pattern looks like a date, match category exclusively
        if re.match(r'^\d{4}-\d{2}-\d{2}$', pattern):
          matched_category = [category]
          date_matched = True
          break
        if (category not in matched_category):
          matched_category.append(category)
    if date_matched:
      break

  # Get tags from EXIF and check if any match categories
  tags = get_tags(str(file))
  tag_categories = [tag for tag in tags if tag in cat_keys]
  invalid_tags = [tag for tag in tags if tag not in cat_keys]

  # If tags-based categories exist, override filename-based categories
  if tag_categories:
    matched_category = tag_categories
    
  # Insert year separator comment if year changes
  current_year = date[:4]
  if current_year != previous_year:
    output.write(f"// {current_year}\n")
    print(f"📅 {current_year}")
    previous_year = current_year

  # Determine status icon based on presence and validity of tags
  if invalid_tags:
    status = '🔴'
  elif tags:
    status = '🟢'
  else:
    status = '🟡'

  # Prepare JS object and Python log string
  js_obj = f"{{date: '{date}', catg: {matched_category}, name: '{name}'}},"
  python_log = f"{status} {js_obj}"

  # Write JS object to output file
  output.write(js_obj + '\n')

  # @sup Log
  if not YEAR or date.startswith(f'{YEAR}'):
    print(python_log)


# Write footer
output.write(']')

# Close the output file
output.close()

# Reapply hidden attribute to output file
subprocess.run(['attrib', '+H', outputPath])

print('🏆 Conversion done!')