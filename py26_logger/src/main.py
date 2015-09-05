#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python2.6+ compatible logging setup module to be used as point-of-entry to a
program."""

import os
import optparse
import logging
import logging.config

import example_package.example_module
# We imported example_module before setting logging configuration.
# This can cause issues, see the module for explanation.

def parse_cli_args():
    """Parse command line args.  Additional options can be added."""
    parser = optparse.OptionParser()
    parser.add_option('-v', '--verbose', dest="verbose",
                      action='count', default=0,
                      help='increase debug logging level')

    return parser.parse_args()

def load_logging_conf(log_cfg_filename):
    """Find/load logging configuration at '../logs/<filename>' (os agnostic)."""
    log_cfg_dir = 'logs'
    par_cfg_dir = os.pardir
    rel_cfg_dir = os.sep.join((par_cfg_dir, log_cfg_dir, log_cfg_filename))
    abs_cfg_dir = os.path.abspath(rel_cfg_dir)

    logging.config.fileConfig(abs_cfg_dir)

def set_debug_verbosity(verbosity_counter):
    """Deactivates the debug handler if verbosity_counter is 0, else sets
    the logging level appropriately."""

    debug_handler = logging.root.handlers[1]

    if verbosity_counter == 0:
        logging.root.removeHandler(debug_handler)
    elif verbosity_counter == 1:
        debug_handler.level = logging.INFO
    elif verbosity_counter == 2:
        debug_handler.level = logging.DEBUG
    else:
        debug_handler.level = logging.NOTSET

if __name__ == '__main__':
    opts, args = parse_cli_args()

    load_logging_conf('logging.conf')
    # All loggers MUST be started AFTER this point, including for imported modules!

    set_debug_verbosity(opts.verbose)

# Start the logger for this module.
log = logging.getLogger(__name__)

log.debug('test debug message')
log.info('test info message')
log.warn('test warn message')
log.error('test error message')
log.critical('test critical message')

example_package.example_module.do_stuff()
