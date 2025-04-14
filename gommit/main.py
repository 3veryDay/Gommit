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


# 3. generate commit message
def generate_commit_message(diff, lang="ko"):
    prompt = f"""다음은 git diff 결과야. 이 내용을 기반으로 한 줄짜리 커밋 메시지를 생성해줘.

- 반드시 [Conventional Commits 1.0.0] 규격을 따르도록 해줘.
- 기본 구조는 다음과 같아:
  <type>[optional scope]: <description>

- type은 다음 중 하나를 선택해서 사용해:
  - feat: 새로운 기능 추가
  - fix: 버그 수정
  - docs: 문서 변경
  - style: 코드 포맷팅, 세미콜론 누락 등 기능에 영향 없는 변경
  - refactor: 코드 리팩토링 (기능 변경 없이 구조 개선)
  - test: 테스트 추가 또는 수정
  - chore: 빌드 업무, 패키지 매니저 설정 등 기타 변경
  - perf: 성능 향상
  - ci: CI 관련 설정 수정
  - build: 빌드 관련 파일 수정

- scope는 선택사항이지만, 변경된 코드 영역(예: login, parser 등)이 명확하다면 소괄호로 표시해줘. 예: `feat(login): ...`
- description은 **50자 이내**로 핵심 요약만 담아줘.
- 만약 API 구조 변경이나 파괴적 변경이 있다면 `feat!:`, `fix!:`처럼 `!`를 붙이고, 하단에 `BREAKING CHANGE:`로 이유를 설명할 수도 있어.
- description은 소문자로 시작하고 마침표는 붙이지 마.
- 전체 메시지는 한 줄만 생성해줘 (body나 footer는 생략 가능).
- 결과는 {"한국어" if lang == "ko" else "영어"}로 작성해줘.

다음은 git diff 내용이야:

{diff}

이 내용을 바탕으로 한 줄짜리 커밋 메시지를 Conventional Commit 형식으로 작성해줘."""

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
# 6. 메인 실행 함수
def main():
    parser = argparse.ArgumentParser(description="Gommit: GPT 기반 커밋 메시지 생성기")
    parser.add_argument("--lang", choices=["ko", "en"], default="ko", help="커밋 메시지 언어 (ko 또는 en)")
    args = parser.parse_args()

    print("Git 변경사항을 확인하는 중...")
    diff = get_staged_diff()

    if not diff:
        print(" 스테이징된 변경사항이 없습니다. 먼저 'git add'를 해주세요.")
        return

    print("🤖 GPT가 커밋 메시지를 생성하는 중...")
    commit_message = generate_commit_message(diff, lang=args.lang)

    print(f"\n 생성된 메시지:\n\"{commit_message}\"\n")

    confirm = input("이 메시지로 커밋할까요? (y/n): ").strip().lower()
    if confirm == "y":
        run_commit(commit_message)
        print("커밋 완료! 커밋문: ", commit_message)
    else:
        print("커밋이 취소되었습니다.")




if __name__ == "__main__":
    main()
