build:
	docker build . -t far_abltagger_api
run:
	docker run -d --name=abltagger -p 8080:8080 far_abltagger_api
stop:
	docker container stop abltagger
	docker container rm abltagger
