import os
from utils.logger_handler import logger
from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
import random
from utils.config_handler import agent_conf
from utils.path_tool import get_abs_path

rag = RagSummarizeService()

user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010",]
month_arr = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
             "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12", ]

external_data = {}


@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    try:
        # 输入验证
        if not query or not isinstance(query, str):
            return "请提供有效的查询内容"
        return rag.rag_summarize(query)
    except Exception as e:
        logger.error(f"rag_summarize工具调用失败: {str(e)}")
        return f"处理查询时出现错误: {str(e)}"


@tool(description="获取指定城市的天气，以消息字符串的形式返回")
def get_weather(city: str) -> str:
    try:
        # 输入验证
        if not city or not isinstance(city, str):
            return "请提供有效的城市名称"
        return f"城市{city}天气为晴天，气温26摄氏度，空气湿度50%，南风1级，AQI21，最近6小时降雨概率极低"
    except Exception as e:
        logger.error(f"get_weather工具调用失败: {str(e)}")
        return f"获取天气信息时出现错误: {str(e)}"


@tool(description="获取用户所在城市的名称，以纯字符串形式返回")
def get_user_location() -> str:
    return random.choice(["深圳", "合肥", "杭州"])


@tool(description="获取用户的ID，以纯字符串形式返回")
def get_user_id() -> str:
    return random.choice(user_ids)


@tool(description="获取当前月份，以纯字符串形式返回")
def get_current_month() -> str:
    return random.choice(month_arr)


def generate_external_data():
    """
    {
        "user_id": {
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            ...
        },
        "user_id": {
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            ...
        },
        "user_id": {
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            "month" : {"特征": xxx, "效率": xxx, ...}
            ...
        },
        ...
    }
    :return:
    """
    if not external_data:
        external_data_path = get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")

                user_id: str = arr[0].replace('"', "")
                feature: str = arr[1].replace('"', "")
                efficiency: str = arr[2].replace('"', "")
                consumables: str = arr[3].replace('"', "")
                comparison: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "特征": feature,
                    "效率": efficiency,
                    "耗材": consumables,
                    "对比": comparison,
                }


@tool(description="从外部系统中获取指定用户在指定月份的使用记录，以纯字符串形式返回， 如果未检索到返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    try:
        # 输入验证
        if not user_id or not isinstance(user_id, str):
            return "请提供有效的用户ID"
        if not month or not isinstance(month, str):
            return "请提供有效的月份"
        
        generate_external_data()

        try:
            return external_data[user_id][month]
        except KeyError:
            logger.warning(f"[fetch_external_data]未能检索到用户：{user_id}在{month}的使用记录数据")
            return ""
    except Exception as e:
        logger.error(f"fetch_external_data工具调用失败: {str(e)}")
        return f"获取使用记录时出现错误: {str(e)}"


@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    try:
        return "fill_context_for_report已调用"
    except Exception as e:
        logger.error(f"fill_context_for_report工具调用失败: {str(e)}")
        return f"触发报告生成上下文时出现错误: {str(e)}"


@tool(description="比较不同型号扫地机器人的功能和价格")
def compare_robots(robot1: str, robot2: str) -> str:
    try:
        # 输入验证
        if not robot1 or not isinstance(robot1, str) or not robot2 or not isinstance(robot2, str):
            return "请提供有效的机器人型号"
        
        # 模拟比较结果
        return f"{robot1}和{robot2}的比较结果：\n1. 价格：{robot1} ¥2999，{robot2} ¥3999\n2. 功能：两者都支持自动清扫、智能规划，{robot2}额外支持自动集尘\n3. 续航：{robot1} 120分钟，{robot2} 150分钟\n4. 噪音：{robot1} 55dB，{robot2} 50dB"
    except Exception as e:
        logger.error(f"compare_robots工具调用失败: {str(e)}")
        return f"比较机器人时出现错误: {str(e)}"


@tool(description="获取扫地机器人的价格信息")
def get_robot_price(robot_model: str) -> str:
    try:
        # 输入验证
        if not robot_model or not isinstance(robot_model, str):
            return "请提供有效的机器人型号"
        
        # 模拟价格信息
        price_dict = {
            "X1": "¥2999",
            "X2": "¥3999",
            "X3": "¥4999",
            "S1": "¥1999",
            "S2": "¥2499"
        }
        
        price = price_dict.get(robot_model, "未找到该型号的价格信息")
        return f"{robot_model}的价格为：{price}"
    except Exception as e:
        logger.error(f"get_robot_price工具调用失败: {str(e)}")
        return f"获取价格信息时出现错误: {str(e)}"


@tool(description="生成扫地机器人的购买链接")
def generate_purchase_link(robot_model: str) -> str:
    try:
        # 输入验证
        if not robot_model or not isinstance(robot_model, str):
            return "请提供有效的机器人型号"
        
        # 模拟购买链接
        return f"{robot_model}的购买链接：https://example.com/buy/{robot_model}"
    except Exception as e:
        logger.error(f"generate_purchase_link工具调用失败: {str(e)}")
        return f"生成购买链接时出现错误: {str(e)}"


@tool(description="获取扫地机器人的维护保养建议")
def get_maintenance_tips(robot_model: str = None) -> str:
    try:
        # 输入验证
        if robot_model and not isinstance(robot_model, str):
            return "请提供有效的机器人型号"
        
        # 模拟维护保养建议
        if robot_model:
            return f"{robot_model}的维护保养建议：\n1. 每周清洁一次集尘盒\n2. 每月清理一次边刷和主刷\n3. 每三个月更换一次滤网\n4. 定期检查电池状态\n5. 避免在潮湿环境使用"
        else:
            return "通用扫地机器人维护保养建议：\n1. 每周清洁一次集尘盒\n2. 每月清理一次边刷和主刷\n3. 每三个月更换一次滤网\n4. 定期检查电池状态\n5. 避免在潮湿环境使用\n6. 定期更新固件"
    except Exception as e:
        logger.error(f"get_maintenance_tips工具调用失败: {str(e)}")
        return f"获取维护保养建议时出现错误: {str(e)}"


@tool(description="获取扫地机器人的故障排除指南")
def get_troubleshooting_guide(problem: str) -> str:
    try:
        # 输入验证
        if not problem or not isinstance(problem, str):
            return "请提供具体的故障描述"
        
        # 模拟故障排除指南
        problem_map = {
            "不充电": "1. 检查充电器是否正常工作\n2. 检查充电接口是否清洁\n3. 尝试重启机器人\n4. 如果问题仍然存在，联系客服",
            "不出水": "1. 检查水箱是否有水\n2. 检查水管是否堵塞\n3. 检查水泵是否正常工作\n4. 尝试重启机器人",
            "噪音大": "1. 检查是否有异物卡住\n2. 检查边刷和主刷是否需要清理\n3. 检查轮子是否有障碍物\n4. 如果问题仍然存在，联系客服",
            "迷路": "1. 确保机器人在开阔区域启动\n2. 清理地面上的障碍物\n3. 尝试重新 Mapping\n4. 检查传感器是否清洁"
        }
        
        solution = problem_map.get(problem, "请提供更具体的故障描述，或联系客服获取帮助")
        return f"故障：{problem}\n解决方案：\n{solution}"
    except Exception as e:
        logger.error(f"get_troubleshooting_guide工具调用失败: {str(e)}")
        return f"获取故障排除指南时出现错误: {str(e)}"


@tool(description="获取扫地机器人的使用技巧")
def get_usage_tips(robot_model: str = None) -> str:
    try:
        # 输入验证
        if robot_model and not isinstance(robot_model, str):
            return "请提供有效的机器人型号"
        
        # 模拟使用技巧
        if robot_model:
            return f"{robot_model}的使用技巧：\n1. 首次使用前请充满电\n2. 启动前清理地面障碍物\n3. 定期清理机器人传感器\n4. 使用app设置定时清扫\n5. 根据地面类型选择合适的清扫模式"
        else:
            return "通用扫地机器人使用技巧：\n1. 首次使用前请充满电\n2. 启动前清理地面障碍物\n3. 定期清理机器人传感器\n4. 使用app设置定时清扫\n5. 根据地面类型选择合适的清扫模式\n6. 避免在黑暗环境使用"
    except Exception as e:
        logger.error(f"get_usage_tips工具调用失败: {str(e)}")
        return f"获取使用技巧时出现错误: {str(e)}"
