######################################################################
#
# Copyright 2011 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

"""
External event transform code lives here. This keeps logic that shouldn't be
touched in the web interface from being accessible. Another benefit to this
approach is the better flow control allowed in normal functions rather than
exec code. It is also far easier to unit test this code than event transforms
that exist in the object database.
"""

import logging
LOG = logging.getLogger('zen.AIN')

import os
import time

from Products.ZenUtils.Utils import zenPath

# How often the ain_rules.py file will be reloaded (in seconds.)
RELOAD_FREQUENCY = 60


def get_ain_rules(dmd):
    """Get the AIN rules.

    Only reloads from file once per minute. Once the rules are loaded they are
    stored in a volatile (non-persistent) property of ``dmd``.
    """
    last_ain_rules_load = getattr(dmd, '_v_last_ain_rules_load', 0)

    if last_ain_rules_load > (time.time() - RELOAD_FREQUENCY):
        return getattr(dmd, '_v_ain_rules', [])
    else:
        rules = []

        rules_filename = zenPath('etc', 'ain_rules.py')
        if os.path.isfile(rules_filename):
            LOG.info("Reloading AIN rules from %s", rules_filename)
            try:
                rules_file = open(rules_filename, 'r')
                for line in rules_file:
                    rule_wo_comment = line.split('#')[0].strip()
                    if rule_wo_comment != '':
                        rules.append(rule_wo_comment)

                rules_file.close()
            except Exception:
                LOG.exception("Error loading AIN rules from %s", rules_filename)

        else:
            LOG.info("No AIN rules file found at %s", rules_filename)

        # Store rules as a volatile property on dmd.
        dmd._v_ain_rules = rules
        dmd._v_last_ain_rules_load = time.time()

        return rules


def add_ain_tag(dmd, evt):
    """Add "AIN:" prefix to event summary and message.

    Periodically processes $ZENHOME/etc/ain_rules.py for rules. Evaluates the
    list of rules in order like a firewall ruleset for the event passed into
    this method and adds an "AIN:" prefix to the summary and message fields
    if one of the rules matches.
    """
    ain = None

    for rule in get_ain_rules(dmd):
        exec_context = {'evt': evt, 'retVal': False, 'ain': None}
        rule = '%s; retVal = True' % rule

        try:
            exec(rule, exec_context)
        except Exception:
            LOG.exception(">>> FIXME! <<< Rule malformed: %s", rule)

        if exec_context['retVal'] == True:
            ain = exec_context.get('ain', None)

            # Stop evaluating rules once we get a match.
            break

    if ain == None:
        evt.summary = 'AIN:XXXXX %s' % evt.summary
        evt.message = 'AIN:XXXXX %s' % evt.message
    else:
        evt.summary = 'AIN:%s %s' % (ain, evt.summary)
        evt.message = 'AIN:%s %s' % (ain, evt.message)
