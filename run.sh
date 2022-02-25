docker container stop abltagger
docker container rm abltagger
docker build . -t glaciersg/far_abltagger_api:v1.0
docker run -d --name=abltagger -p 8080:8080 glaciersg/far_abltagger_api:v1.0
