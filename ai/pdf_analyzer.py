import os
import io
from PIL import Image
from pdf2image import convert_from_path
from openai import OpenAI

client = OpenAI()

def analyze_pdf_and_generate_latex(pdf_path: str) -> str:
    """
    PDFファイルを解析し、その内容からLaTeXコードを生成する。
    各ページを画像に変換し、OpenAIのVisionモデルを使用してLaTeXコードを生成する。
    """
    latex_code_parts = []

    try:
        # PDFの各ページを画像に変換
        images = convert_from_path(pdf_path)

        for i, image in enumerate(images):
            print(f"Analyzing page {i+1} of {len(images)}...")
            # 画像をバイトストリームに保存
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = buffered.getvalue()

            # OpenAI Visionモデルに画像を送信し、LaTeXコードを生成
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "以下の画像は高校数学の教材の1ページです。このページの内容を再現するLaTeXコードを生成してください。数式はLaTeXの数式モードで記述し、図形はTikZで記述してください。日本語はUTF-8で記述してください。完全なLaTeXドキュメントではなく、このページの内容を表す部分的なコード（\\section, \\subsection, \\begin{problem}, \\begin{solution} など）のみを生成してください。"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img_str.hex()}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=4000,
            )
            latex_code_parts.append(response.choices[0].message.content)

    except Exception as e:
        print(f"Error during PDF analysis or LaTeX generation: {e}")
        return f"Error: {e}"

    # 各ページのLaTeXコードを結合して返す
    return "\n\n".join(latex_code_parts)

if __name__ == '__main__':
    # テスト用のPDFファイルパスを指定
    # 実際のPDFファイルに置き換えてテストしてください
    test_pdf_path = "./test_input.pdf"
    if os.path.exists(test_pdf_path):
        print(f"Analyzing {test_pdf_path}...")
        generated_latex = analyze_pdf_and_generate_latex(test_pdf_path)
        print("\n--- Generated LaTeX ---\n")
        print(generated_latex)
        # 生成されたLaTeXコードをファイルに保存
        with open("./generated_from_pdf.tex", "w", encoding="utf-8") as f:
            f.write(generated_latex)
        print("Generated LaTeX saved to generated_from_pdf.tex")
    else:
        print(f"Test PDF file not found at {test_pdf_path}. Please create one to test.")
