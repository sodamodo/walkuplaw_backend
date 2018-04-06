from walkup_law.walkup_law.models import DBManager, Video, Channel, SubChannel, Season, VideoTag
import unittest
# test the db manager

class TestManager(unittest.TestCase):

    def setUp(self):
        self.dbm = DBManager()


    def tearDown(self):
        Video.objects.all().delete()
        Channel.objects.all().delete()
        SubChannel.objects.all().delete()
        Season.objects.all().delete()
        VideoTag.objects.all().delete()

    def fake_create_channel(self):
        channel1 = Channel(name="fake_channel_name", description="fake_channel_description", uuid="randouuid")
        channel1.save()
        self.channel1 = channel1

    def fake_create_subchannel(self):
        subchannel1 = SubChannel(name="fake_subchannel_name", description="fake_subchannel_name", channel_uuid="notaulkuid", uuid="sgshgs")
        subchannel1.save()
        self.subchannel1 = subchannel1

    def fake_create_season(self):
        season1 = Season(name="Season 1",description="Season desc", uuid="gs2f2fmf2")
        season1.save()
        self.season1 = season1



    def build_standard_fake_videos(self):
        video1 = Video(name="fake_name_1", description="fake_description_1", link="fake_link_1", uuid="video1uuid", channel_uuid="channeluuid", sub_channel_uuid="tobeassigned", paid=False)
        video1.save()
        self.video1 = video1

        video2 = Video(name="fake_name_2", description="fake_description_2", link="fake_link_2")
        video2.save()
        self.video2 = video2

        video3 = Video(name="fake_name_3", description="fake_description_3", link="fake_link_3")
        video3.save()
        self.video3 = video3



    def test_create_video(self):
        video_name = "fake_channel"
        video_description = "fake_description"
        video_link = "fake_link"
        video = self.dbm.create_video(name=video_name, description=video_description, link=video_link)
        videos = Video.objects.all()
        self.assertEqual(len(videos), 1)
        self.assertEqual(video.name, video_name)
        self.assertEqual(video.link, video_link)
        self.assertEqual(video.description, video_description)

    def test_list_videos(self):
        # test without videos
        video_list = self.dbm.list_videos()
        self.assertEquals(len(video_list), 0)

        # test with videos
        self.build_standard_fake_videos()
        video_list = self.dbm.list_videos()
        self.assertGreater(len(video_list), 0)

    def test_get_video_by_uuid(self):
        self.build_standard_fake_videos()
        video = self.dbm.get_video_by_uuid(video_uuid=self.video1.uuid)
        bad_uuid = "tt443t3gsdgs"
        bad_video = self.dbm.get_video_by_uuid(bad_uuid)
        self.assertEquals(video.uuid, self.video1.uuid)
        self.assertEquals(bad_video, None)


    def test_set_video_channel(self):
        self.fake_create_channel()
        self.build_standard_fake_videos()
        video_new_channel = self.dbm.set_video_channel(video_uuid=self.video1.uuid, channel_uuid=self.channel1.uuid)
        self.assertEquals(self.channel1.uuid, video_new_channel.channel_uuid)

    def test_set_video_sub_channel(self):
        self.fake_create_channel()
        self.build_standard_fake_videos()
        self.fake_create_subchannel()
        video_new_subchannel = self.dbm.set_video_sub_channel(video_uuid=self.video1.uuid, sub_channel_uuid=self.subchannel1.uuid)
        self.assertEquals(self.subchannel1.uuid, video_new_subchannel.sub_channel_uuid)

    def test_set_video_season(self):
        self.fake_create_channel()
        self.build_standard_fake_videos()
        self.fake_create_season()
        video_new_season = self.dbm.set_video_season(video_uuid=self.video1.uuid, season_uuid=self.season1.uuid)
        self.assertEquals(self.season1.uuid, video_new_season.season_uuid)

    def test_add_video_tag(self):
        self.build_standard_fake_videos()
        fake_tag_uuid = "2hewtwhh352"
        self.dbm.add_video_tag(video_uuid=self.video1.uuid, tag_uuid=fake_tag_uuid)
        updated_tag = Video.objects.filter(uuid=self.video1.uuid).first()
        if fake_tag_uuid not in updated_tag.tags.keys():
            raise Exception('Tag not in tag dict')


    def test_remove_video_tag(self):
        self.build_standard_fake_videos()
        fake_tag_uuid = "2hewtwhhgsd34w352"

        ### Adding a tag to test delete functionality
        self.dbm.add_video_tag(video_uuid=self.video1.uuid, tag_uuid=fake_tag_uuid)
        ### removing tag
        self.dbm.remove_video_tag(video_uuid=self.video1.uuid, tag_uuid=fake_tag_uuid)
        updated_tag_set = Video.objects.filter(uuid=self.video1.uuid).first()

        if fake_tag_uuid in updated_tag_set.tags:
            raise Exception("the tag has not been deleted")

    def test_create_tag(self):
        tag_name = "Tag name"
        tag_desc =  "Tag Desc"
        new_tag = self.dbm.create_tag(name=tag_name, description=tag_desc)
        tags = VideoTag.objects.all()
        self.assertEqual(1, len(tags))
        self.assertEqual(tag_name, new_tag.name)
        self.assertEqual(tag_desc, new_tag.description)

    def test_edit_tag(self):
        name = "tag name"
        description = "tag description"
        uuid = "sgsd9gdsldh"

        tag = VideoTag(name=name, description=description, uuid=uuid)
        tag.save()

        new_name = "taggio"
        new_desc = "new description"

        self.dbm.edit_tag(tag_uuid=tag.uuid, name=new_name, description=new_desc)

        new_tag = VideoTag.objects.filter(uuid=tag.uuid).first()
        self.assertEqual(new_tag.name, new_name)
        self.assertEqual(new_tag.description, new_desc)


    def test_set_video_channel(self):

        self.fake_create_channel()
        self.build_standard_fake_videos()

        self.dbm.set_video_channel(self.video1.uuid, self.channel1.uuid)

        updated_video_uuid = Video.objects.filter(uuid=self.video1.uuid).first()
        self.assertEqual(self.video1.uuid, updated_video_uuid.uuid)


    def test_remove_video_tag(self):
        self.build_standard_fake_videos()

        name = "tag name"
        description = "tag description"
        uuid = "sgsd9gdsldh"

        tag = VideoTag(name=name, description=description, uuid=uuid)
        tag.save()

        #Add tag to video to have a tag to remove
        if self.video1.tags is None:
            self.video1.tags = {}
        self.video1.tags[tag.uuid] = tag.uuid
        self.video1.save()

        #check tag has been added
        self.assertEqual(len(self.video1.tags), 1)

        self.dbm.remove_video_tag(video_uuid=self.video1.uuid, tag_uuid=tag.uuid)
        updated_video = Video.objects.filter(uuid=self.video1.uuid).first()

        self.assertEqual(len(updated_video.tags), 0)

    def test_delete_tag(self):
        self.build_standard_fake_videos()

        name = "tag name"
        description = "tag description"
        uuid = "sgsd9gdsldh"

        tag = VideoTag(name=name, description=description, uuid=uuid)
        tag.save()

        self.dbm.delete_tag(tag_uuid=tag.uuid)
        self.assertEqual(len(VideoTag.objects.all()), 0)


    def test_get_tag_by_uuid(self):
        name ="tag name"
        description ="tag description"
        uuid = "sgsd9gdsldh"

        tag = VideoTag(name=name, description=description, uuid=uuid)
        tag.save()

        returned_tag = self.dbm.get_tag_by_uuid("sgsd9gdsldh")
        self.assertEqual(name, returned_tag.name)
        self.assertEqual(description, returned_tag.description)
        self.assertEqual(uuid, returned_tag.uuid)


    def test_create_channel(self):
        name = "namo"
        description = "descrip"
        uuid="t3toi4j"
        channel = Channel(name=name, description=description, uuid=uuid)
        channel.save()
        len(Channel.objects.all())
        self.assertEqual(len(Channel.objects.all()), 1)



    def test_list_channels(self):

        channel_list = self.dbm.list_channels()
        self.assertEqual(len(channel_list), 0)

        name = "namo"
        description = "descrip"
        uuid = "t3toi4j"
        channel = Channel(name=name, description=description, uuid=uuid)
        channel.save()

        populated_channel_list = Channel.objects.all()

        self.assertEqual(len(populated_channel_list), 1)

    def test_get_channel_by_uuid(self):
        name = "namo"
        description = "descrip"
        uuid = "t3toi4j"
        channel = Channel(name=name, description=description, uuid=uuid)
        channel.save()

        fetched_channel = self.dbm.get_channel_by_uuid(channel_uuid=channel.uuid)
        self.assertEqual(fetched_channel.uuid, channel.uuid)

    def test_remove_channel(self):

        name = "namo"
        description = "descrip"
        uuid = "t3toi4j"
        channel = Channel(name=name, description=description, uuid=uuid)
        channel.save()

        self.dbm.remove_channel(channel_uuid=channel.uuid)

        self.assertEqual(len(Channel.objects.all()), 0)

    def test_edit_channel(self):

        name = "namo"
        description = "descrip"
        uuid = "t3toi4j"
        channel = Channel(name=name, description=description, uuid=uuid)
        channel.save()
        new_channel_name = "New Channel"

        self.dbm.edit_channel(channel_uuid=uuid, name=new_channel_name, description=description)

        renamed_channel = Channel.objects.all().first()
        self.assertEqual(renamed_channel.name, new_channel_name)

    def test_create_sub_channel(self):
        name = "namo"
        description = "descrip"
        uuid = "t3toi4j"
        channel_uuid = "wtetwwte"


        self.assertEqual(len(Channel.objects.all()), 0)

        self.dbm.create_sub_channel(name=name, description=description, channel_uuid=channel_uuid)

        self.assertEqual(len(SubChannel.objects.all()), 1)


    def test_list_sub_channel(self):
        #no sub channels in DB
        subchannel_list = self.dbm.list_sub_channels()
        self.assertEqual(len(subchannel_list), 0)
        #with subchannel in DB
        name = "namo"
        description = "descrip"
        uuid = "t3toi4j"
        channel_uuid = "gwgwgwe"

        subchannel = SubChannel(name=name, description=description, uuid=uuid, channel_uuid=channel_uuid)
        subchannel.save()
        populated_subchannel_list = SubChannel.objects.all()
        self.assertEqual(len(populated_subchannel_list), 1)

    def get_sub_channel_by_uuid(self):
        name = "tag name"
        description = "tag description"
        uuid = "sgsd9gdsldh"
        channel_uuid = "wgsdsg"

        subchannel = SubChannel(name=name, description=description, uuid=uuid, channel_uuid=channel_uuid)
        subchannel.save()

        returned_subchannel = self.dbm.get_sub_channel_by_uuid(sub_channel_uuid=uuid)
        self.assertEqual(name, returned_subchannel.name)
        self.assertEqual(description, returned_subchannel.description)
        self.assertEqual(uuid, returned_subchannel.uuid)

    def test_remove_sub_channel(self):
        name = "namo"
        description = "descrip"
        uuid = "t3toi4j"
        channel_uuid = "kjsdlgjsldg"
        subchannel = SubChannel(name=name, description=description, uuid=uuid, channel_uuid=channel_uuid)
        subchannel.save()

        self.dbm.remove_sub_channel(sub_channel_uuid=uuid)

        self.assertEqual(len(SubChannel.objects.all()), 0)

    def test_edit_sub_channel(self):
        name = "namo"
        description = "descrip"
        uuid = "t3toi4j"
        channel_uuid = "kjsdlgjsldg"
        subchannel = SubChannel(name=name, description=description, uuid=uuid, channel_uuid=channel_uuid)
        subchannel.save()

        new_name = "zambino"

        self.dbm.edit_sub_channel(sub_channel_uuid=subchannel.uuid, name=new_name, description=description, channel_uuid=channel_uuid)

    def test_create_season(self):
        name = "namo"
        description = "descrip"
        channel_uuid = "t3toi4j"
        sub_channel_uuid = "gswsegse"
        self.assertEqual(len(Season.objects.all()), 0)
        self.dbm.create_season(name=name, description=description, sub_channel_uuid=sub_channel_uuid, channel_uuid=channel_uuid)
        self.assertEqual(len(Season.objects.all()), 1)

    def test_get_season_by_uuid(self):

        name = "namo"
        description = "descrip"
        sub_channel_uuid = "t3toi4j"
        channel_uuid = "tsweyre"
        uuid = "gssdgsd"
        season = Season(name=name, description=description, uuid=uuid, sub_channel_uuid=sub_channel_uuid, channel_uuid=channel_uuid)
        season.save()

        fetched_season = self.dbm.get_season_by_uuid(season_uuid=uuid)
        self.assertEqual(fetched_season.uuid, season.uuid)

    def test_edit_season(self):
        name = "namo"
        description = "descrip"
        sub_channel_uuid = "t3toi4j"
        channel_uuid = "tsweyre"
        uuid = "gssdgsd"
        season = Season(name=name, description=description, uuid=uuid, sub_channel_uuid=sub_channel_uuid,
                        channel_uuid=channel_uuid)
        season.save()
        new_season_name = "Season 2!"
        new_season = self.dbm.edit_season(season_uuid=uuid, channel_uuid=channel_uuid, sub_channel_uuid=sub_channel_uuid, name=new_season_name, description=description)

        self.assertEqual("Season 2!", new_season.name)

    def test_remove_season(self):
        name = "namo"
        description = "descrip"
        sub_channel_uuid = "t3toi4j"
        channel_uuid = "tsweyre"
        uuid = "gssdgsd"
        season = Season(name=name, description=description, uuid=uuid, sub_channel_uuid=sub_channel_uuid,
                        channel_uuid=channel_uuid)
        season.save()
        self.assertEqual(len(Season.objects.all()), 1)

        self.dbm.remove_season(season_uuid=uuid)

        self.assertEqual(len(Season.objects.all()), 0)
