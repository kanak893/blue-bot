import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.error import HTTPError
from googlesearch import search
from simple_settings import settings
from utilities.logger import Logger

logger = Logger().get_logger()


class GoogleSearch:

    @classmethod
    def search(cls, query, num=5, tld="co.in"):
        """
        Function used to retrieve google query results.
        """
        try:
            # searching for query on google search.
            search_result = search(query, tld=tld, num=5, stop=5)
            results = list(search_result)
            new_line_separated_results = "\n".join(results)
            return new_line_separated_results
        except Exception as e:
            logger.error(str(e))


if __name__ == "__main__":
    x = GoogleSearch().search(query="nodejs")
    print(x)
