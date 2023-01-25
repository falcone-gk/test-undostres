import json
import unittest
import requests

BASE_URL = 'https://reqres.in'

# Function to get full path of the endpoint
append = lambda path: BASE_URL + path

class TestListUsers(unittest.TestCase):
    """
    Test retrieve list users. I'd test if 'page' parameter is a number (if not then returns error request)
    and if user request a page larger than the total of pages then 'data' array should be empty.
    """

    def test_get_list_user_success(self):

        # Declaring an specific page
        page = 2
        res = requests.get(append('/api/users?page={}'.format(page)))

        # Convert response to json
        json_res = json.loads(res.content)
        page_res = json_res['page']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(page_res, page)

    def test_unknown_api_success(self):

        res = requests.get(append('/api/unknown'))
        self.assertEqual(res.status_code, 200)

class TestUserCreation(unittest.TestCase):
    """
    Testing user creation. It looks like the endpoint let us create a user even though
    there is an empty field or missing field so I am not testing those errors.
    """

    def test_create_user_success(self):

        body = {
            "name":"morpheus",
            "job":"leader"
        }
        res = requests.post(append('/api/users'), data=body)
        json_res = json.loads(res.content)

        # Keys that response must have
        keys = ['name', 'job', 'id', 'createdAt']

        self.assertEqual(res.status_code, 201)
        self.assertEqual(list(json_res.keys()), keys)

        # Check if user data is correct
        self.assertEqual(json_res['name'], body['name'])
        self.assertEqual(json_res['job'], body['job'])

    def test_create_user_success_one_field_job(self):

        body = {"job":"leader",}

        res = requests.post(append('/api/users'), data=body)
        json_res = json.loads(res.content)

        # Keys that response must have
        keys = ['job', 'id', 'createdAt']

        self.assertEqual(res.status_code, 201)
        self.assertEqual(list(json_res.keys()), keys)

        # Check if user data is correct
        self.assertEqual(json_res['job'], body['job'])

    def test_create_user_success_one_field_name(self):

        body = {"name":"morpheus",}

        res = requests.post(append('/api/users'), data=body)
        json_res = json.loads(res.content)

        # Keys that response must have
        keys = ['name', 'id', 'createdAt']

        self.assertEqual(res.status_code, 201)
        self.assertEqual(list(json_res.keys()), keys)

        # Check if user data is correct
        self.assertEqual(json_res['name'], body['name'])

class TestUpdateUser(unittest.TestCase):
    """
    Testing update user values. Endopoint let us make 'PUT' request with just one field
    so I am not testing the error if one field is missing because it returns a success request.
    """

    def test_update_user_success(self):

        new_vals = {
            "name": "morpheus",
            "job": "zion resident",
        }
        res = requests.put(append('/api/users/2'), data=new_vals)
        json_res = json.loads(res.content)

        self.assertEqual(res.status_code, 200)

        # Check if values were updated.
        self.assertEqual(json_res['name'], new_vals['name'])
        self.assertEqual(json_res['job'], new_vals['job'])

    def test_update_user_success_one_field(self):

        new_vals = {
            "name": "morpheus",
        }
        res = requests.patch(append('/api/users/2'), data=new_vals)
        json_res = json.loads(res.content)

        self.assertEqual(res.status_code, 200)

        # Check if values were updated.
        self.assertEqual(json_res['name'], new_vals['name'])

class TestDeleteUser(unittest.TestCase):
    """
    Testing delete user. Normally I'd test if the user doesn't exist but since the endpoint 
    doesn't return an error in that case I am not doing it.
    """

    def test_delete_user_success(self):

        res = requests.delete(append('/api/users/2'))
        self.assertEqual(res.status_code, 204)

class TestRegisterUser(unittest.TestCase):
    """Test user registration"""

    def test_register_user_success(self):

        body = {
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
        res = requests.post(append('/api/register'), data=body)
        json_res = json.loads(res.content)

        # Keys response must have
        keys = ['id', 'token']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(json_res.keys()), keys)

    def test_register_user_error_missing_field_password(self):

        body = {"email": "sydney@fife"}
        res = requests.post(append('/api/register'), data=body)
        json_res = json.loads(res.content)
        error_msg = {'error': 'Missing password'}

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json_res, error_msg)

    def test_register_user_error_missing_field_email(self):

        body = {"password": "pistol"}
        res = requests.post(append('/api/register'), data=body)

        json_res = json.loads(res.content)
        error_msg = {'error': 'Missing email or username'}

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json_res, error_msg)

class TestLoginUser(unittest.TestCase):
    """
    Test user login. I would add to test if username/email or password are correct.
    """

    def test_login_user_success(self):

        body = {
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        }
        res = requests.post(append('/api/login'), data=body)
        json_res = json.loads(res.content)
        keys = ['token']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(json_res.keys()), keys)

    def test_login_user_error_missing_field_password(self):

        body = {"email": "peter@klaven"}
        res = requests.post(append('/api/login'), data=body)
        json_res = json.loads(res.content)
        error_msg = {'error': 'Missing password'}

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json_res, error_msg)

    def test_login_user_error_missing_field_email(self):

        body = {"password": "pistol"}
        res = requests.post(append('/api/login'), data=body)

        json_res = json.loads(res.content)
        error_msg = {'error': 'Missing email or username'}

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json_res, error_msg)