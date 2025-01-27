import pyshark

# Mapping of HID keycodes to characters
hid_keycode_map = {
    0x04: "a",
    0x05: "b",
    0x06: "c",
    0x07: "d",
    0x08: "e",
    0x09: "f",
    0x0A: "g",
    0x0B: "h",
    0x0C: "i",
    0x0D: "j",
    0x0E: "k",
    0x0F: "l",
    0x10: "m",
    0x11: "n",
    0x12: "o",
    0x13: "p",
    0x14: "q",
    0x15: "r",
    0x16: "s",
    0x17: "t",
    0x18: "u",
    0x19: "v",
    0x1A: "w",
    0x1B: "x",
    0x1C: "y",
    0x1D: "z",
    0x1E: "1",
    0x1F: "2",
    0x20: "3",
    0x21: "4",
    0x22: "5",
    0x23: "6",
    0x24: "7",
    0x25: "8",
    0x26: "9",
    0x27: "0",
    0x28: "\n",
    0x29: "ESC",
    0x2A: "BACKSPACE",
    0x2B: "TAB",
    0x2C: " ",
    0x2D: "-",
    0x2E: "=",
    0x2F: "[",
    0x30: "]",
    0x31: "\\",
    0x32: "#",
    0x33: ";",
    0x34: "'",
    0x35: "`",
    0x36: ",",
    0x37: ".",
    0x38: "/",
    0x39: "CAPS",
    # Add more mappings as needed
}


def read_btsnoop(file_path):
    """
    Read the btsnoop file and extract packets.
    """
    capture = pyshark.FileCapture(file_path)
    packets = []
    for packet in capture:
        if "btl2cap" in packet:
            packets.append(packet)
    return packetsimport pyshark

# Mapping of HID keycodes to characters
hid_keycode_map = {
    0x04: "a",
    0x05: "b",
    0x06: "c",
    0x07: "d",
    0x08: "e",
    0x09: "f",
    0x0A: "g",
    0x0B: "h",
    0x0C: "i",
    0x0D: "j",
    0x0E: "k",
    0x0F: "l",
    0x10: "m",
    0x11: "n",
    0x12: "o",
    0x13: "p",
    0x14: "q",
    0x15: "r",
    0x16: "s",
    0x17: "t",
    0x18: "u",
    0x19: "v",
    0x1A: "w",
    0x1B: "x",
    0x1C: "y",
    0x1D: "z",
    0x1E: "1",
    0x1F: "2",
    0x20: "3",
    0x21: "4",
    0x22: "5",
    0x23: "6",
    0x24: "7",
    0x25: "8",
    0x26: "9",
    0x27: "0",
    0x28: "\n",
    0x29: "ESC",
    0x2A: "BACKSPACE",
    0x2B: "TAB",
    0x2C: " ",
    0x2D: "-",
    0x2E: "=",
    0x2F: "[",
    0x30: "]",
    0x31: "\\",
    0x32: "#",
    0x33: ";",
    0x34: "'",
    0x35: "`",
    0x36: ",",
    0x37: ".",
    0x38: "/",
    0x39: "CAPS",
    # Add more mappings as needed
}


def read_btsnoop(file_path):
    """
    Read the btsnoop file and extract packets.
    """
    capture = pyshark.FileCapture(file_path)
    packets = []
    for packet in capture:
        if "btl2cap" in packet:
            packets.append(packet)
    return packets


def extract_hid_reports(packets):
    """
    Extract HID reports from the packets.
    """
    hid_reports = []
    for packet in packets:
        if "btl2cap" in packet and packet.captured_length == '17': # packet len is not an int
            payload = packet.btl2cap.payload
            hid_reports.append(payload)
    return hid_reports


def decode_hid_report(report):
    """
    Decode the HID report into modifier and keycodes.
    """
    # Convert the hex string to bytes
    report_bytes = bytes.fromhex(report.replace(":", ""))

    # The first byte is the modifier
    modifier = report_bytes[0]

    # The next 6 bytes are the keycodes
    keys = report_bytes[1:7]

    return modifier, keys


def map_keys(keys):
    """
    Map HID keycodes to characters using the keycode map.
    """
    decoded_keys = []
    for key in keys:
        if key in hid_keycode_map:
            decoded_keys.append(hid_keycode_map[key])
    return decoded_keys


def handle_modifiers(modifier, keys):
    """
    Handle modifier keys (e.g., Shift) to adjust the output.
    """
    shift = modifier & 0x02
    decoded_keys = map_keys(keys)

    # Apply Shift modifier
    if shift:
        decoded_keys = [
            key.upper() if isinstance(key, str) and key.isalpha() else key
            for key in decoded_keys
        ]

    return decoded_keys


def main(file_path):
    """
    Main function to decode keystrokes from a btsnoop file.
    """
    # Step 1: Read the btsnoop file
    packets = read_btsnoop(file_path)

    # Step 2: Extract HID reports
    hid_reports = extract_hid_reports(packets)

    # Step 3: Decode and print keystrokes
    for report in hid_reports:
        modifier, keys = decode_hid_report(report)
        decoded_keys = handle_modifiers(modifier, keys)
        print("".join(decoded_keys), end="")


if __name__ == "__main__":
    # Path to the btsnoop file
    file_path = "mitm.log"

    # Run the script
    main(file_path)



def extract_hid_reports(packets):
    """
    Extract HID reports from the packets.
    """
    hid_reports = []
    for packet in packets:
        if "btl2cap" in packet and packet.captured_length == '17': # packet len is not an int
            payload = packet.btl2cap.payload
            hid_reports.append(payload)
    return hid_reports


def decode_hid_report(report):
    """
    Decode the HID report into modifier and keycodes.
    """
    # Convert the hex string to bytes
    report_bytes = bytes.fromhex(report.replace(":", ""))

    # The first byte is the modifier
    modifier = report_bytes[0]

    # The next 6 bytes are the keycodes
    keys = report_bytes[1:7]

    return modifier, keys


def map_keys(keys):
    """
    Map HID keycodes to characters using the keycode map.
    """
    decoded_keys = []
    for key in keys:
        if key in hid_keycode_map:
            decoded_keys.append(hid_keycode_map[key])
    return decoded_keys


def handle_modifiers(modifier, keys):
    """
    Handle modifier keys (e.g., Shift) to adjust the output.
    """
    shift = modifier & 0x02
    decoded_keys = map_keys(keys)

    # Apply Shift modifier
    if shift:
        decoded_keys = [
            key.upper() if isinstance(key, str) and key.isalpha() else key
            for key in decoded_keys
        ]

    return decoded_keys


def main(file_path):
    """
    Main function to decode keystrokes from a btsnoop file.
    """
    # Step 1: Read the btsnoop file
    packets = read_btsnoop(file_path)

    # Step 2: Extract HID reports
    hid_reports = extract_hid_reports(packets)

    # Step 3: Decode and print keystrokes
    for report in hid_reports:
        modifier, keys = decode_hid_report(report)
        decoded_keys = handle_modifiers(modifier, keys)
        print("".join(decoded_keys), end="")


if __name__ == "__main__":
    # Path to the btsnoop file
    file_path = "mitm.log"

    # Run the script
    main(file_path)
