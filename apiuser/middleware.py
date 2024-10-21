from typing import Any


class CustomMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response=get_response

    def __call__(self,request, *args, **kwargs) -> Any:
        print("middleware called")    
        response=self.get_response(request)
        user_agent=request.META.get('HTTP_USER_AGENT')
        print('####')
        print(user_agent)
        return response