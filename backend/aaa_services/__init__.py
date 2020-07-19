from django.conf import settings
from keycloak import KeycloakOpenID

config = settings.KEYCLOAK_CONFIG

client_secret_key = config.get(
            'KEYCLOAK_CLIENT_SECRET_KEY', None)

server_url = config['KEYCLOAK_SERVER_URL']
client_id = config['KEYCLOAK_CLIENT_ID']
realm = config['KEYCLOAK_REALM']

keycloak_web = KeycloakOpenID(server_url= server_url,client_id= client_id,realm_name= realm,
                                       client_secret_key= client_secret_key)