from fastapi import Request, Depends, HTTPException
from iam import get_current_user, TokenData

def admin_required_for_method(methods: list[str]):
    async def dependency(request: Request, current_user: TokenData = Depends(get_current_user)):
        if request.method in methods:
            if current_user.role != "admin":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Admin privileges required"
                )
        return current_user
    return dependency