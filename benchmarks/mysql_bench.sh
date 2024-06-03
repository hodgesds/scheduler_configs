#!/usr/bin/env bash

setup_db() {
	sysbench \
		--db-driver=mysql \
		--mysql-user=sbtest_user \
		--mysql_password=password \
		--mysql-db=sbtest \
		--mysql-host=localhost \
		--mysql-port=3306 \
		--tables=16 \
		--table-size=10000 \
		./oltp_read_write.lua \
		prepare
}


do_bench() {
	sysbench \
		--db-driver=mysql \
		--mysql-user=sbtest_user \
		--mysql_password=password \
		--mysql-db=sbtest \
		--mysql-host=localhost \
		--mysql-port=3306 \
		--threads=8 \
		./oltp_read_write.lua \
		run
}

for i in $(seq 1 $1); do
	do_bench
	sleep 2
done
