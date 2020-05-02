# _*_ coding:utf-8 _*_

class BookViewModel:
    def __init__(self,book):
        self.title = book['title']
        self.author = '、'.join(book['author'])
        self.binding = book['binding']
        self.publisher = book['publisher']
        self.image = book['image']
        self.price = '￥' + book['price'] if book['price'] else book['price']
        self.isbn=book['isbn']
        self.pubdate = book['pubdate']
        self.summary = book['summary']
        self.pages = book['pages']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        return '/'.join(intros)

class BookCollection:
    def __init__(self):
        self.total=0
        self.books=[]
        self.keyword=''

    def fill(self,yushu_book,keyword):
        self.total=yushu_book.total
        self.keyword=keyword
        self.books=[BookViewModel(book) for book in yushu_book.books]


# class BookViewModel:
#     @classmethod
#     def package_single(cls,data,keyword):
#         returned={
#             "book":[],
#             "total":0,
#             "keyword":keyword
#         }
#         if data:
#             returned['total']=1
#             returned['book']=[cls._cut_book_data(data)]
#         return returned
#     @classmethod
#     def package_collection(cls,data,keyword):
#         returned = {
#             "book": [],
#             "total": 0,
#             "keyword": keyword
#         }
#         if data:
#             returned['total'] = data['total']
#             returned['book'] = [cls._cut_book_data(book) for book in data['books']]
#         return returned
#     @classmethod
#     def _cut_book_data(cls,data):
#         book={
#             'title':data['title'],
#             'publisher':data['publisher'],
#             'pages':data['pages'] or '',
#             'price':data['price'],
#             'summary':data['summary'] or '',
#             'image':data['image'],
#             'author':'、'.join(data['author'])
#         }
#         return book
