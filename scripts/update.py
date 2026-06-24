import json
import requests

SOURCE_URL = "https://raw.githubusercontent.com/MajoSissi/animeko-source/main/dist/online.json"

# 读取关键词
with open("blacklist.txt", encoding="utf-8") as f:
    BLOCK_KEYWORDS = [
        line.strip()
        for line in f
        if line.strip()
    ]

print("屏蔽关键词:")
print(BLOCK_KEYWORDS)

# 下载源
data = requests.get(
    SOURCE_URL,
    timeout=30
).json()

media_sources = data["exportedMediaSourceDataList"]["mediaSources"]

filtered = []
removed = []

for source in media_sources:

    name = source.get(
        "arguments",
        {}
    ).get(
        "name",
        ""
    )

    if any(
        keyword in name
        for keyword in BLOCK_KEYWORDS
    ):
        removed.append(name)
        continue

    filtered.append(source)

data["exportedMediaSourceDataList"]["mediaSources"] = filtered

with open(
    "online.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        data,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"删除 {len(removed)} 个源")

for x in removed:
    print("删除:", x)
