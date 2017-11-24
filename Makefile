all: run_docker

#### VARIABLES ####
image_name ?= s3_encrypt
py_version ?= 3.6.2
app_version ?= 0.0.1
git_hash = $(shell git rev-parse HEAD | cut -c 1-6)
build_date = $(shell date -u '+%Y-%m-%d_%I:%M:%S%p')

.PHONY: build run test

#### COMMANDS ####
build:
	$(call blue, "# Building Python App...")
	docker build --label APP_VERSION=${app_version} --label BUILT_ON=${build_date} --label GIT_HASH=${git_hash} -t ${image_name} .

run:
	$(call blue, "# Running Python App...")
	docker run --rm --name ${image_name} python:${py_version}-alpine3.6

test:
	$(call blue, "# Testing Python App...")
	docker run --rm --name ${image_name}_test python:${py_version}-alpine3.6

#### FUNCTIONS ####
define blue
	@tput setaf 4
	@echo $1
	@tput sgr0
endef
