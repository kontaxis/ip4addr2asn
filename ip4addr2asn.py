#!/usr/bin/python -u

# kontaxis 2015-10-23

from __future__ import print_function

import os
import sys
import sqlite3

# Prepare ip4masks
ip4mask = [
	0x00000000,
	((~0x0) << 31) & 0xffffffff, # /1
	((~0x0) << 30) & 0xffffffff, # /2
	((~0x0) << 29) & 0xffffffff, # /3
	((~0x0) << 28) & 0xffffffff, # /4
	((~0x0) << 27) & 0xffffffff, # /5
	((~0x0) << 26) & 0xffffffff, # /6
	((~0x0) << 25) & 0xffffffff, # /7
	((~0x0) << 24) & 0xffffffff, # /8
	((~0x0) << 23) & 0xffffffff, # /9
	((~0x0) << 22) & 0xffffffff, # /10
	((~0x0) << 21) & 0xffffffff, # /11
	((~0x0) << 20) & 0xffffffff, # /12
	((~0x0) << 19) & 0xffffffff, # /13
	((~0x0) << 18) & 0xffffffff, # /14
	((~0x0) << 17) & 0xffffffff, # /15
	((~0x0) << 16) & 0xffffffff, # /16
	((~0x0) << 15) & 0xffffffff, # /17
	((~0x0) << 14) & 0xffffffff, # /18
	((~0x0) << 13) & 0xffffffff, # /19
	((~0x0) << 12) & 0xffffffff, # /20
	((~0x0) << 11) & 0xffffffff, # /21
	((~0x0) << 10) & 0xffffffff, # /22
	((~0x0) <<  9) & 0xffffffff, # /23
	((~0x0) <<  8) & 0xffffffff, # /24
	((~0x0) <<  7) & 0xffffffff, # /25
	((~0x0) <<  6) & 0xffffffff, # /26
	((~0x0) <<  5) & 0xffffffff, # /27
	((~0x0) <<  4) & 0xffffffff, # /28
	((~0x0) <<  3) & 0xffffffff, # /29
	((~0x0) <<  2) & 0xffffffff, # /30
	((~0x0) <<  1) & 0xffffffff, # /31
	((~0x0) <<  0) & 0xffffffff  # /32
]

# Header
print("%s | %s | %s | %s" % ("ASN".ljust(5), "IPv4 Address".ljust(15),
	"BGP Prefix".ljust(18), "AS Name"))

# Seperator
print("%s | %s | %s | %s" % ("".ljust(5, "-"), "".ljust(15, "-"),
	"".ljust(18, "-"), "".ljust(7, "-")))

dirname = os.path.dirname(sys.argv[0])
conn = sqlite3.connect(os.path.join(dirname, "db.sqlite3"))
conn.text_factory = str
c = conn.cursor()

for arg in sys.argv[1:]:
	ip4addr_s = arg

	[x, y, z, w] = ip4addr_s.split(".")
	ip4addr_i = (int(x) << 24) | (int(y) << 16) | (int(z) <<  8) | (int(w) <<  0)

	# Test longer networks first.
	hits = []
	for i in range(32,0,-1):
		net = "%u.%u.%u.%u/%u" % (
			((ip4addr_i & ip4mask[i]) >> 24) & 0xff,
			((ip4addr_i & ip4mask[i]) >> 16) & 0xff,
			((ip4addr_i & ip4mask[i]) >>  8) & 0xff,
			((ip4addr_i & ip4mask[i]) >>  0) & 0xff,
			i)

		# Resolve an IPv4 address to an AS number.
		c.execute('SELECT asn FROM ip4net2asn WHERE ip4net=?', (net,))
		asn = c.fetchone()
		if not asn:
			continue
		asn = asn[0]
		if asn in hits:
			continue
		hits.append(asn)

		# Resolve an AS number to a AS name.
		asname = "NA"
		c.execute('SELECT name FROM asn2name WHERE asn=?', (asn,))
		name = c.fetchone()
		if name:
			asname = name[0]

		print("%s | %s | %s | %s" % (asn.ljust(5),
			ip4addr_s.ljust(15), net.ljust(18), asname))

	# Always print something.
	if not hits:
		print("%s | %s | %s | %s" % ("NA".ljust(5), ip4addr_s.ljust(15),
			"NA".ljust(18), "NA"))
