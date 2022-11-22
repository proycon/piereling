docker:
	docker build -t proycon/piereling:latest .

docker-dev:
	docker build -t proycon/piereling:dev --build-arg VERSION=development .
