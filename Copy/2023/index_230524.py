import os
from encodings import utf_8

# Path
inputPath = "B:/Prywatne/Lifebook/Życiorys"
outputPath = "B:/Prywatne/Lifebook/Zyciorys.js"

# Categories
cat = {
  "Góry": "g",
  "Kawiarnie": "w",
  "Koncerty": "k",
  "Kościoły": "c",
  "Miasta": "m",
  "Narty": "n",
  "Ogólne": "o",
  "Restauracje": "r",
  "Rodzina": "f",
  "Rowery": "b",
  "Spacery": "s",
  "Spektakle": "p",
  "Znajomi": "z",
}

# Category patterns
category_patterns = {
  "Góry": [],
  "Kawiarnie": ["kawiarnia"],
  "Koncerty": ["koncert"],
  "Kościoły": ["kościół"],
  "Miasta": [
    'Alwernia', 'Andrychów', 'Bełchatów', 'Biała Podlaska', 'Biała Rawska', 'Białystok', 'Biecz', 'Bielsko-Biała', 'Bieruń', 'Bobowa', 'Bochnia', 'Brzesko', 'Brzeszcze', 'Bukowno', 'Busko-Zdrój', 'Bydgoszcz', 'Bytom', 'Będzin', 'Chełm', 'Chełmek', 'Chorzów', 'Chrzanów', 'Chęciny', 'Ciechanów', 'Cieszyn', 'Ciężkowice', 'Czchów', 'Czechowice-Dziedzice', 'Czeladź', 'Częstochowa', 'Darłowo', 'Dobczyce', 'Działoszyce', 'Dąbrowa Górnicza', 'Dąbrowa Tarnowska', 'Dębica', 'Elbląg', 'Ełk', 'Frombork', 'Garwolin', 'Gdańsk', 'Gdynia', 'Giżycko', 'Gliwice', 'Gniezno', 'Gorlice', 'Gorzów Wielkopolski', 'Grudziądz', 'Grybów', 'Grzybowo', 'Głogów', 'Głogówek', 'Hel', 'Inowrocław', 'Jarosław', 'Jastrzębie-Zdrój', 'Jasło', 'Jaworzno', 'Jelenia Góra', 'Jordanów', 'Jędrzejów', 'Kalisz', 'Kalwaria Zebrzydowska', 'Karpacz', 'Katowice', 'Kazimierz Dolny', 'Kazimierza Wielka', 'Kielce', 'Konin', 'Koszalin', 'Koszyce', 'Kołobrzeg', 'Kraków', 'Krosno', 'Krynica Morska', 'Krynica-Zdrój', 'Krzeszowice', 'Książ Wielki', 'Kutno', 'Kędzierzyn-Koźle', 'Kęty', 'Kłodzko', 'Legionowo', 'Legnica', 'Leszno', 'Libiąż', 'Limanowa', 'Lubin', 'Lublin', 'Maków Podhalański', 'Malbork', 'Miechów', 'Mielec', 'Mielno', 'Mikołów', 'Milanówek', 'Międzylesie', 'Międzyzdroje', 'Mszana Dolna', 'Muszyna', 'Myszków', 'Mysłowice', 'Myślenice', 'Mława', 'Nidzica', 'Niepołomice', 'Nowe Brzesko', 'Nowy Korczyn', 'Nowy Targ', 'Nowy Wiśnicz', 'Nysa', 'Ogrodzieniec', 'Ogólne', 'Ogólne', 'Ogólne', 'Ogólne', 'Ogólne', 'Ogólne', 'Ogólne', 'Olkusz', 'Olsztyn', 'Olsztynek', 'Opatowiec', 'Opoczno', 'Opole', 'Orneta', 'Ostrowiec Świętokrzyski', 'Ostrołęka', 'Ostrów Wielkopolski', 'Otmuchów', 'Otwock', 'Oświęcim', 'Pabianice', 'Pacanów', 'Paczków', 'Piaseczno', 'Piekary Śląskie', 'Pilica', 'Pilzno', 'Piotrków Trybunalski', 'Piwniczna-Zdrój', 'Piła', 'Pińczów', 'Poznań', 'Proszowice', 'Prudnik', 'Pruszków', 'Przemyśl', 'Przeworsk', 'Pszczyna', 'Puławy', 'Płock', 'Rabka-Zdrój', 'Racibórz', 'Radom', 'Radomsko', 'Radymno', 'Radłów', 'Ropczyce', 'Ruda Śląska', 'Rumia', 'Rybnik', 'Ryglice', 'Rzeszów', 'Sandomierz', 'Sanok', 'Siedlce', 'Siemianowice Śląskie', 'Sieradz', 'Siewierz', 'Skalbmierz', 'Skarżysko-Kamienna', 'Skawina', 'Skała', 'Skierniewice', 'Sopot', 'Sosnowiec', 'Stalowa Wola', 'Starachowice', 'Stargard', 'Starogard Gdański', 'Stary Sącz', 'Stopnica', 'Sucha Beskidzka', 'Suwałki', 'Sułkowice', 'Szczawnica', 'Szczebrzeszyn', 'Szczecin', 'Szczekociny', 'Szczucin', 'Szczyrk', 'Sędziszów Małopolski', 'Sępólno Krajeńskie', 'Sławków', 'Słomniki', 'Słupsk', 'Tarnobrzeg', 'Tarnowskie Góry', 'Tarnów', 'Tczew', 'Tomaszów Mazowiecki', 'Toruń', 'Trzebinia', 'Tuchów', 'Tychy', 'Tylicz', 'Ustka', 'Ustroń', 'Wadowice', 'Warszawa', 'Wałbrzych', 'Wejherowo', 'Wieliczka', 'Wiślica', 'Wodzisław Śląski', 'Wodzisław', 'Wojnicz', 'Wolbrom', 'Wrocław', 'Włocławek', 'Zabrze', 'Zakliczyn', 'Zakopane', 'Zamość', 'Zator', 'Zawiercie', 'Zduńska Wola', 'Zgierz', 'Zielona Góra', 'Złotoryja', 'Łańcut', 'Łeba', 'Łomża', 'Łódź', 'Świdnica', 'Świnoujście', 'Świątniki Górne', 'Świętochłowice', 'Żabno', 'Żnin', 'Żory', 'Żywiec'
  ],
  "Narty": ["narty"],
  "Ogólne": ["ogólne"],
  "Restauracje": ["restauracja"],
  "Rodzina": ["wigilia", "boże narodzenie", "wielkanoc", "spotkanie u Ani"],
  "Rowery": ["rower", "rowerach"],
  "Spacery": ["spacer"],
  "Spektakle": ["spektakl", "teatr", "opera"],
  "Znajomi": ["znajomi", "spotkanie w biurze", "spotkanie opłatkowe"]
}

# Transformation categories
transformed_cat = {value: key for key, value in cat.items()}
cat_string = str(transformed_cat)

# Open the output file
output = open(outputPath, "w", encoding="utf8")

# Write header
output.write("const cat = \n" + cat_string + "\n\nconst data = [\n")

# Initialize variable to keep track of the previous year
previous_year = "" 

# Traverse the directory structure
for root, dirs, files in os.walk(inputPath):
  # Sort files
  files = sorted(files)
  for file in files:

    # Process only jpg files
    if file.endswith(".jpg"):

      # Prepare file name
      filePath = os.path.join(root, file)
      string = file.replace(".jpg", "")

      # Separate date and event name
      splitted_string = string.split(" - ", 1)
      if len(splitted_string) < 2:
        continue  
      date = splitted_string[0]
      name = splitted_string[1]

      # Prepare category for event
      matched_category = None
      # Match categories based on patterns in file names
      for category, patterns in category_patterns.items():
        for pattern in patterns:
          if pattern.lower() in name.lower():
            matched_category = category

      # Determine the category for the event based on the matched category
      # If no match is found, default to "o" (general) category
      catg = cat.get(matched_category, "o")

      # Prepare years separators
      current_year = date.split("-")[0]
      if current_year != previous_year:
        header = f"// {current_year}"
        output.write(header + "\n")
        previous_year = current_year
        print(header)

      # Generate JavaScript object for the file
      js_obj = f"{{date: '{date}', catg: cat.{catg}, name: '{name}'}},"

      # Write the JavaScript object to the output file
      output.write(js_obj + "\n")
      print(js_obj)

# Write footer
output.write("]")

# Close the output file
output.close()
