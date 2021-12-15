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


def log4j_scanner_discovery(section):
    yield Service()


def log4j_scanner_checks(section):
    i = 0
    for l in section:
        if l[0] == "[*]":
            i += 1
            yield Result(state=State.CRIT, summary=(' '.join(l[2:])))
    t_state = (State.OK if (i == 0) else State.CRIT)
    yield Result(state=t_state, summary=("%d vulnerabilities found" % i))


register.agent_section(
    name="log4j_scanner",
)

register.check_plugin(
    name="log4j_scanner",
    service_name="Scan for log4j CVE-2021-44228",
    discovery_function=log4j_scanner_discovery,
    check_function=log4j_scanner_checks,
)
