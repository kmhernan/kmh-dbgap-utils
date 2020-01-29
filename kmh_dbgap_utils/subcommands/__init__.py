"""
Abstract base class for all subcommands in kmh-dbgap-utils. 
"""
from abc import ABCMeta, abstractmethod

class Subcommand(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def __add_arguments__(cls, parser):
        """Add the arguments to the parser"""

    @classmethod
    def __get_description__(cls):
        """
        Optionally returns description
        """
        return None

    @classmethod
    def __tool_name__(cls):
        """
        Tool name to use for the subparser
        """
        return cls.__name__.lower()


    @classmethod
    @abstractmethod
    def main(cls, options):
        """
        Main entry point.
        """

    @classmethod
    def add(cls, subparsers):
        """Adds the given subcommand to the subprsers."""
        subparser = subparsers.add_parser(
            name=cls.__tool_name__(),
            description=cls.__get_description__())

        cls.__add_arguments__(subparser)
        subparser.set_defaults(func=cls.main)
        return subparser
