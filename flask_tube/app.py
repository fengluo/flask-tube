# -*- coding: utf-8 -*-

import os
import logging
import inspect
from logging.handlers import SMTPHandler, RotatingFileHandler
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
            middlewares=None,
            errorhandlers=None):
        super(App, self).__init__(
            import_name,
            instance_path=os.getcwd(),
            instance_relative_config=True)
        self.packages = packages if packages else []
        self.exts = extensions if extensions else []
        self.middlewares = middlewares if middlewares else []
        self.errorhandlers = errorhandlers if errorhandlers else[]

        # config
        if config:
            self.config.from_pyfile(config)
        elif os.getenv('FLASK') == 'dev':
            self.config.from_pyfile('config/development.conf')
            self.logger.info("Config: Development")
        elif os.getenv('FLASK') == 'test':
            self.config.from_pyfile('config/test.conf')
            self.logger.info("Config: Test")
        else:
            self.config.from_pyfile('config/production.conf')
            self.logger.info("Config: Production")

        self.configure_extensions(self.exts)
        self.configure_middlewares(self.middlewares)
        self.configure_errorhandlers(self.errorhandlers)

        # register module
        self.configure_packages(self.packages)

        self.configure_logging()

    def configure_extensions(self, extensions):
        for extension in extensions.__dict__.values():
            if not inspect.isclass(extension) and hasattr(extension, 'init_app'):
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

    def configure_errorhandlers(self, errorhandlers):
        for errorhandler in errorhandlers:
            errorhandler(self)

    def configure_logging(self):
        mail_handler = \
            SMTPHandler(self.config['MAIL_SERVER'],
                        self.config['DEFAULT_MAIL_SENDER'],
                        self.config['ADMINS'], 
                        'selflication error',
                        (
                            self.config['MAIL_USERNAME'],
                            self.config['MAIL_PASSWORD'],
                        ))

        mail_handler.setLevel(logging.ERROR)
        self.logger.addHandler(mail_handler)

        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]')

        debug_log = os.path.join(self.root_path, 
                                 self.config['DEBUG_LOG'])

        debug_file_handler = \
            RotatingFileHandler(debug_log,
                                maxBytes=100000,
                                backupCount=10)

        debug_file_handler.setLevel(logging.DEBUG)
        debug_file_handler.setFormatter(formatter)
        self.logger.addHandler(debug_file_handler)

        error_log = os.path.join(self.root_path, 
                                 self.config['ERROR_LOG'])

        error_file_handler = \
            RotatingFileHandler(error_log,
                                maxBytes=100000,
                                backupCount=10)

        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(formatter)
        self.logger.addHandler(error_file_handler)
