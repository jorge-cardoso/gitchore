import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class Parser(ABC):
    """
    The Parser interface declares operations common to all supported parsers for projects.
    """

    @abstractmethod
    def get_dict(self) -> dict:
        raise NotImplementedError('Methods was not implemented')

    def name(self) -> str:
        raise NotImplementedError('Methods was not implemented')

    def overview(self) -> dict:
        raise NotImplementedError('Methods was not implemented')

    def description(self) -> dict:
        raise NotImplementedError('Methods was not implemented')

    def milestones(self) -> dict:
        raise NotImplementedError('Methods was not implemented')

    def tasks(self) -> dict:
        raise NotImplementedError('Methods was not implemented')

    def sprints(self) -> dict:
        raise NotImplementedError('Methods was not implemented')

    def results(self) -> dict:
        raise NotImplementedError('Methods was not implemented')


class Context:
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, parser: Parser) -> None:
        """
        Context accepts a parser through the constructor
        """

        self._parser = parser

    @property
    def parser(self) -> Parser:
        """
        The Context maintains a reference to one of the Parser objects. The
        Context does not know the concrete class of a parser. It should work
        with all strategies via the Parser interface.
        """

        return self._parser

    @parser.setter
    def parser(self, parser: Parser) -> None:
        """
        The Context allows replacing a Parser object at runtime.
        """

        self._parser = parser

    def __getattr__(self, attr):
        """
        The Context delegates functions executions to the implementions available
        """
        return getattr(self._parser, attr)

