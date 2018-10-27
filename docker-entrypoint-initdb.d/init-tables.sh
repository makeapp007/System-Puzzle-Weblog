#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username dbuser --dbname webserver <<-EOSQL
        CREATE USER dbuser WITH PASSWORD 'secure';
        create database webserver;
        GRANT ALL PRIVILEGES ON DATABASE webserver TO dbuser;

        CREATE TABLE  weblogs (
               day    date,
               status varchar(3)
               );
EOSQL
