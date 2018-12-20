import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # Code of your program here
    print("root already\n")
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)



import subprocess
from time import sleep

result = subprocess.run(['netstat','-bno'],stdout=subprocess.PIPE)

def show_me(result):
	print(result)
	sleep(1)
	print(show_me(result))

if __name__ == "__main__":
	show_me(result)

# print(ctypes.windll.shell32.IsUserAnAdmin())
