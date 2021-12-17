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
import collections


def log4j_scanner_discovery(section):
    yield Service()


def log4j_scanner_checks(section):
    f, p = 0, 0
    eld = False
    lb = collections.deque(maxlen=6)
    for line in section:
        if eld:
            lb.append(line)
        if len(line) == 0:
            eld = True
            continue
        if line[0] == "[*]":
            f = (f + 1)
            yield Result(state=State.CRIT, summary=(' '.join(line[2:])))
        elif line[0] == "[?]":
            p = (p + 1)
            yield Result(
                state=State.CRIT,
                summary=("potential %s" % ' '.join(line[2:]))
            )
    for line in lb:
        if len(line) == 6 and line[0] == "Scanned" and line[2] == \
                "directories" and line[5] == "files":
            yield Result
    f_state = (State.OK if (f == 0) else State.CRIT)
    yield Result(state=f_state, summary=("%d vulnerabilities found" % f))
    p_state = (State.OK if (p == 0) else State.CRIT)
    yield Result(
        state=p_state,
        summary=("%d potential vulnerabilities found" % p),
    )


register.agent_section(
    name="log4j_scanner",
)

register.check_plugin(
    name="log4j_scanner",
    service_name="Scan for log4j CVE-2021-44228",
    discovery_function=log4j_scanner_discovery,
    check_function=log4j_scanner_checks,
)
