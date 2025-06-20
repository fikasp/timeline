import os
import re
import win32com.client
# pip install pywin32

YEAR = 2019

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

					# Check for trailing number at the end of the rest
					number_match = re.search(r"(.*?)(?:\s(\d+))?(\.[^.]+)$", rest)
					if number_match:
						rest_base = number_match.group(1)
						number = number_match.group(2) if number_match.group(2) else "0"
						ext = number_match.group(3)
						new_filename = f"{date_part}.{number} {rest_base}{ext}"
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