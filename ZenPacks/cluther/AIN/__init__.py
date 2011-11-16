######################################################################
#
# Copyright 2011 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

"""
This ZenPack demonstrates how event transforms can call out to external code
delivered through a ZenPack. Having transform code be external has the
following advantages.

    * Prevents users from easily or accidentally changing your logic.
    * Allows full Python usage instead of only *exec*.
    * Easier unit testing of transform logic.

However, having your transform logic be in code instead of the object database
does have a disadvantage. You can't change the code on the fly without
restarting portions of Zenoss. You will at least need to restart the *zenhub*
daemon after changing your transform code that lives in a .py file as this is
where transforms are executed.
"""

import logging
LOG = logging.getLogger('zen.AIN')

# The following imports are only here to support documentation generation.
import Globals
from Products.ZenUtils.Utils import unused
unused(Globals)

from Products.ZenModel.ZenPack import ZenPackBase


class ZenPack(ZenPackBase):
    """
    Custom ``ZenPack`` subclass that allows us to override the ``install`` and
    ``remove`` behavior of the ZenPack.
    """

    def install(self, app):
        """Override standard ZenPack install to provide custom install logic.

        After calling the standard ZenPack install method from our superclass
        we call our local ``install_*`` methods.
        """
        super(ZenPack, self).install(app)
        self.install_ain_transform(app.zport.dmd)

    def remove(self, app, leaveObjects=False):
        """Override standard ZenPack remove to provide custom remove logic.

        If the ZenPack is being removed, and not upgraded, we call our local
        ``remove_*`` methods. Then we call the standard ZenPack remove method
        from our superclass.
        """
        if not leaveObjects:
            self.remove_ain_transform(app.zport.dmd)

        super(ZenPack, self).remove(app, leaveObjects=leaveObjects)

    def install_ain_transform(self, dmd):
        """Insert our callout code into the global event transform."""
        if 'ZenPacks.cluther.AIN' not in dmd.Events.transform:
            LOG.info('Adding AIN tagging to global event transform')
            dmd.Events.transform = '\n'.join([
                'from ZenPacks.cluther.AIN import transforms',
                'transforms.add_ain_tag(dmd, evt)',
                '',
                dmd.Events.transform
                ])
        else:
            LOG.info('AIN tagging already present in global event transform')

    def remove_ain_transform(self, dmd):
        """Remove our callout code from the global event transform."""
        if 'ZenPacks.cluther.AIN' in dmd.Events.transform:
            LOG.info('Removing AIN tagging from global event transform')
            cleaned_transform = []
            for line in dmd.Events.transform.split('\n'):
                if 'ZenPacks.cluther.AIN' in line:
                    continue
                elif 'add_ain_tag' in line:
                    continue
                else:
                    cleaned_transform.append(line)

            dmd.Events.transform = '\n'.join(cleaned_transform)
        else:
            LOG.info('AIN tagging not present in global event transform')
