.PHONY: run

run:
	docker-compose up -d

stop:
	docker-compose down -v
