"""Deployment step title matching configuration."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import re
from typing import Literal

type DeploymentStep = Literal[
    "step1",
    "step2",
    "setup_dns",
    "setup_ip",
    "webcertstep",
    "step5",
    "laststep",
]


def _deployment_step_pattern(pattern: str) -> re.Pattern[str]:
    return re.compile(rf"\b{pattern}\b", re.IGNORECASE)


DEPLOYMENT_STEP_TITLE_PATTERNS: tuple[tuple[re.Pattern[str], DeploymentStep], ...] = (
    (_deployment_step_pattern(r"Step\s+1"), "step1"),
    (_deployment_step_pattern("Oneprovider registration"), "step2"),
    (_deployment_step_pattern("DNS setup"), "setup_dns"),
    (_deployment_step_pattern("cluster IP addresses"), "setup_ip"),
    (_deployment_step_pattern("certificate setup"), "webcertstep"),
    (_deployment_step_pattern("storage backend configuration"), "step5"),
    (_deployment_step_pattern("summary"), "laststep"),
)
