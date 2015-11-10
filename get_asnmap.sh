#!/bin/bash

# http://thyme.apnic.net/

tstamp=$(date +%Y%m%d);

# Also current (jp), au, hk, london
curl -L "http://thyme.apnic.net/us/data-raw-table" \
	-o "thyme_apnic_net_us_net2asn_${tstamp}.txt" && \
rm -f ip4net2asn.txt && \
ln -s "thyme_apnic_net_us_net2asn_${tstamp}.txt" ip4net2asn.txt

# Also current (jp), au, hk, london
curl -L "http://thyme.apnic.net/hk/data-used-autnums" \
	-o "thyme_apnic_net_us_asn2name_${tstamp}.txt" && \
rm -f asn2name.txt && \
ln -s "thyme_apnic_net_us_asn2name_${tstamp}.txt" asn2name.txt
