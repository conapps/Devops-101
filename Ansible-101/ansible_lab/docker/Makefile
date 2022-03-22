up:
	docker-compose up -d --build

down:
	docker-compose down

attach:
	docker exec -it controller bash

rm:
	docker rm `docker ps -a -q`

.PHONY: up down attach rm
