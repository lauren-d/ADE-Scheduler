# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 ADE-Scheduler.
#
# ADE-Scheduler is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""."""
import os
import sys

from invenio_base import create_app_factory, create_wsgi_factory
from invenio_base.wsgi import wsgi_proxyfix
from invenio_config import create_config_loader
from jinja2 import BytecodeCache

from ade_scheduler.helpers import TrustedHostsMixin

env_prefix = "ADE_SCHEDULER"

invenio_config_loader = create_config_loader(config=None,
                                             env_prefix=env_prefix)


def instance_path():
    """Instance path for ADE-Scheduler.

    Defaults to ``<env_prefix>_INSTANCE_PATH`` or if environment
    variable is not set ``<sys.prefix>/var/instance``.
    """
    return os.getenv(f"{env_prefix}_INSTANCE_PATH") or \
        os.path.join(sys.prefix, "var", "instance")


def static_folder():
    """Static folder path.

    Defaults to ``<env_prefix>_STATIC_FOLDER`` or if environment
    variable is not set ``<sys.prefix>/var/instance/static``.
    """
    return os.getenv(f"{env_prefix}_STATIC_FOLDER") or \
        os.path.join(instance_path(), "static")


def static_url_path():
    """Static url path.

    Defaults to ``<env_prefix>_STATIC_URL_PATH`` or if environment variable
    is not set ``/static``.
    """
    return os.getenv(f"{env_prefix}_STATIC_URL_PATH") or "/static"


def config_loader(app, **kwargs_config):
    """Configuration loader."""
    invenio_config_loader(app, **kwargs_config)

    app.jinja_env.cache_size = 1000
    app.jinja_env.bytecode_cache = BytecodeCache()


def app_class():
    """Create Flask application class."""
    from flask import Flask as FlaskBase

    # Add Host header validation via APP_ALLOWED_HOSTS configuration variable.
    class Request(TrustedHostsMixin, FlaskBase.request_class):
        pass

    class Flask(FlaskBase):
        request_class = Request

    return Flask


create_api = create_app_factory(
    "ade-scheduler",
    config_loader=config_loader,
    blueprint_entry_points=["ade_scheduler.api_blueprints"],
    extension_entry_points=["ade_scheduler.api_apps"],
    finalize_app_entry_points=["ade_scheduler.api_finalize_app"],
    wsgi_factory=wsgi_proxyfix(),
    instance_path=instance_path,
    root_path=instance_path,
    app_class=app_class(),
)
"""Flask application factory for ADE-Scheduler REST API."""

create_ui = create_app_factory(
    "ade-scheduler",
    config_loader=config_loader,
    blueprint_entry_points=["ade_scheduler.blueprints"],
    extension_entry_points=["ade_scheduler.apps"],
    finalize_app_entry_points=["ade_scheduler.finalize_app"],
    wsgi_factory=wsgi_proxyfix(),
    instance_path=instance_path,
    static_folder=static_folder,
    root_path=instance_path,
    static_url_path=static_url_path(),
    app_class=app_class(),
)
"""Flask application factory for ADE-Scheduler UI."""

create_app = create_app_factory(
    "ade-scheduler",
    config_loader=config_loader,
    blueprint_entry_points=["ade_scheduler.blueprints"],
    extension_entry_points=["ade_scheduler.apps"],
    finalize_app_entry_points=["ade_scheduler.finalize_app"],
    wsgi_factory=wsgi_proxyfix(create_wsgi_factory({"/api": create_api})),
    instance_path=instance_path,
    static_folder=static_folder,
    root_path=instance_path,
    static_url_path=static_url_path(),
    app_class=app_class(),
)
"""Flask application factory for combined UI + REST API.

REST API is mounted under ``/api``.
"""
