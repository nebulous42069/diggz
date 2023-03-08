# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector for openload.io
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# by DrZ3r0
# ------------------------------------------------------------
# Modified by Shani
import re
from six.moves import urllib_request

headers = [
    ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'],
    ['Accept-Encoding', 'gzip, deflate'],
    ['Connection', 'keep-alive']
]


class AADecoder(object):
    def __init__(self, aa_encoded_data):
        self.encoded_str = aa_encoded_data.replace('/*´∇｀*/', '')

        self.b = ["(c^_^o)", "(ﾟΘﾟ)", "((o^_^o) - (ﾟΘﾟ))", "(o^_^o)",
                  "(ﾟｰﾟ)", "((ﾟｰﾟ) + (ﾟΘﾟ))", "((o^_^o) +(o^_^o))", "((ﾟｰﾟ) + (o^_^o))",
                  "((ﾟｰﾟ) + (ﾟｰﾟ))", "((ﾟｰﾟ) + (ﾟｰﾟ) + (ﾟΘﾟ))", "(ﾟДﾟ) .ﾟωﾟﾉ", "(ﾟДﾟ) .ﾟΘﾟﾉ",
                  "(ﾟДﾟ) ['c']", "(ﾟДﾟ) .ﾟｰﾟﾉ", "(ﾟДﾟ) .ﾟДﾟﾉ", "(ﾟДﾟ) [ﾟΘﾟ]"]

    def is_aaencoded(self):
        idx = self.encoded_str.find("ﾟωﾟﾉ= /｀ｍ´）ﾉ ~┻━┻   //*´∇｀*/ ['_']; o=(ﾟｰﾟ)  =_=3; c=(ﾟΘﾟ) =(ﾟｰﾟ)-(ﾟｰﾟ); ")
        if idx == -1:
            return False

        if self.encoded_str.find("(ﾟДﾟ)[ﾟoﾟ]) (ﾟΘﾟ)) ('_');", idx) == -1:
            return False

        return True

    def base_repr(self, number, base=2, padding=0):
        digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if base > len(digits):
            base = len(digits)

        num = abs(number)
        res = []
        while num:
            res.append(digits[num % base])
            num //= base
        if padding:
            res.append('0' * padding)
        if number < 0:
            res.append('-')
        return ''.join(reversed(res or '0'))

    def decode_char(self, enc_char, radix):
        end_char = "+ "
        str_char = ""
        while enc_char != '':
            found = False
            if not found:
                for i in range(len(self.b)):
                    enc_char = enc_char.replace(self.b[i], str(i))
                startpos = 0
                findClose = True
                balance = 1
                result = []
                if enc_char.startswith('('):
                    l = 0
                    for t in enc_char[1:]:
                        l += 1
                        if findClose and t == ')':
                            balance -= 1
                            if balance == 0:
                                result += [enc_char[startpos:l + 1]]
                                findClose = False
                                continue
                        elif not findClose and t == '(':
                            startpos = l
                            findClose = True
                            balance = 1
                            continue
                        elif t == '(':
                            balance += 1

                if result is None or len(result) == 0:
                    return ""
                else:
                    for r in result:
                        value = self.decode_digit(r, radix)
                        if value == "":
                            return ""
                        else:
                            str_char += value
                    return str_char

            enc_char = enc_char[len(end_char):]

        return str_char

    def parseJSString(self, s):
        try:
            offset = 1 if s[0] == '+' else 0  # noQA
            tmp = (s.replace('!+[]', '1').replace('!![]', '1').replace('[]', '0'))
            val = int(eval(tmp))
            return val
        except:
            pass

    def decode_digit(self, enc_int, radix):
        try:
            return str(eval(enc_int))
        except:
            pass
        rr = r'(\(.+?\)\))\+'  # noQA
        rerr = enc_int.split('))+')
        v = ""
        for c in rerr:
            if len(c) > 0:
                if c.strip().endswith('+'):
                    c = c.strip()[:-1]
                startbrackets = len(c) - len(c.replace('(', ''))
                endbrackets = len(c) - len(c.replace(')', ''))
                if startbrackets > endbrackets:
                    c += ')' * startbrackets - endbrackets
                if '[' in c:
                    v += str(self.parseJSString(c))
                else:
                    v += str(eval(c))
        return v

        mode = 0
        value = 0

        while enc_int != '':
            found = False
            for i in range(len(self.b)):
                if enc_int.find(self.b[i]) == 0:
                    if mode == 0:
                        value += i
                    else:
                        value -= i
                    enc_int = enc_int[len(self.b[i]):]
                    found = True
                    break

            if not found:
                return ""

            enc_int = re.sub(r'^\s+|\s+$', '', enc_int)
            if enc_int.find("+") == 0:
                mode = 0
            else:
                mode = 1

            enc_int = enc_int[1:]
            enc_int = re.sub(r'^\s+|\s+$', '', enc_int)

        return self.base_repr(value, radix)

    def decode(self):
        self.encoded_str = re.sub(r'^\s+|\s+$', '', self.encoded_str)

        # get data
        pattern = (r"\(ﾟДﾟ\)\[ﾟoﾟ\]\+ (.+?)\(ﾟДﾟ\)\[ﾟoﾟ\]\)")
        result = re.search(pattern, self.encoded_str, re.DOTALL)
        if result is None:
            return False

        data = result.group(1)

        # hex decode string
        begin_char = "(ﾟДﾟ)[ﾟεﾟ]+"
        alt_char = "(oﾟｰﾟo)+ "

        out = ''
        while data != '':
            # Check new char
            if data.find(begin_char) != 0:
                return False

            data = data[len(begin_char):]

            # Find encoded char
            enc_char = ""
            if data.find(begin_char) == -1:
                enc_char = data
                data = ""
            else:
                enc_char = data[:data.find(begin_char)]
                data = data[len(enc_char):]

            radix = 8
            # Detect radix 16 for utf8 char
            if enc_char.find(alt_char) == 0:
                enc_char = enc_char[len(alt_char):]
                radix = 16

            str_char = self.decode_char(enc_char, radix)

            if str_char == "":
                return False

            out += chr(int(str_char, radix))

        if out == "":
            return False

        return out


def getUrl(url, cookieJar=None, post=None, timeout=20, headers=None):

    cookie_handler = urllib_request.HTTPCookieProcessor(cookieJar)
    opener = urllib_request.build_opener(cookie_handler, urllib_request.HTTPBasicAuthHandler(), urllib_request.HTTPHandler())
    req = urllib_request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h, hv in headers:
            req.add_header(h, hv)

    response = opener.open(req, post, timeout=timeout)
    link = response.read()
    response.close()
    return link
