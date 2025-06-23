import os
import re
import win32com.client
# pip install pywin32

YEAR = 2013

BASE_PATH = r"B:\Prywatne\Lifebook"

def rename_raster_images(dwg_path):
	try:
		print("🔄 AutoCAD starting...")
		acad = win32com.client.Dispatch("AutoCAD.Application.17")
		acad.Visible = True

		print(f"📂 Opening file: {dwg_path}...\n")
		doc = acad.Documents.Open(dwg_path)
		ms = doc.ModelSpace

		# Pattern to extract date and rest of the filename
		pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})(.*)", re.IGNORECASE)

		for obj in ms:
			if obj.ObjectName == "AcDbRasterImage":
				old_path = obj.ImageFile

				# Convert relative path to absolute
				if old_path.startswith(".\\") or old_path.startswith("./"):
					relative_part = old_path[2:]
					abs_path = os.path.join(BASE_PATH, relative_part)
				else:
					abs_path = old_path

				dirname = os.path.dirname(abs_path)
				filename = os.path.basename(abs_path)

				m = pattern.match(filename)
				if m and int(m.group(1)) == YEAR:
					date_part = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
					rest = m.group(4).strip()

					# Check if original file exists
					old_exists = os.path.isfile(abs_path)
					print(f"{'✔️ ' if old_exists else '❌'} {abs_path}")

					if old_exists:
						print("🟢 Original file exists, no update needed.\n")
						continue

					# Separate filename from extension
					ext_match = re.match(r"(.*)(\.[^.]+)$", rest)
					if not ext_match:
						print("⚠️ Could not extract file extension, skipping.\n")
						continue

					name_without_ext = ext_match.group(1).strip()
					ext = ext_match.group(2)

					# Clean up: remove leading dash/underscore/spaces
					cleaned_name = re.sub(r"^[\s\-_]+", "", name_without_ext)

					new_filename = None

					# Case 1: number at the beginning
					leading_number_match = re.match(r"^(\d+)\s+(.*)", cleaned_name)
					if leading_number_match:
						number = leading_number_match.group(1)
						title = leading_number_match.group(2)
						new_filename = f"{date_part}.{number} - {title}{ext}"

					# Case 2: number at the end
					elif re.match(r".*\s\d+$", cleaned_name):
						trailing_number_match = re.match(r"(.*)\s(\d+)$", cleaned_name)
						title = trailing_number_match.group(1)
						number = trailing_number_match.group(2)
						new_filename = f"{date_part}.{number} - {title}{ext}"

					# Case 3: no number
					else:
						number = "0"
						title = cleaned_name
						new_filename = f"{date_part}.{number} - {title}{ext}"

					new_path = os.path.join(dirname, new_filename)

					new_exists = os.path.isfile(new_path)
					print(f"{'✔️ ' if new_exists else '❌'} {new_path}")
					if new_exists:
						obj.ImageFile = new_path
						obj.Update()
						print("🔵 Updated path in DWG.\n")
					else:
						print("🔴 New file not found, skipping update.\n")

		doc.Save()
		doc.Close()
		print("🏆 Done.")

	except Exception as e:
		print("❌ Error:", str(e))


if __name__ == "__main__":
	rename_raster_images(os.path.join(BASE_PATH, "Timeline.dwg"))