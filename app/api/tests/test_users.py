import datetime
import unittest

from faker import Faker

from app.api.users import *
from app.models.fake.profile import ProfileProvider


def customDeepEqual(params, dict1, dict2):
    for param in params:
        if isinstance(dict1[param], datetime.datetime) or isinstance(dict2[param], datetime.datetime):
            if str(dict1[param])[0:9] != str(dict2[param])[0:9]:
                return False
        elif str(dict1[param]) != str(dict2[param]):
            return False
    return True


class UsersTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(UsersTest, self).__init__(*args, **kwargs)
        self.fake = Faker()
        self.fake.add_provider(ProfileProvider)

    def setUp(self):
        self.fake_user = self.fake.moevm_profile()
        self.fake_user['login'] = self.fake.user_name()
        self.fake_user['password'] = self.fake.password()
        register_user(self.fake_user)

    def tearDown(self):
        fake_user_id = get_user_by_login(self.fake_user['login']).id
        delete_user(fake_user_id)

    def test_find_user(self):
        user = get_user_by_login(self.fake_user['login'])
        user = get_user_by_id(user.id)
        profile = get_profile_by_user_id(user.id)
        self.assertTrue(
            customDeepEqual(['last_name', 'first_name', 'patronymic', 'type', 'birth_date', 'github_id',
                             'stepic_id', 'election_date', 'contract_date', 'academic_status', 'year_of_academic_status'],
                            profile, self.fake_user)
        )
        type = get_user_type(user.id)
        self.assertEqual(type, self.fake_user['type'])

    def test_auth_user(self):
        self.assertIsNotNone(check_user_auth(self.fake_user))
        self.assertIsNone(check_user_auth({
            'login': self.fake_user['login'],
            'password': self.fake.password()
        }))

    def test_update_profile(self):
        new_profile = self.fake.moevm_profile()
        fake_user_id = get_user_by_login(self.fake_user['login']).id
        fake_profile_id = get_profile_by_user_id(fake_user_id).id
        new_profile['id'] = fake_profile_id
        update_profile(new_profile)
        profile = get_profile_by_user_id(fake_user_id)
        self.assertTrue(
            customDeepEqual(['last_name', 'first_name', 'patronymic', 'type', 'birth_date', 'github_id',
                             'stepic_id', 'election_date', 'contract_date', 'academic_status',
                             'year_of_academic_status'],
                            new_profile, profile)
        )

    def test_nonexistent_user(self):
        id = str(self.fake.random_number(24))
        login = self.fake.user_name() + '%FAKE%'
        self.assertIsNone(get_profile_by_user_id(id))
        self.assertIsNone(get_user_by_id(id))
        self.assertIsNone(get_user_type(id))
        self.assertIsNone(get_user_by_login(login))
        self.assertIsNone(check_user_auth({
            'login': login
        }))
        self.assertIsNone(delete_user(id))

    def test_available(self):
        user = get_user_by_login(self.fake_user['login'])
        profile = get_profile_by_user_id(user.id)
        profile.type = 'Преподаватель'
        profile.save()
        self.assertEqual(len(get_available_profiles(user)), 1)
        self.assertEqual(len(get_available_users(user)), 1)
        profile.type = 'Администратор'
        profile.save()
        self.assertGreaterEqual(len(get_available_profiles(user)), 1)
        self.assertGreaterEqual(len(get_available_users(user)), 1)
        profile.type = 'Менеджер'
        profile.save()
        self.assertGreaterEqual(len(get_available_profiles(user)), 1)
        self.assertGreaterEqual(len(get_available_users(user)), 1)

    def test_get_registration_form(self):
        form = get_registration_form()
        self.assertGreaterEqual(len(form), 1)
        

if __name__ == '__main__':
    unittest.main()
