#!/usr/bin/python -u

from __future__ import print_function

import os
import sqlite3
import sys
import time

dirname = os.path.dirname(sys.argv[0])

# Populate ip6net2asn records array
ip6net2asn = []

# e.g., http://thyme.apnic.net/us/data-raw-table
f = file(os.path.join(dirname, "ip6net2asn.txt"), "r")

for line in f:
	[ip6net, asn] = line.split("\t")
	asn = asn.rstrip("\n")
	ip6net2asn.append((ip6net, asn))

f.close()

# Populate asn2name records array
asn2name = []

# e.g., http://thyme.apnic.net/hk/data-used-autnums
f = file(os.path.join(dirname, "asn2name.txt"), "r")

for line in f:
	asn = line[0:6].strip(" ")
	name = line[6:].rstrip("\n")
	asn2name.append((asn, name))

f.close()

# Make it happen
conn = sqlite3.connect("db6.sqlite3")
conn.text_factory = str
c = conn.cursor()

# Create schema.
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",
	("last_generated",))
match = c.fetchone()
if not match:
	c.execute("CREATE TABLE last_generated (epoch integer);")
	c.execute("CREATE TABLE ip6net2asn (ip6net text, asn text);")
	c.execute("CREATE INDEX ip6net on ip6net2asn (ip6net);")
	c.execute("CREATE TABLE asn2name (asn text unique, name text);")
	c.execute("CREATE INDEX asn on asn2name (asn);")

c.execute('DELETE FROM last_generated');
c.execute('INSERT INTO last_generated VALUES(?)',
	(str(int(time.time())),))

c.execute('DELETE FROM ip6net2asn');
c.executemany('INSERT INTO ip6net2asn VALUES (?,?)', ip6net2asn)

c.execute('DELETE FROM asn2name');
c.executemany('INSERT INTO asn2name   VALUES (?,?)', asn2name)

conn.commit()
conn.close()
