# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 ADE-Scheduler.
#
# ADE-Scheduler is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Helpers."""

from flask import current_app


class TrustedHostsMixin(object):
    """Mixin for reading trusted hosts from application config."""

    @property
    def trusted_hosts(self):
        """Get list of trusted hosts."""
        if current_app:
            return current_app.config.get("APP_ALLOWED_HOSTS", None)
