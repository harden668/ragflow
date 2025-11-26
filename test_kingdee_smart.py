#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金蝶云星空智能数据测试
正确解析和显示返回的数据格式
"""

import json
from kingdee_api_tool import create_kingdee_tool, KingdeeAPIType

def display_material_data(data):
    """显示物料数据"""
    if isinstance(data, list) and len(data) > 0:
        print(f"获取到 {len(data)} 条物料记录:")
        for i, item in enumerate(data, 1):
            if isinstance(item, list) and len(item) >= 2:
                material_code = item[0] if len(item) > 0 else "N/A"
                material_name = item[1] if len(item) > 1 else "N/A"
                print(f"  物料{i}: {material_code} - {material_name}")
            elif isinstance(item, dict):
                material_code = item.get('FNumber', 'N/A')
                material_name = item.get('FName', 'N/A')
                print(f"  物料{i}: {material_code} - {material_name}")
            else:
                print(f"  物料{i}: {item}")
    else:
        print("无物料数据或数据格式异常")
        print(f"原始数据: {data}")

def display_customer_data(data):
    """显示客户数据"""
    if isinstance(data, list) and len(data) > 0:
        print(f"获取到 {len(data)} 条客户记录:")
        for i, item in enumerate(data, 1):
            if isinstance(item, list) and len(item) >= 2:
                cust_code = item[0] if len(item) > 0 else "N/A"
                cust_name = item[1] if len(item) > 1 else "N/A"
                print(f"  客户{i}: {cust_code} - {cust_name}")
            elif isinstance(item, dict):
                cust_code = item.get('FNumber', 'N/A')
                cust_name = item.get('FName', 'N/A')
                print(f"  客户{i}: {cust_code} - {cust_name}")
            else:
                print(f"  客户{i}: {item}")
    else:
        print("无客户数据或数据格式异常")
        print(f"原始数据: {data}")

def test_smart_data():
    """智能数据测试"""
    
    config = {
        "server_url": "http://192.168.18.224:8191/K3cloud/",
        "acct_id": "63808a1c67ad59",
        "user_name": "TC-ERP",
        "app_id": "245766_x7aO28Fo6IC4X8XIR7WNS8VK0i1XWOts",
        "app_sec": "64f040f95085432ab9447b8549f1fe78",
        "lcid": 2052,
        "org_num": 0
    }
    
    print("金蝶云星空智能数据测试")
    print("=" * 50)
    
    try:
        tool = create_kingdee_tool(config)
        print("✓ 工具初始化成功")
        
        # 测试1: 物料查询
        print("\n=== 测试1: 物料查询 ===")
        result = tool.query_materials(limit=10)
        
        if result.get("success"):
            data = result.get("data", {})
            if data and "Result" in data:
                display_material_data(data["Result"])
            else:
                print("数据格式异常:", json.dumps(data, ensure_ascii=False))
        else:
            print(f"查询失败: {result.get('error')}")
        
        # 测试2: 客户查询（使用正确的字段）
        print("\n=== 测试2: 客户查询 ===")
        result = tool.execute_api("BD_Customer", KingdeeAPIType.BILL_QUERY, {
            "FormId": "BD_Customer",
            "FieldKeys": "FNumber,FName",
            "FilterString": "",
            "Limit": 10,
            "StartRow": 0
        })
        
        if result.get("success"):
            data = result.get("data", {})
            if data and "Result" in data:
                display_customer_data(data["Result"])
            else:
                print("数据格式异常:", json.dumps(data, ensure_ascii=False))
        else:
            print(f"查询失败: {result.get('error')}")
        
        # 测试3: 获取系统基础信息
        print("\n=== 测试3: 系统信息 ===")
        # 金蝶API没有直接的GET_SYSTEM_INFO，我们可以测试其他基础API
        
        # 测试4: 获取单据类型
        print("\n=== 测试4: 获取单据类型 ===")
        result = tool.execute_api("", KingdeeAPIType.GET_BILL_TYPE, {
            "FormId": "BD_MATERIAL"
        })
        
        if result.get("success"):
            print("获取单据类型成功:", json.dumps(result.get("data"), ensure_ascii=False))
        else:
            print(f"获取单据类型失败: {result.get('error')}")
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_smart_data()