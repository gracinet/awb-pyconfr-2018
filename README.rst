Slides for pycon.fr 2018
========================

This are slides of my presentation about Anyblok / WMS Base for the
pycon.fr 2018 conference (2018-10-06).

Of course, since pycon.fr is the annual gathering of the *french
speaking* Pythonistas, these are entirely written in french.

If you're looking for the revision actually projected at the event,
this was or will be the ``pycon.fr-2018`` tag.

How to generate and watch
-------------------------

- install hovercraft with python3::

    python3 -m venv hoverenv
    hoverenv/bin/pip install hovercraft

- run hovercraft::

    hoverenv/bin/hovercraft prez.rst

- open http://localhost:8000 in your favorite web browser

How to install and run the examples
-----------------------------------
Minimal set of steps

- create a virtualenv::

    python3 -m venv venv

- install the demo project::

    pip install -e wms_demo

- have a running PostgreSQL cluster and run the following commands as
  a user that's bound to a PostgreSQL user (role) that has the right
  to create a database.
- create the database and install the provided demo blok in the database::

    venv/bin/anyblok_createdb -c demo.cfg

- add some data for the examples (french version)::

    venv/bin/add_data -c demo.cfg

- Translate the data to english if you wanna try the examples from the
  english version of the talk::

    venv/bin/translate_en -c demo.cfg

- Play with it::

    venv/bin/anyblok_interpreter -c demo.cfg

Credits
-------

Thanks to Lennart Regebro and to the impress.js developers.
