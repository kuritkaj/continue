import json
from typing import List
import os
import aiohttp

from ...core.main import ContextItem, ContextItemDescription, ContextItemId
from ...core.context import ContextProvider


def format_file_tree(startpath) -> str:
    result = ""
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        result += f'{indent}{os.path.basename(root)}/' + "\n"
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            result += f'{subindent}{f}' + "\n"

    return result


class FileTreeContextProvider(ContextProvider):
    title = "tree"

    workspace_dir: str = None

    def _filetree_context_item(self):
        return ContextItem(
            content=format_file_tree(self.workspace_dir),
            description=ContextItemDescription(
                name="File Tree",
                description="Add a formatted file tree of this directory to the context",
                id=ContextItemId(
                    provider_title=self.title,
                    item_id=self.title
                )
            )
        )

    async def provide_context_items(self, workspace_dir: str) -> List[ContextItem]:
        self.workspace_dir = workspace_dir
        return [self._filetree_context_item()]

    async def get_item(self, id: ContextItemId, query: str) -> ContextItem:
        if id.item_id != self.title:
            raise Exception("Invalid item id")

        return self._filetree_context_item()
