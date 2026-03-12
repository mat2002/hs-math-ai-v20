from database.exam_profiles import get_exam_profile

def build_exam_reproduction_prompt(exam_name, topic):
    """
    特定の大学の入試問題を再現するための専用プロンプトを構築する。
    """
    profile = get_exam_profile(exam_name)
    if not profile:
        return f"{topic}に関する標準的な問題を作成してください。"
    
    prompt = f"""
あなたは大学入試数学の専門家です。以下の大学の出題傾向、難易度、記述スタイルを完全に模倣して、{topic}に関する新しい問題を作成してください。

【ターゲット大学: {exam_name}】
- 難易度: {profile['difficulty']} / 5
- 出題形式: {profile['style']}
- 特徴: {profile['characteristics']}
- 頻出分野: {', '.join(profile['frequent_topics'])}

【指示】
1. {exam_name}の過去問でよく見られるような、独特の言い回しや問題の切り口を再現してください。
2. 難易度は{profile['difficulty']}に厳密に合わせてください。
3. 解説は、その大学の受験生が求める論理的レベル（厳密さや計算の工夫）に合わせて記述してください。
4. 図解が必要な場合は、TikZで描画可能な情報を `needs_figure: true` として含めてください。

出力は以前と同様のYAML形式で行ってください。
"""
    return prompt
