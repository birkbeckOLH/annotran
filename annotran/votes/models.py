# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sqlalchemy.orm import exc

from h.db import Base


class Vote(Base):
    __tablename__ = 'vote'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    vote = sa.Column(sa.Text(),
                      unique=True,
                      nullable=False)
    # we need a relationship table between a vote and: a user, a langauge and a page
    relUser = sa.orm.relationship('User',
                                  backref=sa.orm.backref('votes', lazy='dynamic'),
                                  secondary='user_vote',
                                  lazy='dynamic')

    relLanguage = sa.orm.relationship('Language',
                                      backref=sa.orm.backref('votes', lazy='dynamic'),
                                      secondary='language_vote',
                                      lazy='dynamic')

    relPage = sa.orm.relationship('Page',
                                  backref=sa.orm.backref('votes', lazy='dynamic'),
                                  secondary='page_vote',
                                  lazy='dynamic')

    def __init__(self, score, page=None, language=None, user=None, voter=None):
        self.vote = score
        if user and language and page:
            self.relUser.append(user)
            self.relVoter.append(voter)
            self.relLanguage.append(language)
            self.relPage.append(page)

    @classmethod
    def get_by_vote(cls, vote):
        """Return the vote with the given vote value, or None."""
        try:
            return cls.query.filter(
                cls.vote == vote).one()
        except exc.NoResultFound:
            return None

    @classmethod
    def get_by_id(cls, id_):
        """Return the vote with the given id, or None."""
        try:
            return cls.query.filter(
                cls.id == id_).one()
        except exc.NoResultFound:
            return None

    @classmethod
    def get_by_voter(cls, page, language, user, voter):
        """Return the language with the given pubid, or None."""
        if page and language and user and voter:
            return cls.query.filter(cls.relPage.contains(page), cls.relLanguage.contains(language),
                                    cls.relUser.contains(user), cls.relVoter.contains(voter)).first()
        else:
            return None

    @classmethod
    def get_by_language(cls, language):
        """Return the language with the given pubid, or None."""
        if language:
            return cls.query.filter(cls.relLanguage.contains(language))
        else:
            return None

USER_VOTE_TABLE = sa.Table(
    'user_vote', Base.metadata,
    sa.Column('user_id',
              sa.Integer,
              sa.ForeignKey('user.id'),
              nullable=False),
    sa.Column('vote_id',
              sa.Integer,
              sa.ForeignKey('vote.id'),
              nullable=False)
)


LANGUAGE_VOTE_TABLE = sa.Table(
    'language_vote', Base.metadata,
    sa.Column('language_id',
              sa.Integer,
              sa.ForeignKey('language.id'),
              nullable=False),
    sa.Column('vote_id',
              sa.Integer,
              sa.ForeignKey('vote.id'),
              nullable=False)
)

PAGE_VOTE_TABLE = sa.Table(
    'page_vote', Base.metadata,
    sa.Column('page_id',
              sa.Integer,
              sa.ForeignKey('page.id'),
              nullable=False),
    sa.Column('vote_id',
              sa.Integer,
              sa.ForeignKey('vote.id'),
              nullable=False)
)


class UserType(Base):
    __tablename__ = 'user_type'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    type = sa.Column(sa.Text(),
                      unique=True,
                      nullable=False)
    # we need a relationship table between a user_type and a user
    relUser = sa.orm.relationship('User',
                                  backref=sa.orm.backref('user_types', lazy='dynamic'),
                                  secondary='user_type_ref',
                                  lazy='dynamic')

    def __init__(self, type):
        self.type = type

    @classmethod
    def get_by_type(cls, type):
        """Return the type with the given type value, or None."""
        try:
            return cls.query.filter(
                cls.type == type).one()
        except exc.NoResultFound:
            return None

    @classmethod
    def get_by_id(cls, id_):
        """Return the type with the given id, or None."""
        try:
            return cls.query.filter(
                cls.id == id_).one()
        except exc.NoResultFound:
            return None

USER_TYPE_REF_TABLE = sa.Table(
    'user_type_ref', Base.metadata,
    sa.Column('user_id',
              sa.Integer,
              sa.ForeignKey('user.id'),
              nullable=False),
    sa.Column('type_id',
              sa.Integer,
              sa.ForeignKey('user_type.id'),
              nullable=False)
)