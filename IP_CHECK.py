import os
import sys
import subprocess
import urllib.request
import json
import re
from collections import Counter, defaultdict

print(os.getcwd(), sys.executable)

# Define the regex pattern to match IP addresses
PAT = re.compile(r"((25[0-5]|((2[0-4]|1\d\d|\d|\d\d))\.){3}(25[0-5]|((2[0-4]|1\d\d|\d|\d\d))))", flags=re.MULTILINE)

# List of countries to flag for RED_ALERT
red_alert_countries = {
    'China', 'Russia', 'Iran', 'North Korea', 'Syria', 'Iraq', 'Venezuela',
    'Belarus', 'Sudan', 'Pakistan', 'Libya', 'Yemen', 'Afghanistan',
    'Somalia', 'Myanmar', 'Cuba', 'Lebanon'
}

# Function to download lists
def download_list(url, output_file):
    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')
        with open(output_file, 'w') as file:
            file.write(data)
        print(f"List downloaded and saved to {output_file}")
    except Exception as e:
        print(f"Failed to download list from {url}: {e}")

# Function to fetch malicious IPs from AbuseIPDB
def fetch_abuseipdb_malicious_ips(api_key, output_file):
    url = f"https://api.abuseipdb.com/api/v2/blacklist"
    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read().decode('utf-8')
        with open(output_file, 'w') as file:
            file.write(data)
        print(f"Malicious IPs list downloaded and saved to {output_file}")
    except Exception as e:
        print(f"Failed to fetch malicious IPs from AbuseIPDB: {e}")

# URLs for the Tor exit nodes and malicious IPs
tor_exit_nodes_url = 'https://check.torproject.org/torbulkexitlist'

# Output files
tor_exit_nodes_file = 'tor_exit_nodes.txt'
malicious_ips_file = 'malicious_ips.json'

# Replace with your AbuseIPDB API key
abuseipdb_api_key = '61601453f33eeb60eaf21d9d6572d0a6806e8c94c550561345b4b103973bbdcb4c84fe745400bffe'

# Download the lists
download_list(tor_exit_nodes_url, tor_exit_nodes_file)
fetch_abuseipdb_malicious_ips(abuseipdb_api_key, malicious_ips_file)

# Load the lists into sets
tor_exit_nodes = set()
malicious_ips = set()

with open(tor_exit_nodes_file, mode='r') as file:
    for line in file:
        tor_exit_nodes.add(line.strip())

with open(malicious_ips_file, mode='r') as file:
    data = json.load(file)
    for record in data['data']:
        malicious_ips.add(record['ipAddress'])

if __name__ == '__main__':
    RED_ALERT = {}
    country_counter = Counter()
    isp_counter = Counter()
    ip_details = defaultdict(list)

    # Read the IPs from the file
    with open('ipfile.txt', mode='r') as file:
        ip_file = file.read()

    ips = PAT.findall(ip_file)
    scanned_ips = len(ips)

    for ip in ips:
        ip_str = ip[0]
        print('CHECKING IP', ip_str)

        # Perform nslookup and capture output
        nslookup_output = subprocess.run(['nslookup', ip_str], capture_output=True, text=True)
        nslookup_result = nslookup_output.stdout
        print(nslookup_result)
        
        # Check for indicators in the nslookup output
        if 'exit' in nslookup_result or 'node' in nslookup_result:
            RED_ALERT[ip_str] = 'Found string in hostname (exit node)'

        # Fetch IP location data
        try:
            req = urllib.request.Request(f"http://api.iplocation.net/?cmd=ip-country&ip={ip_str}", headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req).read()
            res = json.loads(res)
            country_name = res.get('country_name')
            country_code2 = res.get('country_code2')
            isp = res.get('isp')

            print(f"\tCountry: {country_name}\n\tCountry Code: {country_code2}\n\tISP: {isp}\n")

            if country_name:
                country_counter[country_name] += 1
            if isp:
                isp_counter[isp] += 1
                ip_details[isp].append(ip_str)

            # Check if the IP is from a red alert country
            if country_name in red_alert_countries:
                RED_ALERT[ip_str] = f'Country: {country_name}'

            # Check if the IP is a known Tor exit node
            if ip_str in tor_exit_nodes:
                RED_ALERT[ip_str] = 'Known Tor exit node'

            # Check if the IP is a known malicious IP
            if ip_str in malicious_ips:
                RED_ALERT[ip_str] = 'Known malicious IP'

        except Exception as e:
            print(f"Error processing IP {ip_str}: {e}")

    # Print summary
    print("\nSUMMARY:")
    print(f"Number of scanned IPs: {scanned_ips}")
    print(f"Number of unique countries: {len(country_counter)}")
    print(f"Number of unique ISPs: {len(isp_counter)}")

    print("\nCountry Counts:")
    for country, count in country_counter.items():
        print(f"{country}: {count}")

    print("\nISP Counts and Details:")
    for isp, count in isp_counter.items():
        print(f"{isp}: {count} times")
        for ip in ip_details[isp]:
            print(f"\tIP: {ip}")

    print(f"Number of RED ALERT IPs: {len(RED_ALERT)}")

    print("\nRED ALERT IPs and Reasons:")
    for ip, reason in RED_ALERT.items():
        print(f"{ip}: {reason}")
