.PHONY := check_env infra prod web

docker := docker compose -f .docker/docker-compose.yml
docker_infra_dev := docker compose -f .docker/docker-compose.infra.yml -f .docker/docker-compose.infra.dev.override.yml 
db_env := db.env
web_env := web.env
compose_env := .env
env := .env

check_env:
	@echo "Check docker env files..."
	@test ! -f '.docker/db/${db_env}' && (echo 'Must copy file ...'; cp -v .docker/db/${db_env}.dist .docker/db/${db_env}) || echo 'File .docker/db/'${db_env} 'exists.'
	@test ! -f '.docker/web/${web_env}' && (echo 'Must copy file ...'; cp -v .docker/web/${web_env}.dist .docker/web/${web_env}) || echo 'File .docker/web/'${web_env} 'exists.'
	@test ! -f '.docker/${compose_env}' && (echo 'Must copy file ...'; cp -v .docker/${compose_env}.dist .docker/${compose_env}) || echo 'File .docker/'${compose_env} 'exists.'
	@test ! -f './${env}' && (echo 'Must copy file ...'; cp -v ./${env}.dist ./${env}) || echo 'File ./'${env} 'exists.'

infra:
	$(docker_infra_dev) up
prod:
	$(docker) up
web:
	$(docker) exec web /bin/fish
