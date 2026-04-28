import os

from oauthenticator.generic import GenericOAuthenticator

c.JupyterHub.authenticator_class = GenericOAuthenticator
c.Authenticator.allow_all = True
c.Authenticator.auto_login = True

issuer_url = os.environ["OIDC_ISSUER_URL"].rstrip("/")
client_id = os.environ["OIDC_CLIENT_ID"]
client_secret = os.environ["OIDC_CLIENT_SECRET"]
public_base_url = os.environ["JUPYTERHUB_PUBLIC_URL"].rstrip("/")

c.GenericOAuthenticator.client_id = client_id
c.GenericOAuthenticator.client_secret = client_secret
c.GenericOAuthenticator.oauth_callback_url = f"{public_base_url}/hub/oauth_callback"
c.GenericOAuthenticator.authorize_url = f"{issuer_url}/protocol/openid-connect/auth"
c.GenericOAuthenticator.token_url = f"{issuer_url}/protocol/openid-connect/token"
c.GenericOAuthenticator.userdata_url = f"{issuer_url}/protocol/openid-connect/userinfo"
c.GenericOAuthenticator.username_claim = "preferred_username"
c.GenericOAuthenticator.scope = ["openid", "profile", "email"]
