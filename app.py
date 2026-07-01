# app.py - 车站休息设施管理系统（完整版）
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
from io import BytesIO
import datetime
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 配置图片上传
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ==================== 数据结构 ====================
railway_data = {
    "国铁集团": {
        "北京局": {
            "北京车务段": {
                "北京南站": {
                    "station_name": "北京南站",
                    "basic_info": {
                        "省": "北京市",
                        "市": "北京市",
                        "区": "丰台区",
                        "街道": "南站街道",
                        "车站等级": "一级",
                        "车站类别": "客运站"
                    },
                    "business_waiting_rooms": [
                        {
                            "id": 1,
                            "public": {
                                "station_name": "北京南站",
                                "position": "站房南侧一层",
                                "checkin_equipment": "1套",
                                "ticket_check_equipment": "门式闸机",
                                "has_independent_channel": "是",
                                "platform_access": "通过候车大厅",
                                "can_access_public_hall": "是",
                                "car_dropoff": "停靠落客平台",
                                "has_independent_parking": "是",
                                "parking_spaces": 7,
                                "business_hours": "06:00-22:00",
                                "dedicated_staff": 3,
                                "contact_phone": "010-67561234",
                                "has_reception_desk": "是",
                                "toilet_count": "2处",
                                "has_operation_room": "是",
                                "floor_plan": ""
                            },
                            "lounges": [
                                {
                                    "id": 101,
                                    "name": "1号贵宾室01厅",
                                    "ownership": "北京局集团",
                                    "area": 120,
                                    "investment": "路局出资",
                                    "asset_status": "已移交铁路局集团公司无偿使用",
                                    "asset_date": "2020-06-30",
                                    "decoration_investment": "国铁企业装修",
                                    "decoration_items": "墙面贴装天然大理石；艺术灯5套",
                                    "decoration_transfer": "无偿移交",
                                    "decoration_date": "2020-06-30",
                                    "furniture_investment": "国铁企业装修",
                                    "furniture_items": "紫檀单人沙发10套约30万元；字画及屏风约200万元",
                                    "furniture_transfer": "投资方回收处置",
                                    "furniture_date": "2020-07-15",
                                    "function_adjust": "调整为'礼遇行'经营用房",
                                    "adjust_date": "2022-03-01",
                                    "has_independent_toilet": "是",
                                    "photo": ""
                                },
                                {
                                    "id": 102,
                                    "name": "1号贵宾室02厅",
                                    "ownership": "北京局集团",
                                    "area": 85,
                                    "investment": "路局出资",
                                    "asset_status": "已移交铁路局集团公司无偿使用",
                                    "asset_date": "2020-06-30",
                                    "decoration_investment": "国铁企业装修",
                                    "decoration_items": "木质软包；艺术画5幅",
                                    "decoration_transfer": "无偿移交",
                                    "decoration_date": "2020-06-30",
                                    "furniture_investment": "哈尔滨市市政府",
                                    "furniture_items": "高档家具一批",
                                    "furniture_transfer": "超标准装饰（家具），投资方按无偿使用交车站处理",
                                    "furniture_date": "2020-07-15",
                                    "function_adjust": "调整为商务座候车区",
                                    "adjust_date": "2022-03-01",
                                    "has_independent_toilet": "是",
                                    "photo": ""
                                }
                            ]
                        }
                    ],
                    "business_class_areas": [
                        {
                            "id": 1,
                            "name": "商务座候车区1",
                            "type": "高铁站",
                            "location": "A18检票口旁，站房南侧",
                            "construction_entity": "国铁",
                            "completion_time": "2020-12-01",
                            "area": 200,
                            "decoration_investment": "国铁",
                            "operation_mode": "自营",
                            "outsource_company": "",
                            "has_independent_channel": "是",
                            "checkin_ticket_verify": "安检/检票/验证一体",
                            "lounge1_area": 25,
                            "lounge2_area": 25,
                            "lounge3_area": 30
                        }
                    ],
                    "commercial_waiting_areas": [
                        {
                            "id": 1,
                            "name": "商业候车室",
                            "type": "高铁站",
                            "location": "候车大厅东侧",
                            "construction_entity": "国铁",
                            "completion_time": "2020-12-01",
                            "area": 150,
                            "decoration_investment": "国铁",
                            "outsource_company": "",
                            "operation_status": "营业",
                            "has_naming": "是",
                            "naming_unit": "中国银行",
                            "contract_end_date": "2026-12-31"
                        }
                    ]
                }
            }
        },
        "上海局": {
            "上海车务段": {
                "上海虹桥站": {
                    "station_name": "上海虹桥站",
                    "basic_info": {
                        "省": "上海市",
                        "市": "上海市",
                        "区": "闵行区",
                        "街道": "虹桥街道",
                        "车站等级": "一级",
                        "车站类别": "客运站"
                    },
                    "business_waiting_rooms": [
                        {
                            "id": 1,
                            "public": {
                                "station_name": "上海虹桥站",
                                "position": "站房西侧一层",
                                "checkin_equipment": "2套",
                                "ticket_check_equipment": "门式闸机",
                                "has_independent_channel": "是",
                                "platform_access": "通过专用通道",
                                "can_access_public_hall": "是",
                                "car_dropoff": "专用落客通道",
                                "has_independent_parking": "是",
                                "parking_spaces": 12,
                                "business_hours": "05:30-23:30",
                                "dedicated_staff": 5,
                                "contact_phone": "021-51234567",
                                "has_reception_desk": "是",
                                "toilet_count": "3处",
                                "has_operation_room": "是",
                                "floor_plan": ""
                            },
                            "lounges": [
                                {
                                    "id": 101,
                                    "name": "虹桥厅01",
                                    "ownership": "上海局集团",
                                    "area": 180,
                                    "investment": "路局出资",
                                    "asset_status": "已移交铁路局集团公司无偿使用",
                                    "asset_date": "2020-12-01",
                                    "decoration_investment": "国铁企业装修",
                                    "decoration_items": "墙面采用高级石材；水晶吊灯",
                                    "decoration_transfer": "无偿移交",
                                    "decoration_date": "2020-12-01",
                                    "furniture_investment": "国铁企业装修",
                                    "furniture_items": "高档皮质沙发；红木茶几",
                                    "furniture_transfer": "投资方回收处置",
                                    "furniture_date": "2020-12-15",
                                    "function_adjust": "调整为'礼遇行'经营用房",
                                    "adjust_date": "2022-06-01",
                                    "has_independent_toilet": "是",
                                    "photo": ""
                                }
                            ]
                        }
                    ],
                    "business_class_areas": [
                        {
                            "id": 1,
                            "name": "商务座候车区（西）",
                            "type": "高铁站",
                            "location": "西进站口北侧",
                            "construction_entity": "国铁",
                            "completion_time": "2021-06-01",
                            "area": 350,
                            "decoration_investment": "国铁",
                            "operation_mode": "业务外包",
                            "outsource_company": "北京悦途出行科技（集团）股份有限公司",
                            "has_independent_channel": "是",
                            "checkin_ticket_verify": "安检/检票/验证一体",
                            "lounge1_area": 40,
                            "lounge2_area": 35,
                            "lounge3_area": 30
                        }
                    ],
                    "commercial_waiting_areas": [
                        {
                            "id": 1,
                            "name": "商业候车室（东）",
                            "type": "高铁站",
                            "location": "候车大厅东侧",
                            "construction_entity": "国铁",
                            "completion_time": "2020-12-01",
                            "area": 200,
                            "decoration_investment": "国铁",
                            "outsource_company": "上海悦途实业发展有限公司",
                            "operation_status": "营业",
                            "has_naming": "是",
                            "naming_unit": "中国工商银行",
                            "contract_end_date": "2028-06-30"
                        }
                    ]
                },
                "杭州东站": {
                    "station_name": "杭州东站",
                    "basic_info": {
                        "省": "浙江省",
                        "市": "杭州市",
                        "区": "江干区",
                        "街道": "彭埠街道",
                        "车站等级": "一级",
                        "车站类别": "客运站"
                    },
                    "business_waiting_rooms": [
                        {
                            "id": 1,
                            "public": {
                                "station_name": "杭州东站",
                                "position": "站房南侧二层",
                                "checkin_equipment": "1套",
                                "ticket_check_equipment": "手持终端",
                                "has_independent_channel": "否",
                                "platform_access": "通过候车大厅",
                                "can_access_public_hall": "是",
                                "car_dropoff": "停靠落客平台",
                                "has_independent_parking": "否",
                                "parking_spaces": 0,
                                "business_hours": "06:00-22:30",
                                "dedicated_staff": 2,
                                "contact_phone": "0571-56789012",
                                "has_reception_desk": "是",
                                "toilet_count": "1处",
                                "has_operation_room": "否",
                                "floor_plan": ""
                            },
                            "lounges": [
                                {
                                    "id": 101,
                                    "name": "西湖厅",
                                    "ownership": "上海局集团",
                                    "area": 95,
                                    "investment": "路局出资",
                                    "asset_status": "已移交铁路局集团公司无偿使用",
                                    "asset_date": "2020-12-01",
                                    "decoration_investment": "国铁企业装修",
                                    "decoration_items": "木质软包；西湖主题壁画",
                                    "decoration_transfer": "无偿移交",
                                    "decoration_date": "2020-12-01",
                                    "furniture_investment": "国铁企业装修",
                                    "furniture_items": "实木家具；苏绣屏风",
                                    "furniture_transfer": "投资方按无偿使用交车站处理",
                                    "furniture_date": "2020-12-15",
                                    "function_adjust": "调整为商务座候车区",
                                    "adjust_date": "2022-03-01",
                                    "has_independent_toilet": "是",
                                    "photo": ""
                                }
                            ]
                        }
                    ],
                    "business_class_areas": [],
                    "commercial_waiting_areas": []
                }
            }
        },
        "广州局": {
            "广州车务段": {
                "广州南站": {
                    "station_name": "广州南站",
                    "basic_info": {
                        "省": "广东省",
                        "市": "广州市",
                        "区": "番禺区",
                        "街道": "钟村镇",
                        "车站等级": "一级",
                        "车站类别": "客运站"
                    },
                    "business_waiting_rooms": [
                        {
                            "id": 1,
                            "public": {
                                "station_name": "广州南站",
                                "position": "站房东侧一层",
                                "checkin_equipment": "2套",
                                "ticket_check_equipment": "门式闸机",
                                "has_independent_channel": "是",
                                "platform_access": "通过专用通道",
                                "can_access_public_hall": "是",
                                "car_dropoff": "专用落客通道",
                                "has_independent_parking": "是",
                                "parking_spaces": 15,
                                "business_hours": "05:30-23:00",
                                "dedicated_staff": 6,
                                "contact_phone": "020-61346300",
                                "has_reception_desk": "是",
                                "toilet_count": "4处",
                                "has_operation_room": "是",
                                "floor_plan": ""
                            },
                            "lounges": [
                                {
                                    "id": 101,
                                    "name": "红棉厅",
                                    "ownership": "广州局集团",
                                    "area": 136,
                                    "investment": "路局出资",
                                    "asset_status": "已移交铁路局集团公司无偿使用",
                                    "asset_date": "2023-12-26",
                                    "decoration_investment": "国铁企业装修",
                                    "decoration_items": "高级石材墙面；水晶吊灯",
                                    "decoration_transfer": "无偿移交",
                                    "decoration_date": "2023-12-26",
                                    "furniture_investment": "国铁企业装修",
                                    "furniture_items": "高档皮质沙发；红木家具",
                                    "furniture_transfer": "投资方回收处置",
                                    "furniture_date": "2023-12-30",
                                    "function_adjust": "调整为'礼遇行'经营用房",
                                    "adjust_date": "2024-03-01",
                                    "has_independent_toilet": "是",
                                    "photo": ""
                                },
                                {
                                    "id": 102,
                                    "name": "白云厅",
                                    "ownership": "广州局集团",
                                    "area": 238,
                                    "investment": "路局出资",
                                    "asset_status": "已移交铁路局集团公司无偿使用",
                                    "asset_date": "2023-12-26",
                                    "decoration_investment": "国铁企业装修",
                                    "decoration_items": "大理石墙面；水晶吊灯",
                                    "decoration_transfer": "无偿移交",
                                    "decoration_date": "2023-12-26",
                                    "furniture_investment": "国铁企业装修",
                                    "furniture_items": "高档沙发；实木茶几",
                                    "furniture_transfer": "投资方回收处置",
                                    "furniture_date": "2023-12-30",
                                    "function_adjust": "调整为商务座候车区",
                                    "adjust_date": "2024-03-01",
                                    "has_independent_toilet": "是",
                                    "photo": ""
                                }
                            ]
                        }
                    ],
                    "business_class_areas": [
                        {
                            "id": 1,
                            "name": "商务座候车区（南）",
                            "type": "高铁站",
                            "location": "南进站口东侧",
                            "construction_entity": "国铁",
                            "completion_time": "2024-12-01",
                            "area": 1438,
                            "decoration_investment": "国铁",
                            "operation_mode": "自营",
                            "outsource_company": "",
                            "has_independent_channel": "是",
                            "checkin_ticket_verify": "安检/检票/验证一体",
                            "lounge1_area": 50,
                            "lounge2_area": 45,
                            "lounge3_area": 40
                        }
                    ],
                    "commercial_waiting_areas": [
                        {
                            "id": 1,
                            "name": "悦途贵宾厅",
                            "type": "高铁站",
                            "location": "候车大厅B14-B18检票口上方夹层",
                            "construction_entity": "国铁",
                            "completion_time": "2012-09-29",
                            "area": 300,
                            "decoration_investment": "企业出资",
                            "outsource_company": "北京悦途出行科技（集团）股份有限公司",
                            "operation_status": "营业",
                            "has_naming": "是",
                            "naming_unit": "中国移动全球通",
                            "contract_end_date": "2027-04-16"
                        }
                    ]
                },
                "深圳北站": {
                    "station_name": "深圳北站",
                    "basic_info": {
                        "省": "广东省",
                        "市": "深圳市",
                        "区": "龙华区",
                        "街道": "民治街道",
                        "车站等级": "一级",
                        "车站类别": "客运站"
                    },
                    "business_waiting_rooms": [
                        {
                            "id": 1,
                            "public": {
                                "station_name": "深圳北站",
                                "position": "站房西侧一层",
                                "checkin_equipment": "1套",
                                "ticket_check_equipment": "门式闸机",
                                "has_independent_channel": "是",
                                "platform_access": "通过候车大厅",
                                "can_access_public_hall": "是",
                                "car_dropoff": "停靠落客平台",
                                "has_independent_parking": "是",
                                "parking_spaces": 8,
                                "business_hours": "06:30-23:00",
                                "dedicated_staff": 4,
                                "contact_phone": "0755-61370095",
                                "has_reception_desk": "是",
                                "toilet_count": "2处",
                                "has_operation_room": "是",
                                "floor_plan": ""
                            },
                            "lounges": [
                                {
                                    "id": 101,
                                    "name": "商务座候车室1",
                                    "ownership": "广州局集团",
                                    "area": 80,
                                    "investment": "路局出资",
                                    "asset_status": "已移交铁路局集团公司无偿使用",
                                    "asset_date": "2011-06-22",
                                    "decoration_investment": "国铁企业装修",
                                    "decoration_items": "墙面采用高级石材；木质软包",
                                    "decoration_transfer": "无偿移交",
                                    "decoration_date": "2011-06-22",
                                    "furniture_investment": "国铁企业装修",
                                    "furniture_items": "布艺沙发；实木茶几",
                                    "furniture_transfer": "投资方回收处置",
                                    "furniture_date": "2011-07-15",
                                    "function_adjust": "调整为商务座候车区",
                                    "adjust_date": "2020-12-01",
                                    "has_independent_toilet": "否",
                                    "photo": ""
                                }
                            ]
                        }
                    ],
                    "business_class_areas": [
                        {
                            "id": 1,
                            "name": "商务座候车区3",
                            "type": "高铁站",
                            "location": "候车室A9检票口旁",
                            "construction_entity": "国铁",
                            "completion_time": "2011-06-22",
                            "area": 340,
                            "decoration_investment": "企业出资",
                            "operation_mode": "委托服务",
                            "outsource_company": "广州龙腾出行网络科技有限公司",
                            "has_independent_channel": "是",
                            "checkin_ticket_verify": "安检/检票/验证一体",
                            "lounge1_area": 30,
                            "lounge2_area": 25,
                            "lounge3_area": 20
                        }
                    ],
                    "commercial_waiting_areas": [
                        {
                            "id": 1,
                            "name": "悦途商务休息室",
                            "type": "高铁站",
                            "location": "候车室A9检票口旁",
                            "construction_entity": "国铁",
                            "completion_time": "2011-06-22",
                            "area": 225,
                            "decoration_investment": "企业出资",
                            "outsource_company": "北京悦途出行科技（集团）股份有限公司",
                            "operation_status": "营业",
                            "has_naming": "是",
                            "naming_unit": "广发银行",
                            "contract_end_date": "2026-12-31"
                        }
                    ]
                }
            }
        }
    }
}

current_path = {"railway": "国铁集团", "bureau": "北京局", "section": "北京车务段", "station": "北京南站"}

id_counters = {}


def init_counters_for_station(station_key):
    if station_key not in id_counters:
        id_counters[station_key] = {
            "business_waiting_rooms": 1,
            "lounges": 1,
            "business_class_areas": 1,
            "commercial_waiting_areas": 1
        }


def get_station_by_path(railway, bureau, section, station):
    try:
        return railway_data[railway][bureau][section][station]
    except:
        return None


def init_sample_data():
    for railway in railway_data:
        for bureau in railway_data[railway]:
            for section in railway_data[railway][bureau]:
                for station in railway_data[railway][bureau][section]:
                    station_key = f"{railway}_{bureau}_{section}_{station}"
                    init_counters_for_station(station_key)


# ==================== 选项数据 ====================
OPTIONS = {
    "asset_status": ["已移交铁路局集团公司无偿使用", "XX站与XX政府、企业协商，按无偿使用处理", "XX政府、企业自行处置"],
    "decoration_transfer": ["无偿移交", "有偿移交", "投资方回收处置", "超标准装饰投资方回收处置",
                            "其他可移动资产投资方回收处置", "协商中"],
    "furniture_transfer": [
        "超标准装饰（家具），投资方回收处置",
        "超标准装饰（家具），投资方按无偿使用交车站处理",
        "其他可移动资产，投资方回收处置",
        "其他可移动资产，投资方按无偿使用交车站处理"
    ],
    "function_adjust": [
        "调整为'礼遇行'经营用房",
        "调整为商务座候车区",
        "调整为'四区一室'（商务座候车区除外）服务用房",
        "调整为车站生产生活用房",
        "其他用房"
    ],
    "has_independent_toilet": ["是", "否"],
    "checkin_equipment": ["1套", "2套"],
    "ticket_check_equipment": ["门式闸机", "柱式闸机", "手持终端", "人工检票"],
    "has_independent_channel": ["是", "否"],
    "platform_access": ["通过候车大厅", "通过专用通道", "通过站台楼梯"],
    "can_access_public_hall": ["是", "否"],
    "car_dropoff": ["停靠落客平台", "专用落客通道", "站前广场落客", "无专用通道"],
    "has_independent_parking": ["是", "否"],
    "has_reception_desk": ["是", "否"],
    "toilet_count": ["0处", "1处", "2处", "3处", "4处", "5处", "6处"],
    "has_operation_room": ["是", "否"],
    "class_type": ["高铁站", "高普混", "普速站"],
    "construction_entity": ["国铁", "铁路局", "地方政府", "投资企业"],
    "operation_mode": ["自营", "业务外包", "委托服务", "合作"],
    "operation_status": ["营业", "停业", "改建", "新建", "暂停", "未启用"],
    "has_naming": ["是", "否"]
}


# ==================== API路由 ====================
@app.route('/api/get_tree_data')
def get_tree_data():
    return jsonify(railway_data)


@app.route('/api/get_options')
def get_options():
    return jsonify(OPTIONS)


@app.route('/api/get_station_list')
def get_station_list():
    path = request.args.get('path', '[]')
    node_type = request.args.get('type', 'railway')

    try:
        path = json.loads(path)
    except:
        path = []

    stations = []
    if len(path) == 0:
        return jsonify(stations)

    try:
        data = railway_data
        for node in path:
            if node in data:
                data = data[node]
            else:
                return jsonify(stations)

        if node_type == 'station':
            stations.append({'railway': path[0], 'bureau': path[1], 'section': path[2], 'station': path[3]})
        elif node_type == 'section':
            for station in data:
                stations.append({'railway': path[0], 'bureau': path[1], 'section': path[2], 'station': station})
        elif node_type == 'bureau':
            for section in data:
                for station in data[section]:
                    stations.append({'railway': path[0], 'bureau': path[1], 'section': section, 'station': station})
        else:
            for bureau in data:
                for section in data[bureau]:
                    for station in data[bureau][section]:
                        stations.append({'railway': path[0], 'bureau': bureau, 'section': section, 'station': station})
    except Exception as e:
        print(f"Error: {e}")

    return jsonify(stations)


@app.route('/api/get_station_data')
def get_station_data():
    railway = request.args.get('railway', '国铁集团')
    bureau = request.args.get('bureau', '北京局')
    section = request.args.get('section', '北京车务段')
    station = request.args.get('station', '北京南站')
    station_data = get_station_by_path(railway, bureau, section, station)
    if station_data:
        return jsonify(station_data)
    return jsonify({"status": "error"}), 404


@app.route('/api/get_current_path', methods=['GET'])
def get_current_path():
    return jsonify(current_path)


@app.route('/api/set_current_path', methods=['POST'])
def set_current_path():
    data = request.json
    global current_path
    current_path = data
    return jsonify({"status": "success"})


# ==================== 商务候车室CRUD ====================
@app.route('/api/business_waiting_room/add', methods=['POST'])
def add_business_waiting_room():
    data = request.json
    railway = data.get('railway')
    bureau = data.get('bureau')
    section = data.get('section')
    station = data.get('station')
    room_data = data.get('room', {})

    station_data = get_station_by_path(railway, bureau, section, station)
    if not station_data:
        return jsonify({"status": "error", "message": "车站不存在"}), 404

    station_key = f"{railway}_{bureau}_{section}_{station}"
    init_counters_for_station(station_key)

    new_id = id_counters[station_key]['business_waiting_rooms']
    id_counters[station_key]['business_waiting_rooms'] += 1

    room_data['id'] = new_id
    room_data['lounges'] = room_data.get('lounges', [])

    station_data['business_waiting_rooms'].append(room_data)
    return jsonify({"status": "success", "id": new_id, "room": room_data})


@app.route('/api/business_waiting_room/<int:room_id>', methods=['PUT'])
def update_business_waiting_room(room_id):
    data = request.json
    railway = data.get('railway')
    bureau = data.get('bureau')
    section = data.get('section')
    station = data.get('station')
    room_data = data.get('room', {})

    station_data = get_station_by_path(railway, bureau, section, station)
    if not station_data:
        return jsonify({"status": "error", "message": "车站不存在"}), 404

    for i, room in enumerate(station_data['business_waiting_rooms']):
        if room['id'] == room_id:
            room_data['id'] = room_id
            room_data['lounges'] = room_data.get('lounges', [])
            station_data['business_waiting_rooms'][i] = room_data
            return jsonify({"status": "success"})

    return jsonify({"status": "error", "message": "房间不存在"}), 404


@app.route('/api/business_waiting_room/<int:room_id>', methods=['DELETE'])
def delete_business_waiting_room(room_id):
    data = request.json
    railway = data.get('railway')
    bureau = data.get('bureau')
    section = data.get('section')
    station = data.get('station')

    station_data = get_station_by_path(railway, bureau, section, station)
    if not station_data:
        return jsonify({"status": "error", "message": "车站不存在"}), 404

    station_data['business_waiting_rooms'] = [r for r in station_data['business_waiting_rooms'] if r['id'] != room_id]
    return jsonify({"status": "success"})


# ==================== 休息厅CRUD ====================
@app.route('/api/lounge/add', methods=['POST'])
def add_lounge():
    data = request.json
    railway = data.get('railway')
    bureau = data.get('bureau')
    section = data.get('section')
    station = data.get('station')
    room_id = data.get('room_id')
    lounge_data = data.get('lounge', {})

    station_data = get_station_by_path(railway, bureau, section, station)
    if not station_data:
        return jsonify({"status": "error", "message": "车站不存在"}), 404

    station_key = f"{railway}_{bureau}_{section}_{station}"
    init_counters_for_station(station_key)

    for room in station_data['business_waiting_rooms']:
        if room['id'] == room_id:
            new_id = id_counters[station_key]['lounges']
            id_counters[station_key]['lounges'] += 1
            lounge_data['id'] = new_id
            room['lounges'].append(lounge_data)
            return jsonify({"status": "success", "id": new_id, "lounge": lounge_data})

    return jsonify({"status": "error", "message": "商务候车室不存在"}), 404


@app.route('/api/lounge/<int:lounge_id>', methods=['PUT'])
def update_lounge(lounge_id):
    data = request.json
    railway = data.get('railway')
    bureau = data.get('bureau')
    section = data.get('section')
    station = data.get('station')
    room_id = data.get('room_id')
    lounge_data = data.get('lounge', {})

    station_data = get_station_by_path(railway, bureau, section, station)
    if not station_data:
        return jsonify({"status": "error", "message": "车站不存在"}), 404

    for room in station_data['business_waiting_rooms']:
        if room['id'] == room_id:
            for i, lounge in enumerate(room['lounges']):
                if lounge['id'] == lounge_id:
                    lounge_data['id'] = lounge_id
                    room['lounges'][i] = lounge_data
                    return jsonify({"status": "success"})

    return jsonify({"status": "error", "message": "休息厅不存在"}), 404


@app.route('/api/lounge/<int:lounge_id>', methods=['DELETE'])
def delete_lounge(lounge_id):
    data = request.json
    railway = data.get('railway')
    bureau = data.get('bureau')
    section = data.get('section')
    station = data.get('station')
    room_id = data.get('room_id')

    station_data = get_station_by_path(railway, bureau, section, station)
    if not station_data:
        return jsonify({"status": "error", "message": "车站不存在"}), 404

    for room in station_data['business_waiting_rooms']:
        if room['id'] == room_id:
            room['lounges'] = [l for l in room['lounges'] if l['id'] != lounge_id]
            return jsonify({"status": "success"})

    return jsonify({"status": "error", "message": "休息厅不存在"}), 404


# ==================== 商务座候车区CRUD ====================
@app.route('/api/business_class_area/add', methods=['POST'])
def add_business_class_area():
    data = request.json
    railway = data.get('railway')
    bureau = data.get('bureau')
    section = data.get('section')
    station = data.get('station')
    area_data = data.get('area', {})

    station_data = get_station_by_path(railway, bureau, section, station)
    if not station_data:
        return jsonify({"status": "error", "message": "车站不存在"}), 404

    station_key = f"{railway}_{bureau}_{section}_{station}"
    init_counters_for_station(station_key)

    new_id = id_counters[station_key]['business_class_areas']
    id_counters[station_key]['business_class_areas'] += 1
    area_data['id'] = new_id

    station_data['business_class_areas'].append(area_data)
    return jsonify({"status": "success", "id": new_id, "area": area_data})


@app.route('/api/business_class_area/<int:area_id>', methods=['PUT'])
def update_business_class_area(area_id):
    data = request.json
    railway = data.get('railway')
    bureau = data.get('bureau')
    section = data.get('section')
    station = data.get('station')
    area_data = data.get('area', {})

    station_data = get_station_by_path(railway, bureau, section, station)
    if not station_data:
        return jsonify({"status": "error", "message": "车站不存在"}), 404

    for i, area in enumerate(station_data['business_class_areas']):
        if area['id'] == area_id:
            area_data['id'] = area_id
            station_data['business_class_areas'][i] = area_data
            return jsonify({"status": "success"})

    return jsonify({"status": "error", "message": "商务座候车区不存在"}), 404


@app.route('/api/business_class_area/<int:area_id>', methods=['DELETE'])
def delete_business_class_area(area_id):
    data = request.json
    railway = data.get('railway')
    bureau = data.get('bureau')
    section = data.get('section')
    station = data.get('station')

    station_data = get_station_by_path(railway, bureau, section, station)
    if not station_data:
        return jsonify({"status": "error", "message": "车站不存在"}), 404

    station_data['business_class_areas'] = [a for a in station_data['business_class_areas'] if a['id'] != area_id]
    return jsonify({"status": "success"})


# ==================== 商业候车区CRUD ====================
@app.route('/api/commercial_area/add', methods=['POST'])
def add_commercial_area():
    data = request.json
    railway = data.get('railway')
    bureau = data.get('bureau')
    section = data.get('section')
    station = data.get('station')
    area_data = data.get('area', {})

    station_data = get_station_by_path(railway, bureau, section, station)
    if not station_data:
        return jsonify({"status": "error", "message": "车站不存在"}), 404

    station_key = f"{railway}_{bureau}_{section}_{station}"
    init_counters_for_station(station_key)

    new_id = id_counters[station_key]['commercial_waiting_areas']
    id_counters[station_key]['commercial_waiting_areas'] += 1
    area_data['id'] = new_id

    station_data['commercial_waiting_areas'].append(area_data)
    return jsonify({"status": "success", "id": new_id, "area": area_data})


@app.route('/api/commercial_area/<int:area_id>', methods=['PUT'])
def update_commercial_area(area_id):
    data = request.json
    railway = data.get('railway')
    bureau = data.get('bureau')
    section = data.get('section')
    station = data.get('station')
    area_data = data.get('area', {})

    station_data = get_station_by_path(railway, bureau, section, station)
    if not station_data:
        return jsonify({"status": "error", "message": "车站不存在"}), 404

    for i, area in enumerate(station_data['commercial_waiting_areas']):
        if area['id'] == area_id:
            area_data['id'] = area_id
            station_data['commercial_waiting_areas'][i] = area_data
            return jsonify({"status": "success"})

    return jsonify({"status": "error", "message": "商业候车区不存在"}), 404


@app.route('/api/commercial_area/<int:area_id>', methods=['DELETE'])
def delete_commercial_area(area_id):
    data = request.json
    railway = data.get('railway')
    bureau = data.get('bureau')
    section = data.get('section')
    station = data.get('station')

    station_data = get_station_by_path(railway, bureau, section, station)
    if not station_data:
        return jsonify({"status": "error", "message": "车站不存在"}), 404

    station_data['commercial_waiting_areas'] = [a for a in station_data['commercial_waiting_areas'] if
                                                a['id'] != area_id]
    return jsonify({"status": "success"})


# ==================== 图片上传 ====================
@app.route('/api/upload_photo', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({"status": "error", "message": "没有文件"})
    file = request.files['photo']
    if file.filename == '':
        return jsonify({"status": "error", "message": "文件名为空"})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({"status": "success", "url": f"/static/uploads/{filename}"})
    return jsonify({"status": "error", "message": "文件类型不支持"})


# ==================== 导入导出 ====================
# app.py - 下载模板部分（彻底修复）
@app.route('/api/download_template/<string:template_type>')
def download_template(template_type):
    """下载Excel模板（包含下拉选项）"""
    import io
    import xlsxwriter

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    # 定义格式
    header_format = workbook.add_format({
        'bold': True, 'font_size': 10, 'font_color': 'white',
        'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
        'bg_color': '#4472C4', 'border': 1
    })

    header_format_yellow = workbook.add_format({
        'bold': True, 'font_size': 10, 'font_color': '#333333',
        'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
        'bg_color': '#FFD700', 'border': 1
    })

    header_format2 = workbook.add_format({
        'bold': True, 'font_size': 10, 'font_color': 'white',
        'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
        'bg_color': '#ED7D31', 'border': 1
    })

    header_format3 = workbook.add_format({
        'bold': True, 'font_size': 10, 'font_color': 'white',
        'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
        'bg_color': '#70AD47', 'border': 1
    })

    comment_format = workbook.add_format({
        'font_size': 8, 'font_color': '#333333', 'italic': True,
        'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
        'bg_color': '#FFEE99', 'border': 1
    })

    data_format = workbook.add_format({
        'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
        'border': 1, 'bg_color': '#E2EFDA'
    })

    data_format_yellow = workbook.add_format({
        'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
        'border': 1, 'bg_color': '#FFF8E1'
    })

    # ==================== Sheet1: 商务候车室 ====================
    ws = workbook.add_worksheet('商务候车室')

    headers = [
        '序号', '车站名称', '所属路局', '所属站段', '车站类别',
        '原贵宾候车室位置', '休息厅名称', '权属主体', '面积(㎡)', '投资主体',
        '资产办理', '资产时间', '装修出资', '装修情况', '装修移交',
        '装修时间', '家具出资', '家具明细', '家具移交', '家具时间',
        '功能调整', '调整时间', '独立卫生间', '整改照片',
        '位置', '安检设备', '检票设备', '独立站外通道', '进站台方式',
        '入公共大厅', '落客通道', '独立停车区', '停车位数',
        '营业时间', '服务人员', '联系电话', '接待台',
        '卫生间数', '操作间', '平面图'
    ]

    # 写入表头
    for col in range(0, 24):
        ws.write(0, col, headers[col], header_format)
    for col in range(24, len(headers)):
        ws.write(0, col, headers[col], header_format_yellow)

    comments = [
        '系统自动编号，可留空',
        '手动填写，如：北京朝阳站',
        '下拉选择：哈尔滨/沈阳/北京/太原/呼和浩特/郑州/武汉/西安/济南/上海/南昌/广州/南宁/成都/昆明/兰州/乌鲁木齐/青藏',
        '手动填写，如：北京站直属站',
        '下拉选择：一类/二类/三类/四类',
        '手动填写，按具体位置填报',
        '手动填写，按所属贵宾候车室+休息厅名称填报',
        '手动填写，按照XX局集团公司等填写',
        '手动填写，面积测量范围仅为休息区域使用面积，单位：㎡',
        '手动填写，如建设投资主体和站房权属主体一致则同填',
        '下拉选择：已移交铁路局集团公司无偿使用/已移交铁路局集团公司出资回购/其他（需手动填写）',
        '日历选择，办结或拟办结日期',
        '手动填写，如装修出资主体与权属主体一致则同填',
        '手动填写，与站房结构融为一体的不可移动设施明细',
        '下拉选择：无偿移交/有偿移交/投资方回收处置/超标准装饰投资方回收处置/其他可移动资产投资方回收处置/协商中',
        '日历选择，装修办理日期',
        '手动填写，与权属主体一致则同填',
        '手动填写，高档装饰（家具）资产明细和其他可移动资产明细',
        '下拉选择：超标准装饰（家具），投资方回收处置/超标准装饰（家具），投资方按无偿使用交车站处理/其他可移动资产，投资方回收处置/其他可移动资产，投资方按无偿使用交车站处理',
        '日历选择，移交办理日期',
        '下拉选择：调整为礼遇行经营用房/调整为商务座候车区/调整为四区一室服务用房/调整为车站生产生活用房/其他用房',
        '日历选择，调整日期',
        '下拉选择：是/否',
        '导入后单独上传图片',
        '手动填写，公共属性位置',
        '下拉选择：1套/2套（留空表示无）',
        '下拉选择：门式闸机/柱式闸机/手持检票终端/无（留空表示无）',
        '下拉选择：是/否',
        '下拉选择：通过候车大厅/站内专用通道/无',
        '下拉选择：是/否',
        '下拉选择：停靠落客平台/停靠消防通道/停靠基本站台/停靠停车场',
        '下拉选择：是/否',
        '手动填写数字',
        '手动填写，格式XX:XX-XX:XX',
        '手动填写数字',
        '手动填写，格式：区号+号码',
        '下拉选择：是/否',
        '下拉选择：0处/1处/2处/3处/4处/5处/6处/7处',
        '下拉选择：是/否',
        '导入后单独上传图片'
    ]

    for col, comment in enumerate(comments):
        ws.write(1, col, comment, comment_format)

    col_widths = [8, 16, 14, 16, 12, 20, 18, 16, 12, 16,
                  18, 14, 16, 20, 18, 14, 16, 22, 18, 14,
                  20, 14, 14, 16, 14, 14, 16, 16, 16, 14,
                  16, 14, 14, 16, 14, 16, 14, 14, 14, 16]
    for col, width in enumerate(col_widths):
        ws.set_column(col, col, width)

    ws.set_row(0, 30)
    ws.set_row(1, 50)

    # ===== 下拉选项（使用普通列表，不包含特殊字符） =====
    bureaus = ['哈尔滨', '沈阳', '北京', '太原', '呼和浩特', '郑州', '武汉', '西安',
               '济南', '上海', '南昌', '广州', '南宁', '成都', '昆明', '兰州',
               '乌鲁木齐', '青藏']

    # 使用 try-except 包裹，如果某个验证失败不影响整体
    try:
        # 所属路局 (C列, 索引2)
        ws.data_validation(2, 2, 100, 2, {'validate': 'list', 'source': bureaus})
    except:
        pass

    try:
        # 车站类别 (E列, 索引4)
        ws.data_validation(2, 4, 100, 4, {'validate': 'list', 'source': ['一类', '二类', '三类', '四类']})
    except:
        pass

    try:
        # 资产办理 (K列, 索引10)
        ws.data_validation(2, 10, 100, 10, {'validate': 'list',
                                            'source': ['已移交铁路局集团公司无偿使用', '已移交铁路局集团公司出资回购',
                                                       '其他需手动填写']})
    except:
        pass

    try:
        # 装修移交 (O列, 索引14)
        ws.data_validation(2, 14, 100, 14, {'validate': 'list', 'source': ['无偿移交', '有偿移交', '投资方回收处置',
                                                                           '超标准装饰投资方回收处置',
                                                                           '其他可移动资产投资方回收处置', '协商中']})
    except:
        pass

    try:
        # 家具移交 (S列, 索引18)
        ws.data_validation(2, 18, 100, 18, {'validate': 'list', 'source': ['超标准装饰家具投资方回收处置',
                                                                           '超标准装饰家具投资方按无偿使用交车站处理',
                                                                           '其他可移动资产投资方回收处置',
                                                                           '其他可移动资产投资方按无偿使用交车站处理']})
    except:
        pass

    try:
        # 功能调整 (U列, 索引20) - 移除中文引号
        ws.data_validation(2, 20, 100, 20, {'validate': 'list', 'source': ['调整为礼遇行经营用房', '调整为商务座候车区',
                                                                           '调整为四区一室服务用房',
                                                                           '调整为车站生产生活用房', '其他用房']})
    except:
        pass

    try:
        # 独立卫生间 (W列, 索引22)
        ws.data_validation(2, 22, 100, 22, {'validate': 'list', 'source': ['是', '否']})
    except:
        pass

    try:
        # 安检设备 (Z列, 索引25)
        ws.data_validation(2, 25, 100, 25, {'validate': 'list', 'source': ['1套', '2套']})
    except:
        pass

    try:
        # 检票设备 (AA列, 索引26)
        ws.data_validation(2, 26, 100, 26,
                           {'validate': 'list', 'source': ['门式闸机', '柱式闸机', '手持检票终端', '无']})
    except:
        pass

    try:
        # 独立站外通道 (AB列, 索引27)
        ws.data_validation(2, 27, 100, 27, {'validate': 'list', 'source': ['是', '否']})
    except:
        pass

    try:
        # 进站台方式 (AC列, 索引28)
        ws.data_validation(2, 28, 100, 28, {'validate': 'list', 'source': ['通过候车大厅', '站内专用通道', '无']})
    except:
        pass

    try:
        # 入公共大厅 (AD列, 索引29)
        ws.data_validation(2, 29, 100, 29, {'validate': 'list', 'source': ['是', '否']})
    except:
        pass

    try:
        # 落客通道 (AE列, 索引30)
        ws.data_validation(2, 30, 100, 30, {'validate': 'list',
                                            'source': ['停靠落客平台', '停靠消防通道', '停靠基本站台', '停靠停车场']})
    except:
        pass

    try:
        # 独立停车区 (AF列, 索引31)
        ws.data_validation(2, 31, 100, 31, {'validate': 'list', 'source': ['是', '否']})
    except:
        pass

    try:
        # 接待台 (AK列, 索引36)
        ws.data_validation(2, 36, 100, 36, {'validate': 'list', 'source': ['是', '否']})
    except:
        pass

    try:
        # 卫生间数 (AL列, 索引37)
        ws.data_validation(2, 37, 100, 37,
                           {'validate': 'list', 'source': ['0处', '1处', '2处', '3处', '4处', '5处', '6处', '7处']})
    except:
        pass

    try:
        # 操作间 (AM列, 索引38)
        ws.data_validation(2, 38, 100, 38, {'validate': 'list', 'source': ['是', '否']})
    except:
        pass

    # 示例数据
    sample_data = [
        '1', '北京朝阳站', '北京', '北京站直属站', '二类',
        '北京朝阳站（东北侧）', '1号贵宾室01厅',
        '已移交铁路局集团公司无偿使用', '120', '已移交铁路局集团公司无偿使用',
        '已移交铁路局集团公司无偿使用', '2026-06-15', '已移交铁路局集团公司无偿使用',
        '墙面贴装天然大理石；艺术灯5套', '无偿移交', '2026-06-15',
        '已移交铁路局集团公司无偿使用', '紫檀单人沙发10套约30万元；字画及屏风约200万元',
        '投资方回收处置', '2026-06-15',
        '调整为礼遇行经营用房', '2026-08-15', '是', '[图片]',
        '站房南侧一层', '1套', '门式闸机', '是', '通过候车大厅',
        '是', '停靠落客平台', '是', '7',
        '06:00-22:00', '5', '010-12345678',
        '是', '5处', '是', '[图片]'
    ]

    for col in range(0, 24):
        ws.write(2, col, sample_data[col], data_format)
    for col in range(24, len(sample_data)):
        ws.write(2, col, sample_data[col], data_format_yellow)

    # ==================== Sheet2: 商务座候车区 ====================
    ws2 = workbook.add_worksheet('商务座候车区')

    headers2 = [
        '序号', '车站名称', '所属路局', '所属站段', '车站类别',
        '类型', '点位', '建设主体', '建成时间', '面积(㎡)',
        '装修出资主体', '运营模式', '业务外包企业名称',
        '休息间1面积', '休息间2面积', '休息间3面积',
        '独立进站通道', '安检检票验证'
    ]

    for col, header in enumerate(headers2):
        ws2.write(0, col, header, header_format2)

    comments2 = [
        '系统自动编号，可留空',
        '手动填写，如：北京朝阳站',
        '下拉选择：哈尔滨/沈阳/北京/太原/呼和浩特/郑州/武汉/西安/济南/上海/南昌/广州/南宁/成都/昆明/兰州/乌鲁木齐/青藏',
        '手动填写，如：北京站直属站',
        '下拉选择：一类车站/二类车站/三类车站/四类车站',
        '下拉选择：高铁站/高普混/普速站',
        '如：A18检票口旁',
        '下拉选择：国铁/铁路局/地方政府全称/投资企业全称',
        '格式：YYYY-MM-DD',
        '手动填写数值',
        '下拉选择：国铁/铁路局/地方政府全称/投资企业全称',
        '下拉选择：自营/业务外包',
        '运营模式为业务外包时必填',
        '手动填写数值，无则留空',
        '手动填写数值，无则留空',
        '手动填写数值，无则留空',
        '下拉选择：是/否',
        '下拉选择：有/无'
    ]

    for col, comment in enumerate(comments2):
        ws2.write(1, col, comment, comment_format)

    col_widths2 = [8, 16, 14, 16, 12, 12, 20, 14, 14, 14, 16, 12, 25, 14, 14, 14, 14, 14]
    for col, width in enumerate(col_widths2):
        ws2.set_column(col, col, width)
    ws2.set_row(0, 30)
    ws2.set_row(1, 50)

    # 下拉选项
    try:
        ws2.data_validation(2, 2, 100, 2, {'validate': 'list', 'source': bureaus})
    except:
        pass
    try:
        ws2.data_validation(2, 4, 100, 4,
                            {'validate': 'list', 'source': ['一类车站', '二类车站', '三类车站', '四类车站']})
    except:
        pass
    try:
        ws2.data_validation(2, 5, 100, 5, {'validate': 'list', 'source': ['高铁站', '高普混', '普速站']})
    except:
        pass
    try:
        ws2.data_validation(2, 7, 100, 7,
                            {'validate': 'list', 'source': ['国铁', '铁路局', '地方政府全称', '投资企业全称']})
    except:
        pass
    try:
        ws2.data_validation(2, 10, 100, 10,
                            {'validate': 'list', 'source': ['国铁', '铁路局', '地方政府全称', '投资企业全称']})
    except:
        pass
    try:
        ws2.data_validation(2, 11, 100, 11, {'validate': 'list', 'source': ['自营', '业务外包']})
    except:
        pass
    try:
        ws2.data_validation(2, 16, 100, 16, {'validate': 'list', 'source': ['是', '否']})
    except:
        pass
    try:
        ws2.data_validation(2, 17, 100, 17, {'validate': 'list', 'source': ['有', '无']})
    except:
        pass

    sample_data2 = [
        '1', '北京朝阳站', '北京', '北京站直属站', '一类车站',
        '高铁站', 'A18检票口旁', '国铁', '2020-01-15', '300',
        '国铁', '自营', '', '50', '', '',
        '是', '有'
    ]
    for col, value in enumerate(sample_data2):
        ws2.write(2, col, value, data_format)

    # ==================== Sheet3: 商业候车区 ====================
    ws3 = workbook.add_worksheet('商业候车区')

    headers3 = [
        '序号', '车站名称', '所属路局', '所属站段', '车站类别',
        '类型', '点位', '建设主体', '建成时间', '面积(㎡)',
        '装修出资主体', '业务外包企业名称', '营业状态',
        '是否有冠名', '冠名单位', '合同到期时间'
    ]

    for col, header in enumerate(headers3):
        ws3.write(0, col, header, header_format3)

    comments3 = [
        '系统自动编号，可留空',
        '手动填写，如：北京朝阳站',
        '下拉选择：哈尔滨/沈阳/北京/太原/呼和浩特/郑州/武汉/西安/济南/上海/南昌/广州/南宁/成都/昆明/兰州/乌鲁木齐/青藏',
        '手动填写，如：北京站直属站',
        '下拉选择：一类车站/二类车站/三类车站/四类车站',
        '下拉选择：高铁站/高普混/普速站',
        '按具体位置填报',
        '下拉选择：国铁/铁路局/地方政府全称/投资企业全称',
        '格式：YYYY-MM-DD',
        '手动填写数值',
        '下拉选择：国铁/铁路局/地方政府全称/投资企业全称',
        '手动填写',
        '下拉选择：营业/停业',
        '下拉选择：是/否',
        '填写合同或协议全部名称',
        '按照合同或协议内容填写'
    ]

    for col, comment in enumerate(comments3):
        ws3.write(1, col, comment, comment_format)

    col_widths3 = [8, 16, 14, 16, 12, 12, 20, 14, 14, 14, 16, 25, 12, 12, 25, 16]
    for col, width in enumerate(col_widths3):
        ws3.set_column(col, col, width)
    ws3.set_row(0, 30)
    ws3.set_row(1, 50)

    # 下拉选项
    try:
        ws3.data_validation(2, 2, 100, 2, {'validate': 'list', 'source': bureaus})
    except:
        pass
    try:
        ws3.data_validation(2, 4, 100, 4,
                            {'validate': 'list', 'source': ['一类车站', '二类车站', '三类车站', '四类车站']})
    except:
        pass
    try:
        ws3.data_validation(2, 5, 100, 5, {'validate': 'list', 'source': ['高铁站', '高普混', '普速站']})
    except:
        pass
    try:
        ws3.data_validation(2, 7, 100, 7,
                            {'validate': 'list', 'source': ['国铁', '铁路局', '地方政府全称', '投资企业全称']})
    except:
        pass
    try:
        ws3.data_validation(2, 10, 100, 10,
                            {'validate': 'list', 'source': ['国铁', '铁路局', '地方政府全称', '投资企业全称']})
    except:
        pass
    try:
        ws3.data_validation(2, 12, 100, 12, {'validate': 'list', 'source': ['营业', '停业']})
    except:
        pass
    try:
        ws3.data_validation(2, 13, 100, 13, {'validate': 'list', 'source': ['是', '否']})
    except:
        pass

    sample_data3 = [
        '1', '北京朝阳站', '北京', '北京站直属站', '一类车站',
        '高铁站', '候车大厅东侧', '国铁', '2019-06-20', '150',
        '国铁', 'XX商业公司', '营业', '是', 'XX品牌冠名合作协议', '2027-12-31'
    ]
    for col, value in enumerate(sample_data3):
        ws3.write(2, col, value, data_format)

    workbook.close()
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f"车站商务候车室基本信息导入模板_{datetime.datetime.now().strftime('%Y%m%d')}.xlsx"
    )

@app.route('/api/import_excel', methods=['POST'])
def import_excel():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "没有文件"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "文件名为空"})
    try:
        excel_file = pd.ExcelFile(file)
        sheet_names = excel_file.sheet_names

        data = request.form
        railway = data.get('railway', current_path['railway'])
        bureau = data.get('bureau', current_path['bureau'])
        section = data.get('section', current_path['section'])
        station = data.get('station', current_path['station'])
        import_type = data.get('import_type', 'all')

        station_data = get_station_by_path(railway, bureau, section, station)
        if not station_data:
            return jsonify({"status": "error", "message": "车站不存在"}), 404

        station_key = f"{railway}_{bureau}_{section}_{station}"
        init_counters_for_station(station_key)

        total_count = 0
        total_skip = 0
        details = {
            'business_waiting': 0,
            'business_class': 0,
            'commercial': 0
        }

        # 获取已存在的休息厅名称列表
        existing_lounge_names = set()
        for room in station_data.get('business_waiting_rooms', []):
            for lounge in room.get('lounges', []):
                if lounge.get('name'):
                    existing_lounge_names.add(lounge.get('name'))

        # ===== 导入商务候车室 =====
        if '商务候车室' in sheet_names:
            df = pd.read_excel(file, sheet_name='商务候车室')
            count = 0
            skip = 0
            for _, row in df.iterrows():
                lounge_name = str(row.get('原贵宾候车室休息厅名称', '')) if not pd.isna(
                    row.get('原贵宾候车室休息厅名称')) else ''
                station_name = str(row.get('车站名称', station)) if not pd.isna(row.get('车站名称')) else station

                if not lounge_name and pd.isna(row.get('原贵宾候车室位置')):
                    continue

                if lounge_name and lounge_name in existing_lounge_names:
                    skip += 1
                    continue

                room_id = id_counters[station_key]['business_waiting_rooms']
                id_counters[station_key]['business_waiting_rooms'] += 1

                lounge_id = id_counters[station_key]['lounges']
                id_counters[station_key]['lounges'] += 1

                lounge = {
                    'id': lounge_id,
                    'name': lounge_name,
                    'ownership': str(row.get('原贵宾候车室休息厅隶属站房的权属主体情况', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅隶属站房的权属主体情况')) else '',
                    'area': str(row.get('原贵宾候车室休息厅面积', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅面积')) else '',
                    'investment': str(row.get('原贵宾候车室休息厅建设投资主体情况', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅建设投资主体情况')) else '',
                    'asset_status': str(row.get('原贵宾候车室休息厅建设资产办理情况', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅建设资产办理情况')) else '',
                    'asset_date': str(row.get('原贵宾候车室休息厅建设资产办理时间', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅建设资产办理时间')) else '',
                    'decoration_investment': str(row.get('原贵宾候车室休息厅装修出资主体', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅装修出资主体')) else '',
                    'decoration_items': str(row.get('原贵宾候车室休息厅装修情况', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅装修情况')) else '',
                    'decoration_transfer': str(row.get('原贵宾候车室休息厅装修移交情况', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅装修移交情况')) else '',
                    'decoration_date': str(row.get('原贵宾候车室休息厅装修办理时间', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅装修办理时间')) else '',
                    'furniture_investment': str(row.get('原贵宾候车室休息厅装饰（家具）资产出资主体', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅装饰（家具）资产出资主体')) else '',
                    'furniture_items': str(row.get('原贵宾候车室休息厅装饰（家具）资产明细', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅装饰（家具）资产明细')) else '',
                    'furniture_transfer': str(row.get('原贵宾候车室休息厅装饰（家具）移交情况', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅装饰（家具）移交情况')) else '',
                    'furniture_date': str(row.get('原贵宾候车室休息厅装饰（家具）办理时间', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅装饰（家具）办理时间')) else '',
                    'function_adjust': str(row.get('原贵宾候车室休息厅功能调整情况', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅功能调整情况')) else '',
                    'adjust_date': str(row.get('原贵宾候车室休息厅功能调整办理时间', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅功能调整办理时间')) else '',
                    'has_independent_toilet': str(row.get('原贵宾候车室休息厅是否有独立卫生间', '是')) if not pd.isna(
                        row.get('原贵宾候车室休息厅是否有独立卫生间')) else '是',
                    'photo': str(row.get('原贵宾候车室休息厅整改后照片', '')) if not pd.isna(
                        row.get('原贵宾候车室休息厅整改后照片')) else ''
                }

                public = {
                    'station_name': station_name,
                    'position': str(row.get('原贵宾候车室位置', '')) if not pd.isna(
                        row.get('原贵宾候车室位置')) else '',
                    'checkin_equipment': str(row.get('原贵宾候车室安检设备设施设置情况', '')) if not pd.isna(
                        row.get('原贵宾候车室安检设备设施设置情况')) else '',
                    'ticket_check_equipment': str(row.get('原贵宾候车室检验票设备设施设置情况', '')) if not pd.isna(
                        row.get('原贵宾候车室检验票设备设施设置情况')) else '',
                    'has_independent_channel': str(
                        row.get('是否有独立的站外直接进入原贵宾候车室通道', '是')) if not pd.isna(
                        row.get('是否有独立的站外直接进入原贵宾候车室通道')) else '是',
                    'platform_access': str(row.get('原贵宾候车室如何进入站台', '')) if not pd.isna(
                        row.get('原贵宾候车室如何进入站台')) else '',
                    'can_access_public_hall': str(
                        row.get('原贵宾候车室是否能进入公共候车大厅通道', '是')) if not pd.isna(
                        row.get('原贵宾候车室是否能进入公共候车大厅通道')) else '是',
                    'car_dropoff': str(row.get('站外汽车专用落客通道情况', '')) if not pd.isna(
                        row.get('站外汽车专用落客通道情况')) else '',
                    'has_independent_parking': str(row.get('原贵宾候车室是否有独立停车区', '是')) if not pd.isna(
                        row.get('原贵宾候车室是否有独立停车区')) else '是',
                    'parking_spaces': str(row.get('原贵宾候车室停车位数', '')) if not pd.isna(
                        row.get('原贵宾候车室停车位数')) else '',
                    'business_hours': str(row.get('原贵宾候车室营业时间', '')) if not pd.isna(
                        row.get('原贵宾候车室营业时间')) else '',
                    'dedicated_staff': str(row.get('原贵宾候车室专职服务人员', '')) if not pd.isna(
                        row.get('原贵宾候车室专职服务人员')) else '',
                    'contact_phone': str(row.get('原贵宾候车室联系电话', '')) if not pd.isna(
                        row.get('原贵宾候车室联系电话')) else '',
                    'has_reception_desk': str(row.get('原贵宾候车室是否有接待台', '是')) if not pd.isna(
                        row.get('原贵宾候车室是否有接待台')) else '是',
                    'toilet_count': str(row.get('原贵宾候车室卫生间设置数量', '')) if not pd.isna(
                        row.get('原贵宾候车室卫生间设置数量')) else '',
                    'has_operation_room': str(row.get('原贵宾候车室是否有操作间', '是')) if not pd.isna(
                        row.get('原贵宾候车室是否有操作间')) else '是',
                    'floor_plan': str(row.get('车站平面图', '')) if not pd.isna(row.get('车站平面图')) else ''
                }

                room = {
                    'id': room_id,
                    'public': public,
                    'lounges': [lounge]
                }
                station_data['business_waiting_rooms'].append(room)
                count += 1
                if lounge_name:
                    existing_lounge_names.add(lounge_name)

            details['business_waiting'] = count
            total_count += count
            total_skip += skip

        # ===== 导入商务座候车区 =====
        if '商务座候车区' in sheet_names:
            df = pd.read_excel(file, sheet_name='商务座候车区')
            count = 0
            for _, row in df.iterrows():
                if pd.isna(row.get('点位')) and pd.isna(row.get('类型')):
                    continue
                area_id = id_counters[station_key]['business_class_areas']
                id_counters[station_key]['business_class_areas'] += 1

                area = {
                    'id': area_id,
                    'name': str(row.get('点位', f'商务座候车区{area_id}')) if not pd.isna(
                        row.get('点位')) else f'商务座候车区{area_id}',
                    'type': str(row.get('类型', '高铁站')) if not pd.isna(row.get('类型')) else '高铁站',
                    'location': str(row.get('点位', '')) if not pd.isna(row.get('点位')) else '',
                    'construction_entity': str(row.get('建设主体', '国铁')) if not pd.isna(
                        row.get('建设主体')) else '国铁',
                    'completion_time': str(row.get('建成时间', '')) if not pd.isna(row.get('建成时间')) else '',
                    'area': str(row.get('面积（单位：㎡）', '')) if not pd.isna(row.get('面积（单位：㎡）')) else '',
                    'decoration_investment': str(row.get('装修出资主体', '国铁')) if not pd.isna(
                        row.get('装修出资主体')) else '国铁',
                    'operation_mode': str(row.get('运营模式', '自营')) if not pd.isna(row.get('运营模式')) else '自营',
                    'outsource_company': str(row.get('业务外包企业名称', '')) if not pd.isna(
                        row.get('业务外包企业名称')) else '',
                    'has_independent_channel': str(row.get('是否有独立进站通道', '是')) if not pd.isna(
                        row.get('是否有独立进站通道')) else '是',
                    'checkin_ticket_verify': str(row.get('安检检票验证', '')) if not pd.isna(
                        row.get('安检检票验证')) else '',
                    'lounge1_area': str(row.get('内设休息间1面积', '')) if not pd.isna(
                        row.get('内设休息间1面积')) else '',
                    'lounge2_area': str(row.get('内设休息间2面积', '')) if not pd.isna(
                        row.get('内设休息间2面积')) else '',
                    'lounge3_area': str(row.get('内设休息间3面积', '')) if not pd.isna(
                        row.get('内设休息间3面积')) else ''
                }
                station_data['business_class_areas'].append(area)
                count += 1

            details['business_class'] = count
            total_count += count

        # ===== 导入商业候车区 =====
        if '商业候车区' in sheet_names:
            df = pd.read_excel(file, sheet_name='商业候车区')
            count = 0
            for _, row in df.iterrows():
                if pd.isna(row.get('点位')) and pd.isna(row.get('类型')):
                    continue
                area_id = id_counters[station_key]['commercial_waiting_areas']
                id_counters[station_key]['commercial_waiting_areas'] += 1

                area = {
                    'id': area_id,
                    'name': str(row.get('点位', f'商业候车区{area_id}')) if not pd.isna(
                        row.get('点位')) else f'商业候车区{area_id}',
                    'type': str(row.get('类型', '高铁站')) if not pd.isna(row.get('类型')) else '高铁站',
                    'location': str(row.get('点位', '')) if not pd.isna(row.get('点位')) else '',
                    'construction_entity': str(row.get('建设主体', '国铁')) if not pd.isna(
                        row.get('建设主体')) else '国铁',
                    'completion_time': str(row.get('建成时间', '')) if not pd.isna(row.get('建成时间')) else '',
                    'area': str(row.get('面积（单位：㎡）', '')) if not pd.isna(row.get('面积（单位：㎡）')) else '',
                    'decoration_investment': str(row.get('装修出资主体', '国铁')) if not pd.isna(
                        row.get('装修出资主体')) else '国铁',
                    'outsource_company': str(row.get('业务外包企业名称', '')) if not pd.isna(
                        row.get('业务外包企业名称')) else '',
                    'operation_status': str(row.get('营业状态', '营业')) if not pd.isna(
                        row.get('营业状态')) else '营业',
                    'has_naming': str(row.get('是否有冠名', '否')) if not pd.isna(row.get('是否有冠名')) else '否',
                    'naming_unit': str(row.get('冠名单位', '')) if not pd.isna(row.get('冠名单位')) else '',
                    'contract_end_date': str(row.get('合同到期时间', '')) if not pd.isna(
                        row.get('合同到期时间')) else ''
                }
                station_data['commercial_waiting_areas'].append(area)
                count += 1

            details['commercial'] = count
            total_count += count

        message = f"成功导入 {total_count} 条数据"
        if total_skip > 0:
            message += f"，跳过 {total_skip} 条已存在的重复数据"

        return jsonify({
            "status": "success",
            "count": total_count,
            "skip": total_skip,
            "details": details,
            "message": message
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)})


@app.route('/api/export_excel_by_stations', methods=['POST'])
def export_excel_by_stations():
    """根据传入的车站列表导出数据"""
    data = request.json
    export_type = data.get('export_type', 'all')
    stations = data.get('stations', [])

    if not stations:
        return jsonify({"status": "error", "message": "请选择要导出的车站"}), 400

    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        all_bw_data = []
        all_bc_data = []
        all_com_data = []

        for s in stations:
            station_data = get_station_by_path(s['railway'], s['bureau'], s['section'], s['station'])
            if not station_data:
                continue

            basic = station_data.get('basic_info', {})

            # 商务候车室
            if export_type in ['all', 'business_waiting']:
                for wr in station_data.get('business_waiting_rooms', []):
                    public = wr.get('public', {})
                    for lounge in wr.get('lounges', []):
                        all_bw_data.append({
                            '所属路局': s['bureau'],
                            '所属站段': s['section'],
                            '车站名称': s['station'],
                            '车站类别': basic.get('车站类别', ''),
                            '原贵宾候车室位置': public.get('position', ''),
                            '原贵宾候车室休息厅名称': lounge.get('name', ''),
                            '原贵宾候车室休息厅隶属站房的权属主体情况': lounge.get('ownership', ''),
                            '原贵宾候车室休息厅面积': lounge.get('area', ''),
                            '原贵宾候车室休息厅建设投资主体情况': lounge.get('investment', ''),
                            '原贵宾候车室休息厅建设资产办理情况': lounge.get('asset_status', ''),
                            '原贵宾候车室休息厅建设资产办理时间': lounge.get('asset_date', ''),
                            '原贵宾候车室休息厅装修出资主体': lounge.get('decoration_investment', ''),
                            '原贵宾候车室休息厅装修情况': lounge.get('decoration_items', ''),
                            '原贵宾候车室休息厅装修移交情况': lounge.get('decoration_transfer', ''),
                            '原贵宾候车室休息厅装修办理时间': lounge.get('decoration_date', ''),
                            '原贵宾候车室休息厅装饰（家具）资产出资主体': lounge.get('furniture_investment', ''),
                            '原贵宾候车室休息厅装饰（家具）资产明细': lounge.get('furniture_items', ''),
                            '原贵宾候车室休息厅装饰（家具）移交情况': lounge.get('furniture_transfer', ''),
                            '原贵宾候车室休息厅装饰（家具）办理时间': lounge.get('furniture_date', ''),
                            '原贵宾候车室休息厅功能调整情况': lounge.get('function_adjust', ''),
                            '原贵宾候车室休息厅功能调整办理时间': lounge.get('adjust_date', ''),
                            '原贵宾候车室休息厅是否有独立卫生间': lounge.get('has_independent_toilet', ''),
                            '原贵宾候车室休息厅整改后照片': lounge.get('photo', ''),
                            '原贵宾候车室安检设备设施设置情况': public.get('checkin_equipment', ''),
                            '原贵宾候车室检验票设备设施设置情况': public.get('ticket_check_equipment', ''),
                            '是否有独立的站外直接进入原贵宾候车室通道': public.get('has_independent_channel', ''),
                            '原贵宾候车室如何进入站台': public.get('platform_access', ''),
                            '原贵宾候车室是否能进入公共候车大厅通道': public.get('can_access_public_hall', ''),
                            '站外汽车专用落客通道情况': public.get('car_dropoff', ''),
                            '原贵宾候车室是否有独立停车区': public.get('has_independent_parking', ''),
                            '原贵宾候车室停车位数': public.get('parking_spaces', ''),
                            '原贵宾候车室营业时间': public.get('business_hours', ''),
                            '原贵宾候车室专职服务人员': public.get('dedicated_staff', ''),
                            '原贵宾候车室联系电话': public.get('contact_phone', ''),
                            '原贵宾候车室是否有接待台': public.get('has_reception_desk', ''),
                            '原贵宾候车室卫生间设置数量': public.get('toilet_count', ''),
                            '原贵宾候车室是否有操作间': public.get('has_operation_room', ''),
                            '车站平面图': public.get('floor_plan', '')
                        })

            # 商务座候车区
            if export_type in ['all', 'business_class']:
                for area in station_data.get('business_class_areas', []):
                    all_bc_data.append({
                        '所属路局': s['bureau'],
                        '所属站段': s['section'],
                        '车站名称': s['station'],
                        '车站类别': basic.get('车站类别', ''),
                        '类型': area.get('type', ''),
                        '点位': area.get('location', ''),
                        '建设主体': area.get('construction_entity', ''),
                        '建成时间': area.get('completion_time', ''),
                        '面积（单位：㎡）': area.get('area', ''),
                        '装修出资主体': area.get('decoration_investment', ''),
                        '运营模式': area.get('operation_mode', ''),
                        '业务外包企业名称': area.get('outsource_company', ''),
                        '内设休息间1面积': area.get('lounge1_area', ''),
                        '内设休息间2面积': area.get('lounge2_area', ''),
                        '内设休息间3面积': area.get('lounge3_area', ''),
                        '是否有独立进站通道': area.get('has_independent_channel', ''),
                        '安检检票验证': area.get('checkin_ticket_verify', '')
                    })

            # 商业候车区
            if export_type in ['all', 'commercial']:
                for area in station_data.get('commercial_waiting_areas', []):
                    all_com_data.append({
                        '所属路局': s['bureau'],
                        '所属站段': s['section'],
                        '车站名称': s['station'],
                        '车站类别': basic.get('车站类别', ''),
                        '类型': area.get('type', ''),
                        '点位': area.get('location', ''),
                        '建设主体': area.get('construction_entity', ''),
                        '建成时间': area.get('completion_time', ''),
                        '面积（单位：㎡）': area.get('area', ''),
                        '装修出资主体': area.get('decoration_investment', ''),
                        '业务外包企业名称': area.get('outsource_company', ''),
                        '营业状态': area.get('operation_status', ''),
                        '是否有冠名': area.get('has_naming', ''),
                        '冠名单位': area.get('naming_unit', ''),
                        '合同到期时间': area.get('contract_end_date', '')
                    })

        if all_bw_data:
            pd.DataFrame(all_bw_data).to_excel(writer, sheet_name='商务候车室', index=False)
        if all_bc_data:
            pd.DataFrame(all_bc_data).to_excel(writer, sheet_name='商务座候车区', index=False)
        if all_com_data:
            pd.DataFrame(all_com_data).to_excel(writer, sheet_name='商业候车区', index=False)

    output.seek(0)

    type_names = {
        'business_waiting': '商务候车室',
        'business_class': '商务座候车区',
        'commercial': '商业候车区',
        'all': '全部数据'
    }
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f"{type_names.get(export_type, '数据')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )


# ==================== 路由 ====================
@app.route('/')
def main_page():
    init_sample_data()
    return render_template('main.html')


@app.route('/edit')
def edit_page():
    init_sample_data()
    return render_template('edit.html')


@app.route('/statistics')
def statistics_page():
    init_sample_data()
    return render_template('statistics.html')


if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)
    app.run(debug=True, port=5000)