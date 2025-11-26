#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Kingdee工具集成到智能体系统
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # 测试导入Kingdee工具
    from agent.tools.kingdee import Kingdee, KingdeeParam
    print("✓ Kingdee工具导入成功")
    
    # 测试导入KingdeeAgentTool
    from kingdee_agent_tool_complete import KingdeeAgentTool
    print("✓ KingdeeAgentTool导入成功")
    
    # 测试创建参数实例
    param = KingdeeParam()
    print("✓ KingdeeParam创建成功")
    
    # 测试创建KingdeeAgentTool实例
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
    print("✓ KingdeeAgentTool实例创建成功")
    
    print("\n🎉 所有集成测试通过！Kingdee工具已成功集成到智能体系统中")
    
except ImportError as e:
    print(f"✗ 导入失败: {e}")
    print("请检查文件路径和导入语句")
    
except Exception as e:
    print(f"✗ 其他错误: {e}")
    import traceback
    traceback.print_exc()