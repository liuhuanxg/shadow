from django.db import models


# 用户数据表
class User(models.Model):
    class Meta:
        verbose_name = "普通用户"
        verbose_name_plural = "普通用户"

    username = models.CharField(max_length=32, unique=True, verbose_name="用户名")  # 不可以重复
    password = models.CharField(max_length=32, verbose_name="密码")
    nick_name = models.CharField(max_length=32, blank=True, null=True)
    gender = models.BooleanField(default=1, verbose_name="性别")
    phone = models.CharField(max_length=32, blank=True, null=True, unique=True, verbose_name="手机号")
    email = models.EmailField(blank=True, null=True, unique=True, verbose_name="邮箱")
    address = models.TextField(blank=True, null=True, verbose_name="地址")
    image = models.ImageField(upload_to='upload/user', default='upload/user/!happy-face.png', verbose_name="用户头像")

    def __str__(self):
        return self.username


# 词条名称
class KeyWords(models.Model):
    class Meta:
        verbose_name = "关键词"
        verbose_name_plural = "关键词"

    word_name = models.CharField(max_length=32, unique=True, verbose_name="关键词")  # 不可以重复
    label = models.CharField(max_length=32, verbose_name="标签", default="")
    pinyin = models.CharField(max_length=32)

    def __str__(self):
        return self.word_name


# 词条详情
class WordsDetail(models.Model):
    class Meta:
        verbose_name = "词条详情"
        verbose_name_plural = "词条详情"
        ordering = ("-score",)

    detail_name = models.TextField(verbose_name="词条简称", db_index=True, null=True)
    label = models.CharField(max_length=32, verbose_name="标签", null=True)
    pinyin = models.CharField(max_length=100, null=True)
    href = models.TextField(verbose_name="链接地址", unique=True)
    src = models.TextField(verbose_name="image链接", default="")
    key_id = models.ForeignKey("KeyWords", on_delete=models.CASCADE, verbose_name="所属关键词")
    content = models.TextField(verbose_name="详情", null=True)
    score = models.FloatField(verbose_name="权重", default=0)
    data_source = models.ForeignKey("EngineScore", on_delete=models.CASCADE, verbose_name="数据引擎")
    support_count = models.IntegerField(verbose_name="点赞数量", default=0)
    step_count = models.IntegerField(verbose_name="点踩数量", default=0)

    def __str__(self):
        return self.href


class ClickCount(models.Model):
    class Meta:
        verbose_name = "每日点击次数"
        verbose_name_plural = "每日点击次数"

    href = models.ForeignKey("WordsDetail", on_delete=models.CASCADE, verbose_name="链接")
    date = models.DateField(auto_now_add=True)
    count = models.IntegerField(verbose_name="点击次数", default=1)
    ips = models.TextField(verbose_name="ip来源", default="[]")


class EngineScore(models.Model):
    class Meta:
        verbose_name = "引擎权重"
        verbose_name_plural = "引擎权重"

    engine_name = models.CharField(max_length=30, verbose_name="引擎名称", unique=True)
    weight = models.FloatField(verbose_name="初始权重", default=0)
    click_number = models.IntegerField(verbose_name="点击多少次增加权重", default=10)
    praise_number = models.IntegerField(verbose_name="点赞多少次增加权重", default=10)
    praise_weight = models.FloatField(verbose_name="点赞时增加的权重", default=0.0001)
    step_number = models.IntegerField(verbose_name="点踩多少次减少权重", default=10)
    step_weight = models.IntegerField(verbose_name="点踩时增加权重", default=0.0001)

    @classmethod
    def get_one(cls, engine_name):
        engine = cls.objects.filter(engine_name=engine_name).first()
        return engine

    @classmethod
    def get_score(cls, engine_name, type):
        """取某个属性的值"""
        engine = cls.objects.filter(engine_name=engine_name).value_list(type).first()
        if engine:
            return engine
        return 0

    def __str__(self):
        return self.engine_name


class ActionRecord(models.Model):
    class Meta:
        verbose_name = "赞踩记录"
        verbose_name_plural = "赞踩记录"

    href = models.ForeignKey("WordsDetail", on_delete=models.CASCADE, verbose_name="链接")
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="用户")
    action = models.BooleanField("赞或踩", default=1)  # 1为赞，0为踩


class ComplaintType(models.Model):
    class Meta:
        verbose_name = "举报类型"
        verbose_name_plural = "举报类型"

    type_name = models.CharField(max_length=10, verbose_name="类型名称", unique=True)
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=1, verbose_name="是否启用")

    def __str__(self):
        return self.type_name


class ComplaintRecord(models.Model):
    class Meta:
        verbose_name = "投诉记录"
        verbose_name_plural = "投诉记录"

    href = models.ForeignKey("WordsDetail", on_delete=models.CASCADE, verbose_name="链接")
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="用户")
    types = models.CharField(max_length=100, default="[]")
    comment = models.TextField(verbose_name="投诉详情")
