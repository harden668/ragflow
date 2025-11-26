#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金蝶云星空API工具测试脚本
"""

import json
import os
from kingdee_api_tool import KingdeeAPITool, KingdeeAPIConfig, create_kingdee_tool, KingdeeAPIType


def test_kingdee_tool():
    """测试金蝶API工具"""
    
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
    
    print("正在初始化金蝶API工具...")
    print(f"服务器: {config['server_url']}")
    print(f"账套ID: {config['acct_id']}")
    print(f"用户名: {config['user_name']}")
    
    try:
        # 创建API工具实例
        tool = create_kingdee_tool(config)
        print("✓ 金蝶API工具初始化成功")
        
        # 测试1: 查询物料数据
        print("\n=== 测试1: 查询物料数据 ===")
        result = tool.query_materials(
            filter_string="'FNumber' like '01%'",
            field_keys="FNumber,FName,FCreateOrgId",
            limit=10
        )
        
        if result["success"]:
            print("✓ 物料查询成功")
            if result["data"] and "Result" in result["data"]:
                materials = result["data"]["Result"]
                print(f"获取到 {len(materials)} 条物料记录")
                for i, material in enumerate(materials[:3], 1):
                    print(f"  物料{i}: {material.get('FNumber', 'N/A')} - {material.get('FName', 'N/A')}")
            else:
                print("⚠ 无物料数据返回")
        else:
            print(f"✗ 物料查询失败: {result['error']}")
        
        # 测试2: 查询客户数据
        print("\n=== 测试2: 查询客户数据 ===")
        result = tool.query_customers(
            filter_string="",
            field_keys="FNumber,FName",
            limit=5
        )
        
        if result["success"]:
            print("✓ 客户查询成功")
            if result["data"] and "Result" in result["data"]:
                customers = result["data"]["Result"]
                print(f"获取到 {len(customers)} 条客户记录")
                for i, customer in enumerate(customers[:3], 1):
                    print(f"  客户{i}: {customer.get('FNumber', 'N/A')} - {customer.get('FName', 'N/A')}")
            else:
                print("⚠ 无客户数据返回")
        else:
            print(f"✗ 客户查询失败: {result['error']}")
        
        # 测试3: 自定义API调用
        print("\n=== 测试3: 自定义单据查询 ===")
        params = {
            "FormId": "BD_MATERIAL",
            "FieldKeys": "FNumber,FName",
            "FilterString": "",
            "Limit": 3,
            "StartRow": 0
        }
        
        result = tool.execute_api("BD_MATERIAL", KingdeeAPIType.BILL_QUERY, params)
        
        if result["success"]:
            print("✓ 自定义查询成功")
            if result["data"] and "Result" in result["data"]:
                items = result["data"]["Result"]
                print(f"获取到 {len(items)} 条记录")
                for i, item in enumerate(items, 1):
                    print(f"  记录{i}: {item.get('FNumber', 'N/A')} - {item.get('FName', 'N/A')}")
            else:
                print("⚠ 无数据返回")
        else:
            print(f"✗ 自定义查询失败: {result['error']}")
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"✗ 工具初始化或测试失败: {e}")
        print("请检查:")
        print("1. 金蝶SDK是否安装: pip install kingdee.cdp.webapi.sdk")
        print("2. 网络连接是否正常")
        print("3. API配置参数是否正确")


def test_config_validation():
    """测试配置验证"""
    print("\n=== 配置验证测试 ===")
    
    # 测试缺少必要参数
    try:
        invalid_config = {
            "server_url": "https://apiexp.open.kingdee.com/k3cloud/",
            "user_name": "demo"
            # 缺少 acct_id, app_id, app_sec
        }
        tool = create_kingdee_tool(invalid_config)
        print("✗ 配置验证应该失败")
    except TypeError as e:
        print("✓ 配置验证正确捕获参数缺失错误")
    
    # 测试有效配置
    valid_config = {
        "server_url": "http://192.168.18.224:8191/K3cloud/",
        "acct_id": "63808a1c67ad59",
        "user_name": "TC-ERP",
        "app_id": "245766_x7aO28Fo6IC4X8XIR7WNS8VK0i1XWOts",
        "app_sec": "64f040f95085432ab9447b8549f1fe78",
        "lcid": 2052,
        "org_num": 0
    }
    
    try:
        tool = create_kingdee_tool(valid_config)
        print("✓ 有效配置验证通过")
    except Exception as e:
        print(f"✗ 有效配置验证失败: {e}")


if __name__ == "__main__":
    print("金蝶云星空API工具测试")
    print("=" * 50)
    
    # 运行配置验证测试
    test_config_validation()
    
    # 运行API功能测试
    test_kingdee_tool()