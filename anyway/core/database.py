from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from anyway.core import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, convert_unicode=True, echo=False)

Base = declarative_base(metadata=MetaData(schema='public'))

CBSBase = declarative_base(metadata=MetaData(schema='cbs'))

NewsFlashBase = declarative_base(metadata=MetaData(schema='news_flash'))

SchoolshBase = declarative_base(metadata=MetaData(schema='schools'))

MobileAppBase = declarative_base(metadata=MetaData(schema='mobile_app'))

WazeBase = declarative_base(metadata=MetaData(schema='waze'))

schemas_ignored_in_migration = ['tiger', 'tiger_data', 'topology']

tables_ignored_in_migration = ['spatial_ref_sys']
