#
#  Copyright 2024 The InfiniFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import json
import time
from typing import Dict, List, Any, Optional
from abc import ABC
from agent.component.base import ComponentBase, ComponentParamBase


class KingdeeParam(ComponentParamBase):
    """
    Kingdee OpenAPI 工具参数配置
    """

    def __init__(self):
        super().__init__()
        self.server_url = "https://api.kingdee.com"
        self.acct_id = ""
        self.username = ""
        self.app_id = ""
        self.app_sec = ""
        self.lcid = 2052
        self.org_num = 0

    def check(self):
        """参数校验"""
        if not self.acct_id:
            raise ValueError("acct_id 不能为空")
        if not self.username:
            raise ValueError("username 不能为空")
        if not self.app_id:
            raise ValueError("app_id 不能为空")
        if not self.app_sec:
            raise ValueError("app_sec 不能为空")


class Kingdee(ComponentBase, ABC):
    """
    Kingdee OpenAPI 工具 - 提供金蝶云星空系统的数据查询和操作功能
    """
    
    component_name = "Kingdee"
    
    def __init__(self, canvas, id, param: KingdeeParam):
        super().__init__(canvas, id, param)
        # 延迟导入以避免循环依赖
        from kingdee_agent_tool_complete import KingdeeAgentTool
        
        # 初始化Kingdee工具实例
        config = {
            "server_url": param.server_url,
            "acct_id": param.acct_id,
            "user_name": param.username,  # Map username to user_name
            "app_id": param.app_id,
            "app_sec": param.app_sec,
            "lcid": param.lcid,
            "org_num": param.org_num
        }
        self.kingdee_tool = KingdeeAgentTool(config)
    
    def _run(self, history, **kwargs):
        """
        执行Kingdee操作
        """
        if self.check_if_canceled("Kingdee processing"):
            return
        
        # 获取操作类型和参数
        operation = kwargs.get("operation", "query")
        entity_type = kwargs.get("entity_type", "material")
        
        try:
            if operation == "query":
                # 查询数据
                conditions = kwargs.get("conditions", [])
                fields = kwargs.get("fields", None)
                limit = kwargs.get("limit", 100)
                
                result = self.kingdee_tool.query_data(
                    entity_type=entity_type,
                    conditions=conditions,
                    fields=fields,
                    limit=limit
                )
                
            elif operation == "create_material":
                # 创建物料
                material_data = kwargs.get("material_data", {})
                result = self.kingdee_tool.create_material(material_data)
                
            elif operation == "update_material":
                # 更新物料
                material_data = kwargs.get("material_data", {})
                result = self.kingdee_tool.update_material(material_data)
                
            elif operation == "query_sale_order":
                # 查询销售订单
                conditions = kwargs.get("conditions", [])
                fields = kwargs.get("fields", None)
                limit = kwargs.get("limit", 100)
                
                result = self.kingdee_tool.query_sale_order(
                    conditions=conditions,
                    fields=fields,
                    limit=limit
                )
                
            elif operation == "query_purchase_order":
                # 查询采购订单
                conditions = kwargs.get("conditions", [])
                fields = kwargs.get("fields", None)
                limit = kwargs.get("limit", 100)
                
                result = self.kingdee_tool.query_purchase_order(
                    conditions=conditions,
                    fields=fields,
                    limit=limit
                )
                
            elif operation == "query_inventory":
                # 查询库存
                conditions = kwargs.get("conditions", [])
                fields = kwargs.get("fields", None)
                limit = kwargs.get("limit", 100)
                
                result = self.kingdee_tool.query_inventory(
                    conditions=conditions,
                    fields=fields,
                    limit=limit
                )
                
            elif operation == "query_production_order":
                # 查询生产订单
                conditions = kwargs.get("conditions", [])
                fields = kwargs.get("fields", None)
                limit = kwargs.get("limit", 100)
                
                result = self.kingdee_tool.query_production_order(
                    conditions=conditions,
                    fields=fields,
                    limit=limit
                )
                
            elif operation == "batch_query_materials":
                # 批量查询物料
                material_numbers = kwargs.get("material_numbers", [])
                fields = kwargs.get("fields", None)
                
                result = self.kingdee_tool.batch_query_materials(
                    material_numbers=material_numbers,
                    fields=fields
                )
                
            elif operation == "batch_get_inventory":
                # 批量获取库存
                material_numbers = kwargs.get("material_numbers", [])
                stock_orgs = kwargs.get("stock_orgs", [])
                
                result = self.kingdee_tool.batch_get_inventory(
                    material_numbers=material_numbers,
                    stock_orgs=stock_orgs
                )
                
            elif operation == "submit_sale_order":
                # 提交销售订单
                order_data = kwargs.get("order_data", {})
                result = self.kingdee_tool.submit_sale_order(order_data)
                
            elif operation == "audit_document":
                # 审核单据
                form_id = kwargs.get("form_id", "")
                document_id = kwargs.get("document_id", "")
                
                result = self.kingdee_tool.audit_document(
                    form_id=form_id,
                    document_id=document_id
                )
                
            else:
                result = {
                    "success": False,
                    "error": f"不支持的操作类型: {operation}"
                }
            
            # 返回格式化结果
            if result.get("success", False):
                data = result.get("data", [])
                if isinstance(data, list):
                    return {
                        "status": "success",
                        "count": len(data),
                        "data": data[:10] if len(data) > 10 else data,
                        "total_count": len(data)
                    }
                else:
                    return {
                        "status": "success",
                        "data": data
                    }
            else:
                return {
                    "status": "error",
                    "error": result.get("error", "未知错误")
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": f"Kingdee操作失败: {str(e)}"
            }
    
    def get_meta(self) -> dict[str, Any]:
        """
        获取工具的元数据定义
        """
        return {
            "type": "function",
            "function": {
                "name": "kingdee_operation",
                "description": "执行金蝶云星空系统的数据查询和操作，包括物料、销售订单、采购订单、库存、生产订单等的查询、创建、修改、审核等操作",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "操作类型",
                            "enum": [
                                "query", "create_material", "update_material", 
                                "query_sale_order", "query_purchase_order", "query_inventory", 
                                "query_production_order", "batch_query_materials", "batch_get_inventory",
                                "submit_sale_order", "audit_document"
                            ]
                        },
                        "entity_type": {
                            "type": "string",
                            "description": "实体类型（当operation为query时使用）",
                            "enum": ["material", "sale_order", "purchase_order", "inventory", "production_order"]
                        },
                        "conditions": {
                            "type": "array",
                            "description": "查询条件列表，每个条件格式为{\"field\": \"字段名\", \"operator\": \"操作符\", \"value\": \"值\"}",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {"type": "string"},
                                    "operator": {"type": "string"},
                                    "value": {"type": "any"}
                                }
                            }
                        },
                        "fields": {
                            "type": "array",
                            "description": "需要返回的字段列表",
                            "items": {"type": "string"}
                        },
                        "limit": {
                            "type": "integer",
                            "description": "返回结果数量限制"
                        },
                        "material_data": {
                            "type": "object",
                            "description": "物料数据（创建或更新时使用）"
                        },
                        "material_numbers": {
                            "type": "array",
                            "description": "物料编号列表（批量操作时使用）",
                            "items": {"type": "string"}
                        },
                        "stock_orgs": {
                            "type": "array",
                            "description": "库存组织列表（批量获取库存时使用）",
                            "items": {"type": "string"}
                        },
                        "order_data": {
                            "type": "object",
                            "description": "订单数据（提交订单时使用）"
                        },
                        "form_id": {
                            "type": "string",
                            "description": "表单ID（审核单据时使用）"
                        },
                        "document_id": {
                            "type": "string",
                            "description": "单据ID（审核单据时使用）"
                        }
                    },
                    "required": ["operation"]
                }
            }
        }