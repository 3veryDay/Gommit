import subprocess
import openai
import os
import argparse
from dotenv import load_dotenv

# 1. .env 파일에서 API 키 불러오기
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 2. git diff (스테이징된 변경사항)
def get_staged_diff():
    result = subprocess.run(
        ["git", "diff", "--cached"],
        capture_output=True,
        text=True,
        encoding='utf-8'  # ← 여기가 핵심!!
    )
    return result.stdout.strip()

# 3. 커밋 메시지 스타일 적용
def apply_style(message, style):
    if style == "conventional":
        if "추가" in message or "기능" in message or "add" in message:
            prefix = "feat: "
        elif "수정" in message or "버그" in message or "fix" in message:
            prefix = "fix: "
        else:
            prefix = "chore: "
        return prefix + message
    return message

# 4. GPT로 커밋 메시지 생성
def generate_commit_message(diff, lang="ko"):
    prompt = f"""다음 git diff 내용을 기반으로 한 줄짜리 커밋 메시지를 만들어줘.
너무 길지 않게 핵심만 담고, { '한국어' if lang == 'ko' else '영어' }로 작성해줘:

{diff}

커밋 메시지:"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

# 5. 실제 git commit 실행
def run_commit(message):
    subprocess.run(["git", "commit", "-m", message], encoding='utf-8')

# 6. 메인 실행 함수
def main():
    parser = argparse.ArgumentParser(description="Gommit: GPT 기반 커밋 메시지 생성기")
    parser.add_argument("--lang", choices=["ko", "en"], default="ko", help="커밋 메시지 언어")
    parser.add_argument("--style", choices=["conventional"], help="커밋 스타일 적용 (예: conventional)")
    args = parser.parse_args()

    print(" Git 변경사항을 확인하는 중...")
    diff = get_staged_diff()

    if not diff:
        print("스테이징된 변경사항이 없습니다. 먼저 'git add'를 해주세요.")
        return

    print(" GPT가 커밋 메시지를 생성하는 중...")
    commit_message = generate_commit_message(diff, lang=args.lang)

    if args.style:
        commit_message = apply_style(commit_message, args.style)

    print(f"\생성된 메시지:\n\"{commit_message}\"\n")

    confirm = input("이 메시지로 커밋할까요? (y/n): ").strip().lower()
    if confirm == "y":
        run_commit(commit_message)
        print("커밋 완료! 커밋문 : ", commit_message)
    else:
        print("커밋이 취소되었습니다.")

if __name__ == "__main__":
    main()
