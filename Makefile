build-api:
	docker build -t chat-monitor/back-api -f Dockerfile-api .

build-app:
	docker build -t chat-monitor/front-app -f Dockerfile-app .

start-app:
	docker-compose up -d

stop-app:
	docker-compose stop

all: build-api build-app start-app