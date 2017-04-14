=============================
django_lazifier
=============================

.. image:: https://badge.fury.io/py/django-lazifier.svg
    :target: https://badge.fury.io/py/django-lazifier

.. image:: https://travis-ci.org/hotmit/django-lazifier.svg?branch=master
    :target: https://travis-ci.org/hotmit/django-lazifier

.. image:: https://codecov.io/gh/hotmit/django-lazifier/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/hotmit/django-lazifier

Create a semi scaffolding and other helper methods.

Documentation
-------------

The full documentation is at https://django-lazifier.readthedocs.io.

Quickstart
----------

Install django_lazifier::

    pip install django-lazifier

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_lazifier.apps.DjangoLazifierConfig',
        ...
    )

Add django_lazifier's URL patterns:

.. code-block:: python

    from django_lazifier import urls as django_lazifier_urls


    urlpatterns = [
        ...
        url(r'^', include(django_lazifier_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
