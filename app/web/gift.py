from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.dirft import Drift
from app.models.gift import Gift
from app.view_models.gift import MyGifts
from . import web

__author__ = '七月'


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid=current_user.id
    gifts_of_mine=Gift.get_user_gifts(uid)
    isbn_list=[gift.isbn for gift in gifts_of_mine]
    wish_count_list=Gift.get_wish_counts(isbn_list)
    view_model=MyGifts(gifts_of_mine,wish_count_list)
    return render_template('my_gifts.html',gifts=view_model.my_gifts)




@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        # try:
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
        #     db.session.commit()
        # except Exception as e:
        #     db.session.rollback()
        #     raise e
    else:
        flash('这本书已添加至你的赠送清单或已存在你的心愿清单，请不要重复添加')

    return redirect(url_for('web.book_detail',isbn=isbn))

@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first()
    if not gift:
        flash('该书籍不存在，或已经交易，删除失败')
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash('这个礼物正处于交易状态，请先前往鱼漂完成该交易')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))
