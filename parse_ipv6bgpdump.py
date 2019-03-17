#!/usr/bin/python

from __future__ import print_function

import re
import sys

import ip6utils

debug = False

# Initially all lines are ignored. (LINE_BUFFER_STATE_IGNORE)
#
# When the beginning of a line matches the beginning of a route
# a new line_buffer is set. (LINE_BUFFER_STATE_NEW)
# Subsequent lines are buffered. (LINE_BUFFER_STATE_APPEND)
#
# When the state changes back to LINE_BUFFER_STATE_NEW
# or when the input ends then line_buffer is parsed as a route.

LINE_BUFFER_STATE_IGNORE = 0
LINE_BUFFER_STATE_NEW = 1
LINE_BUFFER_STATE_APPEND = 2

# Routes define a network (ROUTE_STATE_NEW) followed by one or more
# paths (ROUTE_STATE_OK), possibly one or more preferred paths.
# (ROUTE_STATE_PREFERRED_OK)

ROUTE_STATE_UNINITIALIZED = 0
ROUTE_STATE_NEW = 1
ROUTE_STATE_PREFERRED_OK = 2
ROUTE_STATE_OK = 3

def line_buffer_state_ignore():
	print("WARNING: Ignoring : %d:%s" % (line_count, line), file=sys.stderr)

# Holds one line or multiple lines concatenated together.
# Used to construct a potential route.
line_buffer = []

route_state = ROUTE_STATE_UNINITIALIZED
# Current network
network = None

cisco_ip6_bgp_route_status_e_txt  = "(?P<status>[s|d|h|\*|>|i|r|S|m|b|f|x|a|c]+) "
cisco_ip6_bgp_route_network_e_txt = "(?P<network>(?:[0-9a-fA-F]{0,16}:){0,7}(?:[0-9a-fA-F]{0,16}){0,1}/[0-9]+ )?"
cisco_ip6_bgp_route_nexthop_e_txt = "(?P<nexthop>(?:[0-9a-fA-F]{0,16}:){0,7}(?:[0-9a-fA-F]{0,16}){0,1}) "
cisco_ip6_bgp_route_metric_e_txt  = "(?P<metric>[0-9]+ )?"
cisco_ip6_bgp_route_locprf_e_txt  = "(?P<locprf>[0-9]+ )?"
cisco_ip6_bgp_route_weight_e_txt  = "(?P<weight>[0-9]+ )?"
cisco_ip6_bgp_route_asnpath_e_txt = "(?P<asnpath>(?P<asn>(?:[0-9]+|{(?:[0-9]+,)*[0-9]+}) )+(?P<origin>[i|e|\?]+))"

cisco_ip6_bgp_route_e = re.compile(
	"^{status}{network}{nexthop}{metric}{locprf}{weight}{asnpath}$".format(
		status=cisco_ip6_bgp_route_status_e_txt,
		network=cisco_ip6_bgp_route_network_e_txt,
		nexthop=cisco_ip6_bgp_route_nexthop_e_txt,
		metric=cisco_ip6_bgp_route_metric_e_txt,
		locprf=cisco_ip6_bgp_route_locprf_e_txt,
		weight=cisco_ip6_bgp_route_weight_e_txt,
		asnpath=cisco_ip6_bgp_route_asnpath_e_txt,
	))

ip6net2asn = {}

def parse_route():
	global route_state
	global network

	candidate_route = "".join(line_buffer)

	candidate_route = re.sub("[ ]+", " ", candidate_route)
	candidate_route = candidate_route.strip(" ")

	# Match against the route expression.
	m = cisco_ip6_bgp_route_e.match(candidate_route)

	if m:
		if (m.group("network")):
			# This route describes a new network.
			if (route_state != ROUTE_STATE_UNINITIALIZED and
				route_state != ROUTE_STATE_PREFERRED_OK and
				route_state != ROUTE_STATE_OK):
				print("WARNING: No Path  : %d:Network %s" % (
					  line_count, network),
					  file=sys.stderr)
			route_state = ROUTE_STATE_NEW
			network = ip6utils.ip6net_expand(m.group("network")[:-1])
			debug and print("NOTICE : Nw Netwrk: %s" % candidate_route)
		else:
			debug and print("NOTICE : Nw Path  : %s" % candidate_route)

		if (m.group("asn")):
			asn = m.group("asn")[:-1]
			# This route describes an ASN path.
			if (route_state != ROUTE_STATE_NEW and
				route_state != ROUTE_STATE_PREFERRED_OK and
				route_state != ROUTE_STATE_OK):
				print("WARNING: No Netwrk: %d:ASN %s" % (line_count, asn),
					  file=sys.stderr)
			else:
				preferred = False
				if (m.group("status") and
					re.search(">", m.group("status"))):
					route_state = ROUTE_STATE_PREFERRED_OK
					not_preferred = ""
					preferred = True
				else:
					route_state = ROUTE_STATE_OK

				if asn[0] == '{':
					asn = asn.strip("{}")
					asn = asn.split(",")
				else:
					asn = [ asn ]

				for a in asn:
					debug and \
					print("NOTICE : Nw ASN   : %s (Netwrk: %s, Pref: %s)" % (
						  a, network, preferred))

					if network not in ip6net2asn:
						ip6net2asn[network] = []
					ip6net2asn[network].append(
						{"asn": a, "preferred": preferred})
	else:
		print("WARNING: Bad Syntx: %d:%s" % (line_count, candidate_route),
			  file=sys.stderr)


def line_buffer_state_new():
	global line_buffer
	global line_buffer_state

	if len(line_buffer) > 0:
		parse_route()

	line_buffer = [ line ]
	line_buffer_state = LINE_BUFFER_STATE_APPEND

	debug and print("NOTICE : New lnbuf: %d:%s" % (
					line_count, "".join(line_buffer)))


def line_buffer_state_append():
	global line_buffer

	line_buffer.append(line)

	debug and print("NOTICE : Ext lnbuf: %d:%s" % (
					line_count, "".join(line_buffer)))


cisco_ip6_bgp_route_status_e = \
	re.compile("^[ ]*%s" % cisco_ip6_bgp_route_status_e_txt)

line_buffer_state = LINE_BUFFER_STATE_IGNORE

line_buffer_state_action = \
{
	LINE_BUFFER_STATE_IGNORE: line_buffer_state_ignore,
	LINE_BUFFER_STATE_NEW:	line_buffer_state_new,
	LINE_BUFFER_STATE_APPEND: line_buffer_state_append,
};

line_count = 0

f = open("ipv6bgpdump.txt", "r")

for line in f:
	line = line.rstrip("\r\n")

	if cisco_ip6_bgp_route_status_e.match(line):
		line_buffer_state = LINE_BUFFER_STATE_NEW

	line_buffer_state_action[line_buffer_state]()

	line_count += 1

if len(line_buffer) > 0:
	parse_route()

for n in ip6net2asn:
	for a in ip6net2asn[n]:
		if a["preferred"] == False:
			continue
		print("%s\t%s" % (n, a["asn"]))

f.close()
