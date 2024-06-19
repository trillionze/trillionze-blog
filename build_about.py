import feedparser
import httpx
import pathlib
import re
import datetime

root = pathlib.Path(__file__).parent.resolve()


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = "\n{}\n".format(chunk)
    chunk = "<!-- {} starts -->{}<!-- {} ends -->".format(
        marker, chunk, marker)
    return r.sub(chunk, content)


def formatGMTime(timestamp):
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
    dateStr = datetime.datetime.strptime(
        timestamp, GMT_FORMAT) + datetime.timedelta(hours=8)
    return dateStr.date()


def fetch_code_time():
    return httpx.get(
        "https://gist.githubusercontent.com/trillionze/6c974f79ed1cdb3ad90cd93ce309531d/raw/"
    )


def fetch_douban():
    entries = feedparser.parse(
        "https://www.douban.com/feed/people/trillionze/interests")["entries"]
    return [
        {
            "title": item["title"],
            "url": item["link"].split("#")[0],
            "published": formatGMTime(item["published"])
        }
        for item in entries
    ]


def fetch_blog_entries():
    entries = feedparser.parse(
        "https://www.trillionze.com/en/index.xml")["entries"]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": entry["published"].split("T")[0],
        }
        for entry in entries
    ]


if __name__ == "__main__":
    about_zh = root / "content/zh/about.md"
    about_en = root / "content/en/about.md"
    about_zh_contents = about_zh.open().read()
    about_en_contents = about_en.open().read()

    code_time_text = "\n```text\n"+fetch_code_time().text+"\n```\n"
    rewritten_zh = replace_chunk(
        about_zh_contents, "code_time", code_time_text)
    rewritten_en = replace_chunk(
        about_en_contents, "code_time", code_time_text)

    doubans = fetch_douban()[:5]
    doubans_md = "\n".join(
        ["* <a href='{url}' target='_blank'>{title}</a> - {published}".format(
            **item) for item in doubans]
    )
    rewritten_zh = replace_chunk(rewritten_zh, "douban", doubans_md)
    rewritten_en = replace_chunk(rewritten_en, "douban", doubans_md)

    entries = fetch_blog_entries()[:5]
    entries_md = "\n".join(
        ["* <a href={url} target='_blank'>{title}</a>".format(
            **entry) for entry in entries]
    )
    rewritten_zh = replace_chunk(rewritten_zh, "blog", entries_md)
    about_zh.open("w").write(rewritten_zh)

    rewritten_en = replace_chunk(rewritten_en, "blog", entries_md)
    about_en.open("w").write(rewritten_en)
