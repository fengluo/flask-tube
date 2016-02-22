import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('flask_tube/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='Flask-Tube',
    version=version,
    url='http://github.com/fengluo/flask-tube',
    license='MIT',
    author='Shawn Xie',
    author_email='fengluo17@gmail.com',
    discription='Flask-tube is a wrapper of Flask',
    packages=['flask_tube', 'flask_tube.middleware'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Flask>=0.10",
        "Flask-SQLAlchemy>=2.1"
    ])
