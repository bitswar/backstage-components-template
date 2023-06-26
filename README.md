# Backstage repo-components template (Version 0.0.1)

To install these components into your repo simply run following command:

### Wget:
```bash
wget https://github.com/bitswar/backstage-components-template/releases/download/0.0.1/install.sh && chmod +x install.sh && ./install.sh
```

### Curl:
```bash
curl -L https://github.com/bitswar/backstage-components-template/releases/download/0.0.1/install.sh -o install.sh && chmod +x install.sh && ./install.sh
```

This command will create `cataog` folder in the place where you are locating. To add your components into `Backstage` simply specify link to your `main.yaml` file in the dialog.

## API
### Remove providing:
If you don't need to provide API documentation follow this steps:
1. Remove `api` folder in `catalog/api`
2. Remove `catalog/apis.yaml`
3. Delete line with `apis.yaml` in `main.yaml`:
```yaml
apiVersion: backstage.io/v1aplha1
kind: Location
metadata:
  name:  ${MAIN_NAME}
  description: ${MAIN_DESCRIPTION}
spec:
  targets:
    - ./apis.yaml # Delete this line
    - ./components.yaml
```

After these steps you won't provide APIs documentation into `Backstage`

---
### API configuration steps:
If you need to provide some APIs the best way is to have separated files for `Backstage` components and files with schemas. In the example there are 2 files: `example.yaml` with `Backstage` component and `example.oas.yaml` with schema where `oas` means `Open API Scheme`.

If you need to add new scheme follow these steps:
1. Add file with description of new scheme for example `new-scheme.yaml`
    ```yaml
    apiVersion: backstage.io/v1alpha1
    kind: API
    metadata:
        name: Example API
        description: Example API of scaffolded project
    spec:
        type: openapi
        lifecycle: production
        owner: guest
        system: examples
        definition:
            $text: new-schmeme.oas.yaml
    ```
2. Add scheme with `OpenAPI` in `new-scheme.oas.yaml
3. Add `new-scheme.yaml` to array in `catalog/apis.yaml`
```yaml
apiVersion: backstage.io/v1alpha1
kind: Location
metadata:
  name: ${API_LOCATION_MAME}
  description: ${API_LOCATION_DESCRIPTION}
spec:
  targets:
    - ./api/example.yaml
    - ./api/new-scheme.yaml
```
3. Reload components in `Backstage`
> If you need another scheme check `Backstage` documentation and choose apropriate `type` for the scheme

## Documentation
### Disabling PlantUML
If you're not using `PlantUML` for diagrams you can remove in from this structure:
1. Go to `catalog/mkdocs.yaml`
2. Remove `plantuml-colocator` from array of plugins
3. Remove line `14` and `16` from `makefile`. By removing them you will disable preprocessing `PlantUML` files for generation documantation for publishing
    ```make
    ...
    .PHONY: generate
    generate:
    ifneq ($(origin DEFAULT_SRC_DIR), undefined)
    ifneq ($(origin DEFAULT_OUT_DIR), undefined)
        @echo "DEFAULT"
        @make -- --preprocess # Remove this line
        @npx @techdocs/cli generate --source-dir $(DEFAULT_SRC_DIR) --output-dir $(DEFAULT_OUT_DIR) --no-docker
        @make -- --restore # Remove this line
    else
    ...
    ```

## Publishing documentation to S3 buckets
You should specify .env file in derictory from where you call `Make` functions.Is should be located in `catalog/.env`:
```shell
# S3 settings
S3_ENDPOINT=https://storage.company.com
S3_BUCKET=public
S3_REGION=us-east-1
S3_ACCESS_KEY_ID=your-access-key-id
S3_SECRET_ACCESS_KEY=your-access-key-secret
S3_TYPE=awsS3

# PlantUML generation
DEFAULT_SRC_DIR=.
DEFAULT_OUT_DIR=./site

# Backstage entity description
BACKSTAGE_ENTITY=default/Components/Documentation
```

### PlantUML generation
If you're using `PlantUML` add variables for generation settings:
```shell
# PlantUML generation
PUML_INCLUDE_DIR=docs/utils/
PUML_ROOT_DIR=docs/
```

- `PUML_INCLUDE_DIR` and/or `PUML_INCLUDE_DIR_*` for adding directories with files that should be included to another `.puml` fiels (like stylings or predefined functions)
- `PUML_ROOT_DIR` is root dir where all `.puml` files are located

### Commands

#### Generation documentation
To generate documentation run the command:
```shell
make generate
```
By default it gets documentation from the root folder where you located `$(pwd)` and stores generated documentation to `./site` folder
> Be sure that in you root folder file `mkdocs.yaml` exists

If you wanna customize directories you can add parameters to command:
```shell
make generate src=. out=./site
```
Where `src` is directory from where script will take `.md` files and `out` where documentation will be saved

#### Publishing documentation
To publish doumentation run the command:
```
make publish
```
It will get all environment from `.env` file and try to publish documentation to bucket that you specified