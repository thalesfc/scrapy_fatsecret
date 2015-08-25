from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import FormRequest, Request
import config
import logging
from scrapy_fatsecret.helpers import buddies
from scrapy_fatsecret.common_lib import deprecated


@deprecated
class LoginSpider(CrawlSpider):
    name = 'login_spider'
    allowed_domains = ['fatsecret.com']
    login_url = 'https://www.fatsecret.com/Auth.aspx?pa=s'
    start_urls = ['http://www.fatsecret.com/member/alphamares']

    rules = [
        Rule(
            LinkExtractor(allow='pa=memb', deny='(order=|pg=0)'),
            follow=True,
            callback=buddies.parse_buddy
        )
    ]

    def start_requests(self):
        return [
            FormRequest(
                self.login_url,
                formdata={
                    'ctl00$ctl07$Logincontrol1$Name': config.GMAIL_USER,
                    'ctl00$ctl07$Logincontrol1$Password': config.PASSWORD,
                    '__EVENTTARGET': 'ctl00$ctl07$Logincontrol1$Login',
                },
                callback=self.after_login
            )
        ]

    def after_login(self, response):
        if response.url == 'https://www.fatsecret.com/Default.aspx?pa=m':
            self.log('Successfully LOGGED.', logging.INFO)
            return [Request(url=u) for u in self.start_urls]
        else:
            self.log('LOGIN error: ' + response.url, logging.CRITICAL)
