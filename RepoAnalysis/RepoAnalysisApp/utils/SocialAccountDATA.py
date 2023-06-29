from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialToken

class SocialAccountDATA:
    
    def __init__(self, request):
        
        self.__request = request
    
    def get_extra_data(self):
        
        return SocialAccount.objects.get(user=self.__request.user).extra_data
        
    def get_access_token(self):
        
        return SocialToken.objects.get(account__user=self.__request.user, account__provider='github')
