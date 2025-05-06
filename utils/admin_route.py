from fastapi import Depends
from typing import List, Any, Dict
from crud.user import require_admin


def admin_route_depends(
    *,
    dependencies: List = None,
    description: str = "🔒 Requires admin privileges.",
    **kwargs: Any
) -> Dict[str, Any]:
    deps = dependencies or []
    deps.append(Depends(require_admin))

    return {
        "dependencies": deps,
        "description": description,
        **kwargs
    }