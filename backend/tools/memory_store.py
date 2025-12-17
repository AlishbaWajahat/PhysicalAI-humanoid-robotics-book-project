"""
Simple in-memory store implementation for ChatKit.
Based on OpenAI ChatKit advanced samples.
"""

from datetime import datetime
from typing import Any
from chatkit.store import Store, NotFoundError
from chatkit.types import ThreadMetadata, ThreadItem, Page, Attachment
from dataclasses import dataclass, field


@dataclass
class _ThreadState:
    """Internal state for a thread."""
    thread: ThreadMetadata
    items: list[ThreadItem] = field(default_factory=list)


class MemoryStore(Store[dict]):
    """
    Thread-safe in-memory store for ChatKit threads and items.
    Suitable for development and testing. Not for production use.
    """

    def __init__(self) -> None:
        self._threads: dict[str, _ThreadState] = {}
        self._attachments: dict[str, Attachment] = {}

    async def save_thread(
        self,
        thread: ThreadMetadata,
        context: dict
    ) -> None:
        """Save or update a thread."""
        state = self._threads.get(thread.id)
        if state:
            state.thread = thread.model_copy(deep=True)
        else:
            self._threads[thread.id] = _ThreadState(
                thread=thread.model_copy(deep=True),
                items=[],
            )

    async def load_thread(self, thread_id: str, context: dict) -> ThreadMetadata:
        """Load a thread by ID."""
        state = self._threads.get(thread_id)
        if not state:
            raise NotFoundError(f"Thread {thread_id} not found")
        return state.thread.model_copy(deep=True)

    async def load_thread_items(
        self,
        thread_id: str,
        after: str | None,
        limit: int,
        order: str,
        context: dict,
    ) -> Page[ThreadItem]:
        """Load paginated thread items."""
        state = self._threads.get(thread_id)
        if not state:
            raise NotFoundError(f"Thread {thread_id} not found")

        items = [item.model_copy(deep=True) for item in state.items]
        items.sort(
            key=lambda i: getattr(i, "created_at", datetime.utcnow()),
            reverse=(order == "desc"),
        )

        start = 0
        if after:
            index_map = {item.id: idx for idx, item in enumerate(items)}
            start = index_map.get(after, -1) + 1

        slice_items = items[start : start + limit + 1]
        has_more = len(slice_items) > limit
        return Page(
            data=slice_items[:limit],
            has_more=has_more,
            after=slice_items[-1].id if has_more else None
        )

    async def add_thread_item(
        self, thread_id: str, item: ThreadItem, context: dict
    ) -> None:
        """Add an item to a thread."""
        state = self._threads.get(thread_id)
        if not state:
            raise NotFoundError(f"Thread {thread_id} not found")
        state.items.append(item.model_copy(deep=True))

    async def save_item(
        self, thread_id: str, item: ThreadItem, context: dict
    ) -> None:
        """Save or update a thread item."""
        state = self._threads.get(thread_id)
        if not state:
            raise NotFoundError(f"Thread {thread_id} not found")

        # Find and update existing item or append new one
        for idx, existing_item in enumerate(state.items):
            if existing_item.id == item.id:
                state.items[idx] = item.model_copy(deep=True)
                return
        state.items.append(item.model_copy(deep=True))

    async def load_item(
        self, thread_id: str, item_id: str, context: dict
    ) -> ThreadItem:
        """Load a specific item from a thread."""
        state = self._threads.get(thread_id)
        if not state:
            raise NotFoundError(f"Thread {thread_id} not found")

        for item in state.items:
            if item.id == item_id:
                return item.model_copy(deep=True)
        raise NotFoundError(f"Item {item_id} not found in thread {thread_id}")

    async def delete_thread(self, thread_id: str, context: dict) -> None:
        """Delete a thread and all its items."""
        if thread_id in self._threads:
            del self._threads[thread_id]

    async def delete_thread_item(
        self, thread_id: str, item_id: str, context: dict
    ) -> None:
        """Delete a specific item from a thread."""
        state = self._threads.get(thread_id)
        if not state:
            raise NotFoundError(f"Thread {thread_id} not found")

        state.items = [item for item in state.items if item.id != item_id]

    async def load_threads(
        self,
        limit: int,
        after: str | None,
        order: str,
        context: dict,
    ) -> Page[ThreadMetadata]:
        """Load paginated list of threads."""
        threads = [state.thread for state in self._threads.values()]
        threads.sort(
            key=lambda t: getattr(t, "created_at", datetime.utcnow()),
            reverse=(order == "desc"),
        )

        start = 0
        if after:
            index_map = {thread.id: idx for idx, thread in enumerate(threads)}
            start = index_map.get(after, -1) + 1

        slice_threads = threads[start : start + limit + 1]
        has_more = len(slice_threads) > limit
        return Page(
            data=slice_threads[:limit],
            has_more=has_more,
            after=slice_threads[-1].id if has_more else None
        )

    # Attachment methods
    async def save_attachment(
        self, attachment: Attachment, context: dict
    ) -> None:
        """Save an attachment."""
        self._attachments[attachment.id] = attachment.model_copy(deep=True)

    async def load_attachment(
        self, attachment_id: str, context: dict
    ) -> Attachment:
        """Load an attachment by ID."""
        attachment = self._attachments.get(attachment_id)
        if not attachment:
            raise NotFoundError(f"Attachment {attachment_id} not found")
        return attachment.model_copy(deep=True)

    async def delete_attachment(
        self, attachment_id: str, context: dict
    ) -> None:
        """Delete an attachment."""
        if attachment_id in self._attachments:
            del self._attachments[attachment_id]
