from rest_framework import status
from rest_framework.test import APIRequestFactory
from test_plus import APITestCase

from building_post.tests.factories import BuildingPostFactory
from comment.models import BuildingPostComment
from comment.serializers import BuildingPostCommentReadSerializer
from comment.tests.factories import BuildingPostCommentFactory


class BuildingPostCommentAPITests(APITestCase):
    def setUp(self):
        self.client.user = self.make_user()
        self.client.force_authenticate(user=self.client.user)
        self.factory = APIRequestFactory()

    def test_building_post_comment_list(self):
        comment = BuildingPostCommentFactory()
        url = self.reverse(
            'building-post-comments-list',
            building_pk=comment.building_post.building_id,
            post_pk=comment.building_post_id,
        )
        response = self.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            1,
            BuildingPostComment.objects.filter(is_enabled=True, building_post_id=comment.building_post_id).count()
        )
        self.assertContains(response, comment.content)

    def test_valid_building_post_comment_create(self):
        building_post = BuildingPostFactory()
        url = self.reverse(
            'building-post-comments-list',
            building_pk=building_post.building_id,
            post_pk=building_post.id,
        )
        payload = {
            'building_post': building_post.id,
            'content': '안녕'
        }
        response = self.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertContains(response, payload['content'], status_code=201)

    def test_invalid_building_post_comment_create(self):
        building_post = BuildingPostFactory()
        url = self.reverse(
            'building-post-comments-list',
            building_pk=building_post.building_id,
            post_pk=building_post.id,
        )
        payload = {
            'building_post': building_post.id,
        }
        response = self.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_building_post_comment_detail(self):
        building_post_comment = BuildingPostCommentFactory()
        url = self.reverse(
            'building-post-comments-detail',
            building_pk=building_post_comment.building_post.building_id,
            post_pk=building_post_comment.building_post_id,
            pk=building_post_comment.id,
        )
        request = self.factory.get(url)
        response = self.get(url)
        serializer = BuildingPostCommentReadSerializer(building_post_comment, context={'request': request})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertTrue(response.data['is_enabled'])

    def test_building_post_comment_detail_not_exists(self):
        building_post = BuildingPostFactory()
        url = self.reverse(
            'building-post-comments-detail',
            building_pk=building_post.building_id,
            post_pk=building_post.id,
            pk=1,
        )
        response = self.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_building_post_comment(self):
        building_post_comment = BuildingPostCommentFactory()
        url = self.reverse(
            'building-post-comments-detail',
            building_pk=building_post_comment.building_post.building_id,
            post_pk=building_post_comment.building_post_id,
            pk=building_post_comment.id,
        )
        updated_content = 'modify content'
        payload = {
            'content': updated_content,
        }
        response = self.patch(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, updated_content)

    def test_disable_building_post_comment(self):
        building_post_comment = BuildingPostCommentFactory()
        url = self.reverse(
            'building-post-comments-detail',
            building_pk=building_post_comment.building_post.building_id,
            post_pk=building_post_comment.building_post_id,
            pk=building_post_comment.id,
        )
        response = self.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            self.get(url).status_code,
            status.HTTP_404_NOT_FOUND
        )
