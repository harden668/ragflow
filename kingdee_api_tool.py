#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金蝶云星空WebAPI智能体工具
提供统一的接口调用工具，支持多种业务对象的数据查询和操作
"""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

# 尝试导入金蝶SDK
try:
    from k3cloud_webapi_sdk.main import K3CloudApiSdk
except ImportError:
    print("警告: 未找到金蝶SDK，请先安装 kingdee.cdp.webapi.sdk 包")
    K3CloudApiSdk = None


class KingdeeAPIType(Enum):
    """金蝶API接口类型枚举"""
    BILL_QUERY = "ExecuteBillQuery"  # 单据查询
    BILL_SAVE = "Save"  # 单据保存
    BILL_SUBMIT = "Submit"  # 单据提交
    BILL_AUDIT = "Audit"  # 单据审核
    BILL_VIEW = "View"  # 单据查看
    BILL_DELETE = "Delete"  # 单据删除
    REPORT_DATA = "GetSysReportData"  # 报表数据查询


@dataclass
class KingdeeAPIConfig:
    """金蝶API配置类"""
    server_url: str
    acct_id: str
    user_name: str
    app_id: str
    app_sec: str
    lcid: int = 2052
    org_num: int = 0
    connect_timeout: int = 120
    request_timeout: int = 120


class KingdeeAPITool:
    """金蝶云星空API调用工具类"""
    
    def __init__(self, config: KingdeeAPIConfig):
        """初始化API工具"""
        if K3CloudApiSdk is None:
            raise ImportError("金蝶SDK未安装，请先安装: pip install kingdee.cdp.webapi.sdk")
        
        self.config = config
        self.api_sdk = K3CloudApiSdk(config.server_url)
        self._initialize_sdk()
        
    def _initialize_sdk(self):
        """初始化SDK配置"""
        self.api_sdk.InitConfig(
            acct_id=self.config.acct_id,
            user_name=self.config.user_name,
            app_id=self.config.app_id,
            app_secret=self.config.app_sec,
            server_url=self.config.server_url,
            lcid=int(self.config.lcid),
            org_num=int(self.config.org_num) if self.config.org_num else 0
        )
    
    def execute_api(self, form_id: str, api_type: KingdeeAPIType, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行金蝶API调用
        
        Args:
            form_id: 表单ID（如: BD_MATERIAL, SAL_SaleOrder）
            api_type: API类型
            params: 请求参数
            
        Returns:
            返回API调用结果
        """
        try:
            if api_type == KingdeeAPIType.BILL_QUERY:
                response = self.api_sdk.ExecuteBillQuery(params)
            elif api_type == KingdeeAPIType.BILL_SAVE:
                response = self.api_sdk.Save(form_id, params)
            elif api_type == KingdeeAPIType.BILL_SUBMIT:
                response = self.api_sdk.Submit(form_id, params)
            elif api_type == KingdeeAPIType.BILL_AUDIT:
                response = self.api_sdk.Audit(form_id, params)
            elif api_type == KingdeeAPIType.BILL_VIEW:
                response = self.api_sdk.View(form_id, params)
            elif api_type == KingdeeAPIType.BILL_DELETE:
                response = self.api_sdk.Delete(form_id, params)
            elif api_type == KingdeeAPIType.REPORT_DATA:
                response = self.api_sdk.GetSysReportData(params)
            else:
                raise ValueError(f"不支持的API类型: {api_type}")
            
            return self._parse_response(response)
            
        except Exception as e:
            logging.error(f"金蝶API调用失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """解析API响应"""
        try:
            # 金蝶API返回的是数组格式，需要特殊处理
            result = json.loads(response)
            
            # 如果是数组格式（通常是查询结果）
            if isinstance(result, list):
                return {
                    "success": True,
                    "data": {"Result": result},
                    "error": None
                }
            
            # 检查响应是否成功
            if "Result" in result and "ResponseStatus" in result["Result"]:
                is_success = result["Result"]["ResponseStatus"]["IsSuccess"]
                
                if is_success:
                    return {
                        "success": True,
                        "data": result["Result"],
                        "error": None
                    }
                else:
                    errors = result["Result"]["ResponseStatus"]["Errors"]
                    error_msg = "; ".join([error["Message"] for error in errors]) if errors else "未知错误"
                    return {
                        "success": False,
                        "data": None,
                        "error": error_msg
                    }
            else:
                return {
                    "success": True,
                    "data": result,
                    "error": None
                }
                
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "data": None,
                "error": f"响应解析失败: {e}"
            }
    
    def query_materials(self, filter_string: str = "", field_keys: str = "FName,FNumber", limit: int = 1000) -> Dict[str, Any]:
        """查询物料数据"""
        params = {
            "FormId": "BD_MATERIAL",
            "FieldKeys": field_keys,
            "FilterString": filter_string,
            "Limit": limit,
            "StartRow": 0
        }
        return self.execute_api("BD_MATERIAL", KingdeeAPIType.BILL_QUERY, params)
    
    def query_sale_orders(self, filter_string: str = "", field_keys: str = "FBillNo,FCustomerID,FDate", limit: int = 1000) -> Dict[str, Any]:
        """查询销售订单数据"""
        params = {
            "FormId": "SAL_SaleOrder",
            "FieldKeys": field_keys,
            "FilterString": filter_string,
            "Limit": limit,
            "StartRow": 0
        }
        return self.execute_api("SAL_SaleOrder", KingdeeAPIType.BILL_QUERY, params)
    
    def query_purchase_orders(self, filter_string: str = "", field_keys: str = "FBillNo,FSupplierID,FDate", limit: int = 1000) -> Dict[str, Any]:
        """查询采购订单数据"""
        params = {
            "FormId": "PUR_PurchaseOrder",
            "FieldKeys": field_keys,
            "FilterString": filter_string,
            "Limit": limit,
            "StartRow": 0
        }
        return self.execute_api("PUR_PurchaseOrder", KingdeeAPIType.BILL_QUERY, params)
    
    def query_customers(self, filter_string: str = "", field_keys: str = "FName,FNumber,FCustomerCategoryID", limit: int = 1000) -> Dict[str, Any]:
        """查询客户数据"""
        params = {
            "FormId": "BD_Customer",
            "FieldKeys": field_keys,
            "FilterString": filter_string,
            "Limit": limit,
            "StartRow": 0
        }
        return self.execute_api("BD_Customer", KingdeeAPIType.BILL_QUERY, params)
    
    def query_suppliers(self, filter_string: str = "", field_keys: str = "FName,FNumber,FSupplierCategoryID", limit: int = 1000) -> Dict[str, Any]:
        """查询供应商数据"""
        params = {
            "FormId": "BD_Supplier",
            "FieldKeys": field_keys,
            "FilterString": filter_string,
            "Limit": limit,
            "StartRow": 0
        }
        return self.execute_api("BD_Supplier", KingdeeAPIType.BILL_QUERY, params)
    
    def query_inventory(self, filter_string: str = "", field_keys: str = "FName,FNumber,FBaseProperty", limit: int = 1000) -> Dict[str, Any]:
        """查询库存数据"""
        params = {
            "FormId": "STK_Inventory",
            "FieldKeys": field_keys,
            "FilterString": filter_string,
            "Limit": limit,
            "StartRow": 0
        }
        return self.execute_api("STK_Inventory", KingdeeAPIType.BILL_QUERY, params)
    
    def get_report_data(self, scheme_id: str, field_keys: str = "", limit: int = 1000) -> Dict[str, Any]:
        """获取报表数据"""
        params = {
            "SchemeId": scheme_id,
            "FieldKeys": field_keys,
            "Limit": limit,
            "StartRow": 0,
            "IsVerifyBaseDataField": "false"
        }
        return self.execute_api("", KingdeeAPIType.REPORT_DATA, params)


def create_kingdee_tool(config_dict: Dict[str, str]) -> KingdeeAPITool:
    """
    创建金蝶API工具实例
    
    Args:
        config_dict: 配置字典，包含以下键:
            - server_url: 服务器URL
            - acct_id: 账套ID
            - user_name: 用户名
            - app_id: 应用ID
            - app_sec: 应用密钥
            - lcid: 语言ID（可选，默认2052）
            - org_num: 组织编码（可选）
    """
    config = KingdeeAPIConfig(
        server_url=config_dict.get("server_url"),
        acct_id=config_dict.get("acct_id"),
        user_name=config_dict.get("user_name"),
        app_id=config_dict.get("app_id"),
        app_sec=config_dict.get("app_sec"),
        lcid=int(config_dict.get("lcid", 2052)),
        org_num=int(config_dict.get("org_num")) if config_dict.get("org_num") else 0
    )
    return KingdeeAPITool(config)


# 示例配置（从环境变量或配置文件中读取）
DEFAULT_CONFIG = {
    "server_url": "https://apiexp.open.kingdee.com/k3cloud/",
    "acct_id": "6304ba61219bf5",
    "user_name": "demo",
    "app_id": "225649_7ZbM6dDO0qrVXXUKX/Xs09wH2u5d4rLE",
    "app_sec": "2bb1d972f3574a46aebee03cdc80aeae",
    "lcid": "2052",
    "org_num": ""
}


if __name__ == "__main__":
    # 示例用法
    tool = create_kingdee_tool(DEFAULT_CONFIG)
    
    # 查询物料数据
    result = tool.query_materials(
        filter_string="'FNumber' like '01%'",
        field_keys="FNumber,FName,FCreateOrgId",
        limit=100
    )
    
    if result["success"]:
        print("查询成功:", json.dumps(result["data"], ensure_ascii=False, indent=2))
    else:
        print("查询失败:", result["error"])