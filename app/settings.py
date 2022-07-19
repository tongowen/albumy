# -*- coding: utf-8 -*-

import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class BaseConfig:
    O_ADMIN_EMAIL = os.getenv('O_ADMIN', 'admin@owen.com')
    O_PHOTO_PER_PAGE = 12
    O_COMMENT_PER_PAGE = 15
    O_NOTIFICATION_PER_PAGE = 20
    O_USER_PER_PAGE = 20
    O_MANAGE_PHOTO_PER_PAGE = 20
    O_MANAGE_USER_PER_PAGE = 30
    O_MANAGE_TAG_PER_PAGE = 50
    O_MANAGE_COMMENT_PER_PAGE = 30
    O_SEARCH_RESULT_PER_PAGE = 20
    O_MAIL_SUBJECT_PREFIX = '[篮球之境]'
    O_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    O_PHOTO_SIZE = {'small': 400,
                         'medium': 800}
    O_PHOTO_SUFFIX = {
        O_PHOTO_SIZE['small']: '_s',  # thumbnail
        O_PHOTO_SIZE['medium']: '_m',  # display
    }

    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024  # file size exceed to 1 Gb will return a 413 error response.

    BOOTSTRAP_SERVE_LOCAL = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AVATARS_SAVE_PATH = os.path.join(O_UPLOAD_PATH, 'avatars')
    AVATARS_SIZE_TUPLE = (30, 100, 200)

    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USERNAME = "846565422@qq.com"
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('篮球之境 管理员', MAIL_USERNAME)

    DROPZONE_ALLOWED_FILE_TYPE = 'image'
    DROPZONE_MAX_FILE_SIZE = 3
    DROPZONE_MAX_FILES = 30
    DROPZONE_ENABLE_CSRF = True

    WHOOSHEE_MIN_STRING_LEN = 1


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = \
        prefix + os.path.join(basedir, 'owen-dev.db')
    REDIS_URL = "redis://localhost"


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        prefix + os.path.join(basedir, 'owen.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
