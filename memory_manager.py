import re
import json
import os

from config import MEMORY_BASE_DIR
import time as time_module

# STM 存储路径
STM_DIR = f"{MEMORY_BASE_DIR}/stm"
os.makedirs(STM_DIR, exist_ok=True)


def parse_attribute_rationale(response_text):
    """
    使用正则从 LLM 输出中提取属性字典
    兼容格式（方括号可有可无）：
        - [attribute]: [item_name] | positive | 5
        - attribute: item_name | positive | 5
        - [attribute]: item_name with, commas | negative | 3
    返回: {dimension: {item_name, polarity, score}}
    """
    attributes = {}
    pattern = (
        r"-\s*"
        r"\[?\s*([^\[\]\:\n]+?)\s*\]?\s*:\s*"
        r"\[?\s*(.+?)\s*\]?\s*"
        r"\|\s*(positive|negative)\s*"
        r"\|\s*(\d+)"
    )
    matches = re.findall(pattern, response_text, flags=re.IGNORECASE)

    for match in matches:
        attr_dim = match[0].strip().lower().replace(" ", "_")
        item_name = match[1].strip().strip("[]").strip()
        polarity = match[2].strip().lower()
        try:
            score = int(match[3].strip())
        except ValueError:
            continue

        attributes[attr_dim] = {
            "item_name": item_name,
            "polarity": polarity,
            "score": score
        }
    return attributes


# def process_stm_and_check_ltm(userId, extracted_attrs, new_self_intro):
#     """
#     记录属性历史并判断是否固化到LTM
#     """
#     from config import MEMORY_BASE_DIR
#     import time as time_module
#     import json
#     import os
#
#     # 1. 加载STM
#     stm_file = f"{MEMORY_BASE_DIR}/stm/user_{userId}.json"
#     os.makedirs(os.path.dirname(stm_file), exist_ok=True)
#
#     if os.path.exists(stm_file):
#         with open(stm_file, 'r', encoding='utf-8') as f:
#             stm = json.load(f)
#     else:
#         stm = {"attributes": {}, "history": []}
#
#     # 2. 记录本次交互到history（关键：保留每轮的属性快照）
#     stm["history"].append({
#         "timestamp": time_module.time(),
#         "round": len(stm["history"]),
#         "extracted_attrs": extracted_attrs  # 完整的属性字典
#     })
#
#     # 3. 更新STM维度积分
#     for dim, detail in extracted_attrs.items():
#         if detail.get("polarity") == "positive":
#             if dim not in stm["attributes"]:
#                 stm["attributes"][dim] = {
#                     "count": 0,
#                     "total_score": 0,
#                     "evidence_items": []
#                 }
#
#             stm["attributes"][dim]["count"] += 1
#             stm["attributes"][dim]["total_score"] += detail.get("score", 0)
#             stm["attributes"][dim]["evidence_items"].append(detail.get("item_name"))
#
#     # 4. 固化判断（属性出现3次以上固化到LTM）
#     LTM_THRESHOLD = 2
#     verified_dims = [dim for dim, data in stm["attributes"].items()
#                      if data["count"] >= LTM_THRESHOLD]
#
#     if verified_dims:
#         # 固化到LTM
#         update_user_memory_from_ltm(userId, new_self_intro)
#
#         # 重置计数
#         for dim in verified_dims:
#             stm["attributes"][dim]["count"] = 0
#             stm["attributes"][dim]["evidence_items"] = []
#
#         decision_tag = "UPDATED_TO_LTM"
#     else:
#         decision_tag = "KEEP_IN_STM"
#
#     # 5. 持久化STM
#     with open(stm_file, 'w', encoding='utf-8') as f:
#         json.dump(stm, f, ensure_ascii=False, indent=2)
#
#     return decision_tag


# ============= P0: Confidence Parsing =============
def parse_confidence(user_response):
    """
    从LLM输出中提取confidence score (1-5)，归一化到[0, 1]。
    格式: [Confidence Assessment] ... (1-5): <score> ... Justification: <text>
    """
    # primary pattern: score on same line or next line before Justification
    pattern = r'\[Confidence Assessment\].*?(?:Rate[^\d]*)?(\d)\s*\n?\s*Justification:\s*(.+?)(?=\n\n|\n\[|\n*$)'
    match = re.search(pattern, user_response, re.DOTALL | re.IGNORECASE)
    if match:
        score = int(match.group(1))
        return {"confidence": max(0.0, min(1.0, score / 5.0)), "justification": match.group(2).strip()}
    # fallback: find any digit after [Confidence Assessment]
    pattern2 = r'\[Confidence Assessment\].*?(\d)'
    match2 = re.search(pattern2, user_response, re.DOTALL | re.IGNORECASE)
    if match2:
        return {"confidence": max(0.0, min(1.0, int(match2.group(1)) / 5.0)), "justification": "PARSE_PARTIAL"}
    return {"confidence": 0.5, "justification": "PARSE_FAILURE"}


def strip_confidence_section(user_response):
    """Remove [Confidence Assessment] block from text before saving as memory."""
    cleaned = re.sub(r'\n*\s*\[Confidence Assessment\].*', '', user_response, flags=re.DOTALL | re.IGNORECASE).strip()
    return cleaned if cleaned else user_response


def load_stm_attributes(userId, rounds=[2, 3]):
    """
    加载指定轮次的属性提取结果（用于prompt提示）

    参数:
    - userId: 用户ID
    - rounds: 要加载的轮次列表，默认[2, 3]表示Round 2和Round 3

    返回: 列表，包含这些轮次的属性
    """
    from config import MEMORY_BASE_DIR
    import os
    import json

    history_file = f"{MEMORY_BASE_DIR}/stm_history/user_{userId}.json"

    if not os.path.exists(history_file):
        return None

    # 加载History
    with open(history_file, 'r', encoding='utf-8') as f:
        history_data = json.load(f)

    stm_attributes = []

    for round_num in rounds:
        # 从history中找到对应轮次的属性
        for entry in history_data["history"]:
            if entry["round"] == round_num:
                stm_attributes.append({
                    "round": round_num + 1,  # 转换为1-based显示
                    "attributes": entry["extracted_attrs"]
                })
                break

    return stm_attributes if stm_attributes else None

def compute_stm_score_two_rounds(current_attrs, round_2_attrs, round_3_attrs):
    """
    计算短期记忆分数：当前轮与倒数第二轮和倒数第三轮的平均相似度

    参数:
    - current_attrs: 当前轮（Round 4）的属性
    - round_2_attrs: Round 2的属性
    - round_3_attrs: Round 3的属性

    返回: 0-1之间的分数
    """
    if not current_attrs:
        return 0.0

    # 计算与Round 3的相似度
    score_round_3 = compute_stm_score(current_attrs, round_3_attrs)

    # 计算与Round 2的相似度
    score_round_2 = compute_stm_score(current_attrs, round_2_attrs)

    # 加权平均（Round 3权重更高，因为更近）
    stm_score = 0.5 * score_round_3 + 0.5 * score_round_2

    return stm_score

def compute_stm_score(current_attrs, previous_attrs):
    """
    计算短期记忆分数：当前轮与前一轮的属性相关性

    参数:
    - current_attrs: 当前轮属性 {dim: {"polarity": ..., "score": ...}}
    - previous_attrs: 前一轮属性 {dim: {"polarity": ..., "score": ...}}

    返回: 0-1之间的分数
    """
    if not previous_attrs:
        # 第0轮，没有前一轮，返回中性分数
        return 0.5

    if not current_attrs:
        return 0.0

    current_dims = set(current_attrs.keys())
    prev_dims = set(previous_attrs.keys())
    overlap_dims = current_dims & prev_dims

    if len(current_dims) == 0:
        return 0.0

    # 1. 维度重叠率（权重0.5）
    overlap_ratio = len(overlap_dims) / len(current_dims)

    # 2. 极性一致性（权重0.5）
    if len(overlap_dims) > 0:
        polarity_match = sum(
            1 for dim in overlap_dims
            if current_attrs[dim]["polarity"] == previous_attrs[dim]["polarity"]
        ) # 所有属性中有多少个属性的正负性是一致的
        polarity_consistency = polarity_match / len(overlap_dims)
    else:
        polarity_consistency = 0.0

    # STM分数
    stm_score = 0.7 * overlap_ratio + 0.3 * polarity_consistency

    return stm_score

### 2.2 LTM分数计算（当前轮 vs 所有历史）
def compute_ltm_score(current_attrs, history_attrs_list):
    """
    计算长期记忆分数：当前轮与所有历史轮次的属性一致性

    参数:
    - current_attrs: 当前轮属性
    - history_attrs_list: 历史所有轮次的属性列表 [round0_attrs, round1_attrs, ...]

    返回: 0-1之间的分数
    """
    if not history_attrs_list:
        # 第0轮，没有历史，返回中性分数
        return 0.5

    if not current_attrs:
        return 0.0

    # 统计每个维度在历史中的出现情况
    dim_history = {}

    for hist_attrs in history_attrs_list:
        for dim, detail in hist_attrs.items():
            if dim not in dim_history:
                dim_history[dim] = {
                    "count": 0,
                    "polarity_list": []
                }
            dim_history[dim]["count"] += 1
            dim_history[dim]["polarity_list"].append(detail["polarity"])

    # 计算当前轮与历史的一致性
    current_dims = set(current_attrs.keys())
    hist_dims = set(dim_history.keys())
    overlap_dims = current_dims & hist_dims

    if len(current_dims) == 0:
        return 0.0

    # 1. 维度重叠率（权重0.4）
    overlap_ratio = len(overlap_dims) / len(current_dims)

    # 2. 极性一致性（权重0.6）
    # 对于重叠的维度，检查当前极性是否与历史主导极性一致
    if len(overlap_dims) > 0:
        polarity_match = 0
        for dim in overlap_dims:
            # 历史主导极性（出现最多的极性）
            polarity_counts = {}
            for p in dim_history[dim]["polarity_list"]:
                polarity_counts[p] = polarity_counts.get(p, 0) + 1
            dominant_polarity = max(polarity_counts, key=polarity_counts.get) # 主要是看每个属性的极性在历史轮数里面是正向多还是负向多

            # 当前极性是否匹配
            if current_attrs[dim]["polarity"] == dominant_polarity:
                polarity_match += 1

        polarity_consistency = polarity_match / len(overlap_dims)
    else:
        polarity_consistency = 0.0

    # LTM分数
    ltm_score = 0.7 * overlap_ratio + 0.3 * polarity_consistency

    return ltm_score

### 2.3 综合门控函数
def evaluate_memory_gate(userId, round_num, current_attrs, is_choice_right, confidence_score=None):
    """
    动态记忆门控评估

    参数:
    - userId: 用户ID
    - round_num: 当前轮次（0-based，0-4）
    - current_attrs: 当前轮提取的属性
    - is_choice_right: 是否选择正确
    - confidence_score: P0 LLM自评置信度 [0,1]，默认 0.5

    返回: {
        "gate_score": float,
        "should_update": bool,
        "stm_score": float,
        "ltm_score": float,
        "threshold": float,
        "confidence": float
    }
    """
    from config import MEMORY_BASE_DIR, ENABLE_CONFIDENCE_GATE
    import json
    import os

    if confidence_score is None:
        confidence_score = 0.5

    # 1. Round 0-1: 强制通过（无历史数据）
    if round_num < 2:
        return {
            "gate_score": 1.0,
            "should_update": True,
            "stm_score": 0.0,
            "ltm_score": 0.0,
            "threshold": 0.0,
            "weights": {"alpha": 0.0, "beta": 0.0},
            "round_num": round_num,
            "history_count": 0,
            "confidence": confidence_score
        }

    # 2. Round 2-3: 只使用STM分数（当前轮 vs 前两轮加权，与 Round 4 同口径）
    elif round_num in [2, 3]:
        # 加载History
        history_file = f"{MEMORY_BASE_DIR}/stm_history/user_{userId}.json"

        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            history = history_data.get("history", [])
        else:
            history = []

        # 提取前两轮的属性
        # near_attrs  = 最近一轮 (round_num - 1)，权重 0.6
        # far_attrs   = 次近一轮 (round_num - 2)，权重 0.4
        near_attrs = {}
        far_attrs = {}
        for entry in history:
            if entry["round"] == round_num - 1:
                near_attrs = entry.get("extracted_attrs", {}) or {}
            elif entry["round"] == round_num - 2:
                far_attrs = entry.get("extracted_attrs", {}) or {}

        # 与前两轮加权比较：compute_stm_score_two_rounds 内部
        # = 0.6 * compute_stm_score(current, round_3_attrs)
        # + 0.4 * compute_stm_score(current, round_2_attrs)
        # 所以把 near 传给 round_3_attrs、far 传给 round_2_attrs
        stm_score = compute_stm_score_two_rounds(
            current_attrs,
            round_2_attrs=far_attrs,
            round_3_attrs=near_attrs,
        )

        # gate_score: blend STM + confidence when enabled
        if ENABLE_CONFIDENCE_GATE:
            gate_score = 0.7 * stm_score + 0.3 * confidence_score
        else:
            gate_score = stm_score

        # 阈值
        threshold = 0.3 if is_choice_right else 0.4

        should_update = gate_score >= threshold

        return {
            "gate_score": gate_score,
            "should_update": should_update,
            "stm_score": stm_score,
            "ltm_score": 0.0,  # Round 2-3 不使用 LTM
            "threshold": threshold,
            "weights": {"alpha": 0.0, "beta": 1.0},  # 只用 STM
            "round_num": round_num,
            "history_count": len(history),
            "confidence": confidence_score
        }

    # 3. Round 4: 启用长短记忆门控（STM + LTM加权）
    elif round_num == 4:
        # 加载History（从stm_history而不是stm）
        history_file = f"{MEMORY_BASE_DIR}/stm_history/user_{userId}.json"

        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            history = history_data.get("history", [])
        else:
            history = []

        # 提取Round 2和Round 3的属性（短记忆）
        round_2_attrs = {}
        round_3_attrs = {}

        for entry in history:
            if entry["round"] == 2:
                round_2_attrs = entry.get("extracted_attrs", {})
            elif entry["round"] == 3:
                round_3_attrs = entry.get("extracted_attrs", {})

        # 提取Round 0-3的所有属性（长记忆）
        history_attrs_list = []
        for entry in history:
            if entry["round"] < 4:  # 只取Round 0-3
                history_attrs_list.append(entry.get("extracted_attrs", {}))

        # 计算STM分数（与Round 2和Round 3比较）
        stm_score = compute_stm_score_two_rounds(current_attrs, round_2_attrs, round_3_attrs)

        # 计算LTM分数（与Round 0-3比较）
        ltm_score = compute_ltm_score(current_attrs, history_attrs_list)

        # 综合门控分数（可选融入confidence）
        if ENABLE_CONFIDENCE_GATE:
            alpha, beta, gamma = 0.5, 0.2, 0.3  # LTM 50% + STM 20% + confidence 30%
            gate_score = alpha * ltm_score + beta * stm_score + gamma * confidence_score
        else:
            alpha, beta = 0.7, 0.3  # LTM权重更高
            gate_score = alpha * ltm_score + beta * stm_score

        # 阈值
        threshold = 0.4 if is_choice_right else 0.5

        should_update = gate_score >= threshold

        return {
            "gate_score": gate_score,
            "should_update": should_update,
            "stm_score": stm_score,
            "ltm_score": ltm_score,
            "threshold": threshold,
            "weights": {"alpha": alpha, "beta": beta},
            "round_num": round_num,
            "history_count": len(history),
            "confidence": confidence_score
        }

# def save_stm_and_history(userId, extracted_attrs, round_num):
#     """
#     保存当前轮次的STM和累积的History
#
#     参数:
#     - userId: 用户ID
#     - extracted_attrs: 当前轮次提取的属性
#     - round_num: 当前轮次（0-based）
#     """
#     from config import MEMORY_BASE_DIR
#     import json
#     import os
#     import time as time_module
#
#     # ========== 1. 保存STM（当前轮次，覆盖式）==========
#     stm_dir = f"{MEMORY_BASE_DIR}/stm"
#     os.makedirs(stm_dir, exist_ok=True)
#
#     stm_file = f"{stm_dir}/user_{userId}.json"
#     stm_data = {
#         "user_id": userId,
#         "current_round": round_num,
#         "timestamp": time_module.time(),
#         "extracted_attrs": extracted_attrs
#     }
#
#     with open(stm_file, 'w', encoding='utf-8') as f:
#         json.dump(stm_data, f, ensure_ascii=False, indent=2)
#
#     print(f"✅ [STM] User {userId} Round {round_num} saved")
#
#     # ========== 2. 追加到History（累积式）==========
#     history_dir = f"{MEMORY_BASE_DIR}/stm_history"
#     os.makedirs(history_dir, exist_ok=True)
#
#     history_file = f"{history_dir}/user_{userId}.json"
#
#     # 加载或初始化History
#     if os.path.exists(history_file):
#         with open(history_file, 'r', encoding='utf-8') as f:
#             history_data = json.load(f)
#     else:
#         history_data = {
#             "user_id": userId,
#             "history": []
#         }
#
#     # 追加当前轮次
#     history_data["history"].append({
#         "round": round_num,
#         "timestamp": time_module.time(),
#         "extracted_attrs": extracted_attrs
#     })
#
#     # 保存History
#     with open(history_file, 'w', encoding='utf-8') as f:
#         json.dump(history_data, f, ensure_ascii=False, indent=2)
#
#     print(f"✅ [History] User {userId} Round {round_num} appended to history")
def save_stm_and_history(userId, extracted_attrs, round_num, gate_score=None):
    from config import MEMORY_BASE_DIR
    import json, os
    import time as time_module

    if gate_score is None:
        gate_score = 1.0 if round_num == 0 else 0.9 if round_num == 1 else 0.0

    # STM（当前快照）
    stm_dir = f"{MEMORY_BASE_DIR}/stm"
    os.makedirs(stm_dir, exist_ok=True)
    with open(f"{stm_dir}/user_{userId}.json", 'w', encoding='utf-8') as f:
        json.dump({"user_id": str(userId), "current_round": round_num,
                   "timestamp": time_module.time(),
                   "gate_score": float(gate_score),
                   "extracted_attrs": extracted_attrs},
                  f, ensure_ascii=False, indent=2)

    # STM_history（累积）
    history_dir = f"{MEMORY_BASE_DIR}/stm_history"
    os.makedirs(history_dir, exist_ok=True)
    history_file = f"{history_dir}/user_{userId}.json"

    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"user_id": str(userId), "history": []}

    data["history"] = [h for h in data["history"] if h.get("round") != round_num]
    data["history"].append({
        "round": round_num,
        "timestamp": time_module.time(),
        "gate_score": float(gate_score),
        "extracted_attrs": extracted_attrs
    })
    data["history"].sort(key=lambda h: h["round"])

    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_ltm_from_history(userId, min_occurrences=2):
    """
    从History文件中提取稳定属性，生成LTM prompt

    参数:
    - userId: 用户ID
    - min_occurrences: 最小出现次数（默认2，即至少出现3次）

    返回: 格式化的属性字典，用于prompt构建
    """
    from config import MEMORY_BASE_DIR
    import json
    import os

    history_file = f"{MEMORY_BASE_DIR}/stm_history/user_{userId}.json"

    if not os.path.exists(history_file):
        return None

    # 加载History
    with open(history_file, 'r', encoding='utf-8') as f:
        history_data = json.load(f)

    # 统计每个维度的正向属性出现次数
    dimension_stats = {}

    for entry in history_data["history"]:
        for dim, detail in entry["extracted_attrs"].items():
            if detail.get("polarity") == "positive":
                if dim not in dimension_stats:
                    dimension_stats[dim] = {
                        "count": 0,
                        "total_score": 0,
                        "items": []
                    }

                dimension_stats[dim]["count"] += 1
                dimension_stats[dim]["total_score"] += detail.get("score", 0)
                dimension_stats[dim]["items"].append(detail.get("item_name"))

    # 筛选出现次数 > min_occurrences 的维度
    verified_dims = {
        dim: stats for dim, stats in dimension_stats.items()
        if stats["count"] >= min_occurrences  # > 2 表示至少3次
    }

    if not verified_dims:
        return None

    # 返回格式化的属性字典（用于prompt构建）
    ltm_attributes = {}
    for dim, stats in verified_dims.items():
        avg_score = stats["total_score"] / stats["count"]
        ltm_attributes[dim] = {
            "count": stats["count"],
            "avg_score": avg_score,
            "items": stats["items"]
        }

    return ltm_attributes

# ============================================================================
# 门控档案（gate_history）：归档每轮门控决策与 user_response 全文
# 用于「门控失败时回溯历史最高分」策略
# ============================================================================

# 早期轮次的先验门控分数（Round 0/1 没有真实门控分数，给硬编码先验）
_PRIOR_GATE_SCORES = {
    0: 1.0,   # 第一轮：原始 self-introduction 出发的干净起点
    1: 0.9,   # 第二轮：已经发生过一次更新，略低
}


def get_prior_gate_score(round_num):
    """Round 0/1 的先验门控分数；其它轮返回 None（应使用真实 gate_score）"""
    return _PRIOR_GATE_SCORES.get(round_num)


def save_gate_history(userId, round_num, gate_result, is_choice_right,
                      user_response, memory_snapshot, decision):
    """
    把本轮门控决策追加到 gate_history/user_{userId}.json

    参数:
    - userId: 用户ID
    - round_num: 0-based 轮次
    - gate_result: dict，至少含 gate_score / stm_score / ltm_score
                   （Round 0/1 调用方应直接传入先验分数）
    - is_choice_right: bool
    - user_response: 本轮 LLM 原始输出（保留 attribute rationale + my updated self-introduction）
    - memory_snapshot: 实际写入 user/user.{userId} 的纯文本
    - decision: "DIRECT" / "ADJUSTED" / "ROLLBACK_FROM_ROUND_X"
    """
    from config import MEMORY_BASE_DIR
    import json
    import os
    import time as _time

    gate_dir = f"{MEMORY_BASE_DIR}/gate_history"
    os.makedirs(gate_dir, exist_ok=True)
    gate_file = f"{gate_dir}/user_{userId}.json"

    if os.path.exists(gate_file):
        with open(gate_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"user_id": str(userId), "history": []}

    # 同轮次去重：断点续训重跑时覆盖旧条目
    data["history"] = [h for h in data["history"] if h.get("round") != round_num]

    data["history"].append({
        "round": round_num,
        "timestamp": _time.time(),
        "gate_score": float(gate_result.get("gate_score", 1.0)),
        "stm_score": float(gate_result.get("stm_score", 0.0)),
        "ltm_score": float(gate_result.get("ltm_score", 0.0)),
        "is_choice_right": bool(is_choice_right),
        "user_response": user_response or "",
        "memory_snapshot": memory_snapshot or "",
        "decision": decision or "UNKNOWN"
    })

    data["history"].sort(key=lambda h: h["round"])

    with open(gate_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"📝 [GateHistory] User {userId} Round {round_num} "
          f"decision={decision} score={gate_result.get('gate_score', 1.0):.3f}")


def find_best_attributes_from_history(userId, current_round):
    """
    从 stm_history 找 gate_score 最高的历史属性。
    Phase A: Round 2+ 最高分；Phase B: Round 0 兜底。
    """
    from config import MEMORY_BASE_DIR
    import json, os

    history_file = f"{MEMORY_BASE_DIR}/stm_history/user_{userId}.json"
    if not os.path.exists(history_file):
        return None

    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f).get("history", [])
    except (OSError, json.JSONDecodeError):
        return None

    # Phase A: Round 2+ 中最高分
    candidates = [
        h for h in history
        if h.get("round", -1) >= 2
        and h.get("round", -1) < current_round
        and h.get("extracted_attrs")
    ]
    if candidates:
        candidates.sort(key=lambda h: (-h.get("gate_score", 0), -h.get("round", 0)))
        best = candidates[0]
        return {"round": best["round"], "gate_score": best["gate_score"],
                "extracted_attrs": best["extracted_attrs"], "phase": "A"}

    # Phase B: Round 0 兜底
    round_0 = next((h for h in history if h.get("round") == 0 and h.get("extracted_attrs")), None)
    if round_0:
        return {"round": 0, "gate_score": round_0.get("gate_score", 1.0),
                "extracted_attrs": round_0["extracted_attrs"], "phase": "B"}

    return None


def build_user_anchor(userId, anchor_rounds=(0, 1)):
    """
    从 stm_history 中读取 Round 0/1 的属性，按 dimension 聚合得到锚点极性。

    参数:
    - userId: 用户ID
    - anchor_rounds: 用作锚点的轮次（默认 Round 0 和 Round 1）

    返回: {dim: dominant_polarity}
        dim 为 lower_case_with_underscore 字符串（与 parse_attribute_rationale 一致）
        当某维度在 anchor_rounds 内 positive/negative 计数相等时不纳入锚点。
    """
    from config import MEMORY_BASE_DIR
    import json
    import os

    history_file = f"{MEMORY_BASE_DIR}/stm_history/user_{userId}.json"
    if not os.path.exists(history_file):
        return {}

    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f).get("history", [])
    except (OSError, json.JSONDecodeError):
        return {}

    # {dim: {"positive": n, "negative": m}}
    anchor_buckets = {}
    anchor_round_set = set(anchor_rounds)
    for entry in history:
        if entry.get("round") not in anchor_round_set:
            continue
        for dim, attr in (entry.get("extracted_attrs") or {}).items():
            polarity = attr.get("polarity")
            if polarity not in ("positive", "negative"):
                continue
            bucket = anchor_buckets.setdefault(dim, {"positive": 0, "negative": 0})
            bucket[polarity] += 1

    anchor = {}
    for dim, b in anchor_buckets.items():
        if b["positive"] == b["negative"]:
            continue  # 不确定的维度不纳入锚点
        anchor[dim] = "positive" if b["positive"] > b["negative"] else "negative"
    return anchor


def check_anchor_violation(current_attrs, anchor):
    """
    检查 current_attrs 是否与锚点存在硬冲突（极性反转）。

    参数:
    - current_attrs: 当前轮提取的属性 {dim: {"polarity": ...}}
    - anchor: build_user_anchor 返回的 {dim: polarity}

    返回: (violation_count, violating_dims)
    """
    if not anchor or not current_attrs:
        return 0, []
    violating = []
    for dim, attr in current_attrs.items():
        if dim in anchor and attr.get("polarity") != anchor[dim]:
            violating.append(dim)
    return len(violating), violating


# ============= P1: 两阶段非对称门控 =============

def evaluate_asymmetric_gate(userId, round_num, current_attrs, is_choice_right,
                              confidence_score=None):
    """
    两阶段非对称门控

    Stage 1 — 新属性准入（低门槛）：
        历史未出现过的属性维度，is_choice_right=True 直接放行，
        is_choice_right=False 降权但不封杀。

    Stage 2 — 已有属性修正（高门槛）：
        已有维度的极性翻转需要 is_choice_right=True 作为证据，
        无证据翻转 → 硬拒绝（分数归零）。

    探索/利用权重随轮次动态调整：早期鼓励探索，后期趋于保守。

    返回: {gate_score, should_update, stm_score, ltm_score, threshold, ...}
    """
    from config import MEMORY_BASE_DIR, ENABLE_CONFIDENCE_GATE
    import json, os

    if confidence_score is None:
        confidence_score = 0.5

    # Round 0-1: 无条件通过
    if round_num < 2:
        return {
            "gate_score": 1.0,
            "should_update": True,
            "stm_score": 0.0,
            "ltm_score": 0.0,
            "threshold": 0.0,
            "round_num": round_num,
            "history_count": 0,
            "new_dims": [],
            "flip_violations": [],
            "confidence": confidence_score,
        }

    # 加载历史属性
    history_file = f"{MEMORY_BASE_DIR}/stm_history/user_{userId}.json"
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            history_data = json.load(f)
        history = history_data.get("history", [])
    else:
        history = []

    # 收集所有历史维度及其主导极性
    history_all_dims = {}
    for entry in history:
        if entry["round"] >= round_num:
            continue
        for dim, detail in (entry.get("extracted_attrs") or {}).items():
            if dim not in history_all_dims:
                history_all_dims[dim] = {"positive": 0, "negative": 0}
            pol = detail.get("polarity")
            if pol in ("positive", "negative"):
                history_all_dims[dim][pol] += 1

    current_dim_set = set(current_attrs.keys())
    history_dim_set = set(history_all_dims.keys())
    new_dims = current_dim_set - history_dim_set
    existing_dims = current_dim_set & history_dim_set

    # ===== Stage 1: 新属性准入 =====
    new_attrs_score = 1.0
    if new_dims:
        if is_choice_right:
            new_attrs_score = 0.9  # 选择正确的新属性：高置信度
        else:
            new_attrs_score = 0.5  # 选择错误时的新属性：可能是噪声，降权

    # ===== Stage 2: 已有属性翻转检查 =====
    flip_violations = []
    existing_attrs_score = 1.0

    for dim in existing_dims:
        pol = current_attrs[dim].get("polarity")
        if pol not in ("positive", "negative"):
            continue
        hist_counts = history_all_dims.get(dim, {"positive": 0, "negative": 0})
        dominant_pol = "positive" if hist_counts["positive"] >= hist_counts["negative"] else "negative"

        if pol != dominant_pol:
            flip_violations.append(dim)

    if flip_violations:
        if is_choice_right:
            # 有正确选择作为证据：允许翻转，但降分
            existing_attrs_score = 0.5
        else:
            # 无证据翻转：硬拒绝
            existing_attrs_score = 0.0

    # ===== 综合分数 =====
    # 探索/利用权重 — 随轮次从 0.5→0.1
    import math
    exploration_weight = 0.5 * math.exp(-0.3 * (round_num - 2))
    exploitation_weight = 1.0 - exploration_weight

    attr_score = (
        exploration_weight * new_attrs_score * (len(new_dims) / max(1, len(new_dims)))
        + exploitation_weight * existing_attrs_score * (len(existing_dims) / max(1, len(current_dim_set)))
    ) if current_dim_set else 0.5

    # 如果有新维度但没有现有维度，提高属性分数
    if existing_dims and not new_dims:
        attr_score = existing_attrs_score
    elif new_dims and not existing_dims:
        attr_score = new_attrs_score

    # 融合置信度
    if ENABLE_CONFIDENCE_GATE:
        gate_score = 0.4 * attr_score + 0.3 * confidence_score + 0.3 * (1 if is_choice_right else 0.5)
    else:
        gate_score = 0.6 * attr_score + 0.4 * (1 if is_choice_right else 0.5)

    # 无证据 flip 硬上限：极性翻转但没选对 → 最多 FUSION 级别
    if flip_violations and not is_choice_right:
        gate_score = min(gate_score, 0.35)

    # 自适应阈值
    if round_num <= 2:
        threshold = 0.30  # 早期宽松
    elif round_num <= 3:
        threshold = 0.35  # 中期
    else:
        threshold = 0.40  # 后期收紧

    should_update = gate_score >= threshold

    return {
        "gate_score": gate_score,
        "should_update": should_update,
        "stm_score": attr_score,
        "ltm_score": 0.0,
        "threshold": threshold,
        "round_num": round_num,
        "history_count": len(history),
        "new_dims": list(new_dims),
        "flip_violations": flip_violations,
        "exploration_weight": exploration_weight,
        "confidence": confidence_score,
    }


# ============= P3: 软着陆融合 =============

def soft_fusion_memory(existing_memory, proposed_memory, gate_score):
    """
    三段式记忆更新决策

    gate_score >= 0.5  → DIRECT:  完全接受新记忆
    0.3 <= score < 0.5 → FUSION:  将新信息追加到旧记忆末尾
    gate_score < 0.3   → REJECT:  保持旧记忆不变

    返回: (decision, final_memory)
        decision ∈ {"DIRECT", "FUSION", "REJECT"}
    """
    if not proposed_memory:
        return "REJECT", existing_memory

    if gate_score >= 0.5:
        return "DIRECT", proposed_memory

    if gate_score >= 0.3:
        # FUSION: 提取 proposed 中新增的具体物品/偏好描述
        # 通过简单的句号/分号分割，尝试提取新信息
        existing_set = set(existing_memory.lower().split())
        proposed_sentences = [s.strip() for s in proposed_memory.replace('. ', '.\n').split('\n') if s.strip()]

        new_info = []
        for sent in proposed_sentences:
            sent_words = set(sent.lower().split())
            overlap = len(sent_words & existing_set) / max(1, len(sent_words))
            if overlap < 0.6:  # 与现有记忆重叠低于60%视为新信息
                new_info.append(sent)

        if new_info:
            fusion_text = existing_memory.rstrip() + " Additionally, " + " ".join(new_info)
            return "FUSION", fusion_text
        else:
            return "FUSION", existing_memory  # 无实质性新信息，保留旧记忆

    return "REJECT", existing_memory
