# coding:utf-8
from db.mysql_model import BaseModel
from db.mysql_model.user import User

import datetime
from peewee import *


class RegistryImage(BaseModel):
    user = ForeignKeyField(User, verbose_name="user", related_name="registry_user", null=True)
    action = CharField(max_length=16, null=True)
    repository = CharField(max_length=72, verbose_name='仓库名称')
    tag = CharField(max_length=72, verbose_name='仓库标签')
    create_time = DateTimeField(default=datetime.datetime.now, verbose_name="时间")
