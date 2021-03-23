from scrapy.crawler import CrawlerProcess
import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://www.zyte.com/blog/']
    def __init__(self,data):
        self.data=data
    def parse(self, response):
        print(response)
        # for title in response.css('.oxy-post-title'):
        #     yield {'title': title.css('::text').get()}

        # for next_page in response.css('a.next'):
        #     yield response.follow(next_page, self.parse)


if __name__=="__main__":
    spider=BlogSpider()
    crawler= CrawlerProcess()
    data=[]

    #Parseado=spider.parse()
    crawler.crawl(spider, data)
    crawler.start()
    
