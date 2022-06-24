import re
from dataclasses import dataclass
from pathlib import Path

SECRETS_PATH = Path("secrets.sh")

@dataclass
class Secret:
  name: str
  template: str
  description: str

SECRETS = [
  Secret(name="RIOT_API_KEY", template="RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", description="Riot Development API Key"),
  Secret(name="LOG_DIRECTORY", template="/Users/ron/logs/", description="Folder where log outputs will be stored"),
  Secret(name="DISCORD_TOKEN", template="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", description="Discord Developer Portal API Key"),
]

VALS = {}

SECRETS_PATH.touch()

with open(SECRETS_PATH, "r") as f:
  for line in f:
    m = re.match(r'export (.*)="(.*)"', line)
    secret_name = m.group(1)
    secret_val = m.group(2)
    VALS[secret_name] = secret_val

for secret in SECRETS:
  if secret.name not in VALS:
    print(f"Please enter your {secret.name}")
    print(f"Template: {secret.template}")
    print(f"Description: {secret.description}")
    VALS[secret.name] = input("Value: ")

with open(SECRETS_PATH, "w") as f:
  for name, val in VALS.items():
    f.write(f'export {name}="{val}"\n')

print("Done!")
