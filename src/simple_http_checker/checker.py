import logging
import requests
from typing import Collection

logger = logging.getLogger(__name__)


def check_urls(urls: Collection[str], timeout: int = 5) -> dict[str, str]:
    """
    Check a list of URLs for their status codes.

    Args:
        urls (list[str]): A list of URLs to check.
        timeout (int, optional): The timeout in seconds for each request. Defaults to 5.

    Returns:
        dict[str, str]: A dictionary mapping each URL to its status code.
    """

    logger.info(
        f"Starting check for {len(urls)} URLS with a timeout of {timeout} seconds"
    )
    results: dict[str, str] = {}
    for url in urls:
        status = "UNKNOWN"
        try:
            logger.debug(f"Checking URL: {url}")
            response = requests.get(url, timeout=timeout)
            if response.ok:
                status = f"{response.status_code} OK"
            else:
                status = f"{response.status_code} {response.reason}"
        except requests.exceptions.Timeout:
            status = "TIMEOUT"
            logger.warning(f"Request to {url} timed out.")
        except requests.exceptions.ConnectionError:
            status = "CONNECTION ERROR"
            logger.error(f"Connection error for {url}.")
        except requests.exceptions.RequestException as e:
            status = f"REQUEST_ERROR {type(e).__name__}"
            logger.error(
                f"An unexpected request error occurred for{url}:{e}", exc_info=True
            )
        results[url] = status
        logger.debug(f"Checked: {url:<40} {status}")
    logger.info("Check completed")
    return results
