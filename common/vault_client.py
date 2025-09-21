import os
from dotenv import load_dotenv
import hvac
load_dotenv()

class VaultClient:
    def __init__(self, mount_point: str = "secret"):
        self.client = hvac.Client(
            url=os.environ['VAULT_ADDR'],
            token=os.environ['VAULT_TOKEN']
        )
        self.mount_point = mount_point

    def get_creds(self, path: str) -> dict:
        secret = self.client.secrets.kv.v2.read_secret_version(
            path=path,
            mount_point=self.mount_point,
            raise_on_deleted_version = True
        )
        return secret["data"]["data"]
