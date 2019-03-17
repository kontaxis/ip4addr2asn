.PHONY: all clean

all: db.sqlite3 db6.sqlite3

db.sqlite3:
	bash get_asnmap.sh
	python makedb.py

db6.sqlite3:
	bash get_asnmap6.sh
	python parse_ipv6bgpdump.py > ip6net2asn.txt
	python makedb6.py

clean:
	rm -i thyme_apnic_net_* ip4net2asn.txt asn2name.txt db.sqlite3 \
		  ipv6bgpdump.txt ip6net2asn.txt db6.sqlite3
