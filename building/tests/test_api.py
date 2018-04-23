from test_plus import APITestCase

from building.models import Building
from core.models import Cities, Country, States, Timezone


class BuildingAPITests(APITestCase):
    def setUp(self):
        country = Country.objects.create(country_code='KR', country_name='대한민국')
        state = States.objects.create(country=country, state_code='KK', state_name='경기도')
        timezone = Timezone.objects.create(country=country, timezone_name='Asia/Seoul',
                                           gmt_offset=9, dst_offset=9, raw_offset=9)
        city = Cities.objects.create(country=country, state=state, city_name='고양',
                                     city_name_ascii='goyang',
                                     latitude=245,
                                     longitude=281,
                                     timezone_name=timezone)
        Building.objects.get_or_create(name='스타필드', city=city, address='덕양구 창릉동 고양대로 1955')
        Building.objects.get_or_create(name='킨텍스', city=city, address='일산서구 대화동 킨텍스로 217-59')
        self.list_url = self.reverse('api:building-list')
        self.user = self.make_user()
        self.jwt_response = self.post('/api-token-auth/',
                                      data={'username': 'testuser',
                                            'password': 'password'})

        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.jwt_response.data["token"]}')

    def test_building_list(self):
        response = self.get(self.list_url)
        self.assertContains(response, '스타필드')
        self.assertContains(response, '킨텍스')
        self.assertContains(response, '경기도')
        self.assertContains(response, '고양')
        self.assertContains(response, 'Asia/Seoul')
        self.assertContains(response, 'goyang')
