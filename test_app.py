import unittest
from app import app, db, User, Question

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        with app.app_context():
            db.drop_all()
            db.create_all()
            test_user = User(role='Doctor', username='testuser', password='testpassword', name='Test User', age=30, gender='Male')
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_valid_login(self):
        tester = app.test_client(self)
        response = tester.post('/login_submit', data=dict(username='testuser', password='testpassword'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_login(self):
        tester = app.test_client(self)
        response = tester.post('/login_submit', data=dict(username='testuser', password='wrongpassword'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_registration(self):
        tester = app.test_client(self)
        response = tester.post('/register', data=dict(role='Patient', username='newuser', password='password', name='New User', age=25, gender='Female'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_duplicate_username_registration(self):
        tester = app.test_client(self)
        response = tester.post('/register', data=dict(role='Patient', username='testuser', password='password', name='New User', age=25, gender='Female'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # def test_question_submission(self):
    #     tester = app.test_client(self)
    #     tester.post('/login_submit', data=dict(username='testuser', password='testpassword'))
    #     response = tester.post('/ask_question', data=dict(question='Test question'), follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)

    # def test_question_display(self):
    #     tester = app.test_client(self)
    #     tester.post('/login_submit', data=dict(username='testuser', password='testpassword'))
    #     question = Question(question='Test question')
    #     db.session.add(question)
    #     db.session.commit()
    #     response = tester.get('/view_questions', content_type='html/text')
    #     self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
