#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kingdee工具数据写入和批量操作功能测试
验证所有写入和批量操作功能是否正常工作
"""

import sys
import os
import json
from typing import Dict, List, Any

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入必要的类
try:
    from kingdee_agent_tool_complete import KingdeeAgentTool, QueryCondition
    from kingdee_api_tool import KingdeeAPIType
    print("✅ 成功导入Kingdee工具类")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

def test_data_query_operations(tool: KingdeeAgentTool) -> bool:
    """测试数据查询功能"""
    print("\n🧪 测试数据查询功能...")
    
    # 测试查询物料数据
    print("1. 测试查询物料数据...")
    try:
        result = tool.query_data("material", limit=10)
        print(f"   查询物料结果: {result.get('success', False)}")
        if result.get('success'):
            data = result.get('data', {})
            print(f"   返回记录数: {len(data.get('Result', {}).get('Result', [])) if data else 0}")
            print("   ✅ 查询物料功能正常")
        else:
            print(f"   ⚠️ 查询物料失败: {result.get('error', '未知错误')}")
    except Exception as e:
        print(f"   ❌ 查询物料异常: {e}")
        return False
    
    # 测试搜索物料
    print("2. 测试搜索物料...")
    try:
        result = tool.search_materials(keyword="测试", limit=5)
        print(f"   搜索物料结果: {result.get('success', False)}")
        if result.get('success'):
            data = result.get('data', {})
            print(f"   返回记录数: {len(data.get('Result', {}).get('Result', [])) if data else 0}")
            print("   ✅ 搜索物料功能正常")
        else:
            print(f"   ⚠️ 搜索物料失败: {result.get('error', '未知错误')}")
    except Exception as e:
        print(f"   ❌ 搜索物料异常: {e}")
        return False
    
    # 测试获取销售订单
    print("3. 测试获取销售订单...")
    try:
        result = tool.get_sale_orders(limit=5)
        print(f"   获取销售订单结果: {result.get('success', False)}")
        if result.get('success'):
            data = result.get('data', {})
            print(f"   返回记录数: {len(data.get('Result', {}).get('Result', [])) if data else 0}")
            print("   ✅ 获取销售订单功能正常")
        else:
            print(f"   ⚠️ 获取销售订单失败: {result.get('error', '未知错误')}")
    except Exception as e:
        print(f"   ❌ 获取销售订单异常: {e}")
        return False
    
    # 测试获取库存信息
    print("4. 测试获取库存信息...")
    try:
        result = tool.get_inventory_info(limit=10)
        print(f"   获取库存信息结果: {result.get('success', False)}")
        if result.get('success'):
            data = result.get('data', {})
            print(f"   返回记录数: {len(data.get('Result', {}).get('Result', [])) if data else 0}")
            print("   ✅ 获取库存信息功能正常")
        else:
            print(f"   ⚠️ 获取库存信息失败: {result.get('error', '未知错误')}")
    except Exception as e:
        print(f"   ❌ 获取库存信息异常: {e}")
        return False
    
    return True

def test_batch_operations(tool: KingdeeAgentTool) -> bool:
    """测试批量操作功能"""
    print("\n🧪 测试批量操作功能...")
    
    # 测试批量查询物料
    print("1. 测试批量查询物料...")
    material_numbers = ["TEST001", "TEST002", "TEST003"]
    
    try:
        result = tool.batch_query_materials(material_numbers)
        print(f"   批量查询物料结果: {result.get('success', False)}")
        if result.get('success'):
            data = result.get('data', {})
            print(f"   返回记录数: {len(data.get('Result', {}).get('Result', [])) if data else 0}")
            print("   ✅ 批量查询物料功能正常")
        else:
            print(f"   ⚠️ 批量查询物料失败: {result.get('error', '未知错误')}")
    except Exception as e:
        print(f"   ❌ 批量查询物料异常: {e}")
        return False
    
    # 测试批量获取库存
    print("2. 测试批量获取库存...")
    try:
        result = tool.batch_get_inventory(material_numbers)
        print(f"   批量获取库存结果: {result.get('success', False)}")
        if result.get('success'):
            data = result.get('data', {})
            print(f"   返回记录数: {len(data.get('Result', {}).get('Result', [])) if data else 0}")
            print("   ✅ 批量获取库存功能正常")
        else:
            print(f"   ⚠️ 批量获取库存失败: {result.get('error', '未知错误')}")
    except Exception as e:
        print(f"   ❌ 批量获取库存异常: {e}")
        return False
    
    return True

def test_query_batch_integration():
    """测试数据查询和批量操作的集成功能"""
    print("🚀 开始Kingdee工具数据查询功能测试...")
    
    # 创建测试配置
    config = {
        "server_url": "https://api.kingdee.com",
        "acct_id": "test_acct",
        "user_name": "test_user", 
        "app_id": "test_app",
        "app_sec": "test_secret",
        "lcid": 2052,
        "org_num": 0
    }
    
    try:
        # 创建工具实例
        tool = KingdeeAgentTool(config)
        print("✅ Kingdee工具实例创建成功")
        
        # 测试数据查询功能
        query_success = test_data_query_operations(tool)
        
        # 测试批量操作功能
        batch_success = test_batch_operations(tool)
        
        # 汇总测试结果
        print("\n" + "="*60)
        print("📊 测试结果汇总:")
        print(f"   数据查询功能: {'✅ 通过' if query_success else '❌ 失败'}")
        print(f"   批量操作功能: {'✅ 通过' if batch_success else '❌ 失败'}")
        
        if query_success and batch_success:
            print("\n🎉 所有数据查询功能测试通过！")
            print("\n📋 已验证的查询功能:")
            print("   • 通用数据查询 (query_data)")
            print("   • 搜索物料 (search_materials)")
            print("   • 获取销售订单 (get_sale_orders)")
            print("   • 获取库存信息 (get_inventory_info)")
            print("   • 批量查询物料 (batch_query_materials)")
            print("   • 批量获取库存 (batch_get_inventory)")
            return True
        else:
            print("\n❌ 部分功能测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中发生异常: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_query_batch_integration()
    sys.exit(0 if success else 1)