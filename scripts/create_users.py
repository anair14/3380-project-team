import sys
import time
from pathlib import Path

import sqlalchemy.exc

sys.path.append(str(Path(__file__).parent.parent))

from utils.user_gen import UserGen
from app.factory import create_app
from app.models import db

app = create_app('config.Development')


def add_user(user: UserGen, count: int = 0) -> None:
    """Add the current user to the database.

    :param user: UserGen to be generated and added to the database
    :param count: optional count parameter
    """
    db.session.add(user.generate())
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        # user already exists with current username or email, so we increment
        # count and recurse
        db.session.rollback()
        count = count + 1
        user.gen_un(count=count)
        user.gen_email(count=count)
        add_user(user, count)


def create_users(num_users: int = 1) -> int:
    """Creates num_users number of users.

    :param num_users: the number of users to be created
    :return: the number of users generated, see comment below
    """
    with app.app_context():
        generated = 0
        for i in range(num_users):
            add_user(UserGen().populate())
            # i was going to check for duplicates, but that's a whole thing
            generated = generated + 1
        return generated


if __name__ == '__main__':
    try:
        num_users_argv = int(sys.argv[1])
    except (IndexError, ValueError):
        sys.exit('usage: python create_users.py <num_users: int>')

    start_time = time.time()
    users_generated = create_users(num_users_argv)
    end_time = time.time()

    print(f'generated {users_generated} users in {end_time - start_time:.2f}s')
    sys.exit(0)

# vim: ft=python ts=4 sw=4 sts=4 et
