import requests
from lxml import html


class Model(object):
    def __str__(self):
        class_name = self.__class__.__name__
        properties = (u'{0} = ({1})'.format(k, v) for k, v in self.__dict__.items())
        r = u'\n<{0}:\n  {1}\n>'.format(class_name, u'\n  '.join(properties))
        return r


class Answer(Model):
    def __init__(self, path='', title='', date='', content='', vote_count=0):
        super(Answer, self).__init__()
        self.html = str(content)


def answer_from_node(node):
    link = node.xpath('.//a[@class="answer-date-link meta-item"]')
    if len(link) > 0:
        link = link[0]
        path = link.attrib['href']
        date = link.text
        title = node.xpath('.//a[@class="question_link"]/text()')[0]
        content = node.xpath('.//textarea[@class="content"]/text()')[0]
        vote_count = node.xpath('.//div[@class="zm-item-vote"]/a/text()')[0]
        a = Answer(path, title, date, content, vote_count)
    else:
        a = Answer()
    return a


url_likaifu = 'https://www.zhihu.com/people/kaifulee/answers?page=1'
cookie = '_za=15ccc36a-a228-4f3c-85b9-e8c69bf36d13; d_c0="AFBAGqGLKQqPTpoMlgy7XvC0_vgl5kUFiSA=|1467366758"; q_c1=52eb1a721ba14d53893cb08e3e6ff8dd|1467366758000|1467366758000; l_cap_id="YTMzYjA2ZWU3NzMzNDFiZWIwOGZiY2NmODZmYTQwZTA=|1467368407|a190716417e70142e565eaf0cae0c1cbdf33c7d7"; cap_id="MDA5ZTViYTE4OWRlNGY5MmI1NmRkOTM4ODc3NGYyMWQ=|1467368407|fd63386bcb635b8c4149f011a8bbde16fb7b9030"; _zap=a1199359-ac2f-464b-af72-980219a145fb; login="YjViNWQwZTI0Y2I4NDBiNmFhZDM1OTI2NTU5N2FjMTc=|1467368421|4f57ca4132bb9e6d3abb3fb858e44cf05b784e78"; z_c0=Mi4wQUtDQ3VPQ1Jod2NBVUVBYW9Zc3BDaGNBQUFCaEFsVk41ZENkVndETm1ORGV1YXluZDg0a3k2UEpUdTQwaXV2WWRR|1467368422|736e49d24407703d7448b5773e7790ffcf9e7d5a; _xsrf=288f38997530ffd42bccdb694bd8772a; __utma=51854390.681005669.1467384885.1467384885.1467384885.1; __utmz=51854390.1467384885.1.1.utmcsr=baidu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100-1|2=registration_date=20150125=1^3=entry_date=20150125=1; a_t="2.0AKCCuOCRhwcXAAAAWy2sVwCggrjgkYcHAFBAGqGLKQoXAAAAYQJVTeXQnVcAzZjQ3rmsp3fOJMujyU7uNIrr2HW-n6uvfNdkizLgeRaHxybzzOkVew=="; s-q=likaifu; s-i=5; sid=15ol3d9g; s-t=autocomplete'

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
headers = {
    'Cookie': cookie,
    'User-Agent': useragent,
}
r = requests.get(url_likaifu, headers=headers)
root = html.fromstring(r.text)
items = root.xpath('//div[@class="zm-item"]')
answers = [answer_from_node(item) for item in items]
print(answers[0])
