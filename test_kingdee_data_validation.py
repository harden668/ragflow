#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金蝶云星空数据验证测试
测试实际数据查询条件和权限验证
"""

import os
import json
from kingdee_api_tool import create_kingdee_tool, KingdeeAPIType

def test_data_validation():
    """测试数据验证和查询条件"""
    
    # 使用您提供的测试配置
    config = {
        "server_url": "http://192.168.18.224:8191/K3cloud/",
        "acct_id": "63808a1c67ad59",
        "user_name": "TC-ERP",
        "app_id": "245766_x7aO28Fo6IC4X8XIR7WNS8VK0i1XWOts",
        "app_sec": "64f040f95085432ab9447b8549f1fe78",
        "lcid": 2052,
        "org_num": 0
    }
    
    print("金蝶云星空数据验证测试")
    print("=" * 50)
    print(f"服务器: {config['server_url']}")
    print(f"账套ID: {config['acct_id']}")
    print(f"用户名: {config['user_name']}")
    print()
    
    try:
        # 初始化工具
        tool = create_kingdee_tool(config)
        print("✓ 金蝶API工具初始化成功")
        
        # 测试1: 获取所有物料（无过滤条件）
        print("\n=== 测试1: 获取所有物料 ===")
        result = tool.query_materials(limit=5)
        if result.get("success"):
            data = result.get("data", {})
            if data and "Result" in data and data["Result"]:
                items = data["Result"]
                print(f"✓ 获取到 {len(items)} 条物料记录:")
                for i, item in enumerate(items, 1):
                    print(f"  物料{i}: {item.get('FNumber', 'N/A')} - {item.get('FName', 'N/A')}")
            else:
                print("⚠ 无物料数据返回")
                print(f"响应详情: {json.dumps(data, ensure_ascii=False, indent=2)}")
        else:
            print(f"✗ 物料查询失败: {result.get('error', '未知错误')}")
        
        # 测试2: 获取所有客户
        print("\n=== 测试2: 获取所有客户 ===")
        result = tool.query_customers(limit=5)
        if result.get("success"):
            data = result.get("data", {})
            if data and "Result" in data and data["Result"]:
                items = data["Result"]
                print(f"✓ 获取到 {len(items)} 条客户记录:")
                for i, item in enumerate(items, 1):
                    print(f"  客户{i}: {item.get('FNumber', 'N/A')} - {item.get('FName', 'N/A')}")
            else:
                print("⚠ 无客户数据返回")
                print(f"响应详情: {json.dumps(data, ensure_ascii=False, indent=2)}")
        else:
            print(f"✗ 客户查询失败: {result.get('error', '未知错误')}")
        
        # 测试3: 测试不同的查询条件
        print("\n=== 测试3: 不同查询条件测试 ===")
        
        # 3.1 查询前10条记录
        print("\n--- 查询前10条物料记录 ---")
        result = tool.execute_api("BD_MATERIAL", KingdeeAPIType.BILL_QUERY, {
            "FormId": "BD_MATERIAL",
            "FieldKeys": "FNumber,FName,FCreateOrgId",
            "FilterString": "",
            "Limit": 10,
            "StartRow": 0
        })
        
        if result.get("success"):
            data = result.get("data", {})
            if data and "Result" in data:
                items = data["Result"]
                print(f"获取到 {len(items)} 条记录")
                if items:
                    for i, item in enumerate(items[:3], 1):  # 只显示前3条
                        print(f"  记录{i}: {item.get('FNumber', 'N/A')} - {item.get('FName', 'N/A')}")
                    if len(items) > 3:
                        print(f"  ... 还有 {len(items) - 3} 条记录")
            else:
                print("⚠ 无数据返回")
                print(f"完整响应: {json.dumps(data, ensure_ascii=False)}")
        else:
            print(f"✗ 查询失败: {result.get('error')}")
        
        # 3.2 测试权限验证 - 尝试获取系统信息
        print("\n--- 测试系统权限 ---")
        result = tool.execute_api("", KingdeeAPIType.GET_SYSTEM_INFO, {})
        if result.get("success"):
            print("✓ 系统权限验证通过")
            print(f"系统信息: {result.get('data', {})}")
        else:
            print(f"⚠ 系统权限测试: {result.get('error', '未知错误')}")
        
        # 3.3 测试获取单据类型
        print("\n--- 测试获取单据类型 ---")
        result = tool.execute_api("BD_MATERIAL", KingdeeAPIType.GET_BILL_TYPE, {})
        if result.get("success"):
            print("✓ 获取单据类型成功")
            print(f"单据类型: {result.get('data', {})}")
        else:
            print(f"⚠ 获取单据类型失败: {result.get('error', '未知错误')}")
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_data_validation()