import os
from app import start

application = start()
port = int(os.environ.get("PORT", 5000))
application.run(host="0.0.0.0", port=port)
