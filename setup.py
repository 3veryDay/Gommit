from setuptools import setup, find_packages

setup(
    name="gommit",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "gommit = gommit.main:main"
        ]
    },
    author="YourName",
    description="GPT 기반 자동 커밋 메시지 생성기",
    python_requires=">=3.7"
)
