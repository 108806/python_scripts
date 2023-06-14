import piexif
import os


def clear_exif_data(file_path):
    if file_path.endswith(".png"):
        try:
            print(file_path)
            # Load the EXIF data from the file
            exif_data = piexif.load(file_path)
            print(len(exif_data))

            # Remove the EXIF data from the image
            exif_data.clear()
            print(len(exif_data))

            # Save the image without EXIF data
            piexif.insert(piexif.dump(exif_data), file_path)

            print("EXIF data cleared for:", file_path, "\n")

        except Exception as e:
            print("Error auto clearing EXIF data for:", file_path)
            print(e)

        try:
            start = b"iTXtparameters"
            end = b"\x01\x00\x00IDAT"
            f = bytearray(open(file_path, "rb").read())
            pos1 = f.find(start)
            if 0 >= pos1:
                print("No start point, prolly been cleared already.")
                return 0
            pos2 = f.find(end) - 5
            print("\nDeleting... 1", pos1, "2", pos2, "EXIF:", f[pos1:pos2], "\n")
            for x in range(pos1, pos2):
                f[x] = 0xAA  # Bytes can't be interpreted as an intgers
            with open(file_path, "wb") as buff:
                buff.write(f)
                buff.flush()
                print("Done clearing the exif data from", file_path)
                print("Current exif:", f[: pos2 + 8])
        except Exception as e:
            print("Error manually clearing EXIF data for:", file_path)
            print(e)
            return 1
          

if __name__ == "__main__":
    for f in os.listdir(os.getcwd()):
        if os.path.isfile(os.path.join(os.getcwd(), f)):
            clear_exif_data(f)
