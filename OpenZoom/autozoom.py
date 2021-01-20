#!/usr/local/bin/python3.8
import os
import sys

print(str(sys.argv))

if (len(sys.argv) != 2):
    raise ValueError(f'Script accepts one argument (the zoom url), not {len(sys.argv)}')

arg = sys.argv[1]
print(arg)

def parse_uri(url):
    try:
        out = "zoommtg://"
        domain = url[url.index("https://") + 8:url.index("/j")]
        confno = url[url.index("j/") + 2:url.index("?pwd=")]
        try:
            pwd = url[url.index("pwd=") + 4:url.index("#", url.index("pwd=") + 4)]
        except ValueError:
            pwd = url[url.index("pwd=") + 4:]
    except Exception:
        raise ValueError(f'Invalid zoom url')

    return out + domain + "/join?action=join&confno=" + confno + "&pwd=" + pwd + "&zc=0&browser=firefox"

command = "open '" + parse_uri(arg) + "'"

os.system(command)