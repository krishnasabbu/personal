import zipfile
import os

# Path to your .mar file
MAR_FILE = "sample.mar"   # Change this to your .mar file


def print_file_content(zip_file, file_name):
    try:
        with zip_file.open(file_name) as f:
            data = f.read()

            # Try decoding as text
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    text = data.decode("latin-1")
                except Exception:
                    print(f"\n[BINARY FILE] {file_name} ({len(data)} bytes)")
                    return

            print("\n" + "=" * 80)
            print(f"FILE: {file_name}")
            print("=" * 80)
            print(text)
            print("=" * 80)

    except Exception as e:
        print(f"Error reading {file_name}: {e}")


def main():
    if not os.path.exists(MAR_FILE):
        print(f"File not found: {MAR_FILE}")
        return

    with zipfile.ZipFile(MAR_FILE, 'r') as mar:

        print("\nFILES INSIDE MAR")
        print("-" * 80)

        for file in mar.namelist():
            print(file)

        print("\n\nDISPLAYING FILE CONTENTS")
        print("-" * 80)

        text_extensions = (
            ".xml",
            ".txt",
            ".json",
            ".properties",
            ".yaml",
            ".yml",
            ".vsm",
            ".vsi",
            ".csv",
            ".wsdl",
            ".xsd"
        )

        for file in mar.namelist():
            if file.endswith("/"):
                continue

            if file.lower().endswith(text_extensions):
                print_file_content(mar, file)
            else:
                info = mar.getinfo(file)
                print(f"\n[BINARY] {file} ({info.file_size} bytes)")


if __name__ == "__main__":
    main()