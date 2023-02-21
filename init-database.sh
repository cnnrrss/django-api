#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER django-admin;
	CREATE DATABASE dashboard;
	GRANT ALL PRIVILEGES ON DATABASE dashboard TO django-admin;
EOSQL