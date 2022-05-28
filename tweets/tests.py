from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Tweet

User = get_user_model()


class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="cfe", password="somepassword")
        Tweet.objects.create(content="my first tweet", user=self.user)
        Tweet.objects.create(content="my first tweet", user=self.user)
        Tweet.objects.create(content="my first tweet", user=self.user)
        self.currentCount = Tweet.objects.all().count()
        self.client = APIClient()

    def test_tweet_created(self):
        """
        Tests tweet creation
        id = 4 bc we have id=1-3 in setup
        """
        tweet_obj = Tweet.objects.create(content="my second tweet", user=self.user)
        self.assertEqual(tweet_obj.id, 4)
        self.assertEqual(tweet_obj.user, self.user)

    # -------------- DRF TESTING -------------- #

    def get_client(self):
        client = APIClient()
        client.login(username="cfe", password="somepassword")
        return client

    # def test_api_login(self):
    #     """
    #     Tests api login feature
    #     """
    #     client = APIClient()
    #     client.login(username=self.user.username, password='somepassword')

    def test_tweet_list(self):
        """
        Tests if able to login, grab tweets and get code 200
        Tests that we get the tweet obj
        """
        self.client.force_authenticate(self.user)
        # client = self.get_client()
        response = self.client.get("/api/tweets/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_action_like(self):
        """
        Tests like functionality
        Checks if status == 200 and like is added
        """
        # client = self.get_client()
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/tweets/action/",
                               {"id": 1, "action": "like"})
        print('tets', response.json())
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)

    def test_action_unlike(self):
        """
            Tests unlike functionality
            Checks if status == 200 and like is added
            """

        # client = self.get_client()
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/tweets/action/",
                               {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/api/tweets/action/",
                               {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)


    def test_action_retweet(self):    # TODO ValueError: Content-Type header is "text/html", not "application/json"

        # client = self.get_client()
        self.client.force_authenticate(self.user)
        current_count = self.currentCount
        response = self.client.post("api/tweets/action/",
                               {"id": 2, "action": "retweet"})
        #self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get("id")
        self.assertNotEqual(2, new_tweet_id)
        self.assertEqual((current_count + 1, new_tweet_id))


    def test_tweet_create_api_view(self):
        self.client.force_authenticate(self.user)
        request_data = {"content": "This is my test tweet"}
        #client = self.get_client()
        # print(client._credentials)
        response = self.client.post("/api/tweets/create/", request_data)
        print(response.data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get("id")
        #self.assertEqual(self.currentCount + 1, new_tweet_id)