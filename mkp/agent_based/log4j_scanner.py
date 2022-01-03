#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2021 inett GmbH
# License: GNU General Public License v2
# A file is subject to the terms and conditions defined in the file LICENSE,
# which is part of this source code package.

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from .agent_based_api.v1 import (
    register,
    Service,
    State,
    Result,
)
import collections


def log4j_scanner_discovery(section):
    def vulns():
        yield {"cve": "CVE-2021-44228", "product": "log4j 2"}
        yield {"cve": "CVE-2021-45046", "product": "log4j 2.15.0"}
        yield {"cve": "CVE-2021-45105", "product": "log4j 2.16.0"}
        yield {"cve": "CVE-2021-4104", "product": "log4j 1.x"}
        yield {"cve": "CVE-2021-42550", "product": "logback 0.9-1.2.7"}
        yield {"cve": "CVE-2021-44832", "product": "log4j 2"}

    for vuln in vulns():
        yield Service(
            item=("%s (%s)" % (vuln.get("cve"), vuln.get("product"))),
            parameters=vuln
        )


def log4j_scanner_checks(item, params, section):
    cve, product = params["cve"].lower(), params["product"]
    f, p, e = 0, 0, 0
    empty_line_detected = False
    endblock = collections.deque(maxlen=6)
    for line in section:
        if empty_line_detected:
            endblock.append(line)
        if len(line) == 0:
            empty_line_detected = True
            continue
        if line[0] == "[*]" and line[2].lower() == cve:
            f = (f + 1)
            yield Result(state=State.CRIT, summary=(' '.join(line[2:])))
        elif line[0] == "[?]" and line[2].lower() == cve:
            p = (p + 1)
            yield Result(
                state=State.CRIT,
                summary=("potential %s" % ' '.join(line[2:]))
            )
        elif ' '.join(line[0:1]) == "Scan error:":
            e = (e + 1)

    for line in endblock:
        if len(line) == 6 and line[0] == "Scanned" and line[2] == \
                "directories" and line[5] == "files":
            yield Result(
                state=State.OK, summary=("%d files scanned" % line[4])
            )
            yield Result(
                state=State.OK, summary=("%d directories scanned" % line[1])
            )
    f_state = (State.OK if (f == 0) else State.CRIT)
    yield Result(state=f_state, summary=("%d vulnerabilities found" % f))
    p_state = (State.OK if (p == 0) else State.CRIT)
    yield Result(
        state=p_state,
        summary=("%d potential vulnerabilities found" % p),
    )
    e_state = (State.OK if (e == 0) else State.UNKNOWN)
    yield Result(state=e_state, summary=("%d scan errors" % e))


register.agent_section(
    name="log4j_scanner",
)

register.check_plugin(
    name="log4j_scanner",
    service_name="Vulnerability %s",
    sections=["log4j_scanner"],
    discovery_function=log4j_scanner_discovery,
    check_function=log4j_scanner_checks,
    check_default_parameters={},
)
