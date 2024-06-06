class Context:
    title: str
    content: str
    link: str
    source: str
    score: float

    index: int

    def __init__(
        self, content="", link="", title="", source="", score: float = 0, index=0
    ) -> None:
        self.content = content
        self.link = link
        self.title = title
        self.source = source
        self.index = index
        self.score = score

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
        return f"[\\[{self.index}\\]]: {self.link.replace(' ', '%20')}"


def sort_contexts(contexts: list[Context]):
    contexts.sort(key=lambda ctx: ctx.score, reverse=True)
    for i, ctx in enumerate(contexts):
        ctx.index = i + 1
    return contexts


def generate_markdown_references(contexts: list[Context]):
    return "\n".join([context.__ref__() for context in contexts])
