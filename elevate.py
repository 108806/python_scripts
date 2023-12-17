def elevate():
    import ctypes, win32comext.shell.shell, win32event, win32process, os, sys, pyuac, psutil
    outpath = r'%s\%s.out' % (os.environ["TEMP"], os.path.basename(__file__))
    if ctypes.windll.shell32.IsUserAnAdmin():
        if os.path.isfile(outpath):
            sys.stderr = sys.stdout = open(outpath, 'w', 0)
        return
    with open(outpath, 'w+', 0) as outfile:
        h_proc = win32comext.shell.shell.ShellExecuteEx(lpFile=sys.executable,
                                                        lpVerb='runas', lpParameters=' '.join(sys.argv), fMask=64,
                                                        nShow=0)[
            'hProcess']
        while True:
            hr = win32event.WaitForSingleObject(h_proc, 40)
            while True:
                line = outfile.readline()
                if not line:
                    break
                sys.stdout.write(line)
            if hr != 0x102:
                break
    os.remove(outpath)
    sys.stderr = ''
    sys.exit(win32process.GetExitCodeProcess(h_proc))


if __name__ == '__main__':
    elevate()
