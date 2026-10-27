from datetime import datetime, UTC


def ahora() -> datetime:
    return datetime.now(UTC)