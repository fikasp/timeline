import re
import subprocess
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
from multiprocessing import Pool, cpu_count

#------------------------
# @g CONFIG
#------------------------
YEAR = 2025

# ALL_MODE = False
ALL_MODE = True

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

#------------------------
# @g FUNCTIONS
#------------------------
def normalize_filename(s):
    """Normalize filename by removing accents and converting to lowercase."""
    nfkd = unicodedata.normalize('NFKD', s)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)]).lower()


def get_xmp_tags(image_path: str) -> list[str]:
    """
    Retrieves tags from the XMP section of a JPG image.
    Returns a list of tags or an empty list if no XMP tags are found.
    """
    tags = []
    namespaces = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "dc": "http://purl.org/dc/elements/1.1/"
    }
    try:
        with open(image_path, 'rb') as f:
            data = f.read()

        xmp_start = data.find(b'<x:xmpmeta')
        if xmp_start == -1:
            return tags

        xmp_end = data.find(b'</x:xmpmeta>')
        if xmp_end == -1:
            return tags

        xmp_data = data[xmp_start:xmp_end + len(b'</x:xmpmeta>')]

        root = ET.fromstring(xmp_data)

        for desc in root.findall('.//rdf:Description', namespaces):
            subject = desc.find('dc:subject', namespaces)
            if subject is not None:
                bag = subject.find('rdf:Bag', namespaces)
                if bag is not None:
                    for li in bag.findall('rdf:li', namespaces):
                        tags.append(li.text)

    except ET.ParseError:
        pass
    except Exception:
        pass

    return tags


#------------------------
# @b Worker for multiprocessing
#------------------------
def process_file(file_path):
    """
    Worker for processing a single JPG file.
    Returns tuple: (year, log_str, js_obj_str) or None if file skipped.
    """
    try:
        base_name = file_path.stem

        if ' - ' not in base_name:
            return None  # skip files without expected pattern

        date, name = base_name.split(' - ', 1)

        # Match categories based on patterns in file names
        matched_category = []
        date_matched = False
        for category, patterns in categories.items():
            for pattern in patterns:
                if pattern.lower() in name.lower() or pattern.lower() in date.lower():
                    if re.match(r'^\d{4}-\d{2}-\d{2}$', pattern):
                        matched_category = [category]
                        date_matched = True
                        break
                    if category not in matched_category:
                        matched_category.append(category)
            if date_matched:
                break

        # Get tags from EXIF/XMP
        tags = get_xmp_tags(str(file_path))
        cat_keys = list(categories.keys())
        tag_categories = [tag for tag in tags if tag in cat_keys]
        invalid_tags = [tag for tag in tags if tag not in cat_keys]

        # Override filename categories if tags exist
        if tag_categories:
            matched_category = tag_categories

        # Skip files without any matched category
        if not matched_category:
            return None

        # Status icon
        if invalid_tags:
            status = '🔴'
        elif tags:
            status = '🟢'
        else:
            status = '🟡'

        js_obj = f"{{date: '{date}', catg: {matched_category}, name: '{name}'}},"        
        python_log = f"{status} {js_obj}"

        return (date[:4], python_log, js_obj)

    except Exception:
        return None  # skip problematic file


#------------------------
# @g MAIN
#------------------------
def main():
    print("📷 JPG to JS converter:")

    input_path = Path(__file__).parent.resolve()
    output_path = input_path / 'index.js'

    # Remove hidden attribute from output file if exists
    subprocess.run(['attrib', '-H', output_path], shell=True)

    # Gather and sort all JPG files
    all_files = list(input_path.rglob('*.jpg'))
    sorted_files = sorted(all_files, key=lambda f: normalize_filename(f.name))

    # Multiprocessing
    all_entries = []
    previous_year = ''
    cat_keys = list(categories.keys())

    with Pool(cpu_count()) as pool:
        results = pool.map(process_file, sorted_files)

    for result in results:
        if not result:
            continue
        current_year, log_str, js_obj = result

        # Year separator
        if current_year != previous_year:
            all_entries.append(f"// {current_year}")
            print(f"📅 {current_year}")
            previous_year = current_year

        # Print only entries for current YEAR if YEAR is set
        if not YEAR or current_year == str(YEAR):
            if ALL_MODE:
                print(log_str)

        all_entries.append(js_obj)


    # Write output
    with open(output_path, 'w', encoding='utf8') as output:
        output.write(f"const cat = {cat_keys}\n\nconst data = [\n")
        output.write('\n'.join(all_entries))
        output.write('\n]')

    # Reapply hidden attribute
    subprocess.run(['attrib', '+H', output_path], shell=True)

    print('🏆 Conversion done!')


if __name__ == "__main__":
    main()
