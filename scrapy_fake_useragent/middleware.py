import logging

from scrapy_fake_useragent.user_agent_picker import UserAgentPicker

logger = logging.getLogger(__name__)

class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()

        fallback = crawler.settings.get('FAKEUSERAGENT_FALLBACK', None)
        per_proxy = crawler.settings.get('RANDOM_UA_PER_PROXY', False)
        ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')
        self.ua_picker = UserAgentPicker(ua_type, per_proxy, fallback)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        proxy = request.meta.get('proxy')
        if proxy:
            logger.debug('Proxy is detected %s', proxy)

        ua = self.ua_picker.get_ua(proxy)
        logger.debug('Assigned User-Agent %s', ua)
        request.headers.setdefault('User-Agent', ua)
