from uuid import uuid4


class ParrotResponse:
    uuid: str
    response: str
    status: str
    metadata: dict

    def __init__(
        self, response="", status="success", uuid=str(uuid4()), metadata: dict = {}
    ) -> None:
        self.uuid = uuid
        self.response = response
        self.status = status
        self.metadata = metadata
