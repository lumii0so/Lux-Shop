from aiogram.filters import Filter
from aiogram.types import Message

class IsAdmin(Filter):
    def __init__(self, admin_ids: list[int] | int) -> None:
        if isinstance(admin_ids, int):
            self.admin_ids = {admin_ids}
        else:
            self.admin_ids = set(admin_ids)

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids