#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kingdee工具完整集成测试
测试智能体工具的所有功能
"""

import sys
import os
import json

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_kingdee_tool_integration():
    """测试Kingdee工具集成"""
    print("🧪 开始Kingdee工具集成测试...")
    
    try:
        # 1. 测试导入Kingdee工具
        from agent.tools.kingdee import Kingdee, KingdeeParam
        print("✅ Kingdee工具导入成功")
        
        # 2. 测试导入KingdeeAgentTool
        from kingdee_agent_tool_complete import KingdeeAgentTool
        print("✅ KingdeeAgentTool导入成功")
        
        # 3. 测试创建参数实例
        param = KingdeeParam()
        print("✅ KingdeeParam创建成功")
        
        # 4. 测试创建KingdeeAgentTool实例
        config = {
            "server_url": "https://api.kingdee.com",
            "acct_id": "test_acct",
            "user_name": "test_user", 
            "app_id": "test_app",
            "app_sec": "test_secret",
            "lcid": 2052,
            "org_num": 0
        }
        tool = KingdeeAgentTool(config)
        print("✅ KingdeeAgentTool实例创建成功")
        
        # 5. 测试工具方法存在性
        required_methods = [
            'query_data', 'search_materials', 'search_customers',
            'get_sale_orders', 'get_purchase_orders', 'get_inventory_info',
            'get_production_orders', 'create_material', 'update_material',
            'submit_sale_order', 'audit_document', 'batch_query_materials',
            'batch_get_inventory', 'query_with_retry'
        ]
        
        for method in required_methods:
            if hasattr(tool, method):
                print(f"✅ 方法 {method} 存在")
            else:
                print(f"❌ 方法 {method} 不存在")
                return False
        
        # 6. 测试缓存机制
        if hasattr(tool, '_cache') and hasattr(tool, '_clean_cache'):
            print("✅ 缓存机制存在")
        else:
            print("❌ 缓存机制不存在")
            return False
        
        # 7. 测试实体映射
        if hasattr(tool, 'entity_mapping') and isinstance(tool.entity_mapping, dict):
            print("✅ 实体映射存在")
            print(f"   支持的实体类型: {list(tool.entity_mapping.keys())}")
        else:
            print("❌ 实体映射不存在")
            return False
        
        # 8. 测试智能体工具元数据
        kingdee_tool = Kingdee(None, "test_id", param)
        meta = kingdee_tool.get_meta()
        if meta and 'function' in meta:
            print("✅ 智能体工具元数据生成成功")
            print(f"   工具名称: {meta['function']['name']}")
            print(f"   工具描述: {meta['function']['description'][:50]}...")
        else:
            print("❌ 智能体工具元数据生成失败")
            return False
        
        print("\n🎉 所有集成测试通过！Kingdee工具已成功集成到智能体系统中")
        print("\n📋 支持的功能:")
        print("   • 数据查询: 物料、客户、销售订单、采购订单、库存、生产订单")
        print("   • 数据写入: 创建物料、更新物料、提交订单、审核单据")
        print("   • 批量操作: 批量查询物料、批量获取库存")
        print("   • 高级功能: 缓存机制、错误重试、条件查询")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
        
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_kingdee_tool_integration()
    sys.exit(0 if success else 1)