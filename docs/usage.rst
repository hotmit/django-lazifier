=====
Usage
=====

To use django_lazifier in a project, add it to your `INSTALLED_APPS`:

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
