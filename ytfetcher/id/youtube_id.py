# youtube_id.py - handles the extraction of IDs from URLs across Youtube

import re
from abc import ABC, abstractmethod
from typing import Dict, Literal

PREFIX = r'^(?:https?://)?(?:www\.|m\.)?youtube\.com/'

class BaseYoutubeId:
    """
    Base class for storing Youtube IDs and their conversion to and from URLs
    """
    def __init__(self, str_in: str, patterns: list[Dict[str,str]]):
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
    def as_url(self) -> str:
        """Abstract method to be implemented by subclasses"""
        pass


H_CAP  = r'([\w.\-]+)'
UC_CAP = r'(UC[\w-]{22})'

class ChannelId(BaseYoutubeId):
    """
    A ChannelId is responsible for parsing channel IDs from URLs and properly formatting
    those IDs for fetching.
    """

    _PATTERNS = [
        {'re': re.compile(PREFIX + r'channel/' + UC_CAP + r'(?:[/?#]|$)', re.I),
         'tag': 'UC'},
        {'re': re.compile(PREFIX + r'user/' + H_CAP, re.I),
         'tag': 'user'},
        {'re': re.compile(PREFIX + r'c/' + H_CAP, re.I),
         'tag': 'custom'},
        {'re': re.compile(PREFIX + r'(?:@)' + H_CAP, re.I),
         'tag': '@'},
        {'re': re.compile(r'^' + UC_CAP + r'$'),
         'tag': 'UC'},
        # Note: We assume any bare string is an @ handle.
        {'re': re.compile(r'^@?' + H_CAP + r'$'), 
         'tag': '@'}
    ]
    
    def __init__(self, str_in: str):
        """
        Initialize a ChannelId.

        Args:
            str_in (str): The user input string, either an @handle, UC code
                or any URL linking to a channel (including custom c/ and user/ paths).
        """
        try:
            self.super(str_in, ChannelId._PATTERNS)
        except Exception:
            raise ChannelFetchError(f"Could not extract channel handle from URL: {str_in}")

    def as_url(self) -> str:
        """Returns the Channel ID as a navigable URL"""
        return {'UC': f'https://www.youtube.com/channel/{self.id}',
                'user': f'https://www.youtube.com/user/{self.id}',
                'custom': f'https://www.youtube.com/c/{self.id}',
                '@': f'https://www.youtube.com/@{self.id}'
        }[self._tag]

    def as_tabbed_url(self, tab: Literal['videos', 'shorts', 'streams'] = 'videos') -> str:
        """
        Returns the Channel ID as a navigable URL set to the given tab

        Args:
            tab (Literal): The channel tab to target.
                Options: 'videos', 'shorts', or 'streams'. Defaults to 'videos'.
        """
        return self.as_url() + '/' + tab 
