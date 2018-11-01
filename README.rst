========
Overview of stuffs
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/habitica-challenge-manager/badge/?style=flat
    :target: https://readthedocs.org/projects/habitica-challenge-manager
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/MathWhiz/habitica-challenge-manager.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/MathWhiz/habitica-challenge-manager

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/MathWhiz/habitica-challenge-manager?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/MathWhiz/habitica-challenge-manager

.. |requires| image:: https://requires.io/github/MathWhiz/habitica-challenge-manager/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/MathWhiz/habitica-challenge-manager/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/MathWhiz/habitica-challenge-manager/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/MathWhiz/habitica-challenge-manager

.. |version| image:: https://img.shields.io/pypi/v/habitica-challenge-manager.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/habitica-challenge-manager

.. |commits-since| image:: https://img.shields.io/github/commits-since/MathWhiz/habitica-challenge-manager/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/MathWhiz/habitica-challenge-manager/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/habitica-challenge-manager.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/habitica-challenge-manager

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/habitica-challenge-manager.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/habitica-challenge-manager

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/habitica-challenge-manager.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/habitica-challenge-manager


.. end-badges

Allows for downloading, generating, and creating Habitica Challenges.

* Free software: MIT license

Installation
============

::

    pip install habitica-challenge-manager

Documentation
=============

https://habitica-challenge-manager.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
