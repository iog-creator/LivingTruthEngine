FROM node:18-alpine
RUN apk add --no-cache git bash ca-certificates && update-ca-certificates
WORKDIR /srv/app
COPY entrypoint.git-clone-or-pull.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
# The service's original command remains defined in compose
