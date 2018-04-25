from rest_framework import status
from test_plus import APITestCase

from building.models import Building
from building.serializers import BuildingReadSerializer
from core.models import Cities, Country, States, Timezone


class BuildingAPITests(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(country_code='KR', country_name='대한민국')
        self.state = States.objects.create(country=self.country, state_code='KK', state_name='경기도')
        self.timezone = Timezone.objects.create(country=self.country, timezone_name='Asia/Seoul',
                                                gmt_offset=9, dst_offset=9, raw_offset=9)
        self.city = Cities.objects.create(country=self.country, state=self.state, city_name='고양',
                                          city_name_ascii='goyang',
                                          latitude=245,
                                          longitude=281,
                                          timezone_name=self.timezone)
        self.building1, _ = Building.objects.get_or_create(name='스타필드', city=self.city, address='덕양구 창릉동 고양대로 1955')
        self.building2, _ = Building.objects.get_or_create(name='킨텍스', city=self.city, address='일산서구 대화동 킨텍스로 217-59')
        self.user = self.make_user()
        self.jwt_response = self.post('/api-token-auth/',
                                      data={'username': 'testuser',
                                            'password': 'password'})

        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.jwt_response.data["token"]}')

    def test_building_list(self):
        url = self.reverse('api:building-list')
        response = self.get(url)
        self.assertContains(response, '스타필드')
        self.assertContains(response, '킨텍스')
        self.assertContains(response, '경기도')
        self.assertContains(response, '고양')
        self.assertContains(response, 'Asia/Seoul')
        self.assertContains(response, 'goyang')

    def test_building_detail(self):
        url = self.reverse('api:building-detail', pk=1)
        response = self.get(url)
        serializer = BuildingReadSerializer(self.building1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_building_detail_not_exists(self):
        url = self.reverse('api:building-detail', pk=5)
        response = self.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_building_create(self):
        url = self.reverse('api:building-list')
        payload = {
            'city': self.city.id,
            'name': '유효빌딩',
            'desc': '테스트 건물입니다.',
            'address': 'test_address'
        }
        # serializer = BuildingSerializer(payload)
        response = self.client.post(url, data=payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Building.objects.all().count(), 3)

    def test_invalid_building_create(self):
        url = self.reverse('api:building-list')
        payload = {
            'name': '유효빌딩',
            'address': 'test_address',
            'img_src': None
        }
        # serializer = BuildingSerializer(payload)
        response = self.client.post(url, data=payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
