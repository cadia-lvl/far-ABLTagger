# -*- coding: utf-8 -*-
import requests
import json 

def run(input_text):
    print("INPUT:",input_text)
    return requests.post("http://localhost:8080/tag_simple/impl", params={'input_text':input_text})

text='Øll menniskju eru fødd fræls og jøvn til virðingar og mannarættindi. Tey hava skil og samvitsku og eiga at fara hvørt um annað í bróðuranda.',

r = run(text)
print(r.text)
#print("OUTPUT: "+r.text.encode('utf-8').decode('unicode-escape'))
#json.loads(r.text)
