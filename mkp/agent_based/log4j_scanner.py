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
    n = 0
    for line in section:
        if line[0] == "[*]":
            n = (n + 1)
            yield Result(state=State.CRIT, summary=(' '.join(line[2:])))
    t_state = (State.OK if (n == 0) else State.CRIT)
    yield Result(state=t_state, summary=("%d vulnerabilities found" % n))


register.agent_section(
    name="log4j_scanner",
)

register.check_plugin(
    name="log4j_scanner",
    service_name="Scan for log4j CVE-2021-44228",
    discovery_function=log4j_scanner_discovery,
    check_function=log4j_scanner_checks,
)
