#!/usr/bin/env python3

from tidyexc import Error

class ConfigError(Error):
    """
    Raised when unable to find and/or load test parameters.
    """
    pass
