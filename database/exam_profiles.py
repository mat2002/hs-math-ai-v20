# 大学別入試傾向マスタ
# 各大学の出題スタイル、難易度、頻出分野を定義

EXAM_PROFILES = {
    "共通テスト": {
        "difficulty": 3,
        "style": "誘導形式・穴埋め",
        "characteristics": "太郎さんと花子さんの会話、日常生活の数学的モデル化、計算量よりも論理の飛躍を埋める能力を重視。",
        "frequent_topics": ["データの分析", "場合の数と確率", "図形と計量", "2次関数"],
        "latex_style": "box_fill"
    },
    "東京大学": {
        "difficulty": 5,
        "style": "記述式・発想力重視",
        "characteristics": "高い思考力と論理的厳密さを要求。計算自体はシンプルだが、問題の核心を突く発想が必要。図形問題や整数問題が頻出。",
        "frequent_topics": ["整数", "複素数平面", "空間図形", "積分法の応用"],
        "latex_style": "standard_descriptive"
    },
    "京都大学": {
        "difficulty": 5,
        "style": "記述式・論証重視",
        "characteristics": "問題文が非常に短く、自ら条件を整理して論証を組み立てる力が必要。誘導が少なく、白紙から解き進める力が試される。",
        "frequent_topics": ["確率の漸化式", "整数", "三角関数", "微分・積分"],
        "latex_style": "minimalist_descriptive"
    },
    "早稲田大学（理工）": {
        "difficulty": 4,
        "style": "記述・計算量重視",
        "characteristics": "高い計算能力と処理速度を要求。数IIIの微積分が中心で、複雑な計算を正確にこなす必要がある。",
        "frequent_topics": ["微分法", "積分法", "複素数平面", "極限"],
        "latex_style": "heavy_calculation"
    },
    "慶應義塾大学（理工）": {
        "difficulty": 4,
        "style": "穴埋め・記述併用",
        "characteristics": "典型的な解法を組み合わせた応用問題が多い。計算の工夫が必要な問題が目立つ。",
        "frequent_topics": ["確率", "ベクトル", "数列", "微分・積分"],
        "latex_style": "mixed_format"
    }
}

def get_exam_profile(exam_name):
    return EXAM_PROFILES.get(exam_name)

def get_all_exam_names():
    return list(EXAM_PROFILES.keys())
