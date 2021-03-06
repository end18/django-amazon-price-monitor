#!/usr/bin/env python
from setuptools import setup


setup(
    name='django-amazon-price-monitor',
    description='Monitors prices of Amazon products via Product Advertising API',
    version=__import__('price_monitor').get_version().replace(' ', '-'),
    author='Alexander Herrmann & Martin Mrose',
    author_email='mrosemartin84@gmail.com',
    license='MIT',
    url='https://github.com/ponyriders/django-amazon-price-monitor',
    packages=['price_monitor'],
    long_description=open('README.md').read(),
    install_requires=[
        'Django>=1.5,<1.7',
        'python-amazon-simple-product-api==1.4.0',
        'celery>=3',
        'six'
    ],
    dependency_links=[
    ]
)
