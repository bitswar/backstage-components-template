# ---------------------------------------------------------------------------- #
FROM alpine:3.18 AS base-python-node

RUN apk update && \
    apk add --no-cache \
    make \
    python3 \
    py3-pip \
    nodejs \
    npm
# ---------------------------------------------------------------------------- #
FROM base-python-node AS scaffold

RUN pip install mkdocs mkdocs-techdocs-core plantuml mkdocs-plantuml && \
    pip cache purge

RUN npm install -g @techdocs/cli && \
    npm cache clean --force
# ---------------------------------------------------------------------------- #
FROM scaffold AS runner

VOLUME /docs
WORKDIR /docs-work

CMD cp -r /docs/* /docs-work && \
    printenv > .env && \
    make generate && \
    make publish
# ---------------------------------------------------------------------------- #