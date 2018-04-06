from rest_framework.test import APITestCase
from walkup_law.walkup_law.models import DBManager, Video, Channel, SubChannel, Season, VideoTag
from walkup_law.walkup_law import fixtures
from django.urls import reverse
from unittest import TestCase as TC
from walkup_law.users import models as UM
from rest_framework.authtoken.models import Token
from walkup_law.walkup_law import factories
from walkup_law.walkup_law.serializers import VideoSerializer
from rest_framework.response import Response
import json
from walkup_law.walkup_law.views import list_videos
from walkup_law.walkup_law.views import add_tag_to_video

class TelevisionViewTests(APITestCase):
    def setUp(self):
        self.dbm = DBManager()

        new_user = UM.User(name="testuser@test.com", password="1")
        new_user.is_staff = True
        new_user.save()
        self.test_user = UM.User.objects.get(pk=new_user.id)

    def tearDown(self):
        Video.objects.all().delete()
        Channel.objects.all().delete()
        SubChannel.objects.all().delete()
        Season.objects.all().delete()
        VideoTag.objects.all().delete()

    def test_create_video(self):
        url = reverse('create-video')

        # Include an appropriate `Authorization:` header on all requests.
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        len_videos = len(Video.objects.all())
        # test best case
        response_data = {"name": "video title",
                         "description": "video description",
                         "link": "https://slate.com"}
        response = self.client.post(url, data=response_data, format="json")

        self.assertEqual(response.status_code, 201)
        new_video_uuid = response.data.get('uuid')
        new_len_videos = len(Video.objects.all())
        assert new_len_videos > len_videos
        new_video_relookup = self.dbm.get_video_by_uuid(video_uuid=new_video_uuid)
        assert new_video_relookup is not None

        # test error cases

    def test_list_videos(self):
        video = factories.VideoFactory.build()
        video.save()
        # Include an appropriate `Authorization:` header on all requests.
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


        url = reverse('list-videos')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_add_channel_to_video(self):
        # video uuid: 43a10cdc-21fd-4030-850a-1b040d55312e
        # channel uuid 04a5ad99-b407-4aa4-8eaa-191ec531611f
        video = factories.VideoFactory.build()
        video.save()

        channel = factories.ChannelFactory.build()
        channel.save()
        # Include an appropriate `Authorization:` header on all requests.
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        video_uuid = Video.objects.all().first().uuid
        channel_uuid = Channel.objects.all().first().uuid

        url = reverse("add-channel-to-videos")
        response_data = {"video_uuid": video_uuid,
                         "channel_uuid": channel_uuid}

        # rando_channel = Video.objects.first().uuid

        response = self.client.post(url, data=response_data, format="json")

        get_video = Video.objects.filter(uuid=video_uuid).first()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(get_video.channel_uuid, channel_uuid)

    def test_add_sub_channel_to_video(self):
        # Include an appropriate `Authorization:` header on all requests.
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        video = factories.VideoFactory.build()
        video.save()

        sub_channel = factories.SubChannelFactory.build()
        sub_channel.save()

        video_uuid = Video.objects.first().uuid
        sub_channel_uuid = SubChannel.objects.first().uuid

        url = reverse("add-sub-channel-to-video")
        response_data = {"video_uuid": video_uuid,
                         "sub_channel_uuid": sub_channel_uuid}

        response = self.client.post(url, data=response_data, format="json")

        get_video = Video.objects.filter(uuid=video_uuid).first()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(get_video.sub_channel_uuid, sub_channel_uuid)

    def test_add_season_to_video(self):
        # Include an appropriate `Authorization:` header on all requests.
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        video = factories.VideoFactory.build()
        video.save()

        season = factories.SeasonFactory.build()
        season.save()

        video_uuid = Video.objects.first().uuid
        season_uuid = Season.objects.first().uuid

        url = reverse("add-season-to-video")

        response_data = {"video_uuid": video_uuid,
                         "season_uuid": season_uuid}

        response = self.client.post(url, data=response_data, format="json")
        get_video = Video.objects.filter(uuid=video_uuid).first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(get_video.season_uuid, season_uuid)

    def test_add_tag_to_video(self):
        # Include an appropriate `Authorization:` header on all requests.
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        video = factories.VideoFactory.build()
        video.save()

        tag = VideoTag.objects.create(name="tag name", description="tag description", uuid="tweegsdg434")
        tag.save()

        video_uuid = Video.objects.first().uuid
        tag_uuid = VideoTag.objects.first().uuid

        url = reverse("add-tag-to-video")

        response_data = {"video_uuid": video_uuid,
                         "tag_uuid": tag_uuid}

        response = self.client.post(url, data=response_data, format="json")
        get_video = Video.objects.filter(uuid=video_uuid).first()
        self.assertEqual(response.status_code, 201)
        post_tag_uuid = list(get_video.tags.keys())[0]
        self.assertEqual(post_tag_uuid, tag_uuid)


    def test_remove_tag_from_video(self):
        # This view accepts tag ID and video ID and then removes that tag from ID
        # CHECK: Returns correct code
        # CHECK: That deletes correctly by looking at size of Tags dict


        ###AUTH
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


        ### CREATE VIDEO AND TAG
        video = factories.VideoFactory.build()
        video.save()
        tag = VideoTag.objects.create(name="tag name", description="tag description", uuid="tweegsdg434")
        tag.save()

        video_uuid = Video.objects.filter(uuid=video.uuid).first().uuid
        tag_uuid = VideoTag.objects.filter(uuid='tweegsdg434').first().uuid

        ### ADD TAG TO VIDEO
        self.dbm.add_video_tag(video_uuid=video_uuid, tag_uuid=tag_uuid)
        video = Video.objects.filter(uuid=video_uuid).first()
        self.assertEquals(len(video.tags), 1)

        url = reverse("remove-tag-from-video")


        response_data = {"video_uuid": video_uuid,
                         "tag_uuid": tag_uuid}

        response = self.client.post(url, data=response_data, format="json")
        post_video = Video.objects.filter(uuid=video_uuid).first()

        ### ASSERTING THAT CORRECT RESPONSE CODE RETURNED AND THAT TAG WAS REMOVED
        self.assertEquals(len(post_video.tags), 0)
        self.assertEquals(response.status_code, 201)


    def test_create_channel(self):
        # TEST BY CHECKING FOR CORRECT RESPONSE CODE AND CORRECT NUMBER OF VIDEOS

        ###AUTH
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        ### CREATE CHANNEL

        response_data = {"name": "Name o Channel",
                         "description": "Takwando",
                         }

        url = reverse("create-channel")
        response = self.client.post(url, data=response_data, format="json")
        channel = Channel.objects.all().first()


        # ASSERT THAT CHANNEL HAS SAME NAME + DESCRIPTION AS PARAMETERS AND RESPONSE CODE IS 201
        self.assertEqual(channel.name, "Name o Channel")
        self.assertEqual(channel.description, "Takwando")
        self.assertEquals(response.status_code, 201)

    def test_list_channels(self):
        ### CHECK CORRECT NUMBER OF CHANNELS RETURN
        ### CHECK CORRECT RESPONSE CODE

        ### FACTORY CREATE CHANNELS
        channel_1 = factories.ChannelFactory.build()
        channel_1.save()

        channel_2 = factories.ChannelFactory.build()
        channel_2.save()

        ###AUTH
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        ### GET CHANNELS
        url = reverse('list-channels')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)

    def test_edit_channels(self):
        # CHECK BY ASSERTING PROPS ARE SAME AS PARAMS

        # CREATE CHANNELS
        channel = factories.ChannelFactory.build(name="Unedited Name", description="Unedited Description")
        channel.save()

        #AUTH
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # MAKE VIEW CALL
        response_data = {"channel_uuid": channel.uuid,
                         "name": "Edited Name",
                         "description": "Edited Description"
                        }

        url = reverse("edit-channel")
        response = self.client.post(url, data=response_data, format="json")

        # ASSERTS


        post_channel = Channel.objects.filter(uuid=channel.uuid).first()

        self.assertEqual(post_channel.name, "Edited Name")
        self.assertEqual(post_channel.description, "Edited Description")
        self.assertEqual(response.status_code, 201)

    def test_remove_channel(self):
        # CREATE CHANNELS
        channel = factories.ChannelFactory.build(name="Unedited Name", description="Unedited Description")
        channel.save()

        # AUTH
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        ##CALLS

        response_data = {"channel_uuid": channel.uuid}

        url = reverse("remove-channel")
        response = self.client.post(url, data=response_data, format="json")

        post_channel = Channel.objects.filter(uuid=channel.uuid)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(post_channel), 0)

    def test_create_sub_channel(self):
        # CREATE CHANNELS
        channel = factories.ChannelFactory.build(name="Unedited Name", description="Unedited Description")
        channel.save()

        # AUTH
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response_data = {"name" : "Nameo",
                         "description" : "Descrip",
                         "channel_uuid": channel.uuid}

        url = reverse("create-sub-channel")
        response = self.client.post(url, data=response_data, format="json")

        sub_channel = SubChannel.objects.all()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(sub_channel), 1)


    def test_list_sub_channels(self):

        ### CHECK CORRECT NUMBER OF CHANNELS RETURN
        ### CHECK CORRECT RESPONSE CODE

        ### FACTORY CREATE CHANNELS/SUBCHANNELS
        channel = factories.ChannelFactory.build()
        channel.save()

        sub_channel_1 = factories.SubChannelFactory.build(channel_uuid=channel.uuid)
        sub_channel_1.save()

        sub_channel_2 = factories.SubChannelFactory.build(channel_uuid=channel.uuid)
        sub_channel_2.save()

        ###AUTH
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        ### GET CHANNELS
        url = reverse('list-sub-channels')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)

    def test_remove_subchanel(self):
        ## CREATE SUBCHANNEL

        sub_channel = factories.SubChannelFactory.build()
        sub_channel.save()

        ###AUTH
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        ## CALLS

        url = reverse("remove-sub-channel")
        response_data = {"sub_channel_uuid": sub_channel.uuid}
        response = self.client.post(url, data=response_data, format="json")
        ### ASSERTS

        post_sub_channel = SubChannel.objects.all()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(post_sub_channel), 0)

    def test_edit_sub_channel(self):
        ## CREATE SUBCHANNEL

        channel = factories.ChannelFactory.build()
        channel.save()

        sub_channel = factories.SubChannelFactory.build(name="unedited name", description="unedited description")
        sub_channel.save()


        ###AUTH
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # MAKE VIEW CALL
        response_data = {"channel_uuid": channel.uuid,
                         "sub_channel_uuid": sub_channel.uuid,
                         "name": "Edited Name",
                         "description": "Edited Description"
                         }

        url = reverse("edit-sub-channel")
        response = self.client.post(url, data=response_data, format="json")

        # ASSERTS

        post_sub_channel = SubChannel.objects.filter(uuid=sub_channel.uuid).first()

        self.assertEqual(post_sub_channel.name, "Edited Name")
        self.assertEqual(post_sub_channel.description, "Edited Description")
        self.assertEqual(response.status_code, 201)

    def test_create_season(self):
        ##AUTH
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        ### CREATE CHANNEL + SUBCHANNEL
        channel = factories.ChannelFactory.build()
        channel.save()

        sub_channel = factories.SubChannelFactory.build()
        sub_channel.save()

        ### CREATE SEASON

        response_data = {"name": "Name o Season",
                         "description": "Season 1",
                         "channel_uuid": channel.uuid,
                         "sub_channel_uuid": sub_channel.uuid
                         }

        url = reverse("create-season")
        response = self.client.post(url, data=response_data, format="json")
        season = Season.objects.filter(channel_uuid=channel.uuid).first()
        season_len = len(Season.objects.all())

        # ASSERT THAT CHANNEL HAS SAME NAME + DESCRIPTION AS PARAMETERS IS LENGTH 1 AND RESPONSE CODE IS 201
        self.assertEqual(season_len, 1)
        self.assertEqual(season.name, "Name o Season")
        self.assertEqual(season.description, "Season 1")
        self.assertEquals(response.status_code, 201)

    def test_edit_season(self):
        ##AUTH
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        ### CREATE CHANNEL + SUBCHANNEL + SEASON
        channel = factories.ChannelFactory.build()
        channel.save()

        sub_channel = factories.SubChannelFactory.build()
        sub_channel.save()

        season = factories.SeasonFactory.build(name="Unedited", description="Unedited")
        season.save()

        ## MAKE CALL
        response_data = {"season_uuid": season.uuid,
                         "channel_uuid": channel.uuid,
                         "sub_channel_uuid": sub_channel.uuid,
                         "name": "Edited",
                         "description": "Edited"
                         }

        url = reverse("edit-season")
        response = self.client.post(url, data=response_data, format="json")

        post_season = Season.objects.get(uuid=season.uuid)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(post_season.name, "Edited")
        self.assertEqual(post_season.description, "Edited")

    def test_remove_season(self):
        ##AUTH
        Token.objects.create(user=self.test_user)
        token = Token.objects.get(user=self.test_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        ### CREATE SEASON
        season = factories.SeasonFactory.create()

        ### DELETE SEASON

        url = reverse("remove-season")
        response = self.client.post(url, data={"season_uuid": season.uuid}, format="json")

        ### ASSERT

        post_season = Season.objects.filter(uuid=season.uuid)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(post_season), 0)
