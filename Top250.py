import requests
from lxml import html
import time


class Model(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{} = ({})'.format(k, v) for k, v in self.__dict__.items())
        return '\n<{}:\n  {}\n>'.format(class_name, '\n  '.join(properties))


class Movie(Model):
    def __init__(self):
        super(Movie, self).__init__()
        self.ranking = 0
        self.cover_url = ''
        self.name = ''
        self.staff = ''
        self.publish_info = ''
        self.rating = 0
        self.number_of_comments = 0


def movie_from_div(div):
    movie = Movie()
    movie.ranking = div.xpath('.//div[@class="pic"]/em')[0].text
    movie.cover_url = div.xpath('.//div[@class="pic"]/a/img/@src')
    names = div.xpath('.//span[@class="title"]/text()')
    movie.name = ''.join(names)
    movie.rating = div.xpath('.//span[@class="rating_num"]')[0].text
    infos = div.xpath('.//div[@class="bd"]/p/text()')
    movie.staff, movie.publish_info = [i.strip() for i in infos[:2]]
    movie.number_of_comments = div.xpath('.//div[@class="star"]/span')[-1].text[:-3]
    return movie


def movies_from_url(url):
    page = requests.get(url)
    root = html.fromstring(page.content)
    movie_divs = root.xpath('//div[@class="item"]')
    movies = [movie_from_div(div) for div in movie_divs]
    return movies


def download_covers(movies):
    for m in movies:
        image_url = m.cover_url[0]
        r = requests.get(image_url)
        path = 'download/' + m.name.split('/')[0] + '.jpg'
        with open(path, 'wb') as f:
            f.write(r.content)


def main():
    for i in range(3):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(25 * i)
        movies = movies_from_url(url)
        print(movies)
        print(i)
        download_covers(movies)
        time.sleep(0.1)


if __name__ == '__main__':
    main()
