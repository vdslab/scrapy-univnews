import datetime
import feedparser
import scrapy


class NewsSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        universities = [
            '早稲田大学',
            '慶應大学',
            '上智大学',
            '国際基督教大学',
            '明治大学',
            '立教大学',
            '青山学院大学',
            '中央大学',
            '法政大学',
            '学習院大学',
            '成蹊大学',
            '明治学院大学',
            '成城大学',
            '武蔵大学',
            '國學院大學',
            '獨協大学',
            '東洋大学',
            '日本大学',
            '専修大学',
            '駒澤大学',
        ]
        for university in universities:
            start_date = datetime.date(2017, 1, 1)
            end_date = datetime.date(2021, 12, 31)
            t0 = start_date
            while t0 <= end_date:
                t = t0 + datetime.timedelta(days=1)
                after = t0.strftime('%Y-%m-%d')
                before = t.strftime('%Y-%m-%d')
                url = 'https://news.google.com/rss/search?hl=ja&gl=JP&ceid=JP:ja'\
                    f'&q={university}+after:{after}+before:{before}'
                yield scrapy.Request(url=url, callback=self.parse_feed,
                                     meta={'university': university})
                t0 = t

    def parse_feed(self, response):
        d = feedparser.parse(response.body)
        for item in d.entries:
            yield {
                'id': item.id,
                'title': item.title,
                'link': item.link,
                'description': item.description,
                'published': item.published,
                'university': response.meta['university']
            }
