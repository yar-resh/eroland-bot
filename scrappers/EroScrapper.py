from abc import ABC, abstractmethod


class EroScrapper(ABC):
    """
    An interface for scrappers
    """

    @abstractmethod
    def get_images(self, *args):
        """
        Returns collection of urls depending on passed commands
        :param args: commands
        :return: collection of urls
        """

    @property
    @abstractmethod
    def commands(self):
        """
        :return: collection of available commands that uses for scrapping
        """
    @abstractmethod
    def get_instruction(self):
        """
        Returns instruction based on available commands
        :return:
        """

    @property
    @abstractmethod
    def scrapper_name(self):
        """
        Returns scrapper name
        :return:
        """

    @property
    @abstractmethod
    def identifier(self):
        """
        Returns identifier that will be use to generate bot's coommands
        :return:
        """
