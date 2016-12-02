import requests
import time
from lxml import html


class Model(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{} = ({})'.format(k, v) for k, v in self.__dict__.items())
        return '\n<{}:\n  {}\n>'.format(class_name, '\n  '.join(properties))


class Movie(Model):
    def __init__(self):
        super(Movie, self).__init__()
        # 电影类有 4 个属性
        self.name = ''
        self.score = 0
        self.quote = ''
        self.message = ''


def movie_from_div(div):
    movie = Movie()
    movie.name = div.xpath('.//a[@class=""]')[0].text
    # movie.score = div.xpath('.//span[@class="rating_nums"]')[0].text
    movie.quote = div.xpath('.//span[@class="pl"]')[0].text
    movie.message = div.xpath('.//p[@class="pl"]')[0].text
    return movie


def movies_from_url(url):
    page = requests.get(url)
    root = html.fromstring(page.content)
    movie_divs = root.xpath('//div[@class="pl2"]')
    movies = [movie_from_div(div) for div in movie_divs]
    return movies


def save_covers(movies):
    for m in movies:
        download_img(m.cover_url, m.name + '.jpg')


def main():
    for i in range(392):
        url = 'https://movie.douban.com/tag/%E5%96%9C%E5%89%A7?start={}&type=T'.format(20 * i)
        movies = movies_from_url(url)
        print(movies)
        time.sleep(1)


if __name__ == '__main__':
    main()
