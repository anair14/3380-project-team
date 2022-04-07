from . import db


"""Mapping table for users and their followers."""
followers = db.Table(
    'followers',
    db.Column(
        'follower_id',
        db.Integer,
        db.ForeignKey('user.id')
    ),
    db.Column(
        'followed_id',
        db.Integer,
        db.ForeignKey('user.id')
    )
)