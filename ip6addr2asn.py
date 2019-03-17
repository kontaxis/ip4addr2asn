#!/usr/bin/python -u

# kontaxis 2019-03-16

from __future__ import print_function

import os
import sys
import sqlite3

import ip6utils

# Prepare ip6masks
ip6mask = [
	0x00000000,
	((~0x0) << 127) & 0xffffffffffffffffffffffffffffffff, # /1
	((~0x0) << 126) & 0xffffffffffffffffffffffffffffffff, # /2
	((~0x0) << 125) & 0xffffffffffffffffffffffffffffffff, # /3
	((~0x0) << 124) & 0xffffffffffffffffffffffffffffffff, # /4
	((~0x0) << 123) & 0xffffffffffffffffffffffffffffffff, # /5
	((~0x0) << 122) & 0xffffffffffffffffffffffffffffffff, # /6
	((~0x0) << 121) & 0xffffffffffffffffffffffffffffffff, # /7
	((~0x0) << 120) & 0xffffffffffffffffffffffffffffffff, # /8
	((~0x0) << 119) & 0xffffffffffffffffffffffffffffffff, # /9
	((~0x0) << 118) & 0xffffffffffffffffffffffffffffffff, # /10
	((~0x0) << 117) & 0xffffffffffffffffffffffffffffffff, # /11
	((~0x0) << 116) & 0xffffffffffffffffffffffffffffffff, # /12
	((~0x0) << 115) & 0xffffffffffffffffffffffffffffffff, # /13
	((~0x0) << 114) & 0xffffffffffffffffffffffffffffffff, # /14
	((~0x0) << 113) & 0xffffffffffffffffffffffffffffffff, # /15
	((~0x0) << 112) & 0xffffffffffffffffffffffffffffffff, # /16
	((~0x0) << 111) & 0xffffffffffffffffffffffffffffffff, # /17
	((~0x0) << 110) & 0xffffffffffffffffffffffffffffffff, # /18
	((~0x0) << 109) & 0xffffffffffffffffffffffffffffffff, # /19
	((~0x0) << 108) & 0xffffffffffffffffffffffffffffffff, # /20
	((~0x0) << 107) & 0xffffffffffffffffffffffffffffffff, # /21
	((~0x0) << 106) & 0xffffffffffffffffffffffffffffffff, # /22
	((~0x0) << 105) & 0xffffffffffffffffffffffffffffffff, # /23
	((~0x0) << 104) & 0xffffffffffffffffffffffffffffffff, # /24
	((~0x0) << 103) & 0xffffffffffffffffffffffffffffffff, # /25
	((~0x0) << 102) & 0xffffffffffffffffffffffffffffffff, # /26
	((~0x0) << 101) & 0xffffffffffffffffffffffffffffffff, # /27
	((~0x0) << 100) & 0xffffffffffffffffffffffffffffffff, # /28
	((~0x0) <<  99) & 0xffffffffffffffffffffffffffffffff, # /29
	((~0x0) <<  98) & 0xffffffffffffffffffffffffffffffff, # /30
	((~0x0) <<  97) & 0xffffffffffffffffffffffffffffffff, # /31
	((~0x0) <<  96) & 0xffffffffffffffffffffffffffffffff, # /32
	((~0x0) <<  95) & 0xffffffffffffffffffffffffffffffff, # /33
	((~0x0) <<  94) & 0xffffffffffffffffffffffffffffffff, # /34
	((~0x0) <<  93) & 0xffffffffffffffffffffffffffffffff, # /35
	((~0x0) <<  92) & 0xffffffffffffffffffffffffffffffff, # /36
	((~0x0) <<  91) & 0xffffffffffffffffffffffffffffffff, # /37
	((~0x0) <<  90) & 0xffffffffffffffffffffffffffffffff, # /38
	((~0x0) <<  89) & 0xffffffffffffffffffffffffffffffff, # /39
	((~0x0) <<  88) & 0xffffffffffffffffffffffffffffffff, # /40
	((~0x0) <<  87) & 0xffffffffffffffffffffffffffffffff, # /41
	((~0x0) <<  86) & 0xffffffffffffffffffffffffffffffff, # /42
	((~0x0) <<  85) & 0xffffffffffffffffffffffffffffffff, # /43
	((~0x0) <<  84) & 0xffffffffffffffffffffffffffffffff, # /44
	((~0x0) <<  83) & 0xffffffffffffffffffffffffffffffff, # /45
	((~0x0) <<  82) & 0xffffffffffffffffffffffffffffffff, # /46
	((~0x0) <<  81) & 0xffffffffffffffffffffffffffffffff, # /47
	((~0x0) <<  80) & 0xffffffffffffffffffffffffffffffff, # /48
	((~0x0) <<  79) & 0xffffffffffffffffffffffffffffffff, # /49
	((~0x0) <<  78) & 0xffffffffffffffffffffffffffffffff, # /50
	((~0x0) <<  77) & 0xffffffffffffffffffffffffffffffff, # /51
	((~0x0) <<  76) & 0xffffffffffffffffffffffffffffffff, # /52
	((~0x0) <<  75) & 0xffffffffffffffffffffffffffffffff, # /53
	((~0x0) <<  74) & 0xffffffffffffffffffffffffffffffff, # /54
	((~0x0) <<  73) & 0xffffffffffffffffffffffffffffffff, # /55
	((~0x0) <<  72) & 0xffffffffffffffffffffffffffffffff, # /56
	((~0x0) <<  71) & 0xffffffffffffffffffffffffffffffff, # /57
	((~0x0) <<  70) & 0xffffffffffffffffffffffffffffffff, # /58
	((~0x0) <<  69) & 0xffffffffffffffffffffffffffffffff, # /59
	((~0x0) <<  68) & 0xffffffffffffffffffffffffffffffff, # /60
	((~0x0) <<  67) & 0xffffffffffffffffffffffffffffffff, # /61
	((~0x0) <<  66) & 0xffffffffffffffffffffffffffffffff, # /62
	((~0x0) <<  65) & 0xffffffffffffffffffffffffffffffff, # /63
	((~0x0) <<  64) & 0xffffffffffffffffffffffffffffffff, # /64
	((~0x0) <<  63) & 0xffffffffffffffffffffffffffffffff, # /65
	((~0x0) <<  62) & 0xffffffffffffffffffffffffffffffff, # /66
	((~0x0) <<  61) & 0xffffffffffffffffffffffffffffffff, # /67
	((~0x0) <<  60) & 0xffffffffffffffffffffffffffffffff, # /68
	((~0x0) <<  59) & 0xffffffffffffffffffffffffffffffff, # /69
	((~0x0) <<  58) & 0xffffffffffffffffffffffffffffffff, # /70
	((~0x0) <<  57) & 0xffffffffffffffffffffffffffffffff, # /71
	((~0x0) <<  56) & 0xffffffffffffffffffffffffffffffff, # /72
	((~0x0) <<  55) & 0xffffffffffffffffffffffffffffffff, # /73
	((~0x0) <<  54) & 0xffffffffffffffffffffffffffffffff, # /74
	((~0x0) <<  53) & 0xffffffffffffffffffffffffffffffff, # /75
	((~0x0) <<  52) & 0xffffffffffffffffffffffffffffffff, # /76
	((~0x0) <<  51) & 0xffffffffffffffffffffffffffffffff, # /77
	((~0x0) <<  50) & 0xffffffffffffffffffffffffffffffff, # /78
	((~0x0) <<  49) & 0xffffffffffffffffffffffffffffffff, # /79
	((~0x0) <<  48) & 0xffffffffffffffffffffffffffffffff, # /80
	((~0x0) <<  47) & 0xffffffffffffffffffffffffffffffff, # /81
	((~0x0) <<  46) & 0xffffffffffffffffffffffffffffffff, # /82
	((~0x0) <<  45) & 0xffffffffffffffffffffffffffffffff, # /83
	((~0x0) <<  44) & 0xffffffffffffffffffffffffffffffff, # /84
	((~0x0) <<  43) & 0xffffffffffffffffffffffffffffffff, # /85
	((~0x0) <<  42) & 0xffffffffffffffffffffffffffffffff, # /86
	((~0x0) <<  41) & 0xffffffffffffffffffffffffffffffff, # /87
	((~0x0) <<  40) & 0xffffffffffffffffffffffffffffffff, # /88
	((~0x0) <<  39) & 0xffffffffffffffffffffffffffffffff, # /89
	((~0x0) <<  38) & 0xffffffffffffffffffffffffffffffff, # /90
	((~0x0) <<  37) & 0xffffffffffffffffffffffffffffffff, # /91
	((~0x0) <<  36) & 0xffffffffffffffffffffffffffffffff, # /92
	((~0x0) <<  35) & 0xffffffffffffffffffffffffffffffff, # /93
	((~0x0) <<  34) & 0xffffffffffffffffffffffffffffffff, # /94
	((~0x0) <<  33) & 0xffffffffffffffffffffffffffffffff, # /95
	((~0x0) <<  32) & 0xffffffffffffffffffffffffffffffff, # /96
	((~0x0) <<  31) & 0xffffffffffffffffffffffffffffffff, # /97
	((~0x0) <<  30) & 0xffffffffffffffffffffffffffffffff, # /98
	((~0x0) <<  29) & 0xffffffffffffffffffffffffffffffff, # /99
	((~0x0) <<  28) & 0xffffffffffffffffffffffffffffffff, # /100
	((~0x0) <<  27) & 0xffffffffffffffffffffffffffffffff, # /101
	((~0x0) <<  26) & 0xffffffffffffffffffffffffffffffff, # /102
	((~0x0) <<  25) & 0xffffffffffffffffffffffffffffffff, # /103
	((~0x0) <<  24) & 0xffffffffffffffffffffffffffffffff, # /104
	((~0x0) <<  23) & 0xffffffffffffffffffffffffffffffff, # /105
	((~0x0) <<  22) & 0xffffffffffffffffffffffffffffffff, # /106
	((~0x0) <<  21) & 0xffffffffffffffffffffffffffffffff, # /107
	((~0x0) <<  20) & 0xffffffffffffffffffffffffffffffff, # /108
	((~0x0) <<  19) & 0xffffffffffffffffffffffffffffffff, # /109
	((~0x0) <<  18) & 0xffffffffffffffffffffffffffffffff, # /110
	((~0x0) <<  17) & 0xffffffffffffffffffffffffffffffff, # /111
	((~0x0) <<  16) & 0xffffffffffffffffffffffffffffffff, # /112
	((~0x0) <<  15) & 0xffffffffffffffffffffffffffffffff, # /113
	((~0x0) <<  14) & 0xffffffffffffffffffffffffffffffff, # /114
	((~0x0) <<  13) & 0xffffffffffffffffffffffffffffffff, # /115
	((~0x0) <<  12) & 0xffffffffffffffffffffffffffffffff, # /116
	((~0x0) <<  11) & 0xffffffffffffffffffffffffffffffff, # /117
	((~0x0) <<  10) & 0xffffffffffffffffffffffffffffffff, # /118
	((~0x0) <<   9) & 0xffffffffffffffffffffffffffffffff, # /119
	((~0x0) <<   8) & 0xffffffffffffffffffffffffffffffff, # /120
	((~0x0) <<   7) & 0xffffffffffffffffffffffffffffffff, # /121
	((~0x0) <<   6) & 0xffffffffffffffffffffffffffffffff, # /122
	((~0x0) <<   5) & 0xffffffffffffffffffffffffffffffff, # /123
	((~0x0) <<   4) & 0xffffffffffffffffffffffffffffffff, # /124
	((~0x0) <<   3) & 0xffffffffffffffffffffffffffffffff, # /125
	((~0x0) <<   2) & 0xffffffffffffffffffffffffffffffff, # /126
	((~0x0) <<   1) & 0xffffffffffffffffffffffffffffffff, # /127
	((~0x0) <<   0) & 0xffffffffffffffffffffffffffffffff, # /128
]

# Header
print("%s | %s | %s | %s" % ("ASN".ljust(5), "IPv6 Address".ljust(39),
	"BGP Prefix".ljust(43), "AS Name"))

# Seperator
print("%s | %s | %s | %s" % ("".ljust(5, "-"), "".ljust(39, "-"),
	"".ljust(43, "-"), "".ljust(7, "-")))

dirname = os.path.dirname(sys.argv[0])
conn = sqlite3.connect(os.path.join(dirname, "db6.sqlite3"))
conn.text_factory = str
c = conn.cursor()

for arg in sys.argv[1:]:
	ip6addr_s = arg

	ip6addr_i = ip6utils.ip6addr_atoi(ip6addr_s)

	# Test longer networks first.
	hits = []
	for i in range(128,0,-1):
		net = "%04X:%04X:%04X:%04X:%04X:%04X:%04X:%04X/%u" % (
			((ip6addr_i & ip6mask[i]) >> 112) & 0xffff,
			((ip6addr_i & ip6mask[i]) >>  96) & 0xffff,
			((ip6addr_i & ip6mask[i]) >>  80) & 0xffff,
			((ip6addr_i & ip6mask[i]) >>  64) & 0xffff,
			((ip6addr_i & ip6mask[i]) >>  48) & 0xffff,
			((ip6addr_i & ip6mask[i]) >>  32) & 0xffff,
			((ip6addr_i & ip6mask[i]) >>  16) & 0xffff,
			((ip6addr_i & ip6mask[i]) >>   0) & 0xffff,
			i)

		# Resolve an IPv6 address to an AS number.
		c.execute('SELECT asn FROM ip6net2asn WHERE ip6net=?', (net,))
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
			ip6addr_s.ljust(39), net.ljust(43), asname))

	# Always print something.
	if not hits:
		print("%s | %s | %s | %s" % ("NA".ljust(5), ip6addr_s.ljust(39),
			"NA".ljust(43), "NA"))
