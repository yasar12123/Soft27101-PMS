import os
from dotenv import load_dotenv
from azure.identity import InteractiveBrowserCredential, ClientSecretCredential, DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


# Grabbing environment variables from the .env file
#KVUri = os.getenv('KEY_VAULT_URI')
keyVaultName = "wmsUniKeyVault"
KVUri = f"https://wmsUniKeyVault.vault.azure.net"
secretName = "wmsUniSecret"
#secretValue = "oSfJu980jd"

# This section of code authenticates to an Azure Key Vault Using Interactive Browser Credentials
credential = InteractiveBrowserCredential(additionally_allowed_tenants=['*'] )
client = SecretClient(vault_url = KVUri, credential = credential)

# Lastly the secret is retrieved from the key vault using get_secret
get_secret = client.get_secret(secretName)
print(get_secret)