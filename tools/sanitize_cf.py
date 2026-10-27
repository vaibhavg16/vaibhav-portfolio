#!/usr/bin/env python3
"""Repair Cloudflare artifacts that get injected into index.html.

Cloudflare rewrites any HTML containing a plain email address: it obfuscates the
address, adds email-decode.min.js and a challenge script. These break the site off
Cloudflare (absolute /cdn-cgi paths 404) and show visitors "[email protected]".

This script reverses all of it, decoding the address out of Cloudflare's own
data-cfemail attribute. Run it before validating or deploying.
"""
import re
import sys

TARGET = sys.argv[1] if len(sys.argv) > 1 else 'index.html'

with open(TARGET, encoding='utf-8') as fh:
    src = fh.read()
original_len = len(src.encode())


def decode_cfemail(hexstr):
    """Cloudflare's obfuscation: first byte is an XOR key for the rest."""
    key = int(hexstr[:2], 16)
    return ''.join(chr(int(hexstr[i:i + 2], 16) ^ key)
                   for i in range(2, len(hexstr), 2))


repaired = {'anchors': 0, 'decode_script': 0, 'challenge_script': 0}


def anchor(m):
    addr = decode_cfemail(m.group('payload'))
    repaired['anchors'] += 1
    return '<a href="mailto:%s">%s</a>' % (addr, addr)


src = re.sub(
    r'<a href="/cdn-cgi/l/email-protection#(?P<payload>[0-9a-fA-F]+)">'
    r'\s*<span class="__cf_email__"[^>]*>.*?</span>\s*</a>',
    anchor, src, flags=re.S)

before = src
src = re.sub(
    r'<script[^>]*src="/cdn-cgi/scripts/[^"]*email-decode\.min\.js"[^>]*>\s*</script>',
    '', src)
if src != before:
    repaired['decode_script'] += 1

before = src
src = re.sub(r'<script>\(function\(\)\{function c\(\).*?\}\)\(\);</script>',
             '', src, flags=re.S)
if src != before:
    repaired['challenge_script'] += 1

# safety net: anything else pointing at /cdn-cgi is dead weight
src = re.sub(r'<script[^>]*src="/cdn-cgi/[^"]*"[^>]*>\s*</script>', '', src)

if re.search(r'cdn-cgi/l/email-protection|__cf_email__|__CF\$cv\$params', src):
    print('WARNING: some Cloudflare artifacts could not be repaired', file=sys.stderr)

with open(TARGET, 'w', encoding='utf-8') as fh:
    fh.write(src)

print('sanitized %s: %d email anchor(s), %d decode script(s), %d challenge script(s); '
      '%d -> %d bytes'
      % (TARGET, repaired['anchors'], repaired['decode_script'],
         repaired['challenge_script'], original_len, len(src.encode())))
