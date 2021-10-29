docker container stop abl_tagger
docker container rm abl_tagger
docker build . -t abl_tagger:example
docker run -d --name=abl_tagger -p 8080:8080 abl_tagger:example
