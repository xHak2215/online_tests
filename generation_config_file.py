import json
import secrets

SECRET_KEY = secrets.token_urlsafe(32)

with open("config.json", 'w') as f:
    json.dump({"SECRET_KEY":SECRET_KEY, "log_path":".", "media_path":"media"}, f, ensure_ascii=False, indent=2)
    
print("subprocess!")

