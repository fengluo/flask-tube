# -*- coding: utf-8 -*-

import os
from werkzeug.utils import import_string, find_modules
from flask import Flask, Blueprint


class App(Flask):
    """Custom Flask Class."""

    def __init__(
            self,
            import_name,
            config=None,
            packages=None,
            extensions=None,
            middlewares=None):
        super(App, self).__init__(
            import_name,
            instance_path=os.getcwd(),
            instance_relative_config=True)

        # config
        if os.getenv('FLASK') == 'dev':
            self.config.from_pyfile('config/development.conf')
            self.logger.info("Config: Development")
        elif os.getenv('FLASK') == 'test':
            self.config.from_pyfile('config/test.conf')
            self.logger.info("Config: Test")
        else:
            self.config.from_pyfile('config/production.conf')
            self.logger.info("Config: Production")

        self.configure_extensions(extensions)
        # self.configure_errorhandlers()
        self.configure_middlewares(middlewares)

        # register module
        self.configure_packages(packages)

    def configure_extensions(self, extensions):
        for extension in extensions.__dict__.items():
            if hasattr(extension, 'init_app'):
                extension.init_app(self)

    def configure_packages(self, packages):
        for package_name in packages:
            package_name = '%s.%s' % (self.import_name, package_name)
            modules = find_modules(package_name)
            for module in modules:
                __import__(module)

            package = import_string(package_name)
            for attr_name in dir(package):
                attr = getattr(package, attr_name)
                if isinstance(attr, Blueprint):
                    self.register_blueprint(attr)

    def configure_middlewares(self, middlewares):
        for middleware in middlewares:
            middleware(self)
