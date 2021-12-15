#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright (c) 2021 inett GmbH
# License: GNU General Public License v2
# A file is subject to the terms and conditions defined in the file LICENSE,
# which is part of this source code package.

from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)
from cmk.gui.valuespec import (
    Alternative,
    FixedValue,
)import cmk.utils.version as cmk_version


if cmk_version.is_enterprise_version() or cmk_version.is_managed_version():
    from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import (
        RulespecGroupMonitoringAgentsAgentPlugins
    )

    def _valuespec_agent_config_log4j_scanner():
        return Alternative(
            title=_("log4j CVE-2021-44228 (Linux)"),
            help=_(
                "scan for CVE-2021-44228 (<tt>log4j_scanner</tt>)<br/>"
                "<b>This plugin may result in massive agent outputs</b>"
                ),
            style='dropdown',
            elements=[
                FixedValue(
                    True,
                    title=_("Deploy plugin to scan for log4j"),
                    totext=_("(enabled)"),
                ),
                FixedValue(
                    None,
                    title=_("Do not deploy plugin to scan for log4j"),
                    totext=_("(disabled)"),
                )
            ],
        )


    rulespec_registry.register(
        HostRulespec(
            group=RulespecGroupMonitoringAgentsAgentPlugins,
            name="agent_config:log4j_scanner",
            valuespec=_valuespec_agent_config_log4j_scanner,
        ))
