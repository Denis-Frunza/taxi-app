from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from trips.models import Trip

from .test_http import PASSWORD, create_test_user


class HttpTripTest(APITestCase):
    def setUp(self):
        user = create_test_user()
        response = self.client.post(
            reverse("trips:log_in"),
            data={
                "username": user.username,
                "password": PASSWORD,
            },
        )
        self.access = response.data["access"]

    def test_user_can_list_trips(self):
        trips = [
            Trip.objects.create(pick_up_address="A", drop_off_address="B"),
            Trip.objects.create(pick_up_address="B", drop_off_address="C"),
        ]
        response = self.client.get(
            reverse("trips:trip_list"), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        exp_trip_ids = [str(trip.id) for trip in trips]
        act_trip_ids = [trip.get("id") for trip in response.data]
        self.assertCountEqual(exp_trip_ids, act_trip_ids)

    def test_user_can_retrieve_trip_by_user(self):
        trip = Trip.objects.create(pick_up_address="A", drop_off_address="B")
        response = self.client.get(
            trip.get_absolute_url(), HTTP_AUTHORIZATION=f"Bearer {self.access}"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(str(trip.id), response.data.get("id"))
