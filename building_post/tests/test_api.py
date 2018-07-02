from rest_framework import status
from test_plus import APITestCase

from building.models import Building
from building_post.models import BuildingPost
from building_post.serializers import BuildingPostReadSerializer
from core.models import Country, States, Timezone, Cities


class BuildingPostAPITests(APITestCase):
    def setUp(self):
        self.client.user = self.make_user()
        self.client.jwt_response = self.post('/api-token-auth/',
                                             data={'username': 'testuser',
                                                   'password': 'password'})
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {self.client.jwt_response.data["token"]}')

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
        self.client.building_post1, _ = BuildingPost.objects.get_or_create(building=self.client.building1,
                                                                           title='스타필드 게시물',
                                                                           content='안녕하세요 스타필드 여러분',
                                                                           creator=self.client.user)
        self.client.building_post2, _ = BuildingPost.objects.get_or_create(building=self.client.building2,
                                                                           title='킨텍스 게시물',
                                                                           content='안녕하세요 킨텍스 여러분',
                                                                           creator=self.client.user)

    def test_building_post_list(self):
        url = self.reverse('building-posts', pk=self.client.building1.pk)
        response = self.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, BuildingPost.objects
                         .filter(is_enabled=True, building_id=self.client.building1.pk)
                         .count())
        self.assertContains(response, '스타필드 게시물')
        self.assertContains(response, '안녕하세요 스타필드 여러분')
        self.assertNotContains(response, '킨텍스 게시물')
        self.assertNotContains(response, '안녕하세요 킨텍스 여러분')

    def test_post_list(self):
        url = self.reverse('posts-list')
        response = self.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, BuildingPost.objects.filter(is_enabled=True).count())
        self.assertContains(response, '스타필드 게시물')
        self.assertContains(response, '안녕하세요 스타필드 여러분')
        self.assertContains(response, '킨텍스 게시물')
        self.assertContains(response, '안녕하세요 킨텍스 여러분')

    def test_valid_post_create(self):
        url = self.reverse('posts-list')
        payload = {
            'building': self.client.building1.pk,
            'title': '테스트건물 제목',
            'content': '테스트건물 내용'
        }
        response = self.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_post_create(self):
        url = self.reverse('posts-list')
        payload = {
            'building': 10983,
            'title': '비정상 제목'
        }
        response = self.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_detail(self):
        url = self.reverse('posts-detail', pk=self.client.building_post1.pk)
        response = self.get(url)
        serializer = BuildingPostReadSerializer(self.client.building_post1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data['is_enabled'])

    def test_post_detail_not_exists(self):
        url = self.reverse('posts-detail', pk=494949)
        response = self.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
