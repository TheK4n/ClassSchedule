#!/bin/sh

readonly USER_="$1"; shift
readonly PORT="$1"; shift

chown -R "${USER_}:${USER_}" "/app/data"

exec runuser -u "$USER_" -- gunicorn core.wsgi:application -b "0.0.0.0:${PORT}" -w "$@"