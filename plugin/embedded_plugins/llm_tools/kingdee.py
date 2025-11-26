import logging
from typing import Any, Dict, List
from plugin.llm_tool_plugin import LLMToolMetadata, LLMToolPlugin


class KingdeePlugin(LLMToolPlugin):
    """
    金蝶K/3 Cloud WebAPI工具插件
    提供金蝶云星空系统的数据查询功能
    """
    _version_ = "1.0.0"

    @classmethod
    def get_metadata(cls) -> LLMToolMetadata:
        return {
            "name": "kingdee",
            "displayName": "$t:kingdee.name",
            "description": "A tool to query data from Kingdee K/3 Cloud system",
            "displayDescription": "$t:kingdee.description",
            "parameters": {
                "entity_type": {
                    "type": "string",
                    "description": "The type of entity to query (material, customer, sale_order, purchase_order, inventory, production_order)",
                    "displayDescription": "$t:kingdee.params.entity_type",
                    "required": True
                },
                "conditions": {
                    "type": "array",
                    "description": "Query conditions as list of dictionaries with field, operator, value",
                    "displayDescription": "$t:kingdee.params.conditions",
                    "required": False
                },
                "fields": {
                    "type": "array", 
                    "description": "Fields to return in the query result",
                    "displayDescription": "$t:kingdee.params.fields",
                    "required": False
                },
                "limit": {
                    "type": "number",
                    "description": "Maximum number of records to return",
                    "displayDescription": "$t:kingdee.params.limit",
                    "required": False
                }
            }
        }

    def invoke(self, **kwargs) -> str:
        """
        执行金蝶数据查询操作
        """
        logging.info(f"Kingdee tool was called with arguments: {kwargs}")
        
        # 这里应该调用金蝶工具的实际实现
        # 由于工具调用是在LLM上下文中，我们需要返回字符串格式的结果
        
        # 模拟返回结果
        entity_type = kwargs.get("entity_type", "material")
        limit = kwargs.get("limit", 10)
        
        return f"成功查询金蝶{entity_type}数据，返回{limit}条记录。请在实际使用时配置金蝶API连接参数。"

    def _get_kingdee_tool_instance(self):
        """
        获取金蝶工具实例
        这里需要延迟导入以避免循环依赖
        """
        try:
            from kingdee_agent_tool import KingdeeAgentTool
            
            # 从环境变量或配置中获取金蝶连接参数
            # 在实际使用时需要配置这些参数
            config = {
                "server_url": "https://api.kingdee.com",
                "acct_id": "",
                "username": "",
                "password": "", 
                "lcid": 2052,
                "org_num": 0
            }
            
            return KingdeeAgentTool(**config)
        except ImportError:
            logging.warning("KingdeeAgentTool not found, using mock implementation")
            return None