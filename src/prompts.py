"""
存储所有用于故事生成的prompt模板
"""

THEME_ANALYSIS_PROMPT = """作为一位深刻的文学分析家，请从提供的故事提示中提炼出核心主题和哲学思考。
要求：
1. 每个主题必须以简洁的一句话表达
2. 主题应该包含：
   - 核心矛盾（如人性与科技的冲突）
   - 伦理困境（如个人利益与集体利益的选择）
   - 哲学思考（如存在主义、自由意志等）
3. 确保主题与故事提示紧密相关
4. 每个主题都要有现实意义和普遍性

请严格按照以下格式返回3-5个主题：
1. [第一个主题]
2. [第二个主题]
3. [第三个主题]
...
"""

CHARACTER_DESIGN_PROMPT = """作为一位角色塑造大师，请设计4-5个核心角色，其中必须包含至少一位反派角色。每个角色必须具体、立体、富有个性。

每个角色必须包含以下要素：
1. 基本信息（具体详实）
   - 姓名、年龄、职业
   - 外貌特征（3-5个标志性特征）
   - 衣着习惯和生活方式
   - 社会地位和经济状况
   - 教育背景和专业技能

2. 性格特征（鲜明且有理有据）
   - 3-5个关键性格特点
   - 性格养成的家庭和社会原因
   - 独特的行为习惯和说话方式
   - 处事风格和为人处世态度

3. 心理动机（深入且合理）
   - 核心追求和人生目标
   - 内心恐惧和软肋
   - 道德立场和价值观
   - 重要的心理创伤或难忘经历
   - 对立面和冲突源（特别是反派角色）

4. 人物关系（复杂且富有张力）
   - 与其他角色的关系网络
   - 情感纽带和利益关系
   - 潜在的矛盾和冲突点
   - 在故事中的作用和地位
   - 与主角的对立面（反派角色）

5. 成长轨迹（清晰且有发展空间）
   - 关键的成长经历
   - 故事开始时的处境
   - 可能的改变方向
   - 性格和命运的转折点
   - 最终的结局暗示

请严格按照以下JSON格式返回：
{
    "主角": {
        "基本信息": {},
        "性格特征": {},
        "心理动机": {},
        "人物关系": {},
        "成长轨迹": {}
    },
    "反派": {
        // 必须有一个主要反派角色
    },
    "重要配角1": {},
    "重要配角2": {},
    ...
}

注意：反派角色也要立体丰满，要有合理的动机和背景，不能简单化或脸谱化。
"""

STORY_OUTLINE_PROMPT = """作为一位优秀的故事架构师，请设计一个完整的故事大纲。总体字数控制在2万字左右，分配如下：

1. 起因：《根基》（3000字）
   - 时代背景和城市环境（500字）
   - 主角的生活现状（500字）
   - 重要人物的初次登场（1000字）
   - 引发故事的关键事件（1000字）

2. 经过：《暗流》（4500字）
   - 问题的初步显现（800字）
   - 人物关系的交织（800字）
   - 各方立场的对立（1000字）
   - 矛盾的逐步升温（1000字）
   - 隐藏线索的埋设（900字）

3. 发展：《激流》（5000字）
   - 矛盾的全面爆发（1200字）
   - 各方力量的角逐（1000字）
   - 人物内心的挣扎（900字）
   - 关键抉择的考验（1000字）
   - 局势的进一步恶化（900字）

4. 高潮：《巨浪》（4500字）
   - 终极冲突的爆发（1500字）
   - 重大转折的出现（1200字）
   - 关键时刻的抉择（1000字）
   - 结果的最终显现（800字）

5. 结局：《回归》（3000字）
   - 事件的最终解决（1000字）
   - 人物的命运安排（800字）
   - 情节的完整收束（700字）
   - 主题的深层升华（500字）

要求：
1. 每个部分要有明确的情节主线
2. 场景描写要具体，包含时间、地点、人物
3. 情节要有起伏，节奏要有快慢
4. 要设置悬念和伏笔
5. 人物的行动要有动机
6. 事件的发展要合理
7. 要注意场景的衔接和转换

请严格按照以下格式输出：

【起因：《根基》】
[详细内容，重点描写背景和人物]

【经过：《暗流》】
[详细内容，突出矛盾的初步显现]

【发展：《激流》】
[详细内容，展现冲突的全面爆发]

【高潮：《巨浪》】
[详细内容，呈现终极对决]

【结局：《回归》】
[详细内容，完整收束故事]
"""

CONTENT_CREATION_SYSTEM_PROMPT = """你是一位擅长细节描写和情节构建的小说家。创作时请注意：

1. 场景描写要具体生动：
   - 使用感官描写（视觉、听觉、触觉等）
   - 添加环境细节和氛围营造
   - 注意时间和空间的变化

2. 人物刻画要立体真实：
   - 通过对话展现性格
   - 描写细微的动作和表情
   - 展现内心活动和外在行为的统一

3. 情节发展要合理：
   - 事件之间要有因果关系
   - 保持适当的节奏变化
   - 设置悬念和伏笔

4. 写作技巧要成熟：
   - 善用细节烘托主题
   - 对话要简练自然
   - 避免过多的说教和议论

5. 整体风格要统一：
   - 保持语言风格的一致性
   - 符合故事的整体基调
   - 与主题相呼应"""

def get_section_prompt(section: str, outline_part: str, characters: str, prev_section: str = None) -> str:
    """生成每个部分的具体prompt"""
    context = "这是故事的开始" if section == "起因" else f"承接前面的{prev_section}部分"
    
    word_counts = {
        "起因": 3000,
        "经过": 4500,
        "发展": 5000,
        "高潮": 4500,
        "结局": 3000
    }
    
    section_titles = {
        "起因": "《根基》",
        "经过": "《暗流》",
        "发展": "《激流》",
        "高潮": "《巨浪》",
        "结局": "《回归》"
    }
    
    return f"""作为小说创作者，请基于以下信息创作故事的{section}部分。

要求：
1. 字数要求：{word_counts[section]}字左右
2. 重点关注：
   - 具体的场景描写和环境细节
   - 人物的对话和行动
   - 情节的推进和转折
   - 合理的节奏控制
   - 细节的真实感

背景信息：
1. 当前部分大纲：
{outline_part}

2. 角色设定：
{characters}

3. 上下文联系：
{context}

写作要求：
1. 场景描写要具体，注意细节
2. 对话要自然，展现人物性格
3. 动作描写要准确生动
4. 情节发展要合理
5. 要有适当的悬念和铺垫
6. 注意场景转换的流畅性
7. 保持叙事节奏的变化

请创作这一部分的具体内容，确保与整体故事的连贯性。
"""

SECTION_TITLE_PROMPT = """请为这个故事的五个主要部分生成富有诗意和象征意义的标题。每个标题要：
1. 简洁有力（2-3个字）
2. 与内容相呼应
3. 有意象和象征
4. 能反映情节发展
5. 前后有关联性

已知五个部分的主要内容：
1. 起因部分：介绍背景、人物、引发事件
2. 经过部分：矛盾初显、关系交织
3. 发展部分：冲突加剧、形势恶化
4. 高潮部分：终极对决、重大转折
5. 结局部分：问题解决、回归平静

请按照以下格式返回：
{
    "起因": "《标题》",
    "经过": "《标题》",
    "发展": "《标题》",
    "高潮": "《标题》",
    "结局": "《标题》"
}
""" 