.PHONY := check_env infra infra_dev

docker_infra := docker compose -f .docker/docker-compose.infra.yml
docker_infra_dev := $(docker_infra) -f .docker/docker-compose.infra.dev.override.yml 
db_env := db.env
env := .env

check_env:
	@echo "Check docker env files..."
	@test ! -f '.docker/${db_env}' && (echo 'Must copy file ...'; cp -v .docker/${db_env}.dist .docker/${db_env}) || echo 'File .docker/'${db_env} 'exists.'
	@test ! -f './${env}' && (echo 'Must copy file ...'; cp -v ./${env}.dist ./${env}) || echo 'File ./'${env} 'exists.'

infra:
	$(docker_infra) up
infra_dev:
	$(docker_infra_dev) up
