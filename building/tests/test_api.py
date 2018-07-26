import io

from PIL import Image
from rest_framework import status
from rest_framework.test import APIRequestFactory
from test_plus import APITestCase

from building.models import Building, BuildingHistory
from building.serializers import BuildingReadSerializer
from building.tests.factories import BuildingFactory
from core.models import Cities, Country, States, Timezone
from core.tests.factories import CountryFactory, StatesFactory, TimezoneFactory, CitiesFactory


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
        self.client.force_authenticate(user=self.client.user)
        self.factory = APIRequestFactory()

    def test_building_list(self):
        building1 = BuildingFactory()
        building2 = BuildingFactory()
        url = self.reverse('buildings-list')
        response = self.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Building.objects.filter(is_enabled=True).count())
        self.assertContains(response, building1.name)
        self.assertContains(response, building2.name)

    def test_building_detail(self):
        building = BuildingFactory()
        url = self.reverse('buildings-detail', pk=1)
        request = self.factory.get(url)
        response = self.get(url)
        serializer = BuildingReadSerializer(building, context={'request': request})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data['is_enabled'])

    def test_building_detail_not_exists(self):
        url = self.reverse('buildings-detail', pk=5)
        response = self.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_building_create(self):
        city = CitiesFactory()
        url = self.reverse('buildings-list')
        payload = {
            'city': city.id,
            'name': '유효빌딩',
            'desc': '테스트 건물입니다.',
            'address': 'test_address'
        }
        # serializer = BuildingSerializer(payload)
        response = self.client.post(url, data=payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['creator'], 'testuser')

    def test_valid_building_create_with_image(self):
        city = CitiesFactory()
        url = self.reverse('buildings-list')
        payload = {
            'city': city.id,
            'name': '유효빌딩',
            'desc': '테스트 건물입니다.',
            'address': 'test_address',
            'img_src': generate_photo_file()
        }
        # serializer = BuildingSerializer(payload)
        response = self.post(url, data=payload, extra={'format': 'multipart'})
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
        building = BuildingFactory()
        url = self.reverse('buildings-detail', pk=building.id)
        response = self.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_building_valid_payload(self):
        building = BuildingFactory()
        url = self.reverse('buildings-detail', pk=building.id)
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
        self.assertEqual(1, BuildingHistory.objects.filter(is_enabled=True).count())

    def test_update_building_invalid_payload(self):
        building = BuildingFactory()
        url = self.reverse('buildings-detail', pk=building.id)
        payload = {
            'name': generate_photo_file()
        }
        response = self.client.patch(url, data=payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
