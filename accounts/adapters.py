"""
    Added Custom adapter so user can both login using google and 
    by username and password(after resetting password).
"""

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from accounts.models import User

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """Making custom SocialAccountAdapter and
       extending the DefaultSocialAccountAdapter.

    Args:
        DefaultSocialAccountAdapter (Class): All auth social account adapter class.
    """
    def pre_social_login(self, request, sociallogin):
        """Function build in DefaultSocialAccountAdapter that is overwriting.

        Args:
            request (Parameter): Django request.
            sociallogin (Parameter): All auth social login.
        """
        email = user_email(sociallogin.user)
        if email is not None:
            try:
                existing_user = User.objects.get(email=email)
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                pass