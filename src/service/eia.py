from config import EIA


class EIAService:
    api_key_cursor: int = -1

    @staticmethod
    def key():
        EIAService.api_key_cursor += 1
        return EIA.api_keys[EIAService.api_key_cursor % len(EIA.api_keys)]
