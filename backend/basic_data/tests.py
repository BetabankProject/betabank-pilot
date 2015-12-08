import json
from django.contrib.auth.models import User
from django.test import TestCase
from basic_data.models import Request, SkillFamily, RequestStatus


class RequestManagerTest(TestCase):
    fixtures = ['usersAndSkills']
    test_title = "Request test title"
    data = {"title": test_title,
            "description": "Request test description",
            "hours": 5,
            "category": 5
            }

    def testCreateThroughModel(self):
        """
        """
        user = User.objects.get(username='user1')

        Request.objects.create(user=user, json=self.data)

        req = Request.objects.all()[0]
        self.assertEqual(req.status, RequestStatus.OPEN)
        self.assertEqual(req.title, self.test_title)
        self.assertEqual(req.hours, 5)

    def testCreateThroughApi(self):
        c = self.client
        c.login(username='user1', password='pass')
        response = c.post('/pilot/request/', json.dumps(self.data), content_type="application/json")
        print(response)
        self.assertEqual(response.status_code, 201)

    def testCreateThroughApiWrongInput(self):
        baddata = {"description": "Request test description",
                   "hours": 5,
                   "category": 5
                   }
        c = self.client
        c.login(username='user1', password='pass')
        response = c.post('/pilot/request/', json.dumps(baddata), content_type="application/json")
        json_response = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        assert(json_response["error"].__contains__('title'))
