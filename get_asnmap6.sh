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
vpURLName="uk-data"

tstamp=$(date +%Y%m%d);

y=$(date -j -f "%Y%m%d" "${tstamp}" +%Y);
m=$(date -j -f "%Y%m%d" "${tstamp}" +%m);
d=$(date -j -f "%Y%m%d" "${tstamp}" +%d);

# Note: If IPv4 data is used then it must be from the same vantage point
#       as IPv6 for consistency.
if [ ! -e "thyme_apnic_net_${vp}_net2asn_${tstamp}.txt" ]; then
	>&2 echo "NOTICE! IPv6 data is coming from ${vp}." \
			 "IPv4 data, if used, must be from the same vantage point" \
			 "for consistent results."
fi

curl -L "http://thyme.apnic.net/${vpURLName}/${y}/${m}/${d}/0700/dump.ipv6.nobogon.bz2" |
	bzip2 -d > "thyme_apnic_net_${vp}_ipv6bgpdump_${tstamp}.txt" && \
ln -f -s "thyme_apnic_net_${vp}_ipv6bgpdump_${tstamp}.txt" ipv6bgpdump.txt

if [ -e "asn2name.txt" ]; then
	exit 0
fi

curl -L "http://thyme.apnic.net/${vp}/data-used-autnums" \
	-o "thyme_apnic_net_${vp}_asn2name_${tstamp}.txt" && \
ln -f -s "thyme_apnic_net_${vp}_asn2name_${tstamp}.txt" asn2name.txt
