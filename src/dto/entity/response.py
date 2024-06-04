from uuid import uuid4


class ParrotResponse:
    uuid: str
    response: str
    status: str

    def __init__(self, response="", status="success", uuid=str(uuid4())) -> None:
        self.uuid = uuid
        self.response = response
        self.status = status
