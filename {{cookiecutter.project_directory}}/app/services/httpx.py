import requests
from loguru import logger
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dependency_injector import resources

RAISE_STATUS = [500, 501, 502]
RETRY_TIMEOUT = 5
RETRY_ATTEMPTS = 3


class TimeoutHTTPAdapter(HTTPAdapter):
    default_timeout = 5

    def __init__(self, *args, **kwargs):
        self.timeout = TimeoutHTTPAdapter.default_timeout
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


class RequestClient(resources.Resource):
    def init(
        self,
    ) -> requests.Session:
        logger.info("--- Request client startup ---")
        _retry_strategy = Retry(
            total=RETRY_ATTEMPTS, status_forcelist=RAISE_STATUS, backoff_factor=1
        )
        _adapter = TimeoutHTTPAdapter(
            max_retries=_retry_strategy, timeout=RETRY_TIMEOUT
        )
        client = requests.Session()
        client.mount("https://", _adapter)
        client.mount("http://", _adapter)
        return client

    def shutdown(self, client: requests.Session) -> None:
        logger.info("--- Request client shutdown ---")
        client.close()


class RequestHandler:
    def __init__(self, request_client: requests.Session):
        self._request_client = request_client
