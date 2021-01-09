from django.contrib import admin
from home.models import *
from django.utils.html import format_html
import json

admin.site.site_header = '索影后台管理'
admin.site.site_title = '索影后台管理'


@admin.register(KeyWords)
class KeyWordsAdmin(admin.ModelAdmin):
    list_display = ["word_name", "label", "pinyin"]


@admin.register(WordsDetail)
class WordsDetailAdmin(admin.ModelAdmin):
    list_display = ["detail_name", "label", "score", "data_source", "support_count", "step_count", "href"]
    search_fields = ["detail_name"]


@admin.register(EngineScore)
class EngineScoreAdmin(admin.ModelAdmin):
    list_display = ["engine_name", "weight"]


@admin.register(ClickCount)
class ClickCountAdmin(admin.ModelAdmin):
    list_display = ["href_id", "count", "ips", "date"]
    date_hierarchy = "date"


@admin.register(ActionRecord)
class ActionRecordAdmin(admin.ModelAdmin):
    list_display = ["href", "user", "show_action"]

    def show_action(self, obj):
        if obj.action == 1:
            return "赞"
        else:
            return "踩"

    show_action.short_description = u'点赞说明'


@admin.register(ComplaintRecord)
class ComplaintRecordAdmin(admin.ModelAdmin):
    list_display = ["href", "user", "show_action"]

    def show_action(self, obj):
        print(type(obj.types))
        types = json.loads(obj.types)
        print(type(types))
        c_types = ComplaintType.objects.filter(id__in=types)
        print(c_types)
        lst = [c.type_name for c in c_types]
        return ",".join(lst)

    show_action.short_description = u'投诉类别'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "nick_name"]


@admin.register(ComplaintType)
class ComplaintTypeAdmin(admin.ModelAdmin):
    list_display = ["type_name", "status"]
