"""gridscale auth plugin for HTTPie."""
# -*- coding: utf-8 -*-

import os
import sys

import yaml
from httpie.plugins import AuthPlugin
from httpie.status import ExitStatus
from requests.auth import HTTPBasicAuth

__version__ = "1.0.0"
__author__ = "ghostwheel42"
__license__ = "MIT"


ENV_UID = "GRIDSCALE_UUID"
ENV_TOKEN = "GRIDSCALE_TOKEN"


class GSAuth(HTTPBasicAuth):
    """Attach gridscale authentication to the given Request object."""

    def __call__(self, req):
        """Set gridscale api authentication headers."""
        req.headers.update(
            {
                "X-Auth-UserId": self.username,
                "X-Auth-Token": self.password,
            }
        )
        return req


class GSAuthPlugin(AuthPlugin):
    """gridscale API auth plugin class."""

    name = "gridscale API auth"
    auth_type = "gs"
    description = "token authentication at gridscale api"
    auth_require = False
    auth_parse = True
    prompt_password = False

    def __init__(self) -> None:
        """Initialize own class variables."""
        super().__init__()
        self._file = None
        self._config = None

    def get_auth(self, username: str = None, password: str = None):
        """Get missing auth info from environment or gridscale/config.yaml."""
        # username specified via --auth?
        if username:
            # password specified via --auth?
            if password:
                # use --auth data for login as uid & token
                return GSAuth(username, password)
            # take username from --auth as project name and look-up in config
            if auth := self._getProjectAuth(name=username):
                return auth
            # take username from --auth as userId and look-up in config
            if auth := self._getProjectAuth(userId=username):
                return auth
            # no auth data found. we won't prompt for a password, so this is an error
            self._fail(
                f"project matching {username!r} not found in gridscale/config.yaml"
            )

        # uid specified via env?
        if uid := os.getenv(ENV_UID):
            # token specified via env?
            if token := os.getenv(ENV_TOKEN):
                return GSAuth(uid, token)
            # look up token in config
            if auth := self._getProjectAuth(userId=uid):
                return auth
            # no auth data found. we won't prompt for a password, so this is an error
            self._fail(f"token for userId {uid!r} not found in gridscale/config.yaml")

        # look up project named "default"
        if auth := self._getProjectAuth(name="default"):
            return auth

        # no project "default" - use first project
        if auth := self._getProjectAuth():
            return auth

        # no auth data found. this is an error
        self._fail("no project found in gridscale/config.yaml")

    def _getProjectAuth(self, **match) -> (GSAuth | None):
        """Look-up auth data for matching project in gridscale config."""
        self._loadConfig()

        for project in self._config.get("projects", []):
            if all(project.get(key) == value for key, value in match.items()):
                uid = project.get("userId")
                token = project.get("token")
                if uid and token:
                    return GSAuth(uid, token)

        return None

    def _loadConfig(self):
        """Load configuration from gridscale.yaml."""
        if self._config:
            return

        if not self._file:
            if path := self._configPath():
                self._file = os.path.join(path, "gridscale", "config.yaml")
            if not os.path.isfile(self._file):
                self._file = "config.yaml"

        try:
            with open(self._file) as fp:
                self._config = yaml.safe_load(fp)
        except (OSError, yaml.YAMLError) as exc:
            self._fail(f"error loading {self._file!r} {exc}")

    def _configPath(self) -> (str | None):
        """Determine os-specific local config path like gscloud does."""
        if os.name == "nt":
            return os.getenv("APPDATA")
        if os.sys.platform == "darwin":
            if home := os.getenv("HOME"):
                return os.path.join(home, "Library", "Application Support")
        if xdg := os.getenv("XDG_CONFIG_HOME"):
            return xdg
        if home := os.getenv("HOME"):
            return os.path.join(home, ".config")
        return None

    def _fail(self, msg: str = None):
        """Output error message and exit plugin."""
        if msg is not None:
            print(f"[{self.package_name}]", msg, file=sys.stderr)
        sys.exit(ExitStatus.PLUGIN_ERROR)
