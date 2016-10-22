#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals


def str2bool(v):
	return v.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
