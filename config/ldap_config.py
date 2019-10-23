import os
import ldap
from django_auth_ldap.config import LDAPSearch

# Baseline configuration.
AUTH_LDAP_SERVER_URI = os.environ.get("AUTH_LDAP_SERVER_URI", "ldap://localhost")

AUTH_LDAP_BIND_DN = os.environ.get("AUTH_LDAP_BIND_DN", "")
AUTH_LDAP_BIND_PASSWORD = os.environ.get("AUTH_LDAP_BIND_PASSWORD", "")

if os.environ.get("AUTH_LDAP_USER_DN_TEMPLATE"):
    AUTH_LDAP_USER_DN_TEMPLATE = os.environ.get("AUTH_LDAP_USER_DN_TEMPLATE")
else:
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        os.environ.get("AUTH_LDAP_USER_BASE_CN", ""),
        ldap.SCOPE_SUBTREE,
        os.environ.get("AUTH_LDAP_USER_SEARCH_FILTER", "(objectClass=*)"),
    )

# Simple group restrictions
AUTH_LDAP_REQUIRE_GROUP = os.environ.get("AUTH_LDAP_REQUIRE_GROUP")
AUTH_LDAP_DENY_GROUP = os.environ.get("AUTH_LDAP_DENY_GROUP")

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "username": os.environ.get("AUTH_LDAP_USER_ATTR_MAP_USERNAME", "sAMAccountName"),
    "first_name": os.environ.get("AUTH_LDAP_USER_ATTR_MAP_FIRST_NAME", "givenName"),
    "last_name": os.environ.get("AUTH_LDAP_USER_ATTR_MAP_LAST_NAME", "sn"),
    "email": os.environ.get("AUTH_LDAP_USER_ATTR_MAP_EMAIL", "mail"),
}

if os.environ.get("AUTH_LDAP_START_TLS"):
    AUTH_LDAP_START_TLS = True

# This is the default.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
)
