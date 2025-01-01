from typing import Dict, Optional, List
from openai import OpenAI
from zhipuai import ZhipuAI
import logging
from .prompts import (
    THEME_ANALYSIS_PROMPT,
    CHARACTER_DESIGN_PROMPT,
    STORY_OUTLINE_PROMPT,
    CONTENT_CREATION_SYSTEM_PROMPT,
    CHAPTER_SYNOPSIS_PROMPT,
    SETTING_GENERATION_PROMPT,
    TONE_ANALYSIS_PROMPT
)
import json

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NovelAIAgent:
    def __init__(self, api_key: str, base_url: Optional[str] = None, model_type: str = "puyu"):
        """初始化小说创作智能代理"""
        logger.info(f"初始化NovelAIAgent... (model_type: {model_type})")
        
        self.model_type = model_type
        if model_type == "puyu":
            self.client = OpenAI(api_key=api_key, base_url=base_url)
            self.model = "internlm2.5-latest"
        else:  # zhipu models
            self.client = ZhipuAI(api_key=api_key)
            # 根据任务复杂度选择不同的模型
            self.models = {
                "complex": "glm-4-plus",   # 最复杂的任务：故事大纲、人物设计等
                "medium": "glm-4-air",     # 中等复杂度：章节梗概、主题分析等
                "simple": "glm-4-flash"    # 简单任务：具体内容生成等
            }
            self.model = self.models["medium"]  # 设置默认模型
            
        logger.info(f"API配置完成: model={self.model}")
        
        self.current_story = {
            "title": "",
            "themes": [],
            "setting": "",
            "characters": "",
            "tone": "",
            "outline": "",
            "synopses": "",
            "content": []
        }

    async def _call_api(self, messages: List[Dict], complexity: str = "medium") -> str:
        """根据任务复杂度调用不同的模型"""
        try:
            if self.model_type == "puyu":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
            else:  # zhipu models
                model = self.models.get(complexity, self.models["medium"])
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages
                )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"API调用出错: {str(e)}")
            raise

    async def _generate_chapter_synopses(self, meta_info: Dict) -> str:
        """分阶段生成章节梗概"""
        try:
            logger.info("开始生成章节梗概...")
            all_synopses = []
            stages = ["起", "承", "转", "合", "终"]
            
            for stage_index, stage in enumerate(stages, 1):
                logger.info(f"正在生成第{stage_index}阶段（{stage}）的章节梗概...")
                
                # 计算本阶段的章节编号范围
                start_chapter = (stage_index - 1) * 10 + 1
                end_chapter = start_chapter + 9
                
                response = await self._call_api([
                    {"role": "system", "content": "你是一位优秀的故事规划师，擅长设计扣人心弦的情节。"},
                    {"role": "user", "content": f"""
请为小说的第{stage_index}阶段（{stage}）创作10个章节的详细梗概。

小说基本信息：
标题：{meta_info.get('title', '未命名')}
主题：{', '.join(meta_info.get('themes', []))}
世界观：{meta_info.get('setting', '')}
主要人物：{meta_info.get('characters', '')}

本阶段要求：
1. 创作第{start_chapter}章到第{end_chapter}章的梗概
2. 每章梗概200字左右
3. 体现阶段性特点：
   - 起：引入故事、展示天赋、初入宗门
   - 承：磨练成长、结交好友、树敌对手
   - 转：身世之谜、实力暴涨、危机显现
   - 合：真相揭露、大战爆发、逆境突破
   - 终：终极决战、拯救世界、圆满收官

4. 爽点要求：
   - 每章都要有意外或反转
   - 实力要循序渐进提升
   - 设置合理的打脸情节
   - 制造期待和悬念

请按以下格式输出10个章节的梗概：

【第{start_chapter}章：章节标题】
[详细梗概，包含地点、人物、事件、转折]

【第{start_chapter + 1}章：章节标题】
[详细梗概]
...
"""}], complexity="complex")
                
                all_synopses.append(response)
                logger.info(f"第{stage_index}阶段章节梗概生成完成")
            
            # 合并所有阶段的梗概
            complete_synopses = "\n\n".join(all_synopses)
            logger.info("所有章节梗概生成完成")
            return complete_synopses
        
        except Exception as e:
            logger.error(f"生成章节梗概时出错: {str(e)}")
            raise

    async def _generate_chapters_content(self, meta_info: Dict, chapter_synopses: str) -> List[str]:
        """生成所有章节的具体内容，返回章节列表"""
        try:
            logger.info("开始生成章节内容...")
            chapters = []
            
            # 字数要求配置
            REQUIRED_WORDS = 3000  # 要求模型生成的字数
            MIN_WORDS = 2000      # 实际检查的最小字数
            
            # 解析章节梗概
            synopses_list = chapter_synopses.split("【第")
            synopses_list = [s for s in synopses_list if s.strip()]  # 移除空字符串
            
            for i, synopsis in enumerate(synopses_list, 1):
                logger.info(f"正在生成第{i}章内容...")
                
                # 提取章节标题和梗概内容
                try:
                    chapter_parts = synopsis.split("】\n", 1)
                    title_parts = chapter_parts[0].split("章：", 1)
                    chapter_title = f"第{title_parts[0]}章：{title_parts[1] if len(title_parts) > 1 else '未命名'}"
                    chapter_content = chapter_parts[1].strip() if len(chapter_parts) > 1 else ""
                except Exception as e:
                    logger.warning(f"解析章节{i}梗概时出错: {str(e)}")
                    chapter_title = f"第{i}章"
                    chapter_content = synopsis
                
                # 添加重试机制
                max_retries = 3
                retry_count = 0
                content = ""
                
                while retry_count < max_retries:
                    response = await self._call_api([
                        {"role": "system", "content": CONTENT_CREATION_SYSTEM_PROMPT},
                        {"role": "user", "content": f"""
请根据以下信息创作小说章节的具体内容：

小说基本信息：
标题：{meta_info.get('title', '未命名')}
主题：{', '.join(meta_info.get('themes', []))}
基调：{meta_info.get('tone', '')}

本章信息：
{chapter_title}

本章梗概：
{chapter_content}

主要人物：
{meta_info.get('characters', '')}

创作要求：
1. 字数要求：必须超过{REQUIRED_WORDS}字，建议2500-3500字
   - 如果内容不足{REQUIRED_WORDS}字，请继续补充
   - 保持情节的完整性和连贯性
   - 不要为凑字数而冗长

2. 情节结构：
   - 反转与震撼（35%）：意外展现、打脸装逼
   - 期待与升级（35%）：能力提升、资源获取
   - 场景描写（20%）：震撼场面、众人反应
   - 对话设计（10%）：金句对决、暗藏玄机

3. 爽感要求：
   - 情节要出人意料
   - 打脸要干脆利落
   - 升级要令人期待
   - 反转要令人震惊

4. 写作要点：
   - 合理铺垫伏笔
   - 制造期待感
   - 突出震撼效果
   - 保持爽感节奏

请直接开始创作本章正文，确保字数超过{REQUIRED_WORDS}字：
"""}], complexity="complex")
                    
                    content = response.strip()
                    word_count = len(content)
                    
                    if word_count >= MIN_WORDS:  # 使用较低的阈值进行检查
                        logger.info(f"第{i}章生成成功，字数：{word_count}")
                        break
                    else:
                        retry_count += 1
                        logger.warning(f"第{i}章字数不足（{word_count}字），第{retry_count}次重试...")
                
                if word_count < MIN_WORDS:
                    logger.error(f"第{i}章生成失败，字数不足：{word_count}字")
                
                # 格式化章节内容，确保标题格式统一
                formatted_chapter = f"{chapter_title}\n\n{content}\n"
                chapters.append(formatted_chapter)
                logger.info(f"第{i}章内容生成完成")
            
            logger.info("所有章节内容生成完成")
            return chapters
        except Exception as e:
            logger.error(f"生成章节内容时出错: {str(e)}")
            raise

    async def create_story(self, prompt: str) -> Dict:
        """创建完整的故事"""
        try:
            logger.info("开始创建新故事...")

            # 1. 分析主题（复杂任务）
            logger.info("Step 1/6: 分析故事主题...")
            themes_content = await self._call_api([
                {"role": "system", "content": THEME_ANALYSIS_PROMPT},
                {"role": "user", "content": prompt}
            ], complexity="complex")
            
            # 解析主题
            themes = [theme.strip() for theme in themes_content.split('\n') if theme.strip()]
            self.current_story["themes"] = themes
            logger.info(f"主题分析完成: {themes}")

            # 2. 创建世界观设定（复杂任务）
            logger.info("Step 2/6: 创建世界观设定...")
            setting = await self._call_api([
                {"role": "system", "content": SETTING_GENERATION_PROMPT},
                {"role": "user", "content": f"故事提示：{prompt}\n主题：{themes}"}
            ], complexity="complex")
            
            self.current_story["setting"] = setting
            logger.info("世界观设定完成")

            # 3. 设计角色（复杂任务）
            logger.info("Step 3/6: 设计角色...")
            characters = await self._call_api([
                {"role": "system", "content": CHARACTER_DESIGN_PROMPT},
                {"role": "user", "content": f"故事提示：{prompt}\n主题：{themes}\n世界观：{setting}"}
            ], complexity="complex")
            
            self.current_story["characters"] = characters
            logger.info("角色设计完成")

            # 4. 创建故事大纲（复杂任务）
            logger.info("Step 4/6: 创建故事大纲...")
            outline = await self._call_api([
                {"role": "system", "content": STORY_OUTLINE_PROMPT},
                {"role": "user", "content": f"故事提示：{prompt}\n主题：{themes}\n世界观：{setting}\n角色：{characters}"}
            ], complexity="complex")
            
            self.current_story["outline"] = outline
            logger.info("故事大纲创建完成")
            
            # 5. 生成章节梗概（复杂任务）
            logger.info("Step 5/6: 生成章节梗概...")
            chapter_synopses = await self._generate_chapter_synopses(self.current_story)
            self.current_story["synopses"] = chapter_synopses
            
            # 6. 生成具体内容（复杂任务）
            logger.info("Step 6/6: 生成详细故事内容...")
            story_content = await self._generate_chapters_content(
                meta_info=self.current_story,
                chapter_synopses=chapter_synopses
            )
            self.current_story["content"] = story_content
            
            logger.info("故事创作完成")
            return self.current_story

        except Exception as e:
            logger.error(f"故事创作过程出错: {str(e)}")
            raise

def create_agent(model_type: str, api_key: str, base_url: Optional[str] = None) -> NovelAIAgent:
    """创建AI代理"""
    return NovelAIAgent(api_key=api_key, base_url=base_url, model_type=model_type) 