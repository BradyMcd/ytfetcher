
import re
from typing import


class YoutubeId:
    """
    Base class for storing Youtube IDs and their conversion to and from URLs
    """
    def __init__(self, str_in: str, patterns: list[dict[str,str]]):
        """
        Initialize the ID packet by applying regular expression patterns to the
        input strings.

        Args:
            str_in (str):         An input string, either URL or plain ID.
            patterns (list[dict]): A list of regular expression patterns to match IDs
                                   against paired with a tag for URL building logic.
        """
        for pat in patterns:
            id = re.search(pat['re'], str_in)
            if id.match:
                self.id = id.match
                self.tag = pat['tag']
                return
        raise

    @abstractmethod
    def as_url(self):
        """Abstract method to be implemented by subclasses"""
        pass
