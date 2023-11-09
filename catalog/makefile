include .env
--preprocess:
	@python3 scripts/puml-preprocess.py process

--restore:
	@python3 scripts/puml-preprocess.py restore
	@rm dump.pkl 2> /dev/null || echo

.PHONY: generate
generate:
ifneq ($(origin DEFAULT_SRC_DIR), undefined)
ifneq ($(origin DEFAULT_OUT_DIR), undefined)
	@echo "DEFAULT"
	@make -- --preprocess
	@npx @techdocs/cli generate --source-dir $(DEFAULT_SRC_DIR) --output-dir $(DEFAULT_OUT_DIR) --no-docker || echo - && make -- --restore
	@make -- --restore
else
	@make -- --generate-error
endif
else
	@make -- --generate-error
endif

--generate-error:
	@echo "Command usage: make generate"
	@echo ""
	@echo "You need to specify in .env file arguments"
	@echo "DEFAULT_SRC_DIR = ."
	@echo "DEFAULT_OUT_DIR = ./site"
	@echo "This means that docs will be builded from root folder into ./site"
	@echo ""

publish:
	@export AWS_ACCESS_KEY_ID=$(S3_ACCESS_KEY_ID) && \
	export AWS_SECRET_ACCESS_KEY=$(S3_SECRET_ACCESS_KEY) && \
	export AWS_REGION=$(S3_REGION) && \
	npx @techdocs/cli publish --publisher-type $(S3_TYPE) --storage-name $(S3_BUCKET) --entity $(BACKSTAGE_ENTITY) --awsEndpoint $(S3_ENDPOINT) --awsS3ForcePathStyle true && rm -rf $(DEFAULT_OUT_DIR)