#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright (c) 2021 inett GmbH
# License: GNU General Public License v2
# A file is subject to the terms and conditions defined in the file LICENSE,
# which is part of this source code package.

import pprint
from pathlib import Path
from typing import Any, Dict

from .bakery_api.v1 import (
        FileGenerator,
        OS,
        Plugin,
        register,
)


def get_log4j_scanner_files(conf: Dict[str, Any]) -> FileGenerator:
    if conf != None:
        yield Plugin(
            base_os=OS.LINUX,
            source=Path("log4j_scanner"),
            interval=14400,
      )


register.bakery_plugin(
    name="log4j_scanner",
    files_function=get_log4j_scanner_files,
)
