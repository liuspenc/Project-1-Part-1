##!/usr/bin/python3

# Run me like this:
# $ python3 len_ext_attack.py "https://project1.eecs388.org/uniqname/lengthextension/api?token=...."

import sys
from urllib.parse import quote
from pymd5 import md5, padding

class ParsedURL:
    def __init__(self, url: str):
        # prefix is the slice of the URL from "https://" to "token=", inclusive.
        self.prefix = url[:url.find('=') + 1]
        self.token = url[url.find('=') + 1:url.find('&')]
        # suffix starts at the first "command=" and goes to the end of the URL
        self.suffix = url[url.find('&') + 1:]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} URL_TO_EXTEND [COMMAND_TO_ADD]", file=sys.stderr)
        sys.exit(-1)

    url = ParsedURL(sys.argv[1])

    # get length of original message
    length = len(url.suffix) + 8
    bits = (length + len(padding(length * 8))) * 8

    # add new command
    h = md5(state=bytes.fromhex(url.token), count=bits)
    x = "&command=UnlockSafes"
    h.update(x)

    # calculate new token and suffix (with padding in the middle)
    token = h.hexdigest()
    suffix = url.suffix + quote(padding(length * 8)) + x

    # new url in format
    modified_url = "https://project1.eecs388.org/liuspenc/lengthextension/api?token=" + token + "&" + suffix
    print(modified_url)
