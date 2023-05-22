import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Gamer, Game, Event
from rest_framework.authtoken.models import Token

class EventTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'events']

    def setUp(self):
        self.gamer = Gamer.objects.first()
        self.game = Game.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_event(self):
        """
        Ensure we can create a new event.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/events"

        # Define the request body
        data = {
            "description": "Test description",
            "date": "2023-01-01",
            "time": "07:30",
            "game": 1,
            "organizer": 1
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["description"], "Test description")
        self.assertEqual(json_response["date"], "2023-01-01")
        self.assertEqual(json_response["time"], "07:30")
        self.assertEqual(json_response["game"], 1)
        self.assertEqual(json_response["organizer"], 1)

    def test_get_event(self):
        """
        Ensure we can get an existing event.
        """

        # Seed the database with a game
        event = Event()
        event.description = "Test description"
        event.date = "2023-01-01"
        event.time = "07:30:00"
        event.organizer = Gamer.objects.first()
        event.game = Game.objects.first()

        event.save()

        # Initiate request and store response
        response = self.client.get(f"/events/{event.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["description"], "Test description")
        self.assertEqual(json_response["date"], "2023-01-01")
        self.assertEqual(json_response["time"], "07:30:00")
        self.assertEqual(json_response["organizer"], 1)
        self.assertEqual(json_response["game"], 1)

    def test_change_event(self):
        """
        Ensure we can change an existing event.
        """
        event = Event()
        event.description = "Test description"
        event.date = "2023-01-01"
        event.time = "07:30:00"
        event.organizer = Gamer.objects.first()
        event.game = Game.objects.first()
        event.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "description": "Updated test description",
            "date": "2023-01-02",
            "time": "07:45:00",
            "organizer": 1,
            "game": 1
        }

        response = self.client.put(f"/events/{event.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET game again to verify changes were made
        response = self.client.get(f"/events/{event.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["description"], "Updated test description")
        self.assertEqual(json_response["date"], "2023-01-02")
        self.assertEqual(json_response["time"], "07:45:00")
        self.assertEqual(json_response["organizer"], 1)
        self.assertEqual(json_response["game"], 1)

    def test_delete_event(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.game_type = GameType.objects.first()
        game.skill_level = 5
        game.title = "Sorry"
        game.maker = "Hasbro"
        game.number_of_players = 4
        game.gamer = Gamer.objects.first()
        game.save()

        # DELETE the game you just created
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the game again to verify you get a 404 response
        try:
            game = Game.objects.get(pk=game.id)
        except Game.DoesNotExist:
            game = None

        self.assertIsNone(game)

