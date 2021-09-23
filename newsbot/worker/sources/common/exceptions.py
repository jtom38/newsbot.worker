
class UnableToFindContent(Exception):
    """
    Used when failure to return results from a scrape request.
    """
    pass


class UnableToParseContent(Exception):
    """
    This is used when a failure happens on parsing the content that came back from requests.
    Could be malformed site, or just not what was expected.
    """
    pass


class FailedToFindHtmlObject(Exception):
    """Raised when a failure happens trying to find an object that is expected to be on the page"""


class MissingSourceID(Exception):
    """
    This is raised when the source reaches out to the API to find what should be an active record, but does not find a record.
    """
