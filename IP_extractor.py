import os, sys, re, time
from rich import print
print(sys.executable, os.getcwd())

logfiles = [x for x in os.listdir(os.getcwd()) if x.endswith('.log')]
print(logfiles) 


if __name__  ==  '__main__':
    start = time.time()
    ip_pattern = re.compile(r'''
        \b
        (?:(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])\.){3}
        (?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]?[0-9])
        \b
    ''', re.VERBOSE)

    for log in logfiles:
        with open(log) as file:
            ips = ip_pattern.findall(file.read())
            print(f'Extracted {len(ips)} IPs from the file: {log}')
            ip_counts = {}
            for ip in ips:
                ip_counts[ip] = ip_counts.get(ip, 0) + 1
            sorted_ips = sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)
            
            nicemap, showmax = {}, 16
            for i in range(showmax):
                if len(sorted_ips):
                    try:
                        nicemap[sorted_ips[i][0]] = sorted_ips[i][1]
                    except IndexError as e:
                        pass
            print(f'{showmax} IPs by frequency:\n', nicemap)
    
    end = time.time() - start
    print(f'Done in {end:.2f}s')
