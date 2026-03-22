******************************
Simple Django Personal website
******************************

Made on top of Django 5.x Framework and compatible with Django 4.x

.. image:: https://github.com/vstoykov/venko-django-site/actions/workflows/django.yml/badge.svg
    :target: https://github.com/vstoykov/venko-django-site/actions

.. image:: https://github.com/vstoykov/venko-django-site/actions/workflows/codeql-analysis.yml/badge.svg
    :target: https://github.com/vstoykov/venko-django-site/actions

It contains some basic reusable apps written by me. They are simple and maybe
not vary usefull for others. Maybe in the future I'll made more features.


Running Staging environmnet with Podman
========================================

Podman can play Kubernetes yaml files with the ``podman kube play`` command.
There is example ``kube-secrets-example.yaml``. From it you can create ``kube-secrets.yaml``
and use it to create the needed secrets in podman.

You can play both files like that:

.. code-block:: bash

    podman kube play --replace kube-secrets.yaml
    podman kube play --replace --publish=127.0.0.1:8080:8080 kube-deployment.yaml
