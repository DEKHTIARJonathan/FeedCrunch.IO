#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re


def get_domain(link = ""):
	starts = [match.start() for match in re.finditer(re.escape("/"), link)]
	if len(starts) > 2:
		return link[starts[1]+1:starts[2]]
	elif len(starts) == 2:
		return link[starts[1]+1:]
	else:
		return str("error")
