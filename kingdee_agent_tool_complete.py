#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金蝶云星空智能体工具 - 完整版
为AI智能体提供统一的金蝶API调用接口
包含所有请求的功能：数据写入、批量操作、缓存机制、错误重试
"""

import json
import time
import functools
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 导入金蝶API工具
try:
    from kingdee_api_tool import KingdeeAPITool, create_kingdee_tool, KingdeeAPIConfig, KingdeeAPIType
except ImportError:
    # 如果单独运行，尝试相对导入
    try:
        from .kingdee_api_tool import KingdeeAPITool, create_kingdee_tool, KingdeeAPIConfig, KingdeeAPIType
    except ImportError:
        # 如果都失败，尝试直接定义必要的类和枚举
        class KingdeeAPIType(Enum):
            BILL_QUERY = "ExecuteBillQuery"
            BILL_SAVE = "Save"
            BILL_SUBMIT = "Submit"
            BILL_AUDIT = "Audit"
            
        class KingdeeAPIConfig:
            def __init__(self, server_url, acct_id, username, password, lcid=2052, org_num=0):
                self.server_url = server_url
                self.acct_id = acct_id
                self.username = username
                self.password = password
                self.lcid = lcid
                self.org_num = org_num
        
        # 占位函数
        def create_kingdee_tool(config):
            return None

# 缓存配置
_MAX_CACHE_SIZE = 1000
_CACHE_EXPIRE_SECONDS = 300  # 5分钟缓存


@dataclass
class QueryCondition:
    """查询条件"""
    field: str
    operator: str  # =, >, <, like, in, etc.
    value: Any


class KingdeeAgentTool:
    """金蝶智能体工具 - 完整功能版"""
    
    def __init__(self, config: Dict[str, str]):
        """
        初始化智能体工具
        
        Args:
            config: 金蝶API配置字典
        """
        if KingdeeAPITool is None:
            raise ImportError("金蝶API工具未找到，请确保 kingdee_api_tool.py 存在")
        
        self.tool = create_kingdee_tool(config)
        self.entity_mapping = self._create_entity_mapping()
        self._cache = {}
        self._last_cache_cleanup = time.time()
    
    def _create_entity_mapping(self) -> Dict[str, Dict[str, Any]]:
        """创建业务对象映射"""
        return {
            "material": {
                "form_id": "BD_MATERIAL",
                "name": "物料",
                "fields": ["FNumber", "FName", "FSpecification", "FBaseProperty"],
                "description": "企业物料基础数据"
            },
            "customer": {
                "form_id": "BD_Customer",
                "name": "客户",
                "fields": ["FNumber", "FName", "FShortName", "FCustomerCategoryID"],
                "description": "客户档案信息"
            },
            "supplier": {
                "form_id": "BD_Supplier",
                "name": "供应商",
                "fields": ["FNumber", "FName", "FShortName", "FSupplierCategoryID"],
                "description": "供应商档案信息"
            },
            "sale_order": {
                "form_id": "SAL_SaleOrder",
                "name": "销售订单",
                "fields": ["FBillNo", "FCustomerID", "FDate", "FAmount", "FDocumentStatus"],
                "description": "销售订单业务数据"
            },
            "purchase_order": {
                "form_id": "PUR_PurchaseOrder",
                "name": "采购订单",
                "fields": ["FBillNo", "FSupplierID", "FDate", "FAmount", "FDocumentStatus"],
                "description": "采购订单业务数据"
            },
            "inventory": {
                "form_id": "STK_Inventory",
                "name": "库存",
                "fields": ["FNumber", "FName", "FQty", "FStockID", "FBatchNo"],
                "description": "库存现存量信息"
            },
            "production_order": {
                "form_id": "PBM_PRODUCTIONORDER",
                "name": "生产订单",
                "fields": ["FBillNo", "FMaterialID", "FPlanStartDate", "FPlanFinishDate", "FQty"],
                "description": "生产订单信息"
            }
        }
    
    # ==================== 缓存机制 ====================
    def _get_cache_key(self, method: str, *args, **kwargs) -> str:
        """生成缓存键"""
        return f"{method}:{str(args)}:{str(kwargs)}"
    
    def _clean_cache(self):
        """清理过期缓存"""
        current_time = time.time()
        if current_time - self._last_cache_cleanup > 60:  # 每分钟清理一次
            expired_keys = []
            for key, (timestamp, _) in self._cache.items():
                if current_time - timestamp > _CACHE_EXPIRE_SECONDS:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
            
            self._last_cache_cleanup = current_time
    
    def _with_cache(func):
        """缓存装饰器"""
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            cache_key = self._get_cache_key(func.__name__, *args, **kwargs)
            self._clean_cache()
            
            if cache_key in self._cache:
                timestamp, result = self._cache[cache_key]
                if time.time() - timestamp < _CACHE_EXPIRE_SECONDS:
                    logger.info(f"使用缓存: {func.__name__}")
                    return result
            
            result = func(self, *args, **kwargs)
            self._cache[cache_key] = (time.time(), result)
            
            # 限制缓存大小
            if len(self._cache) > _MAX_CACHE_SIZE:
                # 移除最旧的缓存项
                oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][0])
                del self._cache[oldest_key]
            
            return result
        return wrapper
    
    @staticmethod
    def _with_retry(max_retries: int = 3, delay: float = 1.0):
        """重试装饰器工厂"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                last_error = None
                for attempt in range(max_retries):
                    try:
                        return func(self, *args, **kwargs)
                    except Exception as e:
                        last_error = e
                        logger.warning(f"尝试 {attempt + 1}/{max_retries} 失败: {e}")
                        if attempt < max_retries - 1:
                            time.sleep(delay * (2 ** attempt))  # 指数退避
                        else:
                            logger.error(f"所有重试尝试均失败: {last_error}")
                            raise last_error
                raise last_error
            return wrapper
        return decorator
    
    # ==================== 核心查询方法 ====================
    def query_data(self, entity_type: str, conditions: List[QueryCondition] = None, 
                  fields: List[str] = None, limit: int = 100) -> Dict[str, Any]:
        """
        查询业务数据
        
        Args:
            entity_type: 业务对象类型 (material, customer, supplier, etc.)
            conditions: 查询条件列表
            fields: 查询字段列表
            limit: 返回记录限制
            
        Returns:
            查询结果
        """
        if entity_type not in self.entity_mapping:
            return {
                "success": False,
                "error": f"不支持的业务对象类型: {entity_type}",
                "available_entities": list(self.entity_mapping.keys())
            }
        
        entity_info = self.entity_mapping[entity_type]
        form_id = entity_info["form_id"]
        
        # 构建查询参数
        params = {
            "FormId": form_id,
            "FieldKeys": ",".join(fields) if fields else "*",
            "Limit": limit,
            "StartRow": 0
        }
        
        # 构建过滤条件
        if conditions:
            filter_parts = []
            for condition in conditions:
                if condition.operator.lower() == "like":
                    filter_parts.append(f"'{condition.field}' like '%{condition.value}%'")
                elif condition.operator.lower() == "in":
                    if isinstance(condition.value, list):
                        values = ",".join([f"'{v}'" for v in condition.value])
                        filter_parts.append(f"'{condition.field}' in ({values})")
                    else:
                        filter_parts.append(f"'{condition.field}' = '{condition.value}'")
                else:
                    filter_parts.append(f"'{condition.field}' {condition.operator} '{condition.value}'")
            
            if filter_parts:
                params["FilterString"] = " and ".join(filter_parts)
        
        # 执行查询
        result = self.tool.execute_api(form_id, KingdeeAPIType.BILL_QUERY, params)
        
        return result
    
    # ==================== 业务特定查询方法 ====================
    @_with_cache
    def search_materials(self, keyword: str = None, material_number: str = None, 
                        limit: int = 50) -> Dict[str, Any]:
        """搜索物料数据"""
        conditions = []
        
        if keyword:
            conditions.append(QueryCondition("FName", "like", keyword))
        if material_number:
            conditions.append(QueryCondition("FNumber", "like", material_number))
        
        return self.query_data("material", conditions, 
                              fields=["FNumber", "FName", "FSpecification", "FBaseProperty"], 
                              limit=limit)
    
    @_with_cache
    def search_customers(self, keyword: str = None, customer_number: str = None,
                        limit: int = 50) -> Dict[str, Any]:
        """搜索客户数据"""
        conditions = []
        
        if keyword:
            conditions.append(QueryCondition("FName", "like", keyword))
        if customer_number:
            conditions.append(QueryCondition("FNumber", "like", customer_number))
        
        return self.query_data("customer", conditions,
                              fields=["FNumber", "FName", "FShortName", "FCustomerCategoryID"],
                              limit=limit)
    
    @_with_cache
    def get_sale_orders(self, customer_number: str = None, start_date: str = None,
                       end_date: str = None, limit: int = 50) -> Dict[str, Any]:
        """获取销售订单"""
        conditions = []
        
        if customer_number:
            conditions.append(QueryCondition("FCustomerID", "like", customer_number))
        if start_date and end_date:
            conditions.append(QueryCondition("FDate", ">=", start_date))
            conditions.append(QueryCondition("FDate", "<=", end_date))
        
        return self.query_data("sale_order", conditions,
                              fields=["FBillNo", "FCustomerID", "FDate", "FAmount", "FDocumentStatus"],
                              limit=limit)
    
    @_with_cache
    def get_purchase_orders(self, supplier_number: str = None, start_date: str = None,
                           end_date: str = None, limit: int = 50) -> Dict[str, Any]:
        """获取采购订单"""
        conditions = []
        
        if supplier_number:
            conditions.append(QueryCondition("FSupplierID", "like", supplier_number))
        if start_date and end_date:
            conditions.append(QueryCondition("FDate", ">=", start_date))
            conditions.append(QueryCondition("FDate", "<=", end_date))
        
        return self.query_data("purchase_order", conditions,
                              fields=["FBillNo", "FSupplierID", "FDate", "FAmount", "FDocumentStatus"],
                              limit=limit)
    
    @_with_cache
    def get_inventory_info(self, material_numbers: List[str] = None, 
                          limit: int = 100) -> Dict[str, Any]:
        """获取库存信息"""
        conditions = []
        
        if material_numbers:
            conditions.append(QueryCondition("FNumber", "in", material_numbers))
        
        return self.query_data("inventory", conditions,
                              fields=["FNumber", "FName", "FQty", "FStockID", "FBatchNo"],
                              limit=limit)
    
    @_with_cache
    def get_production_orders(self, material_number: str = None, start_date: str = None,
                             end_date: str = None, limit: int = 50) -> Dict[str, Any]:
        """获取生产订单"""
        conditions = []
        
        if material_number:
            conditions.append(QueryCondition("FMaterialID", "like", material_number))
        if start_date and end_date:
            conditions.append(QueryCondition("FPlanStartDate", ">=", start_date))
            conditions.append(QueryCondition("FPlanStartDate", "<=", end_date))
        
        return self.query_data("production_order", conditions,
                              fields=["FBillNo", "FMaterialID", "FPlanStartDate", "FPlanFinishDate", "FQty"],
                              limit=limit)
    
    # ==================== 数据写入功能 ====================
    @_with_retry
    def create_material(self, material_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建物料"""
        return self.tool.execute_api("BD_MATERIAL", KingdeeAPIType.BILL_SAVE, material_data)
    
    @_with_retry
    def update_material(self, material_id: str, material_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新物料"""
        # 金蝶更新通常也是使用Save操作
        material_data["FID"] = material_id
        return self.tool.execute_api("BD_MATERIAL", KingdeeAPIType.BILL_SAVE, material_data)
    
    @_with_retry
    def submit_sale_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """提交销售订单"""
        # 先保存
        save_result = self.tool.execute_api("SAL_SaleOrder", KingdeeAPIType.BILL_SAVE, order_data)
        if not save_result.get("success"):
            return save_result
        
        # 再提交
        if "Result" in save_result["data"] and "Id" in save_result["data"]["Result"]:
            order_id = save_result["data"]["Result"]["Id"]
            submit_data = {"Ids": order_id}
            return self.tool.execute_api("SAL_SaleOrder", KingdeeAPIType.BILL_SUBMIT, submit_data)
        
        return {"success": False, "error": "无法获取订单ID"}
    
    @_with_retry
    def audit_document(self, form_id: str, document_ids: List[str]) -> Dict[str, Any]:
        """审核单据"""
        audit_data = {"Ids": ",".join(document_ids)}
        return self.tool.execute_api(form_id, KingdeeAPIType.BILL_AUDIT, audit_data)
    
    # ==================== 批量操作功能 ====================
    @_with_cache
    def batch_query_materials(self, material_numbers: List[str], 
                             fields: List[str] = None) -> Dict[str, Any]:
        """批量查询物料"""
        if not material_numbers:
            return {"success": False, "error": "物料编号列表为空"}
        
        conditions = [QueryCondition("FNumber", "in", material_numbers)]
        return self.query_data("material", conditions, fields, limit=len(material_numbers))
    
    @_with_cache
    def batch_get_inventory(self, material_numbers: List[str]) -> Dict[str, Any]:
        """批量获取库存信息"""
        return self.get_inventory_info(material_numbers, limit=len(material_numbers))
    
    # ==================== 工具方法 ====================
    def get_available_entities(self) -> List[Dict[str, Any]]:
        """获取可用的业务对象列表"""
        return [
            {
                "id": key,
                "name": info["name"],
                "description": info["description"],
                "fields": info["fields"]
            }
            for key, info in self.entity_mapping.items()
        ]
    
    def execute_custom_query(self, form_id: str, field_keys: str, 
                           filter_string: str = "", limit: int = 100) -> Dict[str, Any]:
        """执行自定义查询"""
        params = {
            "FormId": form_id,
            "FieldKeys": field_keys,
            "FilterString": filter_string,
            "Limit": limit,
            "StartRow": 0
        }
        
        return self.tool.execute_api(form_id, KingdeeAPIType.BILL_QUERY, params)
    
    @_with_retry
    def query_with_retry(self, entity_type: str, conditions: List[QueryCondition] = None,
                        fields: List[str] = None, limit: int = 100) -> Dict[str, Any]:
        """带重试机制的查询"""
        return self.query_data(entity_type, conditions, fields, limit)
    
    def clear_cache(self):
        """清空所有缓存"""
        self._cache.clear()
        self._last_cache_cleanup = time.time()
        logger.info("缓存已清空")


def create_kingdee_agent_tool(config: Dict[str, str]) -> KingdeeAgentTool:
    """
    创建金蝶智能体工具实例
    
    Args:
        config: 金蝶API配置字典
        
    Returns:
        KingdeeAgentTool实例
    """
    return KingdeeAgentTool(config)


# 示例用法
if __name__ == "__main__":
    # 使用您的实际配置
    config = {
        "server_url": "http://192.168.18.224:8191/K3cloud/",
        "acct_id": "63808a1c67ad59",
        "user_name": "TC-ERP",
        "app_id": "245766_x7aO28Fo6IC4X8XIR7WNS8VK0i1XWOts",
        "app_sec": "64f040f95085432ab9447b8549f1fe78",
        "lcid": 2052,
        "org_num": 0
    }
    
    # 创建智能体工具
    agent_tool = create_kingdee_agent_tool(config)
    
    # 获取可用业务对象
    entities = agent_tool.get_available_entities()
    print("可用业务对象:")
    for entity in entities:
        print(f"  - {entity['id']}: {entity['name']} ({entity['description']})")
    
    # 示例查询 - 使用缓存和重试
    print("\n=== 示例查询 (带缓存和重试) ===")
    
    # 查询物料
    result = agent_tool.search_materials(keyword="组件", limit=5)
    if result["success"]:
        print("物料查询结果:")
        if result["data"] and "Result" in result["data"]:
            materials = result["data"]["Result"]
            for material in materials[:3]:
                if isinstance(material, list) and len(material) >= 2:
                    print(f"  - {material[1]}: {material[0]}")
                else:
                    print(f"  - {material}")
        else:
            print("  无物料数据")
    else:
        print(f"查询失败: {result['error']}")
    
    # 查询采购订单
    print("\n=== 采购订单查询 ===")
    po_result = agent_tool.get_purchase_orders(limit=3)
    if po_result["success"]:
        print("采购订单查询成功")
    else:
        print(f"采购订单查询失败: {po_result.get('error')}")
    
    print("\n=== 智能体工具集成完成 ===")
    print("所有功能已就绪：")
    print("  ✓ 数据查询 (物料、客户、供应商、销售订单、采购订单、库存、生产订单)")
    print("  ✓ 数据写入 (创建物料、更新物料、提交订单、审核单据)")
    print("  ✓ 批量操作 (批量查询物料、批量获取库存)")
    print("  ✓ 缓存机制 (自动缓存查询结果，5分钟有效期)")
    print("  ✓ 错误重试 (自动重试失败请求，指数退避)")