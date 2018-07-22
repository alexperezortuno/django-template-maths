=====
Django Template Maths
=====

Django Template Maths is a simple filter for execute maths in template

Quick start
-----------

1. Add "django_template_maths" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_template_maths',
    ]

Example usage
-------------

```html
{% load django_template_maths %}

{{ 10|add:5 }} # print 15

{{ 10|sub:5 }} # print 5

{{ 10|div:5 }} # print 2

{{ 10|mul:5 }} # print 50

{{ 10|mod:5 }} # print 0

{{ 10|exp:5 }} # print 100000

{{ 10|flr:5 }} # print 2

{{ 10|sqr }}   # 3.1622776601683795

{{ 10|add:5|add_decimal:2 }} # print 15.00

{{ 1000|add:5|add_decimal:2|separator:'comma' }} # print 1,005.00

{{ 1000|add:5|add_decimal:2|separator:'dot' }} # print 1.005,00

```