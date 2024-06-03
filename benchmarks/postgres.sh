#!/usr/bin/env bash

setup_db() {
	sysbench \
		--db-driver=pgsql \
		--tables=16 \
		--table-size=10000 \
		--pgsql-host=127.0.0.1 \
		--pgsql-port=5432  \
		--pgsql-user=sbtest  \
		--pgsql-password=password  \
		--pgsql-db=sbtest  \
		./oltp_read_write.lua \
		prepare
}

if [ -n "$2" ]; then
	setup_db
fi

do_bench() {
	sysbench \
		--db-driver=pgsql \
		--table-size=10000 \
		--pgsql-host=127.0.0.1 \
		--pgsql-port=5432  \
		--pgsql-user=sbtest  \
		--pgsql-password=password  \
		--pgsql-db=sbtest  \
		--threads=8 \
		./oltp_read_write.lua \
		run
}

for i in $(seq 1 $1); do
	do_bench
	sleep 2
done
