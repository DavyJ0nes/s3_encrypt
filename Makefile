all: run_docker

#### VARIABLES ####
image_name ?= s3_encrypt
user_name ?= davyj0nes
app_name ?= s3_encrypt

script_profile ?= default
script_bucket ?= bucket_name

py_version ?= 3.6.2
app_version ?= 0.0.1

awscli_dir ?= $(HOME)/.aws/
git_hash = $(shell git rev-parse HEAD | cut -c 1-6)
build_date = $(shell date -u '+%Y-%m-%d_%I:%M:%S%p')

.PHONY: build run test

#### COMMANDS ####
build:
	$(call blue, "# Building Python App...")
	docker build --label APP_VERSION=${app_version} --label BUILT_ON=${build_date} --label GIT_HASH=${git_hash} -t ${user_name}/${image_name} .

run:
	$(call blue, "# Running Python App...")
	docker run --rm --name ${image_name} -v "${awscli_dir}":/root/.aws/ -v "$(CURDIR)":/src/app/ -w /src/app ${user_name}/${image_name} python ${app_name}.py --profile ${script_profile} --bucket-name ${script_bucket}

test:
	$(call blue, "# Testing Python App...")
	docker run --rm --name ${image_name} -v "$(CURDIR)":/src/app/ -w /src/app ${user_name}/${image_name} python ${app_name}_test.py

#### FUNCTIONS ####
define blue
	@tput setaf 4
	@echo $1
	@tput sgr0
endef
