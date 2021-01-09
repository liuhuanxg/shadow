#-*-coding:utf-8 -*-
"""
@project:shadow
@File: init_data.py

初始化Engine数据
"""

from home.models import EngineScore
import config
import traceback


from django.core.management.base import BaseCommand, CommandError
class Command(BaseCommand):
    def handle(self, *args, **options):
        """"""
        self.insert_engine()

    def insert_engine(self):
        """初始化引擎数据"""
        try:
            print("------------insert engine start-----------------")
            engines = config.Engine_lst
            for engine  in engines:
                EngineScore.objects.create(
                    engine_name=engine
                )
            print("------------insert engine end-------------------")
        except:
            print("insert_engine error")
            print(traceback.format_exc())