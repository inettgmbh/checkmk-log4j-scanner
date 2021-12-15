#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2021 inett GmbH
# License: GNU General Public License v2
# A file is subject to the terms and conditions defined in the file LICENSE,
# which is part of this source code package.

from .agent_based_api.v1 import (
    register,
    Service,
    State,
    Result,
)
import re

proxmox_bs_subsection_start = re.compile("^===")
proxmox_bs_subsection_int = re.compile("===.*$")
proxmox_bs_subsection_end = re.compile("^=")


def log4j_scanner_discovery(_section):
    yield Service()


def log4j_scanner_checks(params, section):
    i = 0
    for l in section:
        if l[0] == "[*]":
            i += 1
            yield Result(state=State.CRIT, summary=(' '.join(l[2:])))
    t_state = (State.OK if (i == 0) else State.CRIT)
    yield Result(state=t_state, summary=("%d vulnerabilities found" % i))


register.check_plugin(
    name="log4j_scanner",
    sections=["log4j_scanner"],
    discovery_function=log4j_scanner_discovery,
    check_function=log4j_scanner_checks,
)

