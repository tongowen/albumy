# -*- coding: utf-8 -*-

from flask import url_for

from app.extensions import db
from app.models import Notification


def push_follow_notification(follower, receiver):
    message = '用户 <a href="%s">%s</a> 关注了你！' % \
              (url_for('user.index', username=follower.username), follower.username)
    notification = Notification(message=message, receiver=receiver)
    db.session.add(notification)
    db.session.commit()


def push_comment_notification(photo_id, receiver, page=1):
    message = '<a href="%s#comments">这张照片</a> 有了新的评论/回复！' % \
              (url_for('main.show_photo', photo_id=photo_id, page=page))
    notification = Notification(message=message, receiver=receiver)
    db.session.add(notification)
    db.session.commit()


def push_collect_notification(collector, photo_id, receiver):
    message = '用户 <a href="%s">%s</a> 点赞了你的 <a href="%s">照片！</a>' % \
              (url_for('user.index', username=collector.username),
               collector.username,
               url_for('main.show_photo', photo_id=photo_id))
    notification = Notification(message=message, receiver=receiver)
    db.session.add(notification)
    db.session.commit()
