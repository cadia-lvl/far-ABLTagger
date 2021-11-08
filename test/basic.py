# -*- coding: utf-8 -*-
import requests
import json 

def run(input_text):
    print("INPUT:",input_text)
    return requests.post("http://localhost:8080/tag_simple/impl", params={'input_text':input_text})

text='Øll menniskju eru fødd fræls og jøvn til virðingar og mannarættindi. Tey hava skil og samvitsku og eiga at fara hvørt um annað í bróðuranda.',



r = run(text)
exp = '{"response":{"type":"texts","content":[["Øll","PBNPN"],["menniskju","SNPN"],["eru","VNPP"],["fødd","VANPN"],["fræls","SNSA"],["og","C"],["jøvn","SFSN"],["til","DG"],["virðingar","SFPA"],["og","C"],["mannarættindi","SNPAA"],[".","KE"],["Tey","PPNPN"],["hava","VNPP"],["skil","SNSA"],["og","C"],["samvitsku","SFSA"],["og","C"],["eiga","VNPP"],["at","CI"],["fara","VI"],["hvørt","PBNSA"],["um","DG"],["annað","PBNSA"],["í","DG"],["bróðuranda","SFSDA"],[".","KE"]]}}'
print("|"+r.text+"|")
json.loads(r.text)
print(exp)
print(exp==r.text)
assert r.text == exp
#print("OUTPUT: "+r.text.encode('utf-8').decode('unicode-escape'))
