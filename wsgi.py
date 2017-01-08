import os
import consensus_web as modulo

app = modulo.create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == "__main__":
    app.run()