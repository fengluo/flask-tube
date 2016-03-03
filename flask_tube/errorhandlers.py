# -*- coding: utf-8 -*-

from flask import request

from .response import render_error

def configure_errorhandlers(app):

    @app.errorhandler(400)
    def empty_body(error):
        return render_error(400, 'No input data provided', 400)

    @app.errorhandler(401)
    def unauthorized(error):
        return render_error(401, 'Login required', 401)

    @app.errorhandler(402)
    def authorize_failed(error):
        return render_error(402, 'Authentication Failed', 402)

    @app.errorhandler(403)
    def forbidden(error):
        return render_error(403, 'Sorry, page not allowed', 403)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_error(404, 'Not Found: ' + request.url, 404)

    @app.errorhandler(500)
    def server_error(error):
        return render_error(500, 'Sorry, an error has occurred', 500)
