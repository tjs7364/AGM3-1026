"""site/ 템플릿 → github_upload/ 배포 파일 생성.
.env의 AMPLITUDE_API_KEY만 HTML에 주입한다. 비밀키(AMPLITUDE_SECRET_KEY)는 절대 주입하지 않는다.
사용법: python build_site.py
"""
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(ROOT, "site"), os.path.join(ROOT, "github_upload")


def load_env(path):
    env = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


env = load_env(os.path.join(ROOT, ".env"))
api_key = env.get("AMPLITUDE_API_KEY")
if not api_key:
    sys.exit(".env에 AMPLITUDE_API_KEY가 없습니다. .env.example을 참고하세요.")

os.makedirs(OUT, exist_ok=True)
for name in sorted(os.listdir(SRC)):
    if not name.endswith(".html"):
        continue
    html = open(os.path.join(SRC, name), encoding="utf-8").read()
    html = html.replace("%%AMPLITUDE_API_KEY%%", api_key)
    secret = env.get("AMPLITUDE_SECRET_KEY")
    if secret and secret in html:
        sys.exit(f"{name}에 비밀키가 들어 있습니다. 빌드를 중단합니다.")
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(html)
    print("built", name)
