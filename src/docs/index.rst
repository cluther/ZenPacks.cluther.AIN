ZenPacks.cluther.AIN
================================================

.. automodule:: ZenPacks.cluther.AIN

Usage
-----

After installing this ZenPack you can navigate to *Events* -> *Event Classes*
-> *Gear Menu* -> *Transform*. You'll find that the following code has been
inserted at the beginning of any existing transform you had configured::

    from ZenPacks.cluther.AIN import transforms
    transforms.add_ain_tag(dmd, evt)

This will result in the ``add_ain_tag`` method inside the ZenPack's
``transforms.py`` being called with a couple of parameters it needs to operate.
The ``add_ain_tag`` method can make modifications to the ``evt`` object which
will result in changes to the event that is being transformed.

How it Works
------------

The :py:class:`ZenPacks.cluther.AIN.ZenPack` class below contains all code
related to installing and removing the ZenPack.

.. autoclass:: ZenPacks.cluther.AIN.ZenPack
    :members:

The :py:mod:`ZenPacks.cluther.AIN.transforms` module below contains the code
that the global event transform will call to do more sophisticated event
transformation.

.. automodule:: ZenPacks.cluther.AIN.transforms
    :members:


Compatibility
-------------

This ZenPack is known to be compatible with the following Zenoss versions.

    * Zenoss 4.0, 4.1
    * Zenoss 3.0, 3.1, 3.2
    * Zenoss 2.5
