import os
import base64
import requests
import http.server
import socketserver
import hashlib
from urllib.parse import urlparse, parse_qs
from cryptography.fernet import Fernet

# Key for encryption (you should save this key to decrypt the files later)
key = b"hgAtgqgANA5qYEFr5FgB_wG5WFN-a2s6K07bo5_fMfQ="
cipher_suite = Fernet(key)
print("Running with a key:", key.decode())

PORT = 8000


class ProxyDownloaderHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Extract the encrypted file URL from the query parameter
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        encrypted_file_url = query_params.get("url", [None])[0]

        if not encrypted_file_url:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Bad Request: Missing URL parameter")
            return

        try:
            # Decrypt the file urlparse                 #STAGE 0
            encrypted_file_url_bytes = encrypted_file_url.encode("utf-8")
            file_url = cipher_suite.decrypt(encrypted_file_url_bytes).decode("utf-8")

            # Download the file                         #STAGE 1
            response = requests.get(file_url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            file_data = response.content
            s1_hash = hashlib.sha256(file_data).hexdigest()
            print("original hash:", s1_hash)
            print("original 32:", file_data[:32].hex())

            # Encrypt the file                          #STAGE 2
            encrypted_data = cipher_suite.encrypt(file_data)
            print("\ns1 32:", encrypted_data[:32].hex())
            s2_hash = hashlib.sha256(encrypted_data).hexdigest()
            print("\ns1 hash:", s2_hash, end="\n\n")
            # Create a new file name with the desired extension
            new_file_name = "encrypted_file.mp4"

            # Add proper magic bytes for an MP4 file    #STAGE 3
            # MP4 files start with 0x00000018ftyp
            original_magic = encrypted_data[:8]
            magic_bytes = b"\x00\x00\x00\x18ftyp"
            final_data = magic_bytes + encrypted_data[len(magic_bytes) :]
            print("\ns2 32:", final_data[:32].hex())
            s3_hash = hashlib.sha256(final_data).hexdigest()
            print("\ns2 hash:", s2_hash, end="\n\n")

            # Serve the file
            self.send_response(200)
            self.send_header("Content-type", "video/mp4")
            self.send_header(
                "Content-Disposition", f'attachment; filename="{new_file_name}"'
            )
            self.send_header("hash1", s1_hash)
            self.send_header("hash2", s2_hash)
            self.send_header("hash3", s3_hash)
            self.send_header("magic", original_magic.hex())
            self.end_headers()
            self.wfile.write(final_data)

        except requests.RequestException as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Failed to download the file: {str(e)}".encode())


# Create the HTTP server
with socketserver.TCPServer(("", PORT), ProxyDownloaderHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
