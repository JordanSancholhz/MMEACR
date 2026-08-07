
def user_prompt_system_role(user_description):
    return f"You are an Amazon buyer.\n Here is your previous self-introduction, exhibiting your past preferences and dislikes:\n '{user_description}'."
# 1
def user_prompt_template(list_of_item_description, pos_item_title, neg_item_title, system_reason):
    return f"Recently, you considered choosing one item from two candidates. The features of these items are:\n {list_of_item_description}.\n\n After comparing based on your preferences, you chose '{neg_item_title}' and rejected the other. Your explanation was:\n '{system_reason}'. \n\n However, after encountering these items, you realized you prefer '{pos_item_title}' and don't like '{neg_item_title}'.\n This indicates an incorrect choice, and your previous judgment about your preferences was mistaken. Your task now is to update your self-introduction with your new preferences and dislikes. \n Follow these steps: \n 1. Analyze misconceptions in your previous judgment and correct them.\n 2. Identify new preferences from '{pos_item_title}' and dislikes from '{neg_item_title}'. \n 3. Summarize your past preferences, merging them with new insights and removing conflicting parts.\n 4. Update your self-introduction, starting with new preferences, then summarizing past ones, followed by dislikes. \n\n Important notes:\n 1. Your output format should be: 'My updated self-introduction: [Your updated self-introduction here].' \n 2. Keep it under 150 words.  \n 3. Be concise and clear. \n 4. Describe only the features of items you prefer or dislike, without mentioning your thought process. \n 5. Your self-introduction should be specific and personalized; avoid generic preferences."
# 2
def user_prompt_template_true(list_of_item_description, pos_item_title, neg_item_title, system_reason):
    return f"Recently, you considered choosing one item from two candidates. The features of these items are:\n {list_of_item_description}.\n\n After comparing based on your preferences, you selected '{pos_item_title}' and rejected the other. Your explanation was:\n '{system_reason}'. \n\n After encountering these items, you found that you really like '{pos_item_title}' and dislike '{neg_item_title}'.\n This indicates you made a correct choice, and your judgment about your preferences was accurate. \n Your task now is to update your self-introduction to reflect your preferences and dislikes from this interaction. \n Please follow these steps: \n 1. Analyze your judgment about your preferences and dislikes from your explanation.\n 2. Identify new preferences based on '{pos_item_title}' and dislikes based on '{neg_item_title}'. \n 3. Summarize your past preferences and dislikes from your previous self-introduction, combining them with new insights while removing conflicting parts.\n 4. Update your self-introduction, starting with your new preferences, then summarizing past ones, followed by your dislikes. \n\n Important notes:\n 1. Your output format should be: 'My updated self-introduction: [Your updated self-introduction here].' \n 2. Keep it under 150 words. \n 3. Be concise and clear. \n 4. Describe only the features of items you prefer or dislike, without mentioning your thought process. \n 5. Your self-introduction should be specific and personalized; avoid generic preferences."
# 3
def item_prompt_template(user_description, list_of_item_description, pos_item_title, neg_item_title, system_reason):
    return f"User self-introduction, showing preferences and dislikes: '{user_description}'.\n Recently, the user browsed a shopping site and considered two items:\n {list_of_item_description}.\n\n He chose '{neg_item_title}' and rejected the other, explaining: '{system_reason}'. \n\n However, he prefers '{pos_item_title}' instead, indicating an unsuitable choice due to misleading descriptions. He likes '{pos_item_title}' for its features and dislikes '{neg_item_title}' for undesirable traits. Your task is to update the descriptions of these items. \n Follow these steps:\n 1. Analyze features that led to the poor choice and modify them. \n 2. Examine user preferences and dislikes; explore new features of the preferred item aligning with preferences and opposing dislikes, and do the same for the disliked item, highlighting differences. Your analysis should be thorough. \n 3. Incorporate new features into the previous descriptions, preserving valuable content while being concise.\n\n Important notes: \n 1. Your output should be in the following format: 'The updated description of the first item is: [updated description]. \\n The updated description of the second item is: [updated description].'. \n 2. Each updated description cannot exceed 50 words; be concise and clear. \n 3. In your descriptions, refer to user preferences collectively, avoiding specific individual references, e.g., 'the user with ... preferences/dislikes'.\n 4. The updated description should not contradict the item's inherent characteristics, e.g., do not describe a thriller as having a predictably happy ending. \n 5. The updated description should highlight distinguishing features that differentiate this item from others."
# 4
def item_prompt_template_true(user_description, list_of_item_description, pos_item_title, neg_item_title):
    return f"User self-description, showcasing preferences and dislikes: '{user_description}'.\n Recently, the user browsed a shopping site and considered two items:\n {list_of_item_description}.\n\n The user chose '{pos_item_title}' for its features and rejected '{neg_item_title}' for undesirable traits. Your task is to update the descriptions of these items based on these insights. \n Follow these steps:\n 1. Analyze the user's preferences and dislikes from the self-description. \n 2. Explore the chosen item's features that align with preferences and oppose dislikes, and examine the rejected item's features that align with dislikes and oppose preferences. Highlight the differences thoroughly. \n 3. Incorporate new features into the previous descriptions, preserving key information while being concise.\n\n Important notes: \n 1. Your output should be in the following format: 'The updated description of the first item is: [updated description]. \\n The updated description of the second item is: [updated description].'. \n 2. Each updated description cannot exceed 50 words; be concise and clear! \n 3. In your updated descriptions, refer to preferences collectively, avoiding individual references. For example, say 'the user with ... preferences/dislikes'.\n 4. New features should reflect user preferences, and the updated descriptions must not contradict the inherent characteristics of the items, e.g., do not describe a thriller as having a predictably happy ending."

# 5
def system_prompt_template(user_description, list_of_item_description):
    return f"You are an Amazon buyer. Here is your self-introduction, expressing your preferences and dislikes: '{user_description}'. \n\n Now, you are considering selecting an item from two candidates. The features of these items are:\n {list_of_item_description}.\n\n Please select the item that aligns best with your preferences and explain your choice while rejecting the other. \n Follow these steps:\n 1. Extract your preferences and dislikes from your self-introduction. \n 2. Evaluate the two items based on your preferences and how they relate to the item features.\n 3. Explain your choice, detailing the relationship between your preferences/dislikes and the item features. \n\n Important notes:\n 1. **Output Format:** 'Choice: [Title of the selected item] \\n Explanation: [Rationale behind your choice and reasons for rejecting the other item]'. \n 2. Do not fabricate your preferences! If your self-introduction lacks relevant details, use common knowledge to guide your decision, such as item popularity. \n 3. Select one candidate, not both. \n 4. Your explanation should be specific; general preferences like genre are insufficient. Focus on the item's finer attributes and be concise! \n 5. Base your explanation on facts. If your self-introduction doesn't specify preferences, you cannot claim your decision was influenced by them."

def system_prompt_crossdomain(cross_domain_preference, private_domain_description, main_kind):
    return f"As an Amazon buyer, here is your previous self-introduction: {cross_domain_preference}. Now your preferences across various product domains are outlined as follows: {private_domain_description}. Analyze these preferences across different domains to deduce your likely inclinations within {main_kind} domain. **Output format: 'My deduced preference: [description]' and keep it under 180 words. Important notes: 1. Concentrate on the preferences within the {main_kind} domain that may align with your preferences in other product domains. 2. Directly present your analyzed product preferences in the {main_kind} domain without referencing other product domains."
# 6
def system_prompt_template_evaluation_basic(user_description, candidate_num, example_list_of_item_description):
    return f"I am an Amazon buyer. My preferences: '{user_description}'.\n\nRank these {candidate_num} items based on my preferences:\n{example_list_of_item_description}\n\nOutput format:\nRank:\n1. item title\n2. item title\n3. item title\n...\n{candidate_num}. item title\n\nOnly output the ranking list."

def system_prompt_template_evaluation_basic_g(user_description, candidate_num, example_list_of_item_description, group_Mem_txt):
    return f"I am an Amazon buyer. Here is my self-introduction, which includes my preferences and dislikes:\n\n '{user_description}'. {group_Mem_txt} \n\n Now, I am looking for items that match my preferences from {candidate_num} candidates. The features of these items are as follows:\n {example_list_of_item_description}. \n\n Please rearrange these items based on my preferences and dislikes by following these steps:\n 1. Analyze my preferences and dislikes from my self-introduction. \n 2. Compare the candidate items according to my preferences, then make a recommendation. \n 3. Consider the recent interactions and choices of users with similar tastes, as their preferences may influence mine. \n 4. **Output Format: Your ranking result must follow this format:** 'Rank: {{1. item title \\n 2. item title ...}}.' \n Note: List each item title on a new line."

def system_prompt_template_evaluation_sequential(user_description, historical_interactions, candidate_num, example_list_of_item_description):
    return f"I am an Amazon buyer. Here is my self-introduction, exhibiting my preferences and dislikes: '{user_description}'. Additionally, here is my purchasing history: \n {historical_interactions}. \n\n Now, I want to find items that match my preferences from {candidate_num} candidates. The features of these candidate items are as follows:\n {example_list_of_item_description}. \n\n Please rearrange these items based on my preferences and dislikes. To do this, follow these steps:\n 1. Analyze my preferences and dislikes from my self-introduction. \n 2. Compare the candidate items according to my preferences, and make a recommendation. Consider how these items relate to my previous purchases. \n 3. Please output your recommendation in the following format: 'Rank: {{1. item title \\n 2. item title ...}}.' \n Note that the rank list should be separated by line breaks."

def system_prompt_template_evaluation_sequential_g(user_description, historical_interactions, candidate_num, example_list_of_item_description, group_Mem_txt):
    return f"I am an Amazon buyer. Here is my self-introduction, exhibiting my preferences and dislikes: '{user_description}'. Additionally, here is my purchasing history: \n {historical_interactions}. {group_Mem_txt} \n\n Now, I want to find items that match my preferences from {candidate_num} candidates. The features of these candidate items are as follows:\n {example_list_of_item_description}. \n\n Please rearrange these items based on my preferences and dislikes. To do this, follow these steps:\n 1. Analyze my preferences and dislikes from my self-introduction. \n 2. Compare the candidate items according to my preferences, and make a recommendation. Consider how these items relate to my previous purchases. \n 3. Please output your recommendation in the following format: 'Rank: {{1. item title \\n 2. item title ...}}.' \n Note that the rank list should be separated by line breaks."

def system_prompt_template_evaluation_retrieval(user_past_description, user_description, candidate_num, example_list_of_item_description):
    return f"I am an Amazon buyer. Here is my previous self-introduction, showing my past preferences and dislikes: '{user_past_description}'.\n\n Recently, I encountered some items and updated my self-introduction: '{user_description}'. \n\n Now, I want to find items that match my preferences from {candidate_num} candidates. The features of these items are as follows:\n {example_list_of_item_description}. \n\n Please rearrange these items based on my preferences and dislikes. To do this, follow these steps:\n 1. Analyze my past preferences from my previous self-introduction. \n 2. Analyze my current preferences from my updated self-introduction. \n 3. Compare the candidate items and assess their relationships to my preferences and dislikes. Rearrange them based on your analysis. \n 4. Generate your output in the following format: 'Rank: {{1. item title \\n 2. item title ...}}.' \n Note that the rank list should be separated by line breaks. \n\n Important note:\n When recommending items, prioritize my current preferences. However, my past preferences are also valuable. If unsure, refer to my past preferences and dislikes."

def system_prompt_template_evaluation_retrieval_g(user_past_description, user_description, candidate_num, example_list_of_item_description, group_Mem_txt):
    return f"I am an Amazon buyer. Here is my previous self-introduction, showing my past preferences and dislikes: '{user_past_description}'.\n\n Recently, I encountered some items and updated my self-introduction: '{user_description}'. \n\n {group_Mem_txt} Now, I want to find items that match my preferences from {candidate_num} candidates. The features of these items are as follows:\n {example_list_of_item_description}. \n\n Please rearrange these items based on my preferences and dislikes. To do this, follow these steps:\n 1. Analyze my past preferences from my previous self-introduction. \n 2. Analyze my current preferences from my updated self-introduction. \n 3. Compare the candidate items and assess their relationships to my preferences and dislikes. Rearrange them based on your analysis. \n 4. Generate your output in the following format: 'Rank: {{1. item title \\n 2. item title ...}}.' \n Note that the rank list should be separated by line breaks. \n\n Important note:\n When recommending items, prioritize my current preferences. However, my past preferences are also valuable. If unsure, refer to my past preferences and dislikes."

def get_user_tag_prompt(user_description):
    return f"Please analyze the following self-description of a user and extract multiple interest tags based on their preferences and interests. \n\nSelf-description:{user_description} \n\nOutput the tags in valid JSON format without any extra Markdown or code block indicators. Output format example: \n\n {{\"interest_tags\":[tag1, tag2, ...]}}"


def get_call_llm_for_summary(tag_list):
    return f"Please analyze the following self-description of a user and extract multiple interest tags specifically highlighting their preferences and interests related to the distinctive styles and features of products. \n\nTag list: {tag_list}\n\nInstructions:\n1. The output must be a single phrase. Do not include sentences, lists, or other formats.\n2. The phrase should be as concise and accurate as possible in summarizing all the tags.\n3. There is no need to explain or provide additional information. Just give the summary phrase."

def groupMem_summary(group_Mem_txt):
    return f"Please summarize the following group memories and output the results. Text to be summarized: {group_Mem_txt} \nRequirements:\n1.Summarize the text to ensure concise. 2. Ensure that the rewrite maintains the core points of the group memories.\n3. Highlight the recent preferences of users in different interest groups to ensure the summary is representative.\n4. Follow the output format example: 'Users who have similar preferences to me in ... recently ...,' and ensure that the rewritten results are uniformly formatted.\n5. If necessary, enhance the content with your own understanding and analysis to enrich the summary."

def baseline_llmrank(user_his_text, recent_item, recall_budget, candidate_text_order):
    return f"I have purchased items like: {user_his_text}. Now, take a look at these {recall_budget} products: {candidate_text_order}. Could you provide a ranking for these items based on the history? Please format it as 'Rank: {{1. item title \\n 2. item title ... \\n 10. item title}}.' Remember: 1. use only the information given and avoid making any assumptions about the products, 2. just provide the final output, 3. ensure the rank list is clearly separated by line breaks."

# ============= 消融实验专用 Prompts =============

# Auto模式：直接给定正负样本标签（无决策环节）
def user_prompt_auto(user_description, list_of_item_description, pos_item_title, neg_item_title):
    """Auto模式：用户智能体直接根据标准答案更新记忆（无需判断对错）"""
    return f"You are an Amazon buyer.\n Here is your previous self-introduction, exhibiting your past preferences and dislikes:\n '{user_description}'.\n\n Recently, you encountered two items. The features of these items are:\n {list_of_item_description}.\n\n After encountering these items, you found that you really like '{pos_item_title}' and dislike '{neg_item_title}'.\n Your task now is to update your self-introduction based on these direct experiences. \n Follow these steps: \n 1. Identify new preferences from '{pos_item_title}' that you like. \n 2. Identify new dislikes from '{neg_item_title}' that you dislike. \n 3. Summarize your past preferences and dislikes from your previous self-introduction, combining them with new insights and removing conflicting parts.\n 4. Update your self-introduction, starting with new preferences, then summarizing past ones, followed by dislikes. \n\n Important notes:\n 1. Your output format should be: 'My updated self-introduction: [Your updated self-introduction here].' \n 2. Keep it under 150 words.  \n 3. Be concise and clear. \n 4. Describe only the features of items you prefer or dislike, without mentioning your thought process. \n 5. Your self-introduction should be specific and personalized; avoid generic preferences."

# ============= History-based LLM Baseline Prompt =============

def history_based_ranking_prompt(historical_items_text, candidate_num, candidate_items_text):
    """基于历史交互的排序prompt（严格baseline，仅基于标题文本相似性）"""
    return f"""Task: Rank items based on title text similarity only.

Previously interacted items (titles only):
{historical_items_text}

Candidate items to rank (titles only):
{candidate_items_text}

Instructions:
- Rank the {candidate_num} candidate items based ONLY on how similar their titles are to the previously interacted item titles
- Do NOT use any external knowledge about these items (genre, artist, content, etc.)
- Do NOT infer user preferences or item characteristics
- Only compare the TEXT of the titles: look for similar words, phrases, or patterns
- Items with titles more textually similar to the history should rank higher
- This is a pure text matching task

Output format:
Rank:
1. [item title]
2. [item title]
3. [item title]
...
{candidate_num}. [item title]"""


# ============= 长记忆评估 Prompt =============

def system_prompt_template_long_memory_evaluation(user_description, round_idx, candidate_num, example_list_of_item_description):
    return (
        f"I am an Amazon buyer. Here is my self-introduction captured after round {round_idx} of my interaction history: "
        f"'{user_description}'.\n\n"
        f"Rank these {candidate_num} items based on my current preferences:\n"
        f"{example_list_of_item_description}\n\n"
        "Output format:\n"
        "Rank:\n"
        "1. item title\n"
        "2. item title\n"
        "3. item title\n"
        "...\n"
        f"{candidate_num}. item title\n\n"
        "Only output the ranking list."
    )

LONG_MEMORY_PROMPTS = {
    "long_basic": system_prompt_template_long_memory_evaluation,
}



# 添加创新点1
# ============= 属性级别监督 Prompts =============

# 属性维度定义（建议放在 config 中）
# 针对 CDs 推荐数据集优化的维度
# ATTRIBUTE_DIMENSIONS = [
#     "genre",           # 流派 (Rock, Jazz, Classical等)
#     "artist_style",    # 艺术家风格 (Vocal, Instrumental, Experimental)
#     "audio_quality",   # 音质 (Remastered, Live Recording, Studio)
#     "release_era",     # 发行年代 (80s Nostalgia, Modern Release)
#     "rarity",          # 稀缺性 (Limited Edition, Collector's Item, Second-hand)
#     "price",           # 价格
#     "label",           # 出版厂牌 (如 Sony, Blue Note - 某些用户有厂牌忠诚度)
#     "mood"             # 情感/氛围 (Relaxing, Energetic, Melancholic)
# ]


ATTRIBUTE_DIMENSIONS = [
    "Functionality",  # 品质层次
    "Protection",  # 设计哲学
    "Aesthetics",  # 优先关注点
    "Compatibility",  # 耐用性重视程度
    "Durability",  # 品牌偏好
    "Portability",  # 价格敏感度
    "Innovation",  # 使用场景
    "Premium Quality",  # 便携性需求
    "Security",
]



# ATTRIBUTE_DIMENSIONS = [
#     "Functionality",  # 品质层次
#     "Elegance",  # 设计哲学
#     "Versatility",  # 优先关注点
#     "Comfort",  # 耐用性重视程度
#     "Color",  # 品牌偏好
#     "Uniqueness",  # 价格敏感度
#     "Detailing",  # 使用场景
#     "Pattern",  # 便携性需求
#     "Modernity",
#     "Simplicity",
# ]

def attribute_analysis_prompt_correct(
        user_description,
        pos_item_title,
        neg_item_title,
        pos_item_desc,
        neg_item_desc,
        system_reason):

    attr_list = ", ".join(ATTRIBUTE_DIMENSIONS)

    return f"""
You are an attribute extraction system.

Your ONLY task is to extract attributes that explain WHY the correct item matches the user preference.

Allowed attributes ONLY:
{attr_list}

STRICT RULES:
- Output ONLY attribute lines
- Do NOT output explanations
- Do NOT output reasoning
- Do NOT output self introduction
- Do NOT output summaries
- Do NOT output markdown
- Do NOT output extra text
- Do NOT invent attributes
- Attribute names MUST exactly match the allowed list
- Output at least 2 attributes
- If no valid attribute exists, output ONLY:
NONE

Required format:
Attribute: item_name | positive | score

Example:
Functionality: iPhone 15 | positive | 5
Protection: iPhone 15 | positive | 4

User preferences:
{user_description}

Correct item:
{pos_item_title}

Rejected item:
{neg_item_title}

Previous reasoning:
{system_reason}
"""

def attribute_analysis_prompt_incorrect(
        user_description,
        pos_item_title,
        neg_item_title,
        pos_item_desc,
        neg_item_desc,
        system_reason):

    attr_list = ", ".join(ATTRIBUTE_DIMENSIONS)

    return f"""
You are an attribute extraction system.

Your ONLY task is to extract:
1. positive attributes from the correct item
2. misleading negative attributes from the wrongly selected item

Allowed attributes ONLY:
{attr_list}

STRICT RULES:
- Output ONLY attribute lines
- Do NOT output explanations
- Do NOT output reasoning
- Do NOT output self introduction
- Do NOT output summaries
- Do NOT output markdown
- Do NOT output extra text
- Do NOT invent attributes
- Attribute names MUST exactly match the allowed list
- Output at least 2 attributes
- If no valid attribute exists, output ONLY:
NONE

Required format:
Attribute: item_name | positive/negative | score

Example:
Functionality: iPhone 15 | positive | 5
Aesthetics: Cheap Phone | negative | 4

User preferences:
{user_description}

Correct item:
{pos_item_title}

Wrongly selected item:
{neg_item_title}

Previous reasoning:
{system_reason}
"""


def user_prompt_template_with_attr(list_of_item_description, pos_item_title, neg_item_title, system_reason, attribute_dimensions):
    return f"""Recently, you considered choosing one item from two candidates. The features of these items are:
 {list_of_item_description}.

 After comparing based on your preferences, you chose '{neg_item_title}' and rejected the other. Your explanation was:
 '{system_reason}'. 

 However, after encountering these items, you realized you prefer '{pos_item_title}' and don't like '{neg_item_title}'.
 This indicates an incorrect choice, and your previous judgment about your preferences was mistaken. Your task now is to extract the attribute-level rationale for this correction and update your self-introduction. 

 Follow these steps: 
 1. Attribute Analysis (Silver Rationale): From these dimensions ({attribute_dimensions}), identify 1 to 3 key attributes that caused this misconception. For each, specify which item has the trait, its polarity (positive/negative to your true preference), and its importance score (1-5).
 2. Analyze misconceptions in your previous judgment and correct them based on step 1.
 3. Identify new preferences from '{pos_item_title}' and dislikes from '{neg_item_title}'. 
 4. Summarize your past preferences, merging them with new insights and removing conflicting parts.
 5. Update your self-introduction, starting with new preferences, then summarizing past ones, followed by dislikes. 

 Important notes:
 1. Your output format MUST strictly follow this structure:
 Attribute Rationale:
 - [attribute_1]: [item_name] | [positive/negative] | [score 1-5]
 - [attribute_2]: [item_name] | [positive/negative] | [score 1-5]
 My updated self-introduction: [Your updated self-introduction here]. 
 2. Keep the self-introduction under 150 words.  
 3. Be concise and clear. 
 4. Describe only the features of items you prefer or dislike, without mentioning your thought process in the self-introduction. 
 5. Your self-introduction should be specific and personalized; avoid generic preferences."""


def user_prompt_template_true_with_attr(list_of_item_description, pos_item_title, neg_item_title, system_reason, attribute_dimensions):
    return f"""Recently, you considered choosing one item from two candidates. The features of these items are:
 {list_of_item_description}.

 After comparing based on your preferences, you selected '{pos_item_title}' and rejected the other. Your explanation was:
 '{system_reason}'. 

 After encountering these items, you found that you really like '{pos_item_title}' and dislike '{neg_item_title}'.
 This indicates you made a correct choice, and your judgment about your preferences was accurate. 
 Your task now is to extract the attribute-level rationale confirming your choice and update your self-introduction. 

 Please follow these steps: 
 1. Attribute Analysis (Silver Rationale): From these dimensions ({attribute_dimensions}), identify 1 to 3 key attributes that drove this successful match. For each, specify which item has the trait, its polarity (positive/negative to your preference), and its importance score (1-5).
 2. Analyze your judgment about your preferences and dislikes from your explanation based on step 1.
 3. Identify new preferences based on '{pos_item_title}' and dislikes based on '{neg_item_title}'. 
 4. Summarize your past preferences and dislikes from your previous self-introduction, combining them with new insights while removing conflicting parts.
 5. Update your self-introduction, starting with your new preferences, then summarizing past ones, followed by your dislikes. 

 Important notes:
 1. Your output format MUST strictly follow this structure:
 Attribute Rationale:
 - [attribute_1]: [item_name] | [positive/negative] | [score 1-5]
 - [attribute_2]: [item_name] | [positive/negative] | [score 1-5]
 My updated self-introduction: [Your updated self-introduction here]. 
 2. Keep the self-introduction under 150 words. 
 3. Be concise and clear. 
 4. Describe only the features of items you prefer or dislike, without mentioning your thought process in the self-introduction. 
 5. Your self-introduction should be specific and personalized."""


def item_prompt_template_with_attr(user_description, list_of_item_description, pos_item_title, neg_item_title, system_reason, attribute_dimensions):
    return f"""User self-introduction, showing preferences and dislikes: '{user_description}'.
 Recently, the user browsed a shopping site and considered two items:
 {list_of_item_description}.

 He chose '{neg_item_title}' and rejected the other, explaining: '{system_reason}'. 

 However, he prefers '{pos_item_title}' instead, indicating an unsuitable choice due to misleading descriptions. He likes '{pos_item_title}' for its features and dislikes '{neg_item_title}' for undesirable traits. Your task is to extract the attribute-level rationale for this gap and update the item descriptions. 

 Follow these steps:
 1. Attribute Analysis (Silver Rationale): From these dimensions ({attribute_dimensions}), identify 1 to 3 key attributes where the original descriptions misled the user. For each, specify the item, its true polarity (positive/negative to the user), and its importance score (1-5).
 2. Analyze features that led to the poor choice and modify them based on step 1. 
 3. Examine user preferences and dislikes; explore new features of the preferred item aligning with preferences and opposing dislikes, and do the same for the disliked item, highlighting differences. 
 4. Incorporate new features into the previous descriptions, preserving valuable content while being concise.

 Important notes: 
 1. Your output format MUST strictly follow this structure:
 Attribute Rationale:
 - [attribute_1]: [item_name] | [positive/negative] | [score 1-5]
 - [attribute_2]: [item_name] | [positive/negative] | [score 1-5]
 The updated description of the first item is: [updated description]. 
 The updated description of the second item is: [updated description].
 2. Each updated description cannot exceed 50 words; be concise and clear. 
 3. In your descriptions, refer to user preferences collectively, avoiding specific individual references, e.g., 'the user with ... preferences/dislikes'.
 4. The updated description should not contradict the item's inherent characteristics. 
 5. The updated description should highlight distinguishing features that differentiate this item from others.
 Do NOT output any analysis or reasoning. Output ONLY the two updated descriptions starting with "The updated description of the first item is:" immediately."""


def item_prompt_template_true_with_attr(user_description, list_of_item_description, pos_item_title, neg_item_title, attribute_dimensions):
    return f"""User self-description, showcasing preferences and dislikes: '{user_description}'.
 Recently, the user browsed a shopping site and considered two items:
 {list_of_item_description}.

 The user chose '{pos_item_title}' for its features and rejected '{neg_item_title}' for undesirable traits. Your task is to extract the attribute-level rationale confirming this choice and update the descriptions of these items. 

 Follow these steps:
 1. Attribute Analysis (Silver Rationale): From these dimensions ({attribute_dimensions}), identify 1 to 3 key attributes that drove this successful choice. For each, specify the item, its polarity (positive/negative to the user), and its importance score (1-5).
 2. Analyze the user's preferences and dislikes from the self-description based on step 1. 
 3. Explore the chosen item's features that align with preferences and oppose dislikes, and examine the rejected item's features that align with dislikes and oppose preferences. Highlight the differences thoroughly. 
 4. Incorporate new features into the previous descriptions, preserving key information while being concise.

 Important notes: 
 1. Your output format MUST strictly follow this structure:
 Attribute Rationale:
 - [attribute_1]: [item_name] | [positive/negative] | [score 1-5]
 - [attribute_2]: [item_name] | [positive/negative] | [score 1-5]
 The updated description of the first item is: [updated description]. 
 The updated description of the second item is: [updated description].
 2. Each updated description cannot exceed 50 words; be concise and clear! 
 3. In your updated descriptions, refer to preferences collectively.
 4. New features should reflect user preferences, and the updated descriptions must not contradict the inherent characteristics of the items.
 Do NOT output any analysis or reasoning. Output ONLY the two updated descriptions starting with "The updated description of the first item is:" immediately."""






# ============= P0: LLM Confidence Self-Assessment =============
def get_confidence_prompt():
    return """\n\n[Confidence Assessment]
Rate your confidence in this memory update (1-5):
Justification: <one sentence>

Scoring guide:
5 = Strongly supported by both recent interactions and long-term preferences
4 = Well-supported by recent evidence, consistent with history
3 = Reasonable inference but some uncertainty
2 = Weak signal, might be noisy or transient
1 = Speculative, likely noise or irrelevant to long-term preferences"""


# 创新点二---------------------------------------------------------------------------------------------------------------------------------
# ============================================================================
# Function 1: user_prompt_template (incorrect choice) - UPDATED VERSION
# ============================================================================
def user_prompt_template_with_attr_ltm(list_of_item_description, pos_item_title,
                                       neg_item_title, system_reason,
                                       attribute_dimensions, ltm_attributes=None, stm_attributes=None):
    """
    用户prompt - 选择错误 - 包含属性分析 + LTM + STM

    参数:
    - ltm_attributes: LTM属性字典 {dim: {"count": int, "avg_score": float, "items": [...]}}
    - stm_attributes: STM属性列表 [{"round": 3, "attributes": {...}}, {"round": 2, "attributes": {...}}]
    """

    # 构建LTM提示（基于属性）
    ltm_prompt = ""
    if ltm_attributes:
        ltm_parts = []
        for dim, stats in ltm_attributes.items():
            ltm_parts.append(
                f"  - {dim}: consistently preferred (appeared {stats['count']} times, "
                f"avg importance: {stats['avg_score']:.1f}/5)"
            )

        ltm_prompt = f"""

Your core long-term stable attributes (verified through Round 0-3):
{chr(10).join(ltm_parts)}

Note: These attributes have been validated at least 3 times in your interaction history, representing your stable and reliable preferences."""

    # 构建STM提示（基于属性）
    stm_prompt = ""
    if stm_attributes:
        stm_parts = []
        for idx, entry in enumerate(stm_attributes):
            round_num = entry["round"]
            attrs = entry["attributes"]

            # 格式化属性
            attr_lines = []
            for dim, detail in attrs.items():
                attr_lines.append(
                    f"    - {dim}: {detail['item_name']} | {detail['polarity']} | score {detail['score']}"
                )

            if idx == 0:  # 最近一轮
                stm_parts.append(f"\nYour past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))
            else:  # 倒数第二轮
                stm_parts.append(f"\nYour second past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))

        stm_prompt = "\n".join(stm_parts)

    return f"""Recently, you considered choosing one item from two candidates. The features of these items are:
{list_of_item_description}.

After comparing based on your preferences, you chose '{neg_item_title}' and rejected the other. Your explanation was:
'{system_reason}'.

However, after encountering these items, you realized you prefer '{pos_item_title}' and don't like '{neg_item_title}'.
This indicates an incorrect choice, and your previous judgment about your preferences was mistaken.{ltm_prompt}{stm_prompt}

Your task now is to update your self-introduction with your new preferences and dislikes, considering:
1. Your core long-term stable attributes (if provided above) - these dimensions have been consistently preferred across multiple interactions
2. Your recent attribute preferences (if provided above) - these show how your taste has evolved in recent rounds
3. The attribute-level analysis from the current interaction

Please follow these steps:
1. Attribute Analysis (Silver Rationale): From these dimensions ({attribute_dimensions}), identify 1 to 3 key attributes that explain why you actually prefer '{pos_item_title}'. For each attribute, specify which item has it, its polarity (positive/negative), and importance score (1-5).
2. Reflect on your long-term stable attributes and recent attribute trends - do they align with this new preference? If there's a conflict, prioritize the current interaction but acknowledge the shift.
3. Analyze misconceptions in your previous judgment and correct them.
4. Identify new preferences from '{pos_item_title}' and dislikes from '{neg_item_title}'.
5. Summarize your past preferences (both long-term and recent), merging them with new insights and removing conflicting parts.
6. Update your self-introduction, starting with new preferences, then summarizing past ones, followed by dislikes.

Important notes:
1. Your output format MUST strictly follow this structure:
Attribute Rationale:
- [attribute_1]: [item_name] | [positive/negative] | [score 1-5]
- [attribute_2]: [item_name] | [positive/negative] | [score 1-5]
My updated self-introduction: [Your updated self-introduction here].
2. Keep the self-introduction under 150 words.
3. Be concise and clear.
4. Describe only the features of items you prefer or dislike, without mentioning your thought process.
5. Your self-introduction should be specific and personalized; avoid generic preferences.
6. When integrating long-term and short-term attributes, maintain consistency but allow for natural preference evolution."""


def user_prompt_template_true_with_attr_ltm(list_of_item_description, pos_item_title,
                                            neg_item_title, system_reason,
                                            attribute_dimensions, ltm_attributes=None, stm_attributes=None):
    """
    用户prompt - 选择正确 - 包含属性分析 + LTM + STM

    参数:
    - ltm_attributes: LTM属性字典 {dim: {"count": int, "avg_score": float, "items": [...]}}
    - stm_attributes: STM属性列表 [{"round": 3, "attributes": {...}}, {"round": 2, "attributes": {...}}]
    """

    # 构建LTM提示（基于属性）
    ltm_prompt = ""
    if ltm_attributes:
        ltm_parts = []
        for dim, stats in ltm_attributes.items():
            ltm_parts.append(
                f"  - {dim}: consistently preferred (appeared {stats['count']} times, "
                f"avg importance: {stats['avg_score']:.1f}/5)"
            )

        ltm_prompt = f"""

Your core long-term stable attributes (verified through Round 0-3):
{chr(10).join(ltm_parts)}

Note: These attributes have been validated at least 3 times in your interaction history, representing your stable and reliable preferences."""

    # 构建STM提示（基于属性）
    stm_prompt = ""
    if stm_attributes:
        stm_parts = []
        for idx, entry in enumerate(stm_attributes):
            round_num = entry["round"]
            attrs = entry["attributes"]

            # 格式化属性
            attr_lines = []
            for dim, detail in attrs.items():
                attr_lines.append(
                    f"    - {dim}: {detail['item_name']} | {detail['polarity']} | score {detail['score']}"
                )

            if idx == 0:  # 最近一轮
                stm_parts.append(f"\nYour past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))
            else:  # 倒数第二轮
                stm_parts.append(f"\nYour second past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))

        stm_prompt = "\n".join(stm_parts)

    return f"""Recently, you considered choosing one item from two candidates. The features of these items are:
{list_of_item_description}.

After comparing based on your preferences, you selected '{pos_item_title}' and rejected the other. Your explanation was:
'{system_reason}'.

After encountering these items, you found that you really like '{pos_item_title}' and dislike '{neg_item_title}'.
This indicates you made a correct choice, and your judgment about your preferences was accurate.{ltm_prompt}{stm_prompt}

Your task now is to update your self-introduction with your confirmed preferences and dislikes, considering:
1. Your core long-term stable attributes (if provided above) - these dimensions have been consistently preferred across multiple interactions
2. Your recent attribute preferences (if provided above) - these show how your taste has evolved in recent rounds
3. The attribute-level analysis from the current interaction

Please follow these steps:
1. Attribute Analysis (Silver Rationale): From these dimensions ({attribute_dimensions}), identify 1 to 3 key attributes that drove this successful match. For each, specify which item has the trait, its polarity (positive/negative to your preference), and its importance score (1-5).
2. Consider your long-term stable attributes and recent attribute trends - do they align with this confirmed preference? Reinforce consistent patterns.
3. Analyze your judgment about your preferences and dislikes from your explanation.
4. Identify new preferences based on '{pos_item_title}' and dislikes based on '{neg_item_title}'.
5. Summarize your past preferences and dislikes from your previous self-introduction, combining them with new insights while removing conflicting parts.
6. Update your self-introduction, starting with your new preferences, then summarizing past ones, followed by your dislikes.

Important notes:
1. Your output format MUST strictly follow this structure:
Attribute Rationale:
- [attribute_1]: [item_name] | [positive/negative] | [score 1-5]
- [attribute_2]: [item_name] | [positive/negative] | [score 1-5]
My updated self-introduction: [Your updated self-introduction here].
2. Keep the self-introduction under 150 words.
3. Be concise and clear.
4. Describe only the features of items you prefer or dislike, without mentioning your thought process in the self-introduction.
5. Your self-introduction should be specific and personalized; avoid generic preferences.
6. When integrating long-term and short-term attributes, maintain consistency and reinforce stable patterns."""


def item_prompt_template_with_attr_ltm(user_description, list_of_item_description,
                                       pos_item_title, neg_item_title, system_reason,
                                       attribute_dimensions, ltm_attributes=None, stm_attributes=None):
    """
    物品prompt - 选择错误 - 包含属性分析 + LTM + STM

    参数:
    - ltm_attributes: LTM属性字典 {dim: {"count": int, "avg_score": float, "items": [...]}}
    - stm_attributes: STM属性列表 [{"round": 3, "attributes": {...}}, {"round": 2, "attributes": {...}}]
    """

    # 构建LTM提示（基于属性）
    ltm_prompt = ""
    if ltm_attributes:
        ltm_parts = []
        for dim, stats in ltm_attributes.items():
            ltm_parts.append(
                f"  - {dim}: consistently preferred (appeared {stats['count']} times, "
                f"avg importance: {stats['avg_score']:.1f}/5)"
            )

        ltm_prompt = f"""

User's core long-term stable attributes (verified through Round 0-3):
{chr(10).join(ltm_parts)}

Note: These attributes have been validated at least 3 times, representing stable preferences."""

    # 构建STM提示（基于属性）
    stm_prompt = ""
    if stm_attributes:
        stm_parts = []
        for idx, entry in enumerate(stm_attributes):
            round_num = entry["round"]
            attrs = entry["attributes"]

            # 格式化属性
            attr_lines = []
            for dim, detail in attrs.items():
                attr_lines.append(
                    f"    - {dim}: {detail['item_name']} | {detail['polarity']} | score {detail['score']}"
                )

            if idx == 0:  # 最近一轮
                stm_parts.append(f"\nUser's past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))
            else:  # 倒数第二轮
                stm_parts.append(f"\nUser's second past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))

        stm_prompt = "\n".join(stm_parts)

    return f"""You are an item description updater. A user with the following preferences interacted with two items:
User preferences: {user_description}.{ltm_prompt}{stm_prompt}

Items:
{list_of_item_description}

The user initially chose '{neg_item_title}' over '{pos_item_title}', reasoning: '{system_reason}'.
However, after experiencing both items, the user realized they actually prefer '{pos_item_title}' and dislike '{neg_item_title}'.

Your task is to update the descriptions of both items to better reflect the user's true preferences, considering:
1. The user's core long-term stable attributes (if provided above) - dimensions consistently preferred across multiple interactions
2. The user's recent attribute preferences (if provided above) - how their taste has evolved in recent rounds
3. The attribute-level analysis from these dimensions: {attribute_dimensions}

Please follow these steps:
1. Attribute Analysis: Identify 1-3 key attributes from ({attribute_dimensions}) that explain why the user prefers '{pos_item_title}'. For each attribute, specify which item has it, its polarity (positive/negative), and importance score (1-5).
2. For '{pos_item_title}': Emphasize features that align with the user's true preferences (both long-term stable attributes and recent attribute trends).
3. For '{neg_item_title}': Highlight aspects that conflict with the user's preferences.
4. Keep descriptions concise and focused on attributes that matter to this user.

Output format:
Attribute Rationale:
- [attribute_1]: [item_name] | [positive/negative] | [score 1-5]
- [attribute_2]: [item_name] | [positive/negative] | [score 1-5]
The updated description of the first item is: [Updated description for '{neg_item_title}']
The updated description of the second item is: [Updated description for '{pos_item_title}']
Do NOT output any analysis or reasoning. Output ONLY the two updated descriptions starting with "The updated description of the first item is:" immediately."""


def item_prompt_template_true_with_attr_ltm(user_description, list_of_item_description,
                                            pos_item_title, neg_item_title,
                                            attribute_dimensions, ltm_attributes=None, stm_attributes=None):
    """
    物品prompt - 选择正确 - 包含属性分析 + LTM + STM

    参数:
    - ltm_attributes: LTM属性字典 {dim: {"count": int, "avg_score": float, "items": [...]}}
    - stm_attributes: STM属性列表 [{"round": 3, "attributes": {...}}, {"round": 2, "attributes": {...}}]
    """

    # 构建LTM提示（基于属性）
    ltm_prompt = ""
    if ltm_attributes:
        ltm_parts = []
        for dim, stats in ltm_attributes.items():
            ltm_parts.append(
                f"  - {dim}: consistently preferred (appeared {stats['count']} times, "
                f"avg importance: {stats['avg_score']:.1f}/5)"
            )

        ltm_prompt = f"""

User's core long-term stable attributes (verified through Round 0-3):
{chr(10).join(ltm_parts)}

Note: These attributes have been validated at least 3 times, representing stable preferences."""

    # 构建STM提示（基于属性）
    stm_prompt = ""
    if stm_attributes:
        stm_parts = []
        for idx, entry in enumerate(stm_attributes):
            round_num = entry["round"]
            attrs = entry["attributes"]

            # 格式化属性
            attr_lines = []
            for dim, detail in attrs.items():
                attr_lines.append(
                    f"    - {dim}: {detail['item_name']} | {detail['polarity']} | score {detail['score']}"
                )

            if idx == 0:  # 最近一轮
                stm_parts.append(f"\nUser's past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))
            else:  # 倒数第二轮
                stm_parts.append(f"\nUser's second past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))

        stm_prompt = "\n".join(stm_parts)

    return f"""You are an item description updater. A user with the following preferences interacted with two items:
User preferences: {user_description}.{ltm_prompt}{stm_prompt}

Items:
{list_of_item_description}

The user chose '{pos_item_title}' over '{neg_item_title}', and after experiencing both items, confirmed this was the right choice.
They really like '{pos_item_title}' and dislike '{neg_item_title}'.

Your task is to update the descriptions of both items to better reflect the user's preferences, considering:
1. The user's core long-term stable attributes (if provided above) - dimensions consistently preferred across multiple interactions
2. The user's recent attribute preferences (if provided above) - how their taste has evolved in recent rounds
3. The attribute-level analysis from these dimensions: {attribute_dimensions}

Please follow these steps:
1. Attribute Analysis: Identify 1-3 key attributes from ({attribute_dimensions}) that explain why the user prefers '{pos_item_title}'. For each attribute, specify which item has it, its polarity (positive/negative), and importance score (1-5).
2. For '{pos_item_title}': Emphasize features that align with the user's preferences (both long-term stable attributes and recent attribute trends).
3. For '{neg_item_title}': Highlight aspects that the user dislikes.
4. Keep descriptions concise and focused on attributes that matter to this user.

Output format:
Attribute Rationale:
- [attribute_1]: [item_name] | [positive/negative] | [score 1-5]
- [attribute_2]: [item_name] | [positive/negative] | [score 1-5]
The updated description of the first item is: [Updated description for '{neg_item_title}']
The updated description of the second item is: [Updated description for '{pos_item_title}']
Do NOT output any analysis or reasoning. Output ONLY the two updated descriptions starting with "The updated description of the first item is:" immediately."""



# 只有短期记忆----------------------------------------------
def user_prompt_template_with_attr_stm(list_of_item_description, pos_item_title,
                                       neg_item_title, system_reason,
                                       attribute_dimensions, stm_attributes=None):
    """
    用户prompt - 选择错误 - 包含属性分析 + LTM + STM

    参数:
    - ltm_attributes: LTM属性字典 {dim: {"count": int, "avg_score": float, "items": [...]}}
    - stm_attributes: STM属性列表 [{"round": 3, "attributes": {...}}, {"round": 2, "attributes": {...}}]
    """

    # 构建STM提示（基于属性）
    stm_prompt = ""
    if stm_attributes:
        stm_parts = []
        for idx, entry in enumerate(stm_attributes):
            round_num = entry["round"]
            attrs = entry["attributes"]

            # 格式化属性
            attr_lines = []
            for dim, detail in attrs.items():
                attr_lines.append(
                    f"    - {dim}: {detail['item_name']} | {detail['polarity']} | score {detail['score']}"
                )

            if idx == 0:  # 最近一轮
                stm_parts.append(f"\nYour past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))
            else:  # 倒数第二轮
                stm_parts.append(f"\nYour second past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))

        stm_prompt = "\n".join(stm_parts)

    return f"""Recently, you considered choosing one item from two candidates. The features of these items are:
{list_of_item_description}.

After comparing based on your preferences, you chose '{neg_item_title}' and rejected the other. Your explanation was:
'{system_reason}'.

However, after encountering these items, you realized you prefer '{pos_item_title}' and don't like '{neg_item_title}'.
This indicates an incorrect choice, and your previous judgment about your preferences was mistaken.{stm_prompt}

Your task now is to update your self-introduction with your new preferences and dislikes, considering:
1. Your core long-term stable attributes (if provided above) - these dimensions have been consistently preferred across multiple interactions
2. Your recent attribute preferences (if provided above) - these show how your taste has evolved in recent rounds
3. The attribute-level analysis from the current interaction

Please follow these steps:
1. Attribute Analysis (Silver Rationale): From these dimensions ({attribute_dimensions}), identify 1 to 3 key attributes that explain why you actually prefer '{pos_item_title}'. For each attribute, specify which item has it, its polarity (positive/negative), and importance score (1-5).
2. Reflect on your long-term stable attributes and recent attribute trends - do they align with this new preference? If there's a conflict, prioritize the current interaction but acknowledge the shift.
3. Analyze misconceptions in your previous judgment and correct them.
4. Identify new preferences from '{pos_item_title}' and dislikes from '{neg_item_title}'.
5. Summarize your past preferences (both long-term and recent), merging them with new insights and removing conflicting parts.
6. Update your self-introduction, starting with new preferences, then summarizing past ones, followed by dislikes.

Important notes:
1. Your output format MUST strictly follow this structure:
Attribute Rationale:
- [attribute_1]: [item_name] | [positive/negative] | [score 1-5]
- [attribute_2]: [item_name] | [positive/negative] | [score 1-5]
My updated self-introduction: [Your updated self-introduction here].
2. Keep the self-introduction under 150 words.
3. Be concise and clear.
4. Describe only the features of items you prefer or dislike, without mentioning your thought process.
5. Your self-introduction should be specific and personalized; avoid generic preferences.
6. When integrating long-term and short-term attributes, maintain consistency but allow for natural preference evolution."""


def user_prompt_template_true_with_attr_stm(list_of_item_description, pos_item_title,
                                            neg_item_title, system_reason,
                                            attribute_dimensions, stm_attributes=None):
    """
    用户prompt - 选择正确 - 包含属性分析 + LTM + STM

    参数:
    - ltm_attributes: LTM属性字典 {dim: {"count": int, "avg_score": float, "items": [...]}}
    - stm_attributes: STM属性列表 [{"round": 3, "attributes": {...}}, {"round": 2, "attributes": {...}}]
    """

    # 构建STM提示（基于属性）
    stm_prompt = ""
    if stm_attributes:
        stm_parts = []
        for idx, entry in enumerate(stm_attributes):
            round_num = entry["round"]
            attrs = entry["attributes"]

            # 格式化属性
            attr_lines = []
            for dim, detail in attrs.items():
                attr_lines.append(
                    f"    - {dim}: {detail['item_name']} | {detail['polarity']} | score {detail['score']}"
                )

            if idx == 0:  # 最近一轮
                stm_parts.append(f"\nYour past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))
            else:  # 倒数第二轮
                stm_parts.append(f"\nYour second past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))

        stm_prompt = "\n".join(stm_parts)

    return f"""Recently, you considered choosing one item from two candidates. The features of these items are:
{list_of_item_description}.

After comparing based on your preferences, you selected '{pos_item_title}' and rejected the other. Your explanation was:
'{system_reason}'.

After encountering these items, you found that you really like '{pos_item_title}' and dislike '{neg_item_title}'.
This indicates you made a correct choice, and your judgment about your preferences was accurate.{stm_prompt}

Your task now is to update your self-introduction with your confirmed preferences and dislikes, considering:
1. Your core long-term stable attributes (if provided above) - these dimensions have been consistently preferred across multiple interactions
2. Your recent attribute preferences (if provided above) - these show how your taste has evolved in recent rounds
3. The attribute-level analysis from the current interaction

Please follow these steps:
1. Attribute Analysis (Silver Rationale): From these dimensions ({attribute_dimensions}), identify 1 to 3 key attributes that drove this successful match. For each, specify which item has the trait, its polarity (positive/negative to your preference), and its importance score (1-5).
2. Consider your long-term stable attributes and recent attribute trends - do they align with this confirmed preference? Reinforce consistent patterns.
3. Analyze your judgment about your preferences and dislikes from your explanation.
4. Identify new preferences based on '{pos_item_title}' and dislikes based on '{neg_item_title}'.
5. Summarize your past preferences and dislikes from your previous self-introduction, combining them with new insights while removing conflicting parts.
6. Update your self-introduction, starting with your new preferences, then summarizing past ones, followed by your dislikes.

Important notes:
1. Your output format MUST strictly follow this structure:
Attribute Rationale:
- [attribute_1]: [item_name] | [positive/negative] | [score 1-5]
- [attribute_2]: [item_name] | [positive/negative] | [score 1-5]
My updated self-introduction: [Your updated self-introduction here].
2. Keep the self-introduction under 150 words.
3. Be concise and clear.
4. Describe only the features of items you prefer or dislike, without mentioning your thought process in the self-introduction.
5. Your self-introduction should be specific and personalized; avoid generic preferences.
6. When integrating long-term and short-term attributes, maintain consistency and reinforce stable patterns."""


def item_prompt_template_with_attr_stm(user_description, list_of_item_description,
                                       pos_item_title, neg_item_title, system_reason,
                                       attribute_dimensions, stm_attributes=None):
    """
    物品prompt - 选择错误 - 包含属性分析 + LTM + STM

    参数:
    - ltm_attributes: LTM属性字典 {dim: {"count": int, "avg_score": float, "items": [...]}}
    - stm_attributes: STM属性列表 [{"round": 3, "attributes": {...}}, {"round": 2, "attributes": {...}}]
    """

    # 构建STM提示（基于属性）
    stm_prompt = ""
    if stm_attributes:
        stm_parts = []
        for idx, entry in enumerate(stm_attributes):
            round_num = entry["round"]
            attrs = entry["attributes"]

            # 格式化属性
            attr_lines = []
            for dim, detail in attrs.items():
                attr_lines.append(
                    f"    - {dim}: {detail['item_name']} | {detail['polarity']} | score {detail['score']}"
                )

            if idx == 0:  # 最近一轮
                stm_parts.append(f"\nUser's past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))
            else:  # 倒数第二轮
                stm_parts.append(f"\nUser's second past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))

        stm_prompt = "\n".join(stm_parts)

    return f"""You are an item description updater. A user with the following preferences interacted with two items:
User preferences: {user_description}.{stm_prompt}

Items:
{list_of_item_description}

The user initially chose '{neg_item_title}' over '{pos_item_title}', reasoning: '{system_reason}'.
However, after experiencing both items, the user realized they actually prefer '{pos_item_title}' and dislike '{neg_item_title}'.

Your task is to update the descriptions of both items to better reflect the user's true preferences, considering:
1. The user's core long-term stable attributes (if provided above) - dimensions consistently preferred across multiple interactions
2. The user's recent attribute preferences (if provided above) - how their taste has evolved in recent rounds
3. The attribute-level analysis from these dimensions: {attribute_dimensions}

Please follow these steps:
1. Attribute Analysis: Identify 1-3 key attributes from ({attribute_dimensions}) that explain why the user prefers '{pos_item_title}'. For each attribute, specify which item has it, its polarity (positive/negative), and importance score (1-5).
2. For '{pos_item_title}': Emphasize features that align with the user's true preferences (both long-term stable attributes and recent attribute trends).
3. For '{neg_item_title}': Highlight aspects that conflict with the user's preferences.
4. Keep descriptions concise and focused on attributes that matter to this user.

Output format:
Attribute Rationale:
- [attribute_1]: [item_name] | [positive/negative] | [score 1-5]
- [attribute_2]: [item_name] | [positive/negative] | [score 1-5]
The updated description of the first item is: [Updated description for '{neg_item_title}']
The updated description of the second item is: [Updated description for '{pos_item_title}']
Do NOT output any analysis or reasoning. Output ONLY the two updated descriptions starting with "The updated description of the first item is:" immediately."""


def item_prompt_template_true_with_attr_stm(user_description, list_of_item_description,
                                            pos_item_title, neg_item_title,
                                            attribute_dimensions, stm_attributes=None):
    """
    物品prompt - 选择正确 - 包含属性分析 + LTM + STM

    参数:
    - ltm_attributes: LTM属性字典 {dim: {"count": int, "avg_score": float, "items": [...]}}
    - stm_attributes: STM属性列表 [{"round": 3, "attributes": {...}}, {"round": 2, "attributes": {...}}]
    """

    # 构建STM提示（基于属性）
    stm_prompt = ""
    if stm_attributes:
        stm_parts = []
        for idx, entry in enumerate(stm_attributes):
            round_num = entry["round"]
            attrs = entry["attributes"]

            # 格式化属性
            attr_lines = []
            for dim, detail in attrs.items():
                attr_lines.append(
                    f"    - {dim}: {detail['item_name']} | {detail['polarity']} | score {detail['score']}"
                )

            if idx == 0:  # 最近一轮
                stm_parts.append(f"\nUser's past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))
            else:  # 倒数第二轮
                stm_parts.append(f"\nUser's second past attribute preferences (Round {round_num}):\n" + "\n".join(attr_lines))

        stm_prompt = "\n".join(stm_parts)

    return f"""You are an item description updater. A user with the following preferences interacted with two items:
User preferences: {user_description}.{stm_prompt}

Items:
{list_of_item_description}

The user chose '{pos_item_title}' over '{neg_item_title}', and after experiencing both items, confirmed this was the right choice.
They really like '{pos_item_title}' and dislike '{neg_item_title}'.

Your task is to update the descriptions of both items to better reflect the user's preferences, considering:
1. The user's core long-term stable attributes (if provided above) - dimensions consistently preferred across multiple interactions
2. The user's recent attribute preferences (if provided above) - how their taste has evolved in recent rounds
3. The attribute-level analysis from these dimensions: {attribute_dimensions}

Please follow these steps:
1. Attribute Analysis: Identify 1-3 key attributes from ({attribute_dimensions}) that explain why the user prefers '{pos_item_title}'. For each attribute, specify which item has it, its polarity (positive/negative), and importance score (1-5).
2. For '{pos_item_title}': Emphasize features that align with the user's preferences (both long-term stable attributes and recent attribute trends).
3. For '{neg_item_title}': Highlight aspects that the user dislikes.
4. Keep descriptions concise and focused on attributes that matter to this user.

Output format:
Attribute Rationale:
- [attribute_1]: [item_name] | [positive/negative] | [score 1-5]
- [attribute_2]: [item_name] | [positive/negative] | [score 1-5]
The updated description of the first item is: [Updated description for '{neg_item_title}']
The updated description of the second item is: [Updated description for '{pos_item_title}']
Do NOT output any analysis or reasoning. Output ONLY the two updated descriptions starting with "The updated description of the first item is:" immediately."""




# def adjusted_memory_prompt(extracted_response, gate_score, stm_score, ltm_score, round_num):
#     """
#     生成调整后的记忆更新的prompt（只在gate_score < threshold时调用）
#
#     参数:
#         extracted_response: 已提取"My updated self-introduction:"后的内容
#         gate_score: 门控分数（0-1，当前必然 < threshold）
#         round_num: 当前轮次
#
#     返回:
#         prompt: 用于调用LLM的prompt
#     """
#     return f"""You are helping to update a user's preference memory in a recommendation system.
#
# **Current Round**: {round_num}
# **Stability Score**: {gate_score:.2f} (Below threshold - preferences are unstable)
#
# **User's Original Self-Introduction Update**:
# {extracted_response}
#
# **Context**:
# The stability score is below the threshold, indicating that the user's current preferences are unstable or exploratory. We need to generate a MORE CONSERVATIVE and INCREMENTAL version of this update, rather than accepting the full change directly.
#
# **Your Task**:
# Based on the original update, generate an ADJUSTED self-introduction that:
# 1. Softens strong preference changes (e.g., "I now prefer X" → "I'm exploring X")
# 2. Preserves stable preferences from previous rounds
# 3. Marks new interests as tentative rather than definitive
# 4. Maintains the same format and style as the original update
#
# **Output Format**:
# My updated self-introduction: [Your adjusted version here, in the same style as the original]
# """

# def adjusted_memory_prompt(extracted_response, gate_score, stm_score, ltm_score, round_num):
#     """
#     生成带有属性重叠与极性分析思考的 Prompt
#
#     参数逻辑：
#     - stm_score: 基于当前轮与前两轮的属性重叠及极性分析
#     - ltm_score: 基于当前轮与历史所有轮次的对比
#     """
#
#     # 动态生成思考逻辑引导
#     if ltm_score == 0:
#         # 此时主要看近期三轮的局部波动
#         thought_guidance = (
#             "1. **Short-term Fluctuation**: Analyze why the attribute overlap or sentiment polarity "
#             f"has shifted across the last 3 rounds (STM Score: {stm_score:.2f})."
#         )
#     else:
#         # 此时需要对比局部波动与全局长期的差异
#         thought_guidance = (
#             f"1. **Short-term Consistency**: Evaluate the attribute/polarity overlap within the 3-round sliding window (STM Score: {stm_score:.2f}).\n"
#             f"2. **Long-term Deviation**: Analyze how current preferences diverge from the historical global baseline (LTM Score: {ltm_score:.2f})."
#         )
#
#     return f"""You are a specialized agent for maintaining user preference profiles in a recommendation system.
#
# **Context Metrics**:
# - **Current Round**: {round_num}
# - **Gate Score**: {gate_score:.2f} (Stability indicator)
# - **Short-term Memory (STM) Score**: {stm_score:.2f} (Overlap/Polarity check of the last 3 rounds)
# - **Long-term Memory (LTM) Score**: {ltm_score:.2f} (Correlation with all historical rounds)
#
# **User's Original Self-Introduction Update**:
# {extracted_response}
#
# **Task**:
# The low stability score indicates a potential "preference drift" or "exploratory behavior."
# You must output the original update followed by a deep reflection on why the memory is currently unstable.
#
# **Reflection Requirements**:
# {thought_guidance}
# 3. Distinguish between a "genuine interest shift" and "random noise" based on the scores provided.
#
# **Output Format**:
# My updated self-introduction:
# {extracted_response}
#
# [Reflective Thoughts]:
# (Provide a concise analysis focusing on attribute overlap and sentiment polarity changes compared to short-term and long-term history)
# """


# def adjusted_memory_prompt(extracted_response, gate_score, stm_score, ltm_score, round_num):
#     """
#     生成带有属性重叠与极性分析思考的 Prompt，并严格限制反思长度。
#     """
#
#     # 动态生成思考逻辑引导
#     if round_num < 4:
#         thought_guidance = (
#             f"1. **Short-term Pattern**: STM Score = {stm_score:.2f} "
#             f"(Higher = more similar to last 3 rounds; Lower = shifting focus). "
#             f"Briefly explain what this similarity/difference reveals."
#         )
#     else:
#         thought_guidance = (
#             f"1. **Consistency Analysis**: \n"
#             f"   - STM Score = {stm_score:.2f} (similarity to last 3 rounds)\n"
#             f"   - LTM Score = {ltm_score:.2f} (similarity to overall history)\n"
#             f"   Compare: Is current focus aligned with recent trends (STM) or historical baseline (LTM)? "
#             f"Identify if this is a temporary fluctuation or genuine preference shift."
#         )
#
#     # Gate Score 的清晰描述
#     if gate_score == 0:
#         gate_explanation = "**Gate Score = 0**: Current focus matches NEITHER recent rounds NOR historical pattern (significant drift detected)."
#     else:
#         gate_explanation = f"**Gate Score = {gate_score:.2f}**: Indicates alignment with at least one memory layer (STM or LTM)."
#
#     return f"""You are a specialized agent for maintaining user preference profiles.
#
#   **Context Metrics**:
#   - **Current Round**: {round_num}
#   - {gate_explanation}
#   - **Similarity Scores**:
#     - **STM (Short-term)**: {stm_score:.2f} — How similar current focus is to the last 3 rounds
#     - **LTM (Long-term)**: {ltm_score:.2f} — How similar current focus is to overall historical pattern
#
#   **User's Original Update**:
#   {extracted_response}
#
#   **Task**:
#   Analyze the preference consistency/drift indicated by the similarity scores. Output the original update followed by a **highly concise** reflection.
#
#   **Reflection Constraints**:
#   {thought_guidance}
#   2. Distinguish "genuine preference shift" vs. "temporary exploration/noise".
#   3. **LENGTH LIMIT**: Your reflection MUST be shorter than the user's original update. Keep it under 2-3 sentences max.
#
#   **Output Format**:
#   My updated self-introduction:
#   {extracted_response}
#
#   [Reflective Thoughts]:
#   (Concise analysis based on STM/LTM similarity scores. Must be shorter than the introduction above.)
#   - **Similarity Scores**:
#     - **STM (Short-term)**: {stm_score:.2f} — How similar current focus is to the last 3 rounds
#     - **LTM (Long-term)**: {ltm_score:.2f} — How similar current focus is to overall historical pattern
#
#   **User's Original Update**:
#   {extracted_response}
#
#   **Task**:
#   Analyze the preference consistency/drift indicated by the similarity scores. Output the original update followed by a **highly concise** reflection.
#
#   **Reflection Constraints**:
#   {thought_guidance}
#   2. Distinguish "genuine preference shift" vs. "temporary exploration/noise".
#   3. **LENGTH LIMIT**: Your reflection MUST be shorter than the user's original update. Keep it under 2-3 sentences max.
#
#   **Output Format**:
#   My updated self-introduction:
#   {extracted_response}
#
#   [Reflective Thoughts]:
#   (Concise analysis based on STM/LTM similarity scores. Must be shorter than the introduction above.)
#   """


# def adjusted_memory_prompt(extracted_response, gate_score, stm_score, ltm_score, round_num):
#     """
#     生成带有属性重叠与极性分析思考的 Prompt，并严格限制反思长度。
#     """
#
#     # 动态生成思考逻辑引导
#     if round_num < 4 :
#         thought_guidance = (
#             f"1. **Short-term Pattern**: STM Score = {stm_score:.2f} "
#             f"(Higher = more similar to last 3 rounds; Lower = shifting focus). "
#             f"Briefly explain what this similarity/difference reveals."
#         )
#     else:
#         thought_guidance = (
#             f"1. **Consistency Analysis**: \n"
#             f"   - STM Score = {stm_score:.2f} (similarity to last 3 rounds)\n"
#             f"   - LTM Score = {ltm_score:.2f} (similarity to overall history)\n"
#             f"   Compare: Is current focus aligned with recent trends (STM) or historical baseline (LTM)? "
#             f"Identify if this is a temporary fluctuation or genuine preference shift."
#         )
#
#     # Gate Score 的清晰描述
#     if gate_score == 0:
#         gate_explanation = "**Gate Score = 0**: Current focus matches NEITHER recent rounds NOR historical pattern (significant drift detected)."
#     else:
#         gate_explanation = f"**Gate Score = {gate_score:.2f}**: Indicates alignment with at least one memory layer (STM or LTM)."
#
#     # 根据 round_num 决定是否分析 LTM
#     if round_num < 4:
#         ltm_analysis_note = "Note: Only analyze short-term memory (STM) since round_num < 4. Do NOT analyze long-term memory (LTM) at this stage."
#     else:
#         ltm_analysis_note = "Note: Analyze both short-term memory (STM) and long-term memory (LTM) since round_num >= 4."
#
#     return f"""You are a specialized agent for maintaining user preference profiles.
#
#   **Context Metrics**:
#   - **Current Round**: {round_num}
#   - {gate_explanation}
#   - **Similarity Scores**:
#     - **STM (Short-term)**: {stm_score:.2f} — How similar current focus is to the last 3 rounds
#     - **LTM (Long-term)**: {ltm_score:.2f} — How similar current focus is to overall historical pattern
#
#   **User's Original Update**:
#   {extracted_response}
#
#   **Task**:
#   Analyze the preference consistency/drift indicated by the similarity scores. Output the original update followed by a **highly concise** reflection.
#
#   **Reflection Constraints**:
#   {thought_guidance}
#   2. Distinguish "genuine preference shift" vs. "temporary exploration/noise".
#   3. **LENGTH LIMIT**: Your reflection MUST be shorter than the user's original update. Keep it under 2-3 sentences max.
#
#   **Output Format**:
#   My updated self-introduction:
#   {extracted_response}
#
#   [Reflective Thoughts]:
#   {ltm_analysis_note}
#   (Concise analysis based on STM/LTM similarity scores. Must be shorter than the introduction above.)
#   """
# def adjusted_memory_prompt(extracted_response, gate_score, stm_score, ltm_score, round_num):
#     """
#     门控未通过时，让 LLM 在保留原始更新的基础上追加一段简短反思。
#
#     设计要点：
#     - 不向 LLM 暴露 threshold（动态、内部）。
#     - Round < 4 时只提 STM（LTM 尚未启用），避免「LTM=0」的误导。
#     - 分数附自然语言解释，LLM 不需要猜测数值含义。
#     - 反思长度用硬性句数上限约束。
#     """
#
#     # ===== 1. 分数语义化标签 =====
#     def _label(score):
#         if score >= 0.5:
#             return "strongly aligned"
#         if score >= 0.2:
#             return "partially aligned"
#         if score > 0.0:
#             return "weakly aligned"
#         return "misaligned"
#
#     stm_label = _label(stm_score)
#
#     # ===== 2. 早期 vs 后期：是否引入 LTM =====
#     if round_num < 4:
#         memory_context = (
#             f"- **Recent rounds (STM)**: alignment = {stm_score:.2f} ({stm_label} "
#             f"with the user's focus in the previous 2 rounds).\n"
#             f"- Long-term memory is not yet active at this stage (round < 4); "
#             f"focus your reflection on short-term consistency only."
#         )
#         reflection_guidance = (
#             "Reflect on whether the current update continues the user's recent focus, "
#             "or represents an abrupt shift in attention. If the focus has changed, decide "
#             "whether it looks like a tentative exploration or a meaningful refinement of "
#             "what the user truly cares about."
#         )
#     else:
#         ltm_label = _label(ltm_score)
#         memory_context = (
#             f"- **Recent rounds (STM)**: alignment = {stm_score:.2f} ({stm_label} "
#             f"with the user's focus in the previous 2 rounds).\n"
#             f"- **Historical pattern (LTM)**: alignment = {ltm_score:.2f} ({ltm_label} "
#             f"with the user's long-term core interests)."
#         )
#         reflection_guidance = (
#             "Compare STM vs. LTM: "
#             "(a) both low → the user's attention has drifted away from both recent and long-term interests; "
#             "(b) STM low but LTM moderate/high → short-term exploration that still respects core long-term interests; "
#             "(c) STM moderate/high but LTM low → recent trend diverging from the user's established core interests. "
#             "Identify which case applies and whether it represents genuine preference evolution or transient noise."
#         )
#
#     # ===== 3. 不提 threshold，只交代「为什么要反思」=====
#     framing = (
#         "This update did not pass the stability check, so before committing it we want a brief "
#         "self-reflection that flags whether the change is a stable refinement or a noisy fluctuation. "
#         "You are NOT being asked to rewrite the introduction — just to add a short reflective note after it."
#     )
#
#     return f"""You are a specialized agent for maintaining user preference profiles.
#
# **Context**:
# - Current Round: {round_num}
# {memory_context}
#
# **User's Original Update** (to be preserved verbatim):
# {extracted_response}
#
# **Task**:
# {framing}
#
# **Reflection Guidance**:
# {reflection_guidance}
#
# **Hard Constraints**:
# 1. Reproduce the original update verbatim under `My updated self-introduction:`. Do NOT edit it.
# 2. The `[Reflective Thoughts]` block must be **at most 2 sentences** and **strictly shorter** than the original update.
# 3. Do not invent new preferences or attributes in the reflection; only comment on stability.
# 4. Do not mention internal scores numerically in your reflection — refer to them qualitatively (e.g., "weakly aligned with recent focus").
#
# **Output Format**:
# My updated self-introduction:
# {extracted_response}
#
# [Reflective Thoughts]:
# (Your 1–2 sentence qualitative reflection here.)
# """
def adjusted_memory_prompt(extracted_response, gate_score, stm_score, ltm_score, round_num):
    """
    门控未通过时，让 LLM 在保留原始更新的基础上追加一段简短反思。

    设计要点：
    - 不向 LLM 暴露 threshold（动态、内部）。
    - Round < 4 时只提 STM（LTM 尚未启用），避免「LTM=0」的误导。
    - 分数附自然语言解释，LLM 不需要猜测数值含义。
    - 反思长度用硬性句数上限约束。
    """

    # ===== 1. 分数语义化标签 =====
    def _label(score):
        if score >= 0.5:
            return "strongly aligned"
        if score >= 0.2:
            return "partially aligned"
        if score > 0.0:
            return "weakly aligned"
        return "misaligned"

    stm_label = _label(stm_score)

    # ===== 2. 早期 vs 后期：是否引入 LTM =====
    if round_num < 4:
        memory_context = (
            f"- **Recent rounds (STM)**: alignment = {stm_score:.2f} ({stm_label} "
            f"with the user's focus in the previous 2 rounds).\n"
            f"- Long-term memory is not yet active at this stage (round < 4); "
            f"focus your reflection on short-term consistency only."
        )
        reflection_guidance = (
            "Reflect on whether the current update continues the user's recent focus, "
            "or represents an abrupt shift in attention. If the focus has changed, decide "
            "whether it looks like a tentative exploration or a meaningful refinement of "
            "what the user truly cares about."
        )
    else:
        ltm_label = _label(ltm_score)
        memory_context = (
            f"- **Recent rounds (STM)**: alignment = {stm_score:.2f} ({stm_label} "
            f"with the user's focus in the previous 2 rounds).\n"
            f"- **Historical pattern (LTM)**: alignment = {ltm_score:.2f} ({ltm_label} "
            f"with the user's long-term core interests)."
        )
        reflection_guidance = (
            "Compare STM vs. LTM: "
            "(a) both low → the user's attention has drifted away from both recent and long-term interests; "
            "(b) STM low but LTM moderate/high → short-term exploration that still respects core long-term interests; "
            "(c) STM moderate/high but LTM low → recent trend diverging from the user's established core interests. "
            "Identify which case applies and whether it represents genuine preference evolution or transient noise."
        )

    # ===== 3. 不提 threshold，只交代「为什么要反思」=====
    framing = (
        "This update did not pass the stability check, so before committing it we want a brief "
        "self-reflection that flags whether the change is a stable refinement or a noisy fluctuation. "
        "You are NOT being asked to rewrite the introduction — just to add a short reflective note after it."
    )

    return f"""You are a specialized agent for maintaining user preference profiles.

**Context**:
- Current Round: {round_num}
{memory_context}

**User's Original Update** (to be preserved verbatim):
{extracted_response}

**Task**:
{framing}

**Reflection Guidance**:
{reflection_guidance}

**Hard Constraints**:
1. Reproduce the original update verbatim under `My updated self-introduction:`. Do NOT edit it.
2. The `[Reflective Thoughts]` block must be **at most 2 sentences** and **strictly shorter** than the original update.
3. Do not invent new preferences or attributes in the reflection; only comment on stability.
4. Do not mention internal scores numerically in your reflection — refer to them qualitatively (e.g., "weakly aligned with recent focus").

**Output Format**:
My updated self-introduction:
{extracted_response}

[Reflective Thoughts]:
(Your 1–2 sentence qualitative reflection here.)
"""
