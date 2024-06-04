class Context:
    title: str
    content: str
    link: str
    source: str

    index: int

    def __init__(self, content="", link="", title="", source="", index=0) -> None:
        self.content = content
        self.link = link
        self.title = title
        self.source = source
        self.index = index

    def __str__(self) -> str:
        return f"[[{self.index}] {self.title or self.link}]({self.link.replace(' ', '%20')})"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Context):
            return False
        return self.link == value.link

    def __ne__(self, value: object) -> bool:
        return not (self == value)

    def __dict__(self):
        return {
            "title": self.title,
            "content": self.content,
            "link": self.link,
            "source": self.source,
        }

    def __xml__(self):
        return f"""<doc id="{self.index}" title="{self.title}" link="{self.link}" source="{self.source}">{self.content}</doc>"""

    def __ref__(self):
        return f"[\\[{self.index}\\]]: {self.link}"
