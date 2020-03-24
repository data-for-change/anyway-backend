from anyway.core.database  import WazeBase
from sqlalchemy import Column, BigInteger, Integer, String, Boolean, Float, ForeignKey, DateTime, Text, Index, desc, \
    sql, Table, \
    ForeignKeyConstraint, func, and_, TIMESTAMP
from geoalchemy2 import Geometry

class WazeAlerts(WazeBase):
    __tablename__ = "waze_alerts"
    __table_args__ = (Index('ix_waze_waze_alerts_geom', 'geom', postgresql_using='gist'),)
    id = Column(BigInteger(), primary_key=True)
    city = Column(Text())
    confidence = Column(Integer())
    created_at = Column(DateTime, index=True)
    lontitude = Column(Float())
    latitude = Column(Float())
    magvar = Column(Integer())
    number_thumbs_up = Column(Integer())
    report_rating = Column(Integer())
    reliability = Column(Integer())
    alert_type = Column(Text())
    alert_subtype = Column(Text())
    uuid = Column(Text())
    street = Column(Text())
    road_type = Column(Integer())
    geom = Column(Geometry('POINT', srid=4326, spatial_index=False))

class WazeTrafficJams(WazeBase):
    __tablename__ = "waze_traffic_jams"
    __table_args__ = (Index('ix_waze_waze_traffic_jams_geom', 'geom', postgresql_using='gist'),)
    id = Column(BigInteger(), primary_key=True)
    level = Column(Integer())
    line = Column(Text())
    speed_kmh = Column(Integer())
    turn_type = Column(Integer())
    length = Column(Float())
    type = Column(Text())
    uuid = Column(Text())
    speed = Column(Integer())
    segments = Column(Text())
    road_type = Column(Integer())
    delay = Column(Integer())
    street = Column(Text())
    city = Column(Text())
    end_node = Column(Text())
    blocking_alert_uuid = Column(Text())
    start_node = Column(Text())
    created_at = Column(DateTime, index=True)
    geom = Column(Geometry('LINESTRING', srid=4326, spatial_index=False))
