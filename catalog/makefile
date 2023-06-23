include .env
--preprocess:
	@python scripts/puml-preprocess.py

.PHONY: generate
generate: --preprocess
ifneq ($(origin src), undefined)
ifneq ($(origin out), undefined)
	@npx @techdocs/cli generate --source-dir $(src) --output-dir $(out) --no-docker
else
	@npx @techdocs/cli generate --source-dir $(src) --output-dir $(DEFAULT_OUT_DIR) --no-docker
endif
else
ifeq ($(origin default), true)
	@npx @techdocs/cli generate --source-dir $(DEFAULT_SRC_DIR) --output-dir $(DEFAULT_OUT_DIR) --no-docker
else
	@echo "Command usage: make generate [out=path-to-output-dir] [src=path-to-src-dir] [default=true]"
	@echo ""
	@echo "You can specify default=true value to skip \"out\" and \"src\" args"
	@echo "DEFAULT_SRC_DIR = ."
	@echo "DEFAULT_OUT_DIR = ./site"
	@echo "This means that docs will be builded from root folder into ./site"
	@echo ""
	@echo "In another way you should specify both arguments"
endif
endif

publish:
	@export AWS_ACCESS_KEY_ID=$(S3_ACCESS_KEY_ID) && \
	export AWS_SECRET_ACCESS_KEY=$(S3_SECRET_ACCESS_KEY) && \
	export AWS_REGION=$(S3_REGION) && \
	npx @techdocs/cli publish --publisher-type $(S3_TYPE) --storage-name $(S3_BUCKET) --entity $(BACKSTAGE_ENTITY) --awsEndpoint $(S3_ENDPOINT) --awsS3ForcePathStyle true && rm -rf $(DEFAULT_OUT_DIR)