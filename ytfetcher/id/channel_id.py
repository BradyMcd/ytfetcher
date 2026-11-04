
from typing import Literal

PREFIX = r'^(?:https?://)?(?:www\.|m\.)?youtube\.com/'
H_CAP  = r'([\w.\-]+)'
UC_CAP = r'(UC[\w-]{22})'
class ChannelId(YoutubeId):
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

    def as_url(self):
        """Returns the Channel ID as a navigable URL"""
        return {'UC': f'https://www.youtube.com/channel/{self.id}',
                'user': f'https://www.youtube.com/user/{self.id}',
                'custom': f'https://www.youtube.com/c/{self.id}',
                '@': f'https://www.youtube.com/@{self.id}'
        }[self._tag]

    def as_tabbed_url(self, tab: Literal['videos', 'shorts', 'streams'] = 'videos'):
        """
        Returns the Channel ID as a navigable URL set to the given tab

        Args:
            tab (Literal): The channel tab to target.
                Options: 'videos', 'shorts', or 'streams'. Defaults to 'videos'.
        """
        return self.as_url() + '/' + tab 
