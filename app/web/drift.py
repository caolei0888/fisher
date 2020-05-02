from flask import flash, redirect, url_for, render_template, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from app.forms.book import DriftForm
from app.libs.email import send_mail
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.dirft import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftCollection
from . import web

__author__ = '七月'


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift=Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash("书籍是你自己的，不能像自己索要")
        return redirect(url_for('web.book_detail',isbn=current_gift.isbn))
    can=current_user.can_send_drift()
    if not can:
        return render_template('not_enough_beans.html',beans=current_user.beans)
    form=DriftForm(request.form)
    if request.method=="POST" and form.validate():
        save_drift(form,current_gift)
        send_mail(current_gift.user.email, '有人想要一本书', 'email/get_gift.html',
                              wisher=current_user,
                              gift=current_gift)
        return redirect(url_for('web.pending'))
    gifter=current_gift.user.summary
    return render_template('drift.html',gifter=gifter,user_beans=current_user.beans,form=form)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id,
            Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()
    view_model = DriftCollection(drifts,current_user.id)
    views=view_model.data
    return render_template('pending.html', drifts=views)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(Gift.uid == current_user.id,
                                   Drift.id == did).first_or_404()
        drift.pending = PendingStatus.Reject
        # 当收到一个请求时，书籍不会处于锁定状态, 也就是说一个礼物可以收到多个请求
        requester= User.query.filter_by(id=drift.requester_id).first_or_404()
        requester.beans+=1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    with db.auto_commit():
        # requester_id = current_user.id 这个条件可以防止超权
        # 如果不加入这个条件，那么drift_id可能被修改
        drift = Drift.query.filter_by(requester_id = current_user.id,id=did).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans +=1
        # gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        # gift.launched = False
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    with db.auto_commit():
        # requester_id = current_user.id 这个条件可以防止超权
        drift = Drift.query.filter_by(
            gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success
        current_user.beans +=1
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True
        # 不查询直接更新;这一步可以异步来操作
        Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id,
                             launched=False).update({Wish.launched: True})
    return redirect(url_for('web.pending'))


def save_drift(drift_form,current_gift):
    with db.auto_commit():
        drift = Drift()
        drift_form.populate_obj(drift)
        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        book=BookViewModel(current_gift.book)

        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn=book.isbn

        current_user.beans-=1

        db.session.add(drift)