# -*- coding: utf-8 -*-

from flask import render_template, jsonify, Blueprint
from flask_login import current_user

from app.models import User, Photo, Notification
from app.notifications import push_collect_notification, push_follow_notification

ajax_bp = Blueprint('ajax', __name__)


@ajax_bp.route('/notifications-count')
def notifications_count():
    if not current_user.is_authenticated:
        return jsonify(message='请先登录！'), 403

    count = Notification.query.with_parent(current_user).filter_by(is_read=False).count()
    return jsonify(count=count)


@ajax_bp.route('/profile/<int:user_id>')
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('main/profile_popup.html', user=user)


@ajax_bp.route('/followers-count/<int:user_id>')
def followers_count(user_id):
    user = User.query.get_or_404(user_id)
    count = user.followers.count() - 1  # minus user self
    return jsonify(count=count)


@ajax_bp.route('/<int:photo_id>/followers-count')
def collectors_count(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    count = len(photo.collectors)
    return jsonify(count=count)


@ajax_bp.route('/collect/<int:photo_id>', methods=['POST'])
def collect(photo_id):
    if not current_user.is_authenticated:
        return jsonify(message='请先登录！'), 403
    if not current_user.confirmed:
        return jsonify(message='请先确认账号！'), 400
    if not current_user.can('COLLECT'):
        return jsonify(message='没有权限！'), 403

    photo = Photo.query.get_or_404(photo_id)
    if current_user.is_collecting(photo):
        return jsonify(message='已经点赞了！'), 400

    current_user.collect(photo)
    if current_user != photo.author and photo.author.receive_collect_notification:
        push_collect_notification(collector=current_user, photo_id=photo_id, receiver=photo.author)
    return jsonify(message='点赞成功！')


@ajax_bp.route('/uncollect/<int:photo_id>', methods=['POST'])
def uncollect(photo_id):
    if not current_user.is_authenticated:
        return jsonify(message='请先登录！'), 403

    photo = Photo.query.get_or_404(photo_id)
    if not current_user.is_collecting(photo):
        return jsonify(message='你还没有点赞！'), 400

    current_user.uncollect(photo)
    return jsonify(message='已取消！')


@ajax_bp.route('/follow/<username>', methods=['POST'])
def follow(username):
    if not current_user.is_authenticated:
        return jsonify(message='请先登录！'), 403
    if not current_user.confirmed:
        return jsonify(message='请先确认账号！'), 400
    if not current_user.can('FOLLOW'):
        return jsonify(message='权限不足！'), 403

    user = User.query.filter_by(username=username).first_or_404()
    if current_user.is_following(user):
        return jsonify(message='已关注！'), 400

    current_user.follow(user)
    if user.receive_collect_notification:
        push_follow_notification(follower=current_user, receiver=user)
    return jsonify(message='关注成功！')


@ajax_bp.route('/unfollow/<username>', methods=['POST'])
def unfollow(username):
    if not current_user.is_authenticated:
        return jsonify(message='请先登录！'), 403

    user = User.query.filter_by(username=username).first_or_404()
    if not current_user.is_following(user):
        return jsonify(message='还没有关注！'), 400

    current_user.unfollow(user)
    return jsonify(message='取消关注！')
