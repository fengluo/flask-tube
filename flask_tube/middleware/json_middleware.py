# -*- coding: utf-8 -*-
from flask import request, abort

def JSONMiddleware(app):
    @app.before_request
    def check_body_data():
        if request.method in ['POST', 'PUT'] and not request.get_json():
            abort(400)

    @app.after_request
    def headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = \
            'PUT, GET, POST, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = \
            'Authorization,Content-Type,Accept,Origin,User-Agent,\
            DNT,Cache-Control,X-Mx-ReqToken,Keep-Alive,X-Requested-With,\
            If-Modified-Since, X-Total, X-Page'
        response.headers['Content-Type'] = 'application/json'
        return response
