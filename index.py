import re
import subprocess
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

YEAR = 2009

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
        # Read the file in binary mode
        with open(image_path, 'rb') as f:
            data = f.read()

        # Search for the XMP block. It usually starts with "<x:xmpmeta"
        # We are looking for bytes that mark the beginning of the XML block with XMP data
        xmp_start = data.find(b'<x:xmpmeta')
        if xmp_start == -1:
            return tags # XMP block not found

        # Find the end of the XMP block
        xmp_end = data.find(b'</x:xmpmeta>')
        if xmp_end == -1:
            return tags # End of XMP block not found

        # Extract the XML data
        xmp_data = data[xmp_start:xmp_end + len(b'</x:xmpmeta>')]
        
        # Parse the XML data.
        # Defusedxml is safer, but ElementTree works for this use case
        root = ET.fromstring(xmp_data)

        # Traverse all 'description' elements in the XML tree.
        # By default, tags are stored within 'rdf:Description'
        for desc in root.findall('.//rdf:Description', namespaces):
            # Find the 'dc:subject' tags inside 'rdf:Description'
            subject = desc.find('dc:subject', namespaces)
            if subject is not None:
                # Tags are stored inside 'rdf:Bag'
                bag = subject.find('rdf:Bag', namespaces)
                if bag is not None:
                    # Iterate through all 'rdf:li' elements
                    for li in bag.findall('rdf:li', namespaces):
                        # Append the tag (text from the 'rdf:li' element)
                        tags.append(li.text)
    
    except ET.ParseError:
        # Return an empty list in case of a parsing error
        pass
    except Exception:
        # Return an empty list in case of other errors
        pass
        
    return tags


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
        tags = get_xmp_tags(str(file))
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
            if ALL_MODE:
                print(python_log)
            elif not tags or invalid_tags:
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