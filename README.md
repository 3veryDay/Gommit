# Gommit 🧠💬

GPT를 활용해 Git 커밋 메시지를 자동으로 생성해주는 CLI 도구입니다.  
변경사항을 분석해 한 줄 요약 커밋 메시지를 만들어줍니다.

## 🚀 사용법

```bash
# 설치 후, 커밋 전 변경사항 스테이징
git add .

# 커밋 메시지 생성 및 커밋 실행
python gommit.py --lang ko --style conventional
```

옵션:
- `--lang`: 커밋 메시지 언어 (ko | en)
- `--style`: 스타일 적용 (`conventional` 지원)

## 🔧 사전 준비

1. `.env` 파일 생성 후 OpenAI API 키 작성:

```
OPENAI_API_KEY=sk-...
```

2. `.env`는 꼭 `.gitignore`에 추가하세요.

## 💡 예시

```bash
$ python gommit.py --lang en --style conventional
> feat: Add GPT-based commit message generator
```

## 📦 의존성

```bash
pip install openai python-dotenv
```

## 📁 파일 구조

```
gommit.py         # 메인 실행 파일
.env              # (추적 금지) OpenAI API 키 보관
.gitignore        # .env 예외 처리 포함
```

---

Made with 💻 by 3veryday