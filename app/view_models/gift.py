# _*_ coding:utf-8 _*_


from collections import namedtuple

# MyGift = namedtuple('MyGift', ['wishes_count', 'book', 'id'])
from app.view_models.book import BookViewModel


class MyGifts:
    def __init__(self, gifts, wishes_count):
        self.my_gifts = []
        self.gifts = gifts
        self.wishes_count = wishes_count
        self.__parse()

    def __parse(self):
        for gift in self.gifts:
            count = 0
            for wish_count in self.wishes_count:
                if gift.isbn == wish_count['isbn']:
                    count = wish_count['count']
            r = {
                'wishes_count': count,
                'book': BookViewModel(gift.book),
                'id': gift.id
            }
            self.my_gifts.append(r)







