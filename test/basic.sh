#!/bin/sh

#curl http://0.0.0.0:8080/IceNLPWeb/process -H 'Content-Type: application/json' -d '{"type":"text", "content":"hæ"}'

LOC=/process/service
#LOC=/tag_simple

curl http://0.0.0.0:8080$LOC -H 'Content-Type: application/json' -d '{"type":"text", "content":"Øll menniskju eru fødd fræls og jøvn til virðingar og mannarættindi. Tey hava skil og samvitsku og eiga at fara hvørt um annað í bróðuranda."}'
echo


echo "### Error ###"
TEST='{}'
curl http://0.0.0.0:8080$LOC -H 'Content-Type: application/json' -d $TEST
echo

curl http://0.0.0.0:8080$LOC -H 'Content-Type: application/json' -d ''
echo

curl http://0.0.0.0:8080$LOC -H 'Content-Type: application/json' -d 'lskdjflkj'
echo
