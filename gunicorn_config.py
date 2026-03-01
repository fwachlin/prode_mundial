import os

# Render proporciona el puerto a través de la variable PORT
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"

# Workers basados en CPU cores
workers = 2

# Threads por worker
threads = 2

# Worker class
worker_class = "sync"

# Timeout
timeout = 120

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
