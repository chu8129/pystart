"""
环境变量模型 - Environment Variable Model
用于映射数据库中的 enviroments 表
"""

import datetime
from peewee import Model, CharField, TextField, DateTimeField
from provider.database import db


class Environment(Model):
    """环境变量表模型"""

    key = CharField(max_length=255, index=True, verbose_name="环境变量名")
    value = TextField(null=True, verbose_name="环境变量值")
    description = CharField(max_length=500, null=True, verbose_name="描述")
    created_at = DateTimeField(default=datetime.datetime.now, verbose_name="创建时间")
    updated_at = DateTimeField(default=datetime.datetime.now, verbose_name="更新时间")

    class Meta:
        database = db
        table_name = "enviroments"
        indexes = (("key",), True)

    def __str__(self):
        return f"Environment(key={self.key})"

    def __repr__(self):
        return f"Environment(id={self.id}, key={self.key})"
