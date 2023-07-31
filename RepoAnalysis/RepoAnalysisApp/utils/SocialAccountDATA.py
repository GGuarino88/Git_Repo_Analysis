from allauth.socialaccount.models import SocialToken
from allauth.socialaccount.models import SocialAccount

class SocialAccountDATA:
    def __init__(self, request):
        self.__request = request

    def is_social(self):
        return SocialAccount.objects.filter(user=self.__request.user).exists()

    def get_extra_data(self):
        return SocialAccount.objects.get(user=self.__request.user).extra_data

    def get_access_token(self):
        if self.__request and self.__request.user.is_authenticated:
            try:
                social_token = SocialToken.objects.get(account__user=self.__request.user, account__provider='github')
                return social_token.token
            
            except SocialToken.DoesNotExist:
                print("Social token for the user does not exist.")
        return None