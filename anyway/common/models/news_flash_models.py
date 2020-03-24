from anyway.core.database import NewsFlashBase
from sqlalchemy import Column, BigInteger, Integer, String, Boolean, Float, ForeignKey, DateTime, Text, Index, desc, \
    sql, Table, \
    ForeignKeyConstraint, func, and_, TIMESTAMP


class NewsFlash(NewsFlashBase):
    __tablename__ = "news_flash"
    id = Column(BigInteger(), primary_key=True)
    accident = Column(Boolean(), nullable=True)
    author = Column(Text(), nullable=True)
    date = Column(TIMESTAMP(), nullable=True)
    description = Column(Text(), nullable=True)
    lat = Column(Float(), nullable=True)
    link = Column(Text(), nullable=True)
    lon = Column(Float(), nullable=True)
    road1 = Column(Float(), nullable=True)
    road2 = Column(Float(), nullable=True)
    resolution = Column(Text(), nullable=True)
    title = Column(Text(), nullable=True)
    source = Column(Text(), nullable=True)
    location = Column(Text(), nullable=True)
    tweet_id = Column(BigInteger(), nullable=True)
    region_hebrew = Column(Text(), nullable=True)
    district_hebrew = Column(Text(), nullable=True)
    yishuv_name = Column(Text(), nullable=True)
    street1_hebrew = Column(Text(), nullable=True)
    street2_hebrew  = Column(Text(), nullable=True)
    non_urban_intersection_hebrew = Column(Text(), nullable=True)
    road_segment_name = Column(Text(), nullable=True)
