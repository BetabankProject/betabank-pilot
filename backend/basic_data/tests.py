import json

from django.contrib.auth.models import User
from django.test import TestCase

from basic_data.models import Request, Skill, SkillFamily, RequestStatus


class RequestManagerTest(TestCase):
    fixtures = ['usersAndSkills']

    def testCreate(self):
        """
        """
        family = SkillFamily.objects.all()[0]
        user = User.objects.get(username='user1')

        test_title = 'Request test title'

        Request.objects.create(user=user,
                               title=test_title,
                               description='Request test description',
                               hours=5,
                               category=5)

        req = Request.objects.all()[0]
        self.assertEqual(req.status, RequestStatus.OPEN)
        self.assertEqual(req.title, test_title)
        self.assertEqual(req.hours, 5)


class RequestApiTest(TestCase):
    fixtures = ['usersAndSkills']

    def testCreate(self):
        request_json = {
            "title": "Request title",
            "description": "Request description",
            "category": "5",
            "hours": "5"
        }
        json_str = json.dumps(request_json)
        print(json_str)
        c = self.client
        c.login(username='user1', password='pass')
        response = c.post('/pilot/request/', json_str, content_type="application/json")
        print(response)
        self.assertEqual(response.status_code, 201)

