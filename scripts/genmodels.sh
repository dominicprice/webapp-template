#!/bin/sh

fatal() {
	error "$1"
	exit 1
}

error() {
	printf "\033[0;31mfatal: %s\033[0m\n" "$1"
}

warn() {
	printf "\033[0;33mfatal: %s\033[0m\n" "$1"
}

info() {
	[ -n "$VERBOSE" ] && printf "\033[0;36minfo: %s\033[0m\n" "$1"
}

usage() {
	echo "usage: $0 [-h|--help] [-q|--quiet]"
}

help() {
	usage
	echo "genmodels.sh generates the database models from your"
	echo "database schema"
}

VERBOSE="-v"
while [ -n "$1" ]; do
	case "$1" in
		"-h"|"--help")
			help
			exit 0
			;;
		"-q"|"--quiet")
			VERBOSE=
			;;
		*)
			usage
			exit 1
			;;
	esac
	shift
done

# move into api directory
cd "api" || fatal "failed to cd into api directory"

# create a temporary sqlite database and run migrations on it
TEMP_DB="$(mktemp)"
export DB_URL="sqlite:///$TEMP_DB"
info "running migrations on $TEMP_DB"
poetry run python3 -m api.lib.db.migrations $VERBOSE \
	  || fatal "failed to run migrations"

# generate models
info "generating models"
poetry run sqlacodegen \
	--generator declarative \
	--outfile "src/api/lib/db/sql/models.py" \
	"$DB_URL" \
	|| fatal "failed to generate models"

# delete temporary database
info "cleaning up"
rm "$TEMP_DB"
