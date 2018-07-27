from rest_framework import status
from rest_framework.test import APIRequestFactory
from test_plus import APITestCase

from building_post.models import BuildingPost
from building_post.serializers import BuildingPostReadSerializer
from building_post.tests.factories import BuildingPostFactory


class BuildingPostAPITests(APITestCase):
    def setUp(self):
        self.client.user = self.make_user()
        self.client.force_authenticate(user=self.client.user)
        self.factory = APIRequestFactory()

    def test_building_post_list(self):
        building_post = BuildingPostFactory()
        url = self.reverse('building-posts-list', building_pk=building_post.building_id)
        response = self.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, BuildingPost.objects.filter(is_enabled=True, building_id=building_post.building_id).count())
        self.assertContains(response, building_post.title)
        self.assertContains(response, building_post.content)

    def test_valid_post_create(self):
        building_post = BuildingPostFactory()
        url = self.reverse('building-posts-list', building_pk=building_post.building_id)
        payload = {
            'building': building_post.building_id,
            'title': '테스트건물 제목',
            'content': '테스트건물 내용'
        }
        response = self.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_post_create(self):
        building_post = BuildingPostFactory()
        url = self.reverse('building-posts-list', building_pk=building_post.building_id)
        payload = {
            'building': 30000,
            'title': '비정상 제목',
        }
        response = self.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_detail(self):
        building_post = BuildingPostFactory()
        url = self.reverse(
            'building-posts-detail',
            building_pk=building_post.building_id,
            pk=building_post.id,
        )
        request = self.factory.get(url)
        response = self.get(url)
        serializer = BuildingPostReadSerializer(building_post, context={'request': request})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data['is_enabled'])

    def test_post_detail_not_exists(self):
        building_post = BuildingPostFactory()
        url = self.reverse('building-posts-detail', building_pk=building_post.building_id, pk=-1)
        response = self.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post_valid_payload_not_have_permission(self):
        building_post = BuildingPostFactory()
        update_title = 'modify titlie'
        update_content = 'modify content'
        payload = {
            'title': update_title,
            'content': update_content,
        }
        url = self.reverse(
            'building-posts-detail',
            building_pk=building_post.building_id,
            pk=building_post.id,
        )
        response = self.patch(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_post_valid_payload_have_permission(self):
        building_post = BuildingPostFactory()
        self.client.force_authenticate(user=building_post.creator)
        update_title = 'modify titlie'
        update_content = 'modify content'
        payload = {
            'title': update_title,
            'content': update_content,
        }
        url = self.reverse(
            'building-posts-detail',
            building_pk=building_post.building_id,
            pk=building_post.id,
        )
        response = self.patch(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, update_title)
        self.assertContains(response, update_content)

    def test_disabled_building_post(self):
        building_post = BuildingPostFactory()
        url = self.reverse(
            'building-posts-detail',
            building_pk=building_post.building_id,
            pk=building_post.id,
        )
        response = self.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            self.get(url).status_code,
            status.HTTP_404_NOT_FOUND
        )
