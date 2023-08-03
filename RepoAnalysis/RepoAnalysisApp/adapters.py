from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        # This method is used to get the redirect URL after connecting accounts.
        # In our case, we override it to use the specified callback URL.
        return socialaccount.get_provider().get_auth_params()['redirect_uri']
