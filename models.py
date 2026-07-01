"""
数据模型定义
车站 → 商务候车室 → 休息厅 三级结构
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Station(db.Model):
    """车站表（一级）"""
    __tablename__ = 'stations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, comment='车站名称')
    category = db.Column(db.String(20), nullable=True, comment='车站类别')
    bureau = db.Column(db.String(50), nullable=True, comment='所属路局')
    address = db.Column(db.String(200), nullable=True, comment='车站地址')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 一对多：车站 -> 候车室
    lounges = db.relationship('Lounge', backref='station', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_lounges=True):
        """转换为字典"""
        result = {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'bureau': self.bureau,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_lounges:
            result['lounges'] = [l.to_dict() for l in self.lounges]
        return result


class Lounge(db.Model):
    """商务候车室表（二级）- 对应【二级显示内容（原"贵宾室"现状）】"""
    __tablename__ = 'lounges'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id', ondelete='CASCADE'), nullable=False)

    # 基本信息
    name = db.Column(db.String(100), nullable=False, comment='候车室名称')
    location = db.Column(db.String(200), nullable=True, comment='位置')
    business_hours = db.Column(db.String(50), nullable=True, comment='营业时间')
    phone = db.Column(db.String(30), nullable=True, comment='联系电话')

    # 设施
    has_parking = db.Column(db.Boolean, default=False, comment='是否有独立停车区')
    parking_spots = db.Column(db.Integer, default=0, comment='停车位数')
    has_reception = db.Column(db.Boolean, default=False, comment='是否有接待台')
    service_staff = db.Column(db.Integer, default=0, comment='专职服务人员数')
    lounge_area = db.Column(db.String(20), nullable=True, comment='候车室面积')

    # 二级显示内容扩展字段（原"贵宾室"现状）
    security_device = db.Column(db.String(10), nullable=True, comment='安检设备设施设置情况')
    ticket_device = db.Column(db.String(20), nullable=True, comment='检票设备设施设置情况')
    has_independent_channel = db.Column(db.Boolean, default=False, comment='是否有独立的站外直接进入通道')
    platform_access = db.Column(db.String(50), nullable=True, comment='如何进入站台')
    can_access_public_hall = db.Column(db.Boolean, default=False, comment='是否能进入公共候车大厅通道')
    car_dropoff_channel = db.Column(db.String(50), nullable=True, comment='站外汽车专用落客通道情况')
    restroom_count = db.Column(db.String(10), nullable=True, comment='卫生间设置数量')
    has_operation_room = db.Column(db.Boolean, default=False, comment='是否有操作间')
    has_platform_map = db.Column(db.String(200), nullable=True, comment='车站平面图（预留）')

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 一对多：候车室 -> 休息厅
    rooms = db.relationship('Room', backref='lounge', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_rooms=True):
        """转换为字典"""
        result = {
            'id': self.id,
            'station_id': self.station_id,
            'name': self.name,
            'location': self.location,
            'businessHours': self.business_hours,
            'phone': self.phone,
            'hasParking': self.has_parking,
            'parkingSpots': self.parking_spots,
            'hasReception': self.has_reception,
            'serviceStaff': self.service_staff,
            'loungeArea': self.lounge_area,
            'securityDevice': self.security_device,
            'ticketDevice': self.ticket_device,
            'hasIndependentChannel': self.has_independent_channel,
            'platformAccess': self.platform_access,
            'canAccessPublicHall': self.can_access_public_hall,
            'carDropoffChannel': self.car_dropoff_channel,
            'restroomCount': self.restroom_count,
            'hasOperationRoom': self.has_operation_room,
            'hasPlatformMap': self.has_platform_map,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_rooms:
            result['rooms'] = [r.to_dict() for r in self.rooms]
        return result


class Room(db.Model):
    """休息厅表（三级）- 对应【一级显示内容（贵宾室整治情况统计）】"""
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lounge_id = db.Column(db.Integer, db.ForeignKey('lounges.id', ondelete='CASCADE'), nullable=False)

    # ===== 基本信息 =====
    name = db.Column(db.String(100), nullable=False, comment='休息厅名称')
    area = db.Column(db.String(20), nullable=True, comment='面积(m²)')

    # ===== 权属 & 建设（对应 G、H、I、J、K 列） =====
    ownership = db.Column(db.String(200), nullable=True, comment='权属主体（G列）')
    construction_investor = db.Column(db.String(200), nullable=True, comment='建设投资主体（I列）')
    construction_status = db.Column(db.String(50), nullable=True, comment='建设资产办理情况（J列）')
    construction_date = db.Column(db.String(20), nullable=True, comment='建设资产办理时间（K列）')

    # ===== 装修（对应 L、M、N、O 列） =====
    decoration_investor = db.Column(db.String(200), nullable=True, comment='装修出资主体（L列）')
    decoration_detail = db.Column(db.Text, nullable=True, comment='装修情况-不可移动设施明细（M列）')
    decoration_transfer_status = db.Column(db.String(100), nullable=True, comment='装修移交情况（N列）')
    decoration_transfer_date = db.Column(db.String(20), nullable=True, comment='装修办理时间（O列）')

    # ===== 装饰/家具（对应 P、Q、R、S 列） =====
    furniture_investor = db.Column(db.String(200), nullable=True, comment='装饰（家具）出资主体（P列）')
    furniture_detail = db.Column(db.Text, nullable=True, comment='装饰（家具）资产明细（Q列）')
    furniture_transfer_status = db.Column(db.String(100), nullable=True, comment='装饰（家具）移交情况（R列）')
    furniture_transfer_date = db.Column(db.String(20), nullable=True, comment='装饰（家具）办理时间（S列）')

    # ===== 功能调整（对应 T、U 列） =====
    function_adjust = db.Column(db.String(100), nullable=True, comment='功能调整情况（T列）')
    function_adjust_date = db.Column(db.String(20), nullable=True, comment='功能调整办理时间（U列）')

    # ===== 其他（对应 V、W 列） =====
    has_restroom = db.Column(db.Boolean, default=False, comment='是否有独立卫生间（V列）')
    photo_url = db.Column(db.String(500), nullable=True, comment='整改后照片URL（W列，预留）')

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'lounge_id': self.lounge_id,

            # 基本信息
            'name': self.name,
            'area': self.area,

            # 权属 & 建设
            'ownership': self.ownership,
            'constructionInvestor': self.construction_investor,
            'constructionStatus': self.construction_status,
            'constructionDate': self.construction_date,

            # 装修
            'decorationInvestor': self.decoration_investor,
            'decorationDetail': self.decoration_detail,
            'decorationTransferStatus': self.decoration_transfer_status,
            'decorationTransferDate': self.decoration_transfer_date,

            # 装饰/家具
            'furnitureInvestor': self.furniture_investor,
            'furnitureDetail': self.furniture_detail,
            'furnitureTransferStatus': self.furniture_transfer_status,
            'furnitureTransferDate': self.furniture_transfer_date,

            # 功能调整
            'functionAdjust': self.function_adjust,
            'functionAdjustDate': self.function_adjust_date,

            # 其他
            'hasRestroom': self.has_restroom,
            'photoUrl': self.photo_url,

            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }