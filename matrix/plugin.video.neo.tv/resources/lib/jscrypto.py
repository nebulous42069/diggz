import hashlib
import hmac
import base64
from . import pyaes
from .pkcs7 import PKCS7Encoder
import os
import six
from six.moves import urllib_request, urllib_parse, http_cookiejar, range
from operator import xor
from itertools import izip, starmap
from struct import Struct


def evpKDF(passwd, salt, key_size=8, iv_size=4, iterations=1, hash_algorithm="md5"):
    target_key_size = key_size + iv_size
    derived_bytes = six.ensure_binary("")
    number_of_derived_words = 0
    block = None
    hasher = hashlib.new(hash_algorithm)
    while number_of_derived_words < target_key_size:
        if block is not None:
            hasher.update(block)

        hasher.update(passwd)
        hasher.update(salt)
        block = hasher.digest()
        hasher = hashlib.new(hash_algorithm)

        for i in range(1, iterations):
            hasher.update(block)
            block = hasher.digest()
            hasher = hashlib.new(hash_algorithm)

        derived_bytes += block[0: min(len(block), (target_key_size - number_of_derived_words) * 4)]

        number_of_derived_words += len(block) / 4

    return {
        "key": derived_bytes[0: key_size * 4],
        "iv": derived_bytes[key_size * 4:]
    }


def PBKDF2(data, salt, iterations=1000, keylen=24, hashfunc=None):
    """Returns a binary digest for the PBKDF2 hash algorithm of `data`
    with the given `salt`.  It iterates `iterations` time and produces a
    key of `keylen` bytes.  By default SHA-1 is used as hash function,
    a different hashlib `hashfunc` can be provided.
    """
    _pack_int = Struct('>I').pack
    hashfunc = hashfunc or hashlib.sha1
    mac = hmac.new(data, None, hashfunc)

    def _pseudorandom(x, mac=mac):
        h = mac.copy()
        h.update(x)
        return map(ord, h.digest())
    buf = []
    for block in range(1, -(-keylen // mac.digest_size) + 1):
        rv = u = _pseudorandom(salt + _pack_int(block))
        for i in range(iterations - 1):
            u = _pseudorandom(''.join(map(chr, u)))
            rv = starmap(xor, izip(rv, u))
        buf.extend(rv)
    return ''.join(map(chr, buf))[:keylen]


def encode(plaintext, passphrase, saltsize=8):
    salt = os.urandom(saltsize)
    data = evpKDF(six.ensure_binary(passphrase), salt)
    decryptor = pyaes.new(data['key'], pyaes.MODE_CBC, IV=data['iv'])
    plaintext = PKCS7Encoder().encode(plaintext)
    enctext = decryptor.encrypt(plaintext)
    return base64.b64encode("Salted__" + salt + enctext)


# if salt is provided, it should be string
# ciphertext is base64 and passphrase is string
def decode(ciphertext, passphrase, salt=None):
    ciphertext = base64.b64decode(ciphertext)
    if not salt:
        salt = ciphertext[8:16]
        ciphertext = ciphertext[16:]
    data = evpKDF(six.ensure_binary(passphrase), salt)
    decryptor = pyaes.new(data['key'], pyaes.MODE_CBC, IV=data['iv'])
    d = decryptor.decrypt(ciphertext)
    return PKCS7Encoder().decode(d.decode() if six.PY3 else d)


def getUrl(url, cookieJar=None, post=None, timeout=20, headers=None):

    cookie_handler = urllib_request.HTTPCookieProcessor(cookieJar)
    opener = urllib_request.build_opener(cookie_handler, urllib_request.HTTPBasicAuthHandler(), urllib_request.HTTPHandler())
    # opener = urllib2.install_opener(opener)
    req = urllib_request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h, hv in headers:
            req.add_header(h, hv)

    response = opener.open(req, post, timeout=timeout)
    link = response.read()
    response.close()
    return link


def gettvnDecryptedURL(cookiejar=None, globalkey="XXX", passphrase="turbo", videoid="835", ref="http://www.moje-filmy.tk/tv/tvn", pubkeyurl='http://www.moje-filmy.tk/film/cryption/getPublicKey', handshakeurl="http://www.moje-filmy.tk/film/cryption/handshake", getvideourl="http://www.moje-filmy.tk/tv/get"):

    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5
    if cookiejar is None:
        jw = http_cookiejar.LWPCookieJar()
    else:
        jw = cookiejar

    pubkey = getUrl(pubkeyurl, cookieJar=jw, headers=[('Referer', ref)])
    pubkey = eval(pubkey)["publickey"]
    key = encode(globalkey, passphrase)

    key2 = RSA.importKey(pubkey)

    cipher = PKCS1_v1_5.new(key2)
    ciphertext = cipher.encrypt(key)
    getpart = base64.b64encode(ciphertext)

    post = {'key': getpart}
    post = urllib_parse.urlencode(post)
    challenge = getUrl(handshakeurl, post=post, cookieJar=jw, headers=[('Referer', ref)])

    challenge = eval(challenge)["challenge"]
    cc = encode(videoid, key)

    post = {'key': cc}
    post = urllib_parse.urlencode(post)
    url = getUrl(getvideourl, post=post, cookieJar=jw, headers=[('Referer', ref)])

    url = eval(url)["url"]
    finalurl = decode(url, key)
    print(finalurl)
    finalurl = eval(finalurl)["url"]
    finalurl = finalurl.replace('\\/', '/')
    return finalurl
