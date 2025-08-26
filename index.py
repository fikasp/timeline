import re
import subprocess
import unicodedata
from pathlib import Path
from PIL.ExifTags import TAGS
from PIL import Image

YEAR = 2018

categories = {
    'Atrakcje': ['Muzeum', 'Wystawa'],
    'Gastronomia': ['Kawiarnia', 'Restauracja'],
    'Góry': [],
    'Domówki': [],
    'Koncerty': ['Koncert'],
    'Kościoły': ['Kościół'],
    'Miasta': [],
    'Narty': ['Narty'],
    'Ogólne': ['Ogólne'],
    'Rodzina': ['Rodzina'],
    'Rowery': ['Rower'],
    'Spacery': ['Spacer'],
    'Spektakle': ['Kino', 'Opera', 'Spektakl', 'Teatr'],
    'Uroczystości': ['Chrzciny', 'Komunia', 'Pogrzeb', 'Ślub', 'Wesele'],
    'Wyjazdy': ['Wczasy', 'Wyjazd'],
    'Znajomi': ['Znajomi'],
}


def normalize_filename(s):
    """Normalize filename by removing accents and converting to lowercase."""
    nfkd = unicodedata.normalize('NFKD', s)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)]).lower()


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


def main():
    print("📷 JPG to JS converter:")

    # Category keys
    cat_keys = list(categories.keys())

    # Set input and output paths
    input_path = Path(__file__).parent.resolve()
    output_path = input_path / 'index.js'

    # Remove hidden attribute from output file if it exists
    subprocess.run(['attrib', '-H', output_path])

    # Open output file for writing with UTF-8 encoding
    output = open(output_path, 'w', encoding='utf8')

    # Write initial JS header: category keys and start of data array
    output.write(f"const cat = {cat_keys}\n\nconst data = [\n")

    # Keep track of last processed year to insert year separators
    previous_year = '' 

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
    subprocess.run(['attrib', '+H', output_path])

    print('🏆 Conversion done!')


if __name__ == "__main__":
    main()