from abc import ABC, abstractclassmethod


class EroScrapper(ABC):
    """
    An interface for scrappers
    """

    @abstractclassmethod
    def get_images(self, *args):
        """
        Returns collection of urls depending on passed commands
        :param args: commands
        :return: collection of urls
        """

    @property
    @abstractclassmethod
    def commands(self):
        """
        :return: collection of available commands that uses for scrapping
        """
    @abstractclassmethod
    def get_instruction(self):
        """
        Returns instruction based on available commands
        :return: str
        """

    @property
    @abstractclassmethod
    def scrapper_name(self):
        """
        Returns scrapper name
        :return:
        """

    @property
    @abstractclassmethod
    def identifier(self):
        """
        Returns identifier that usees for generate command for using concrete scrapper
        :return:
        """
