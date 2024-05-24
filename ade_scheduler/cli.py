# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 ADE-Scheduler.
#
# ADE-Scheduler is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""CLI application for ADE-Scheduler."""

import click

from flask.cli import FlaskGroup

from .factory import create_app


#: ADE-Scheduler CLI application.
@click.group(cls=FlaskGroup, create_app=create_app)
def cli(**params):
    """Command Line Interface for ADE-Scheduler."""
