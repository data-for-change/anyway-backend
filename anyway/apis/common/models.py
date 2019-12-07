import json
import datetime
import logging
from collections import namedtuple
from geoalchemy2 import Geometry
from six import iteritems
from sqlalchemy import (Column,
                        BigInteger,
                        Integer,
                        Boolean,
                        String,
                        Float,
                        DateTime,
                        Text,
                        Index,
                        desc,
                        sql,
                        func,
                        and_,
                        ForeignKeyConstraint
                        )

from sqlalchemy.orm import relationship, load_only
from sqlalchemy.dialects import postgresql

from anyway.core.localization import Localization
from anyway.core.utils import Utils
from anyway.core.constants import CONST
from anyway.core.database import Base
from anyway import db

MarkerResult = namedtuple('MarkerResult', ['accident_markers', 'rsa_markers', 'total_records'])
logging.basicConfig(level=logging.DEBUG)
db_encoding = 'utf-8'

class RoadSegment(Base):
    __tablename__ = "road_segments"
    id = Column(Integer(), primary_key=True, index=True)
    provider_and_id = Column(BigInteger(), nullable=True)
    provider_code = Column(Integer(), nullable=True)
    provider_code_hebrew = Column(Text(), nullable=True)
    file_type_police = Column(Integer(), nullable=True)
    accident_type = Column(Integer(), nullable=True)
    accident_type_hebrew = Column(Text(), nullable=True)
    accident_severity = Column(Integer(), nullable=True)
    accident_severity_hebrew = Column(Text(), nullable=True)
    accident_timestamp = Column(Text(), nullable=True)
    location_accuracy = Column(Text(), nullable=True)
    location_accuracy_hebrew = Column(Text(), nullable=True)
    road_type = Column(Integer(), nullable=True)
    road_type_hebrew = Column(Text(), nullable=True)
    road_shape = Column(Integer(), nullable=True)
    road_shape_hebrew = Column(Text(), nullable=True)
    day_type = Column(Integer(), nullable=True)
    day_type_hebrew = Column(Text(), nullable=True)
    police_unit = Column(Integer(), nullable=True)
    police_unit_hebrew = Column(Text(), nullable=True)
    one_lane = Column(Integer(), nullable=True)
    one_lane_hebrew = Column(Text(), nullable=True)
    multi_lane = Column(Integer(), nullable=True)
    multi_lane_hebrew = Column(Text(), nullable=True)
    speed_limit = Column(Integer(), nullable=True)
    speed_limit_hebrew = Column(Text(), nullable=True)
    road_intactness = Column(Integer(), nullable=True)
    road_intactness_hebrew = Column(Text(), nullable=True)
    road_width = Column(Integer(), nullable=True)
    road_width_hebrew = Column(Text(), nullable=True)
    road_sign = Column(Integer(), nullable=True)
    road_sign_hebrew = Column(Text(), nullable=True)
    road_light = Column(Integer(), nullable=True)
    road_light_hebrew = Column(Text(), nullable=True)
    road_control = Column(Integer(), nullable=True)
    road_control_hebrew = Column(Text(), nullable=True)
    weather = Column(Integer(), nullable=True)
    weather_hebrew = Column(Text(), nullable=True)
    road_surface = Column(Integer(), nullable=True)
    road_surface_hebrew = Column(Text(), nullable=True)
    road_object = Column(Integer(), nullable=True)
    road_object_hebrew = Column(Text(), nullable=True)
    object_distance = Column(Integer(), nullable=True)
    object_distance_hebrew = Column(Text(), nullable=True)
    didnt_cross = Column(Integer(), nullable=True)
    didnt_cross_hebrew = Column(Text(), nullable=True)
    cross_mode = Column(Integer(), nullable=True)
    cross_mode_hebrew = Column(Text(), nullable=True)
    cross_location = Column(Integer(), nullable=True)
    cross_location_hebrew = Column(Text(), nullable=True)
    cross_direction = Column(Integer(), nullable=True)
    cross_direction_hebrew = Column(Text(), nullable=True)
    road1 = Column(Integer(), nullable=True)
    road2 = Column(Integer(), nullable=True)
    km = Column(Float(), nullable=True)
    km_raw = Column(Float(), nullable=True)
    km_accurate = Column(Text(), nullable=True)
    yishuv_symbol = Column(Integer(), nullable=True)
    yishuv_name = Column(Text(), nullable=True)
    geo_area = Column(Integer(), nullable=True)
    geo_area_hebrew = Column(Text(), nullable=True)
    day_night = Column(Integer(), nullable=True)
    day_night_hebrew = Column(Text(), nullable=True)
    day_in_week = Column(Integer(), nullable=True)
    day_in_week_hebrew = Column(Text(), nullable=True)
    traffic_light = Column(Integer(), nullable=True)
    traffic_light_hebrew = Column(Text(), nullable=True)
    region = Column(Integer(), nullable=True)
    region_hebrew = Column(Text(), nullable=True)
    district = Column(Integer(), nullable=True)
    district_hebrew = Column(Text(), nullable=True)
    natural_area = Column(Integer(), nullable=True)
    natural_area_hebrew = Column(Text(), nullable=True)
    municipal_status = Column(Integer(), nullable=True)
    municipal_status_hebrew = Column(Text(), nullable=True)
    yishuv_shape = Column(Integer(), nullable=True)
    yishuv_shape_hebrew = Column(Text(), nullable=True)
    street1 = Column(Integer(), nullable=True)
    street1_hebrew = Column(Text(), nullable=True)
    street2 = Column(Integer(), nullable=True)
    street2_hebrew = Column(Text(), nullable=True)
    house_number = Column(Integer(), nullable=True)
    non_urban_intersection = Column(Integer(), nullable=True)
    non_urban_intersection_hebrew = Column(Text(), nullable=True)
    non_urban_intersection_by_junction_number = Column(Text(), nullable=True)
    urban_intersection = Column(Integer(), nullable=True)
    accident_year = Column(Integer(), nullable=True)
    accident_month = Column(Integer(), nullable=True)
    accident_day = Column(Integer(), nullable=True)
    accident_hour_raw = Column(Integer(), nullable=True)
    accident_hour_raw_hebrew = Column(Text(), nullable=True)
    accident_hour = Column(Integer(), nullable=True)
    accident_minute = Column(Integer(), nullable=True)
    geom = Column(Text(), nullable=True)
    longitude = Column(postgresql.DOUBLE_PRECISION(precision=53), nullable=True)
    latitude = Column(postgresql.DOUBLE_PRECISION(precision=53), nullable=True)
    x = Column(Float(), nullable=True)
    y = Column(Float(), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "provider_and_id": self.provider_and_id,
            "provider_code": self.provider_code,
            "provider_code_hebrew": self.provider_code_hebrew,
            "file_type_police": self.file_type_police,
            "accident_type": self.accident_type,
            "accident_type_hebrew": self.accident_type_hebrew,
            "accident_severity": self.accident_severity,
            "accident_severity_hebrew": self.accident_severity_hebrew,
            "accident_timestamp": self.accident_timestamp,
            "location_accuracy": self.location_accuracy,
            "location_accuracy_hebrew": self.location_accuracy_hebrew,
            "road_type": self.road_type,
            "road_type_hebrew": self.road_type_hebrew,
            "road_shape": self.road_shape,
            "road_shape_hebrew": self.road_shape_hebrew,
            "day_type": self.day_type,
            "day_type_hebrew": self.day_type_hebrew,
            "police_unit": self.police_unit,
            "police_unit_hebrew": self.police_unit_hebrew,
            "one_lane": self.one_lane,
            "one_lane_hebrew": self.one_lane_hebrew,
            "multi_lane": self.multi_lane,
            "multi_lane_hebrew": self.multi_lane_hebrew,
            "speed_limit": self.speed_limit,
            "speed_limit_hebrew": self.speed_limit_hebrew,
            "road_intactness": self.road_intactness,
            "road_intactness_hebrew": self.road_intactness_hebrew,
            "road_width": self.road_width,
            "road_width_hebrew": self.road_width_hebrew,
            "road_sign": self.road_sign,
            "road_sign_hebrew": self.road_sign_hebrew,
            "road_light": self.road_light,
            "road_light_hebrew": self.road_light_hebrew,
            "road_control": self.road_control,
            "road_control_hebrew": self.road_control_hebrew,
            "weather": self.weather,
            "weather_hebrew": self.weather_hebrew,
            "road_surface": self.road_surface,
            "road_surface_hebrew": self.road_surface_hebrew,
            "road_object": self.road_object,
            "road_object_hebrew": self.road_object_hebrew,
            "object_distance": self.object_distance,
            "object_distance_hebrew": self.object_distance_hebrew,
            "didnt_cross": self.didnt_cross,
            "didnt_cross_hebrew": self.didnt_cross_hebrew,
            "cross_mode": self.cross_mode,
            "cross_mode_hebrew": self.cross_mode_hebrew,
            "cross_location": self.cross_location,
            "cross_location_hebrew": self.cross_location_hebrew,
            "cross_direction": self.cross_direction,
            "cross_direction_hebrew": self.cross_direction_hebrew,
            "road1": self.road1,
            "road2": self.road2,
            "km": self.km,
            "km_raw": self.km_raw,
            "km_accurate": self.km_accurate,
            "yishuv_symbol": self.yishuv_symbol,
            "yishuv_name": self.yishuv_name,
            "geo_area": self.geo_area,
            "geo_area_hebrew": self.geo_area_hebrew,
            "day_night": self.day_night,
            "day_night_hebrew": self.day_night_hebrew,
            "day_in_week": self.day_in_week,
            "day_in_week_hebrew": self.day_in_week_hebrew,
            "traffic_light": self.traffic_light,
            "traffic_light_hebrew": self.traffic_light_hebrew,
            "region": self.region,
            "region_hebrew": self.region_hebrew,
            "district": self.district,
            "district_hebrew": self.district_hebrew,
            "natural_area": self.natural_area,
            "natural_area_hebrew": self.natural_area_hebrew,
            "municipal_status": self.municipal_status,
            "municipal_status_hebrew": self.municipal_status_hebrew,
            "yishuv_shape": self.yishuv_shape,
            "yishuv_shape_hebrew": self.yishuv_shape_hebrew,
            "street1": self.street1,
            "street1_hebrew": self.street1_hebrew,
            "street2": self.street2,
            "street2_hebrew": self.street2_hebrew,
            "house_number": self.house_number,
            "non_urban_intersection": self.non_urban_intersection,
            "non_urban_intersection_hebrew": self.non_urban_intersection_hebrew,
            "non_urban_intersection_by_junction_number": self.non_urban_intersection_by_junction_number,
            "urban_intersection": self.urban_intersection,
            "accident_year": self.accident_year,
            "accident_month": self.accident_month,
            "accident_day": self.accident_day,
            "accident_hour_raw": self.accident_hour_raw,
            "accident_hour_raw_hebrew": self.accident_hour_raw_hebrew,
            "accident_hour": self.accident_hour,
            "accident_minute": self.accident_minute,
            "geom": self.geom,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "x": self.x,
            "y": self.y
        }

class Point(object):
    id = Column(Integer(), primary_key=True)
    latitude = Column(Float())
    longitude = Column(Float())


class MarkerMixin(Point):
    type = Column(Integer())
    title = Column(String(100))
    created = Column(DateTime, default=datetime.datetime.now, index=True)

    __mapper_args__ = {
        'polymorphic_on': type
    }

    @staticmethod
    def format_description(field, value):
        # if the field's value is a static localizable field, fetch it.
        if field in Localization.get_supported_tables():
            value = Utils.decode_hebrew(Localization.get_field(field, value), db_encoding)
        name = Utils.decode_hebrew(Localization.get_field(field), db_encoding)
        return u"{0}: {1}".format(name, value)


class AccidentMarker(MarkerMixin, Base):
    __tablename__ = "markers"
    __table_args__ = (
        Index('acc_long_lat_idx', 'latitude', 'longitude'),
        Index('id_idx_markers', 'id', unique=False),
        Index('provider_and_id_idx_markers', 'provider_and_id', unique=False),
        Index('idx_markers_geom', 'geom', unique=False),

    )

    __mapper_args__ = {
        'polymorphic_identity': CONST.MARKER_TYPE_ACCIDENT
    }
    id = Column(BigInteger(), primary_key=True)
    provider_and_id = Column(BigInteger())
    provider_code = Column(Integer(), primary_key=True)
    file_type_police = Column(Integer())
    description = Column(Text())
    accident_type = Column(Integer())
    accident_severity = Column(Integer())
    address = Column(Text())
    location_accuracy = Column(Integer())
    road_type = Column(Integer())
    road_shape = Column(Integer())
    day_type = Column(Integer())
    police_unit = Column(Integer())
    mainStreet = Column(Text())
    secondaryStreet = Column(Text())
    junction = Column(Text())
    one_lane = Column(Integer())
    multi_lane = Column(Integer())
    speed_limit = Column(Integer())
    road_intactness = Column(Integer())
    road_width = Column(Integer())
    road_sign = Column(Integer())
    road_light = Column(Integer())
    road_control = Column(Integer())
    weather = Column(Integer())
    road_surface = Column(Integer())
    road_object = Column(Integer())
    object_distance = Column(Integer())
    didnt_cross = Column(Integer())
    cross_mode = Column(Integer())
    cross_location = Column(Integer())
    cross_direction = Column(Integer())
    involved = relationship("Involved")
    vehicles = relationship("Vehicle")
    video_link = Column(Text())
    road1 = Column(Integer())
    road2 = Column(Integer())
    km = Column(Float())
    km_raw = Column(Text())
    km_accurate = Column(Boolean())
    yishuv_symbol = Column(Integer())
    yishuv_name = Column(Text())
    geo_area = Column(Integer())
    day_night = Column(Integer())
    day_in_week = Column(Integer())
    traffic_light = Column(Integer())
    region = Column(Integer())
    district = Column(Integer())
    natural_area = Column(Integer())
    municipal_status = Column(Integer())
    yishuv_shape = Column(Integer())
    street1 = Column(Integer())
    street1_hebrew = Column(Text())
    street2 = Column(Integer())
    street2_hebrew = Column(Text())
    house_number = Column(Integer())
    urban_intersection = Column(Integer())
    non_urban_intersection = Column(Integer())
    non_urban_intersection_hebrew = Column(Text())
    accident_year = Column(Integer(), primary_key=True)
    accident_month = Column(Integer())
    accident_day = Column(Integer())
    accident_hour_raw = Column(Integer())
    accident_hour = Column(Integer())
    accident_minute = Column(Integer())
    x = Column(Float())
    y = Column(Float())
    vehicle_type_rsa = Column(Text())
    violation_type_rsa = Column(Text())
    geom = Column(Geometry('POINT'))
    non_urban_intersection_by_junction_number = Column(Text())

    @staticmethod
    def json_to_description(msg):
        description = json.loads(msg, encoding=db_encoding)
        return "\n".join([AccidentMarker.format_description(field, value) for field, value in iteritems(description)])

    def serialize(self, is_thin=False):
        fields = {
            "id": str(self.id),
            "provider_code": self.provider_code,
            "accident_year": self.accident_year,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "accident_severity": self.accident_severity,
            "location_accuracy": self.location_accuracy,
            "created": self.created.isoformat(),
        }
        if not is_thin:
            fields.update({
                "title": self.title,
                "address": self.address,
                "type": self.type,
                "accident_type": self.accident_type,
                "road_type": self.road_type,
                "road_shape": self.road_shape,
                "day_type": self.day_type,
                "police_unit": self.police_unit,
                "mainStreet": self.mainStreet,
                "secondaryStreet": self.secondaryStreet,
                "junction": self.junction,
            })
            # United Hatzala accidents description are not json:
            if self.provider_code == CONST.UNITED_HATZALA_CODE:
                fields.update({"description": self.description})
            else:
                fields.update({"description": AccidentMarker.json_to_description(self.description)})

            optional = {
                "one_lane": self.one_lane,
                "multi_lane": self.multi_lane,
                "speed_limit": self.speed_limit,
                "road_intactness": self.road_intactness,
                "road_width": self.road_width,
                "road_sign": self.road_sign,
                "road_light": self.road_light,
                "road_control": self.road_control,
                "weather": self.weather,
                "road_surface": self.road_surface,
                "road_object": self.road_object,
                "object_distance": self.object_distance,
                "didnt_cross": self.didnt_cross,
                "cross_mode": self.cross_mode,
                "cross_location": self.cross_location,
                "cross_direction": self.cross_direction,
                "video_link": self.video_link,
                "road1": self.road1,
                "road2": self.road2,
                "km": self.km
            }
            for name, value in iteritems(optional):
                if value != 0:
                    fields[name] = value
        return fields

    def update(self, data, current_user):
        self.title = data["title"]
        self.description = data["description"]
        self.type = data["type"]
        self.latitude = data["latitude"]
        self.longitude = data["longitude"]

        self.put()

    @staticmethod
    def bounding_box_query(is_thin=False, yield_per=None, involved_and_vehicles=False, **kwargs):
        from anyway.apis.common.models import MarkerResult, Involved, Vehicle
        approx = kwargs.get('approx', True)
        accurate = kwargs.get('accurate', True)
        page = kwargs.get('page')
        per_page = kwargs.get('per_page')

        if not kwargs.get('show_markers', True):
            return MarkerResult(accident_markers=db.session.query(AccidentMarker).filter(sql.false()),
                                rsa_markers=db.session.query(AccidentMarker).filter(sql.false()),
                                total_records=0)

        sw_lat = float(kwargs['sw_lat'])
        sw_lng = float(kwargs['sw_lng'])
        ne_lat = float(kwargs['ne_lat'])
        ne_lng = float(kwargs['ne_lng'])
        polygon_str = 'POLYGON(({0} {1},{0} {3},{2} {3},{2} {1},{0} {1}))'.format(sw_lng,
                                                                                  sw_lat,
                                                                                  ne_lng,
                                                                                  ne_lat)

        markers = db.session.query(AccidentMarker) \
            .filter(AccidentMarker.geom.intersects(polygon_str)) \
            .filter(AccidentMarker.created >= kwargs['start_date']) \
            .filter(AccidentMarker.created < kwargs['end_date']) \
            .filter(AccidentMarker.provider_code != CONST.RSA_PROVIDER_CODE) \
            .order_by(desc(AccidentMarker.created))

        rsa_markers = db.session.query(AccidentMarker) \
            .filter(AccidentMarker.geom.intersects(polygon_str)) \
            .filter(AccidentMarker.created >= kwargs['start_date']) \
            .filter(AccidentMarker.created < kwargs['end_date']) \
            .filter(AccidentMarker.provider_code == CONST.RSA_PROVIDER_CODE) \
            .order_by(desc(AccidentMarker.created))

        if not kwargs['show_rsa']:
            rsa_markers = db.session.query(AccidentMarker).filter(sql.false())

        if not kwargs['show_accidents']:
            markers = markers.filter(and_(AccidentMarker.provider_code != CONST.CBS_ACCIDENT_TYPE_1_CODE,
                                          AccidentMarker.provider_code != CONST.CBS_ACCIDENT_TYPE_3_CODE,
                                          AccidentMarker.provider_code != CONST.UNITED_HATZALA_CODE))

        if yield_per:
            markers = markers.yield_per(yield_per)
        if accurate and not approx:
            markers = markers.filter(AccidentMarker.location_accuracy == 1)
        elif approx and not accurate:
            markers = markers.filter(AccidentMarker.location_accuracy != 1)
        elif not accurate and not approx:
            return MarkerResult(accident_markers=db.session.query(AccidentMarker).filter(sql.false()),
                                rsa_markers=db.session.query(AccidentMarker).filter(sql.false()),
                                total_records=0)
        if not kwargs.get('show_fatal', True):
            markers = markers.filter(AccidentMarker.accident_severity != 1)
        if not kwargs.get('show_severe', True):
            markers = markers.filter(AccidentMarker.accident_severity != 2)
        if not kwargs.get('show_light', True):
            markers = markers.filter(AccidentMarker.accident_severity != 3)
        if kwargs.get('show_urban', 3) != 3:
            if kwargs['show_urban'] == 2:
                markers = markers.filter(AccidentMarker.road_type >= 1).filter(AccidentMarker.roadType <= 2)
            elif kwargs['show_urban'] == 1:
                markers = markers.filter(AccidentMarker.road_type >= 3).filter(AccidentMarker.roadType <= 4)
            else:
                return MarkerResult(accident_markers=db.session.query(AccidentMarker).filter(sql.false()),
                                    rsa_markers=rsa_markers,
                                    total_records=rsa_markers.count())
        if kwargs.get('show_intersection', 3) != 3:
            if kwargs['show_intersection'] == 2:
                markers = markers.filter(AccidentMarker.road_type != 2).filter(AccidentMarker.roadType != 4)
            elif kwargs['show_intersection'] == 1:
                markers = markers.filter(AccidentMarker.road_type != 1).filter(AccidentMarker.roadType != 3)
            else:
                return MarkerResult(accident_markers=db.session.query(AccidentMarker).filter(sql.false()),
                                    rsa_markers=rsa_markers,
                                    total_records=rsa_markers.count())
        if kwargs.get('show_lane', 3) != 3:
            if kwargs['show_lane'] == 2:
                markers = markers.filter(AccidentMarker.one_lane >= 2).filter(AccidentMarker.one_lane <= 3)
            elif kwargs['show_lane'] == 1:
                markers = markers.filter(AccidentMarker.one_lane == 1)
            else:
                return MarkerResult(accident_markers=db.session.query(AccidentMarker).filter(sql.false()),
                                    rsa_markers=rsa_markers,
                                    total_records=rsa_markers.count())

        if kwargs.get('show_day', 7) != 7:
            markers = markers.filter(func.extract("dow", AccidentMarker.created) == kwargs['show_day'])
        if kwargs.get('show_holiday', 0) != 0:
            markers = markers.filter(AccidentMarker.day_type == kwargs['show_holiday'])

        if kwargs.get('show_time', 24) != 24:
            if kwargs['show_time'] == 25:  # Daylight (6-18)
                markers = markers.filter(func.extract("hour", AccidentMarker.created) >= 6) \
                    .filter(func.extract("hour", AccidentMarker.created) < 18)
            elif kwargs['show_time'] == 26:  # Darktime (18-6)
                markers = markers.filter((func.extract("hour", AccidentMarker.created) >= 18) |
                                         (func.extract("hour", AccidentMarker.created) < 6))
            else:
                markers = markers.filter(func.extract("hour", AccidentMarker.created) >= kwargs['show_time']) \
                    .filter(func.extract("hour", AccidentMarker.created) < kwargs['show_time'] + 6)
        elif kwargs['start_time'] != 25 and kwargs['end_time'] != 25:
            markers = markers.filter(func.extract("hour", AccidentMarker.created) >= kwargs['start_time']) \
                .filter(func.extract("hour", AccidentMarker.created) < kwargs['end_time'])
        if kwargs.get('weather', 0) != 0:
            markers = markers.filter(AccidentMarker.weather == kwargs['weather'])
        if kwargs.get('road', 0) != 0:
            markers = markers.filter(AccidentMarker.road_shape == kwargs['road'])
        if kwargs.get('separation', 0) != 0:
            markers = markers.filter(AccidentMarker.multi_lane == kwargs['separation'])
        if kwargs.get('surface', 0) != 0:
            markers = markers.filter(AccidentMarker.road_surface == kwargs['surface'])
        if kwargs.get('acctype', 0) != 0:
            if kwargs['acctype'] <= 20:
                markers = markers.filter(AccidentMarker.accident_type == kwargs['acctype'])
            elif kwargs['acctype'] == CONST.BIKE_ACCIDENTS:
                markers = markers.filter(AccidentMarker.vehicles.any(Vehicle.vehicle_type == CONST.VEHICLE_TYPE_BIKE))
        if kwargs.get('controlmeasure', 0) != 0:
            markers = markers.filter(AccidentMarker.road_control == kwargs['controlmeasure'])
        if kwargs.get('district', 0) != 0:
            markers = markers.filter(AccidentMarker.police_unit == kwargs['district'])

        if kwargs.get('case_type', 0) != 0:
            markers = markers.filter(AccidentMarker.provider_code == kwargs['case_type'])

        if is_thin:
            markers = markers.options(load_only("id", "longitude", "latitude"))

        if kwargs.get('age_groups'):
            age_groups_list = kwargs.get('age_groups').split(',')
            markers = markers.filter(AccidentMarker.involved.any(Involved.age_group.in_(age_groups_list)))
        else:
            markers = db.session.query(AccidentMarker).filter(sql.false())
        total_records = markers.count() + rsa_markers.count()

        if page and per_page:
            markers = markers.offset((page - 1) * per_page).limit(per_page)

        if involved_and_vehicles:
            fetch_markers = kwargs.get('fetch_markers', True)
            fetch_vehicles = kwargs.get('fetch_vehicles', True)
            fetch_involved = kwargs.get('fetch_involved', True)
            markers_ids = [marker.id for marker in markers]
            markers = None
            vehicles = None
            involved = None
            if fetch_markers:
                markers = db.session.query(AccidentMarker).filter(AccidentMarker.id.in_(markers_ids))
            if fetch_vehicles:
                vehicles = db.session.query(Vehicle).filter(Vehicle.accident_id.in_(markers_ids))
            if fetch_involved:
                involved = db.session.query(Involved).filter(Involved.accident_id.in_(markers_ids))
            result = markers.all() if markers is not None else [], vehicles.all() if vehicles is not None else [], \
                     involved.all() if involved is not None else []
            return MarkerResult(accident_markers=result,
                                rsa_markers=db.session.query(AccidentMarker).filter(sql.false()),
                                total_records=len(result))
        else:
            return MarkerResult(accident_markers=markers,
                                rsa_markers=rsa_markers,
                                total_records=total_records)

    @staticmethod
    def get_marker(marker_id):
        return db.session.query(AccidentMarker).filter_by(id=marker_id)

    @classmethod
    def parse(cls, data):
        return AccidentMarker(
            type=CONST.MARKER_TYPE_ACCIDENT,
            title=data["title"],
            description=data["description"],
            latitude=data["latitude"],
            longitude=data["longitude"]
        )


class Involved(Base):
    __tablename__ = "involved"
    id = Column(BigInteger(), primary_key=True)
    provider_and_id = Column(BigInteger())
    provider_code = Column(Integer())
    file_type_police = Column(Integer())
    accident_id = Column(BigInteger())
    involved_type = Column(Integer())
    license_acquiring_date = Column(Integer())
    age_group = Column(Integer())
    sex = Column(Integer())
    vehicle_type = Column(Integer())
    safety_measures = Column(Integer())
    involve_yishuv_symbol = Column(Integer())
    involve_yishuv_name = Column(Text())
    injury_severity = Column(Integer())
    injured_type = Column(Integer())
    injured_position = Column(Integer())
    population_type = Column(Integer())
    home_region = Column(Integer())
    home_district = Column(Integer())
    home_natural_area = Column(Integer())
    home_municipal_status = Column(Integer())
    home_yishuv_shape = Column(Integer())
    hospital_time = Column(Integer())
    medical_type = Column(Integer())
    release_dest = Column(Integer())
    safety_measures_use = Column(Integer())
    late_deceased = Column(Integer())
    car_id = Column(Integer())
    involve_id = Column(Integer())
    accident_year = Column(Integer())
    accident_month = Column(Integer())
    injury_severity_mais = Column(Integer())
    __table_args__ = (ForeignKeyConstraint([accident_id, provider_code, accident_year],
                                           [AccidentMarker.id,
                                            AccidentMarker.provider_code,
                                            AccidentMarker.accident_year],
                                           ondelete="CASCADE"),
                      Index('accident_id_idx_involved', 'accident_id', unique=False),
                      Index('provider_and_id_idx_involved', 'provider_and_id', unique=False),
                      {})

    def serialize(self):
        return {
            "id": self.id,
            "provider_code": self.provider_code,
            "accident_id": self.accident_id,
            "involved_type": self.involved_type,
            "license_acquiring_date": self.license_acquiring_date,
            "age_group": self.age_group,
            "sex": self.sex,
            "vehicle_type": self.vehicle_type,
            "safety_measures": self.safety_measures,
            "involve_yishuv_symbol": self.involve_yishuv_symbol,
            "injury_severity": self.injury_severity,
            "injured_type": self.injured_type,
            "injured_position": self.injured_position,
            "population_type": self.population_type,
            "home_region": self.home_region,
            "home_district": self.home_district,
            "home_natural_area": self.home_natural_area,
            "home_municipal_status": self.home_municipal_status,
            "home_yishuv_shape": self.home_yishuv_shape,
            "hospital_time": self.hospital_time,
            "medical_type": self.medical_type,
            "release_dest": self.release_dest,
            "safety_measures_use": self.safety_measures_use,
            "late_deceased": self.late_deceased
        }

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(BigInteger(), primary_key=True)
    provider_and_id = Column(BigInteger())
    provider_code = Column(Integer())
    file_type_police = Column(Integer())
    accident_id = Column(BigInteger())
    engine_volume = Column(Integer())
    manufacturing_year = Column(Integer())
    driving_directions = Column(Integer())
    vehicle_status = Column(Integer())
    vehicle_attribution = Column(Integer())
    vehicle_type = Column(Integer())
    seats = Column(Integer())
    total_weight = Column(Integer())
    car_id = Column(Integer())
    accident_year = Column(Integer())
    accident_month = Column(Integer())
    vehicle_damage = Column(Integer())
    __table_args__ = (ForeignKeyConstraint([accident_id, provider_code, accident_year],
                                           [AccidentMarker.id,
                                            AccidentMarker.provider_code,
                                            AccidentMarker.accident_year],
                                           ondelete="CASCADE"),
                      Index('accident_id_idx_vehicles', 'accident_id', unique=False),
                      Index('provider_and_id_idx_vehicles', 'provider_and_id', unique=False),
                      {})

    def serialize(self):
        return {
            "id": self.id,
            "provider_code": self.provider_code,
            "accident_id": self.accident_id,
            "engine_volume": self.engine_volume,
            "manufacturing_year": self.manufacturing_year,
            "driving_directions": self.driving_directions,
            "vehicle_status": self.vehicle_status,
            "vehicle_attribution": self.vehicle_attribution,
            "vehicle_type": self.vehicle_type,
            "seats": self.seats,
            "total_weight": self.total_weight
        }

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
