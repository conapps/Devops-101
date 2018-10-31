up:
	docker-compose up -d --build

down:
	docker-compose down

attach:
	docker exec -it master bash

rm:
	docker rm `docker ps -a -q`

.PHONY: up down attach rm
