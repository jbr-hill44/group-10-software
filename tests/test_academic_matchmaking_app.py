# Testing the Academic Matchmaking App
# NOTE: This was implemented in a notebook

import pytest
import unittest
from unittest.mock import patch
import streamlit as st
from page.login_page import login_page

import warnings
warnings.filterwarnings('ignore')


# Helper function to run test cases

def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)


# Helper function to run test suites

def run_test_suites(test_classes):
    suite = unittest.TestSuite()
    for test_class in test_classes:
        suite.addTest(unittest.makeSuite(test_class))
    runner = unittest.TextTestRunner(verbosity = 2)
    results = runner.run(suite)


# Helper function to add Test Classes to list

test_classes = []
def add_test_class(test_class):
    if test_class not in test_classes:
        test_classes.append(test_class)


# Testing Login Page

class TestLoginPage(unittest.TestCase):

    # test_successful_login
    @patch('streamlit.success', return_value = True)
    @patch('streamlit.button', return_value = True)
    @patch('streamlit.text_input', side_effect = ['valid_user@matchmaking.com', 'valid_password'])
    @patch('utils.db_handler.authenticate_user', return_value = True)
    def test_successful_login(self, mock_auth, mock_input, mock_button, mock_success):
        
        # Clear and prepare a mock session_state
        st.session_state.clear()
        st.session_state['authenticated'] = False
        st.session_state['page'] = 'login'
    
        # Call the login page function (guest_mode=False by default)
        login_page()
    
        # Check the session_state updates
        self.assertIn('authenticated', st.session_state)
        self.assertEqual(st.session_state['page'], 'signup')
    
    # test_failed_login     
    @patch('streamlit.error')
    @patch('streamlit.button', side_effect=[True, False])  # Simulate 'Login' button clicked
    @patch('streamlit.text_input', side_effect=['invalid_user@matchmaking.com', 'invalid_password'])
    @patch('utils.db_handler.authenticate_user', return_value = False)
    @patch('streamlit.session_state', new_callable=dict)
    def test_failed_login(self, mock_session, mock_auth, mock_input, mock_button, mock_error):
        
        login_page()    
    
        # Check that st.error was called with the appropriate message
        mock_error.assert_called_with('Invalid login credentials')

    # test_missing_credentials
    @patch('streamlit.error')
    @patch('streamlit.button', side_effect=[True, False])
    @patch('streamlit.text_input', side_effect = ['', ''])  # No input
    def test_missing_credentials(self, mock_input, mock_button, mock_error):
        
        login_page()
        mock_error.assert_called_with('Please provide email and password')


add_test_class(TestLoginPage)


# Testing Signup Page

from page.signup_page import is_valid_email
import streamlit as st
from unittest.mock import patch, MagicMock
from page.signup_page import verifyOTP

class TestSignupPage(unittest.TestCase):

    # test_successful_signup
    @patch('streamlit.success', return_value = True)
    @patch('page.signup_page.save_user')
    @patch('streamlit.rerun')
    def test_successful_signup(self, mock_rerun, mock_save_user, mock_success): 
        # Mock session state
        st.session_state['otp'] = '123456'
        st.session_state['verifying'] = True
        st.session_state['email'] = 'valid_user@matchmaking.com'
        st.session_state['password'] = 'valid_password'
        st.session_state['role'] = 'student'
        st.session_state['page'] = ''
        
        verifyOTP('123456')  # Match OTP
        mock_save_user.assert_called_once_with('valid_user@matchmaking.com', 'valid_password', 'student')
        self.assertEqual(st.session_state['page'], 'login')
        mock_success.assert_called_with('OTP verified successfully')

    # test_failed_signup    
    @patch('page.signup_page.save_user')
    @patch('streamlit.rerun')
    @patch('streamlit.error')
    def test_failed_signup(self, mock_error, mock_rerun, mock_save_user): 
        # Mock session state
        st.session_state['otp'] = '123456'
        st.session_state['verifying'] = True
        st.session_state['email'] = 'invalid_user@matchmaking.com'
        st.session_state['password'] = 'invalid_password'
        st.session_state['role'] = 'student'
        st.session_state['page'] = ''
        
        verifyOTP('000000')
        mock_save_user.assert_not_called()
        # Confirm error message is shown
        mock_error.assert_called_once_with('Invalid OTP')

add_test_class(TestSignupPage)


# ### Testing Matching Logic

from sentence_transformers import SentenceTransformer, util

def get_similarity_scores(student_skills, project_list, topn=5):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    student_embed = model.encode(student_skills, convert_to_tensor=True)
    project_embeds = model.encode(project_list, convert_to_tensor=True)

    similarities = util.pytorch_cos_sim(student_embed, project_embeds)
    sorted_indices = similarities.argsort(descending=True)

    top_matches = []
    for idx in sorted_indices[0][:topn]:
        top_matches.append({
            'project': project_list[idx],
            'score': float(similarities[0, idx])
        })
    return top_matches


class TestMatchingLogic(unittest.TestCase):

    def setUp(self):
        self.student_input = "Machine Learning, Deep Learning, Python"
        self.project_list = [
            "Machine Learning for Healthcare",
            "Classical Literature Analysis",
            "Neural Networks in Finance",
            "Python-based Data Science Pipelines",
            "Medieval History Studies"
        ]

    def test_top_match_is_relevant(self):
        results = get_similarity_scores(self.student_input, self.project_list)
        top_project = results[0]['project']
        self.assertIn('Machine Learning', top_project)

    def test_returns_limited_matches(self):
        results = get_similarity_scores(self.student_input, self.project_list, topn=3)
        self.assertEqual(len(results), 3)

    def test_score_is_within_range(self):
        results = get_similarity_scores(self.student_input, self.project_list)
        for match in results:
            self.assertGreaterEqual(match['score'], 0.0)
            self.assertLessEqual(match['score'], 1.0)


add_test_class(TestMatchingLogic)


# Testing the App Page (Integrated with seesion changes and matching)
# Expanded to verify session changes and to test what match() actually returns based on user state!

from page.app import app_page

class TestAppPageExpanded(unittest.TestCase):

    def setUp(self):
        st.session_state.clear()
        st.session_state['authenticated'] = False
        st.session_state['guest_mode'] = False
        st.session_state['page'] = 'login'
        st.session_state['extra_input_params'] = {}

    @patch('utils.init_session.reset_session')
    @patch('page.matching.match')
    def test_guest_mode_session_changes_on_login(self, mock_match, mock_reset_session):
        st.session_state['guest_mode'] = True

    # Case 1: Login button is not clicked
    def button_side_effect(label, *args, **kwargs):
        return label == 'Find Matches'
        with patch('streamlit.button', side_effect=button_side_effect):
            app_page()
            mock_match.assert_called_once()
            self.assertEqual(st.session_state['page'], 'app')

        # Case 2: Login button clicked
        mock_match.reset_mock()
        mock_reset_session.side_effect = lambda: st.session_state.update({
            'authenticated': False,
            'guest_mode': False,
            'page': 'login'
        })

        with patch('streamlit.button', side_effect=[True]), patch('streamlit.rerun') as mock_rerun:
            app_page()
            self.assertFalse(st.session_state['authenticated'])
            self.assertFalse(st.session_state['guest_mode'])
            self.assertEqual(st.session_state['page'], 'login')
            mock_rerun.assert_called_once()

    @patch('utils.init_session.reset_session')
    @patch('page.matching.match')
    def test_authenticated_user_logout_behavior(self, mock_match, mock_reset_session):
        st.session_state['authenticated'] = True
        st.session_state['guest_mode'] = False

        # Case: Logout button clicked
        mock_reset_session.side_effect = lambda: st.session_state.update({
            'authenticated': False,
            'guest_mode': False,
            'page': 'login'
        })

        with patch('streamlit.button', return_value=True), patch('streamlit.rerun') as mock_rerun:
            app_page()
            self.assertFalse(st.session_state['authenticated'])
            self.assertEqual(st.session_state['page'], 'login')
            mock_rerun.assert_called_once()

        # Case: No logout click
        mock_reset_session.reset_mock()
        mock_rerun.reset_mock()
        st.session_state['authenticated'] = True

    def button_side_effect(label, *args, **kwargs):
        return label == 'Find Matches'
        with patch('streamlit.button', side_effect=button_side_effect):
            app_page()
            mock_match.assert_called_once()

    @patch('page.matching.match')
    def test_guest_and_authenticated_users_call_match(self, mock_match):
        # Guest
        st.session_state['guest_mode'] = True
        st.session_state['authenticated'] = False

    def button_side_effect(label, *args, **kwargs):
        return label == 'Find Matches'
        with patch('streamlit.button', side_effect=button_side_effect):
            app_page()
            mock_match.assert_called_once()
            mock_match.reset_mock()

        # Authenticated
        st.session_state['guest_mode'] = False
        st.session_state['authenticated'] = True
        with patch('streamlit.button', return_value=False):
            app_page()
            mock_match.assert_called_once()


add_test_class(TestAppPageExpanded)


# Testing the database-related functions

import unittest
from unittest.mock import patch, MagicMock
import bcrypt
import pandas as pd
from utils import db_handler  

class TestDBHandler(unittest.TestCase):

    @patch('utils.db_handler.psycopg2.connect')
    def test_verify_duplicate_user_true(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        result = db_handler.verify_duplicate_user('test@matchmaking.com')
        self.assertTrue(result)

    @patch('utils.db_handler.psycopg2.connect')
    def test_verify_duplicate_user_false(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [0]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        result = db_handler.verify_duplicate_user('valid_user@matchmaking.com')
        self.assertFalse(result)

    @patch('utils.db_handler.psycopg2.connect')
    def test_authenticate_user_success(self, mock_connect):
        password = 'validpassword'
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [hashed_pw]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        result = db_handler.authenticate_user('user@matchmaking.com', password)
        self.assertTrue(result)

    @patch('utils.db_handler.psycopg2.connect')
    def test_authenticate_user_failure(self, mock_connect):
        # Case where email is not found
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        result = db_handler.authenticate_user('fake_user@matchmaking.com', 'invalidpassword')
        self.assertFalse(result)

    @patch('utils.db_handler.psycopg2.connect')
    def test_save_user_executes_insert(self, mock_connect):
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db_handler.save_user('new_user@matchmaking.com', 'newpassword', 'student')
        self.assertTrue(mock_cursor.execute.called)

    @patch('utils.db_handler.psycopg2.connect')
    def test_get_users_returns_list(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('user1', 'password1', 'student')]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        users = db_handler.get_users()
        self.assertIsInstance(users, list)
        self.assertEqual(users[0][0], 'user1')

    @patch('utils.db_handler.pd.read_sql_query')
    def test_get_projects_returns_dataframe(self, mock_read_sql):
        df = pd.DataFrame({'id': [1], 'title': ['AI Research']})
        mock_read_sql.return_value = df

        result = db_handler.get_projects()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.iloc[0]['title'], 'AI Research')


add_test_class(TestDBHandler)


# Run test suites (all tests)

if __name__ == '__main__':
    run_test_suites(test_classes)




