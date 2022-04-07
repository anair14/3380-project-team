import random
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.factory import create_app
from app.models import db
from app.models.user import User

app = create_app('config.Development')


def follow_users(num_followers: int) -> int:
    """Follows num_followers for each user in the database.

    :param num_followers: number of followers for each user to follow
    :return: number of users in the database
    """
    with app.app_context():
        user_count = User.query.count()

        if user_count <= 1:
            sys.exit('database must be populated with more than 1 user')

        # we need minimum user_count + 1 followers or the script will fail
        if user_count <= num_followers:
            sys.exit(
                f'total users ({user_count}) is too low for {num_followers} '
                'followers')

        all_users = User.query.all()
        for user in all_users:
            for i in range(0, num_followers):
                random_id = random.randint(1, user_count)

                # don't allow the current user to follow themselves
                while random_id == user.id:
                    random_id = random.randint(1, user_count)

                to_follow = User.query.filter_by(id=random_id).first()
                user.follow(to_follow)
                db.session.commit()

        return user_count


if __name__ == '__main__':
    try:
        num_followers_argv = int(sys.argv[1])
    except(IndexError, ValueError):
        sys.exit('usage: python follow_users.py <num_followers: int>')

    start_time = time.time()
    users_following = follow_users(5)
    end_time = time.time()

    print(f'{users_following} users now each following {num_followers_argv} other users')
    sys.exit(0)

# vim: ft=python ts=4 sw=4 sts=4 et
