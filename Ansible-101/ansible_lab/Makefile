up:
	docker-compose -f ./docker/docker-compose.yml up -d --build

down:
	docker-compose -f ./docker/docker-compose.yml down

status:
	docker-compose -f ./docker/docker-compose.yml ps

attach:
	docker exec -it controller bash

rm:
	docker rm `docker ps -a -q`

.PHONY: up down attach rm
