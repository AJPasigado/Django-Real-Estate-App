subtemplate/real-estate
=======================

Getting Started
---------------

Prerequisites
~~~~~~~~~~~~~
- `Python 2.7.14 <https://www.python.org/downloads/release/python-2714/>`_
- `Elasticsearch 5.6.9 <https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.9.zip>`_

Set-up
~~~~~~

**1. Install the dependencies** using `pip <https://pip.readthedocs.io/en/latest/quickstart.html>`_. In the terminal,

::

   pip install -r requirements/vanila.json

**2. Create the database**,

::

   python manage.py migrate

**3. Populate the database using fixtures.** There are two fixture files: ``fixtures/vanilla.json`` and ``fixtures/populated.json``. Loading ``vanilla.json`` will only populate the database with the core pages needed for the real estate app. Loading ``populated.json`` will populate the database with the core pages and sample real estate data.
    
    **3a. To populate the database with only the core pages**,
    
    ::
    
       python manage.py loaddata fixtures/vanilla.json
    
    **3b. To populate the database with core pages and sample data**,
    ::
    
       python manage.py loaddata fixtures/populated.json
       python fixtures/realestatedump.py load


**4. Create a superuser**

::

   python manage.py createsuperuser

How the pages work
------------------

Listing
~~~~~~~

Catalog
~~~~~~~

CatalogIndex
~~~~~~~~~~~~

.. _Python 2.7.14: https://www.python.org/downloads/release/python-2714/
.. _Elasticsearch 5.6.9: https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.9.zip
.. _pip: https://pip.readthedocs.io/en/latest/quickstart.html
