from django_auth_ldap.backend import LDAPBackend  
from django.core.exceptions import ObjectDoesNotExist  
from .models import UserProfile  
import logging  

logger = logging.getLogger(__name__)  

class LDAPAndLocalAuthBackend(LDAPBackend):  
    def authenticate(self, request, username=None, password=None, **kwargs):  
        # Étape 1 : Authentification via LDAP  
        user = super().authenticate(request, username, password, **kwargs)  

        if user is None:  
            logger.warning(f"LDAP authentication failed for username: {username}")  
            return None  

        # Étape 2 : Vérification dans UserProfile  
        try:  
            profile, created = UserProfile.objects.get_or_create(  
                ldap_cn=username,  
                defaults={  
                    "role": "user",  # Rôle par défaut  
                    "is_active": True  # Activer par défaut  
                },  
            )  
            if not profile.is_active:  
                logger.warning(f"User {username} is deactivated in UserProfile")  
                return None  # Retourner None si le compte est désactivé  
            return user  

        except Exception as e:  
            logger.error(f"Error occurred while checking UserProfile for {username}: {str(e)}")  
            return None  