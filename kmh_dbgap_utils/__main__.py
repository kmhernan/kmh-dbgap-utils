"""Main entrypoint to kmh-dbgap-utils."""
import argparse
import datetime
import sys

from kmh_dbgap_utils.logger import Logger
from kmh_dbgap_utils.subcommands.extract_data_dict import ExtractDataDict
from kmh_dbgap_utils.subcommands.extract_var_report import ExtractVariableReport


def main(args=None):
    """
    The main entrypoint for all tools.
    """
    # Setup logger
    Logger.setup_root_logger()

    logger = Logger.get_logger("main")

    # Print header
    logger.info('-'*75)
    logger.info("Program Args: kmh-dbgap-utils " + " ".join(sys.argv[1::]))
    logger.info('Date/time: {0}'.format(datetime.datetime.now()))
    logger.info('-'*75)
    logger.info('-'*75)

    # Get args
    p = argparse.ArgumentParser("KMH dbGap Helpers")
    subparsers = p.add_subparsers(dest="subcommand")
    subparsers.required = True

    ExtractDataDict.add(subparsers=subparsers)
    ExtractVariableReport.add(subparsers=subparsers)

    options = p.parse_args(args)

    # Run
    options.func(options) 

    # Finish
    logger.info("Finished!")

if __name__ == '__main__':
    main()
