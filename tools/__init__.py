# -*- encoding: utf-8 -*-
from enum import Enum
from tools import libs  # this registers all tools
from tools.tool_registry import TOOL_REGISTRY

_ = libs, TOOL_REGISTRY  # Avoid pre-commit error