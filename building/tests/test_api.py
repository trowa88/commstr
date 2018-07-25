import io

from PIL import Image
from rest_framework import status
from test_plus import APITestCase

from building.models import Building, BuildingHistory
from building.serializers import BuildingReadSerializer
from core.models import Cities, Country, States, Timezone


def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file


class BuildingAPITests(APITestCase):
    def setUp(self):
        self.client.user = self.make_user()
        self.client.country = Country.objects.create(country_code='KR', country_name='대한민국')
        self.client.state = States.objects.create(country=self.client.country, state_code='KK', state_name='경기도')
        self.client.timezone = Timezone.objects.create(country=self.client.country, timezone_name='Asia/Seoul',
                                                       gmt_offset=9, dst_offset=9, raw_offset=9)
        self.client.city = Cities.objects.create(country=self.client.country, state=self.client.state, city_name='고양',
                                                 city_name_ascii='goyang',
                                                 latitude=245,
                                                 longitude=281,
                                                 timezone_name=self.client.timezone)
        self.client.building1, _ = Building.objects.get_or_create(name='스타필드', city=self.client.city,
                                                                  address='덕양구 창릉동 고양대로 1955',
                                                                  creator=self.client.user)
        self.client.building2, _ = Building.objects.get_or_create(name='킨텍스', city=self.client.city,
                                                                  address='일산서구 대화동 킨텍스로 217-59',
                                                                  creator=self.client.user)
        self.client.jwt_response = self.post('/api-token-auth/',
                                             data={'username': 'testuser',
                                                   'password': 'password'})

        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.client.jwt_response.data["token"]}')

    def test_building_list(self):
        url = self.reverse('buildings-list')
        response = self.get(url)
        self.assertContains(response, '스타필드')
        self.assertContains(response, '킨텍스')
        self.assertContains(response, '경기도')
        self.assertContains(response, '고양')
        self.assertContains(response, 'Asia/Seoul')
        self.assertContains(response, 'goyang')

    def test_building_detail(self):
        url = self.reverse('buildings-detail', pk=1)
        response = self.get(url)
        serializer = BuildingReadSerializer(self.client.building1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data['is_enabled'])

    def test_building_detail_not_exists(self):
        url = self.reverse('buildings-detail', pk=5)
        response = self.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_building_create(self):
        url = self.reverse('buildings-list')
        payload = {
            'city': self.client.city.id,
            'name': '유효빌딩',
            'desc': '테스트 건물입니다.',
            'address': 'test_address'
        }
        # serializer = BuildingSerializer(payload)
        response = self.client.post(url, data=payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['creator'], 'testuser')

    def test_valid_building_create_with_image(self):
        url = self.reverse('buildings-list')
        payload = {
            'city': self.client.city.id,
            'name': '유효빌딩',
            'desc': '테스트 건물입니다.',
            'address': 'test_address',
            'img_src': generate_photo_file()
        }
        # serializer = BuildingSerializer(payload)
        response = self.client.post(url, data=payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_building_create(self):
        url = self.reverse('buildings-list')
        payload = {
            'name': '유효빌딩',
            'address': 'test_address'
        }
        # serializer = BuildingSerializer(payload)
        response = self.client.post(url, data=payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_disabled_building(self):
        url = self.reverse('buildings-detail', pk=self.client.building1.id)
        response = self.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_building_valid_payload(self):
        url = self.reverse('buildings-detail', pk=self.client.building1.id)
        updated_name = '빌딩 이름 수정되었어요'
        updated_address = '주소도 수정되었습니다'
        payload = {
            'name': updated_name,
            'address': updated_address
        }
        response = self.client.patch(url, data=payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, updated_name)
        self.assertContains(response, updated_address)
        self.assertEqual(1, BuildingHistory.objects.count())

    def test_update_building_invalid_payload(self):
        url = self.reverse('buildings-detail', pk=self.client.building1.id)
        payload = {
            'name': generate_photo_file()
        }
        response = self.client.patch(url, data=payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
