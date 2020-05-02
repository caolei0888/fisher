# _*_ coding:utf-8 _*_
from flask import jsonify, request, render_template,flash
from flask_login import current_user

from app.forms.book import SearchForm
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo
from app.web import web
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
import json



#blueprint
@web.route('/book/search')
def search():
    '''
    q:关键字或isbn
    page
    '''
    #导入快捷键alt+enter
    form=SearchForm(request.args)
    books=BookCollection()

    if form.validate():
        q=form.q.data.strip()
        page=form.page.data
        isbn_or_key=is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key=='isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q,page)

        books.fill(yushu_book,q)


    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
        #return jsonify(form.errors)
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts=False
    has_in_wishes=False
    yushu_book=YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id,isbn=isbn,launched=False).first():
            has_in_gifts=True
        if Wish.query.filter_by(uid=current_user.id,isbn=isbn,launched=False).first():
            has_in_wishes=True
    trade_gifts=Gift.query.filter_by(isbn=isbn,launched=False).all()
    trade_wishes=Wish.query.filter_by(isbn=isbn,launched=False).all()

    trade_gifts_model=TradeInfo(trade_gifts)
    trade_wishes_model=TradeInfo(trade_wishes)
    return render_template('book_detail.html',book=book,wishes=trade_wishes_model,
                           gifts=trade_gifts_model,has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes)


# @web.route('/test')
# def test():
#     r={
#         'name':'七月7日',
#         'age': 19
#     }
#     flash("hello,七月",category="error")
#     flash("hello,九月",category='warning')
#     return render_template('layout.html',data=r)