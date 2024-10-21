from .models import User
from datetime import date 

class userBio:
    _age=None
    _instance=None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(userBio, cls).__new__(cls)
            print(f"Creating a new User instance for {args[0]}")  # args[0] is the username
        return cls._instance
    
    def __init__(self,user,user_id) -> None:
       
       if self._age is None:
           birthdate=user.birth_day
           try:
                today = date.today()
                self._age= today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
           except Exception as e:
               self._age=None
               raise e
       else:
           print("not found ")
           
    @property
    def age(self):
        return self._age

    @staticmethod
    def get_logged_in_user_details(request):
        user=request.user
        if user.is_authenticated:
            return user
        else:
            return None