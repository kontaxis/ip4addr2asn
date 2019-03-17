def ip6addr_atoi(ip6addr):
	addr_s = ip6addr

	addr_g = addr_s.split(":")

	if len(addr_g) < 3 or len(addr_g) > 8:
		return 0

	# Expand abbreviated groups of zeros.
	# ::
	if addr_g[0] == "" and addr_g[1] == "" and addr_g[2] == "":
		addr_g = ["0"] * 8
	# ::x
	elif addr_g[0] == "" and addr_g[1] == "":
		x = 8 - (len(addr_g) - 2)
		addr_g = (["0"] * x) + addr_g[2:]
	# x::
	elif addr_g[-1] == "" and addr_g[-2] == "":
		x = 8 - (len(addr_g) - 2)
		addr_g = addr_g[:-2] + (["0"]) * x
	# x::y
	else:
		for i in range(0,len(addr_g)):
			if addr_g[i] != "":
				continue

			x = 8 - (len(addr_g) - 1)
			addr_g = addr_g[0:i] + (["0"] * x) + addr_g[i+1:]

			# Only one such abbreviation is allowed.
			break

	return \
		(int(addr_g[0], 16) << 112) | \
		(int(addr_g[1], 16) <<  96) | \
		(int(addr_g[2], 16) <<  80) | \
		(int(addr_g[3], 16) <<  64) | \
		(int(addr_g[4], 16) <<  48) | \
		(int(addr_g[5], 16) <<  32) | \
		(int(addr_g[6], 16) <<  16) | \
		(int(addr_g[7], 16) <<   0)


def ip6net_expand(ip6net):
	tokens = ip6net.split("/")

	addr_s = tokens[0]
	mask_s = "/128"

	if len(tokens) > 1:
		mask_s = "/%s" % tokens[1]

	addr_i = ip6addr_atoi(addr_s)

	return "%04X:%04X:%04X:%04X:%04X:%04X:%04X:%04X%s" % \
			(
			   (addr_i >> 112) & 0xffff,
			   (addr_i >>  96) & 0xffff,
			   (addr_i >>  80) & 0xffff,
			   (addr_i >>  64) & 0xffff,
			   (addr_i >>  48) & 0xffff,
			   (addr_i >>  32) & 0xffff,
			   (addr_i >>  16) & 0xffff,
			   (addr_i >>   0) & 0xffff,
			   mask_s
			)
