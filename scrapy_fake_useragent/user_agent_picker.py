# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import random
import logging

from fake_useragent import UserAgent
from fake_useragent.errors import FakeUserAgentError

import user_agents

logger = logging.getLogger(__name__)

def group_by_device_type(ua_source):
    '''group user agent by device type, only "desktop", "mobile", "tablet" are supported'''
    uas_by_device = {
        'desktop': {'randomize': []},
        'mobile': {'randomize': []},
        'tablet': {'randomize': []}
    }
    for browser_family, uas in ua_source.data_browsers.items():
        for ua in uas:
            parsed_ua = user_agents.parse(ua)
            if parsed_ua.is_pc:
                uas_key = 'desktop'
            elif parsed_ua.is_mobile:
                uas_key = 'mobile'
            elif parsed_ua.is_tablet:
                uas_key = 'tablet'
            else:
                continue

            uas_by_device[uas_key]['randomize'].append(ua)
            if browser_family in uas_by_device[uas_key]:
                uas_by_device[uas_key][browser_family].append(ua)
            else:
                uas_by_device[uas_key][browser_family] = [ua]

    return uas_by_device


class UserAgentPicker(object):
    '''
    Pick user agent by type
    '''
    def __init__(self, ua_type, per_proxy, fallback):
        self.ua_type = ua_type.split('.')
        self.per_proxy = per_proxy
        self.fallback = fallback
        self.proxy2ua = {}

        ua_source = UserAgent(cache=False, use_cache_server=False, fallback=fallback)
        if len(self.ua_type) > 1:
            self.uas = group_by_device_type(ua_source)
        else:
            self.uas = ua_source

    def get_ua(self, proxy=None):
        '''Gets random UA based on the type setting (random, firefox…)'''
        if proxy and proxy in self.proxy2ua:
            return self.proxy2ua[proxy]

        uas = self.uas
        for key in self.ua_type:
            try:
                uas = uas[key]
            except (KeyError, IndexError):
                uas = None

            if uas is None:
                if self.fallback is None:
                    raise FakeUserAgentError('Error occurred during getting browser')
                else:
                    logger.warning(
                        'Error occurred during getting browser for type "%s", '
                        'but was suppressed with fallback.',
                        '.'.join(self.ua_type)
                    )
                    return self.fallback

        ua = random.choice(uas) if isinstance(uas, list) else uas
        if proxy:
            self.proxy2ua[proxy] = ua

        return ua
