.PHONY: all clean

all: db.sqlite3

db.sqlite3:
	bash get_asnmap.sh
	python makedb.py

clean:
	rm -i thyme_apnic_net_* ip4net2asn.txt asn2name.txt db.sqlite3
