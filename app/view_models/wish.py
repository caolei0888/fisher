# _*_ coding:utf-8 _*_

from app.view_models.book import BookViewModel


class MyWishes:
    def __init__(self, wishes, gifts_count):
        self.my_wishes = []
        self.wishes = wishes
        self.gifts_count = gifts_count
        self.__parse()

    def __parse(self):
        for wish in self.wishes:
            count = 0
            for gift_count in self.gifts_count:
                if wish.isbn == gift_count['isbn']:
                    count = gift_count['count']
            r = {
                'wishes_count': count,
                'book': BookViewModel(wish.book),
                'id': wish.id
            }
            self.my_wishes.append(r)