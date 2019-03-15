#!/bin/bash

# http://thyme.apnic.net/

# Vantage point.
#
# Options:
# - "current" (jp)
# - "au"
# - "london"
# - "singapore"
# - "hk"
# - "guam"
#
vp="london"

tstamp=$(date +%Y%m%d);

curl -L "http://thyme.apnic.net/${vp}/data-raw-table" \
	-o "thyme_apnic_net_${vp}_net2asn_${tstamp}.txt" && \
ln -f -s "thyme_apnic_net_${vp}_net2asn_${tstamp}.txt" ip4net2asn.txt

curl -L "http://thyme.apnic.net/${vp}/data-used-autnums" \
	-o "thyme_apnic_net_${vp}_asn2name_${tstamp}.txt" && \
ln -f -s "thyme_apnic_net_${vp}_asn2name_${tstamp}.txt" asn2name.txt
