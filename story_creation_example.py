import asyncio
import os
from dotenv import load_dotenv
from src.agent import NovelAIAgent, create_agent
import json
import logging
from datetime import datetime
import argparse

# 加载.env文件
load_dotenv()

logger = logging.getLogger(__name__)

# 模型配置
MODEL_CONFIGS = {
    "puyu": {
        "api_key": os.getenv("PUYU_API_KEY"),
        "base_url": os.getenv("PUYU_BASE_URL"),
        "model_type": "puyu",
        "model": "internlm2.5-latest"
    },
    "glm": {
        "api_key": os.getenv("GLM_API_KEY"),
        "base_url": os.getenv("GLM_BASE_URL"),
        "model_type": "glm",
        "model": "glm-4-flash"
    }
}

async def create_sample_story(model_type: str = "puyu"):
    # 获取对应的模型配置
    config = MODEL_CONFIGS.get(model_type)
    if not config:
        raise ValueError(f"不支持的模型类型: {model_type}，请选择 'puyu' 或 'glm'")
    
    if not config["api_key"]:
        raise ValueError(f"请在.env文件中设置{model_type.upper()}_API_KEY")

    # 初始化AI代理
    agent = NovelAIAgent(
        api_key=config["api_key"],
        base_url=config.get("base_url"),
        model_type=model_type
    )

    # 创作提示示例
    prompt = """
    在一个快速发展的大城市里，来自四川农村的农民工张大哥在建筑工地上辛勤工作。一天，他意外发现工程
    项目存在重大安全隐患，这让他陷入两难：举报可能导致工地停工，工友们会失去收入；不报又可能危及未来
    住户的生命安全。在经济压力和道德责任之间，他该如何抉择？
    """

    # 创建故事
    story = await agent.create_story(prompt)
    
    # 准备输出内容
    story_output = {
        "model_type": model_type,
        "model_name": config["model"],
        "themes": story["themes"],
        "characters": story["characters"],
        "outline": story["outline"],
        "content": story["content"]
    }
    
    # 创建output文件夹（如果不存在）
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成输出文件名（使用时间戳和模型类型）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = os.path.join(output_dir, f"story_output_{model_type}_{timestamp}.json")
    txt_filename = os.path.join(output_dir, f"story_{model_type}_{timestamp}.txt")
    
    # 保存到JSON文件
    try:
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(story_output, f, ensure_ascii=False, indent=2)
            logger.info(f"故事元数据已保存到 {json_filename}")
    except Exception as e:
        logger.error(f"保存JSON文件时出错: {str(e)}")
    
    # 保存故事内容到TXT文件
    try:
        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(f"【使用模型】: {config['model']}\n\n")
            
            # 写入主题
            f.write("【故事主题】\n")
            for theme in story["themes"]:
                f.write(f"- {theme}\n")
            f.write("\n")
            
            # 写入故事内容
            f.write(story["content"])
            
            logger.info(f"故事内容已保存到 {txt_filename}")
    except Exception as e:
        logger.error(f"保存TXT文件时出错: {str(e)}")

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='AI小说创作工具')
    parser.add_argument('--model', type=str, choices=['puyu', 'glm'], 
                       default='puyu', help='选择使用的模型 (puyu 或 glm)')
    args = parser.parse_args()

    # 在Windows系统上运行异步代码
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # 运行异步函数
    asyncio.run(create_sample_story(args.model))

if __name__ == "__main__":
    main() 