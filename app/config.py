import os


class Config:

    DATABASE_HOST = os.environ.get("DATABASE_HOST", "host.docker.internal")
    DATABASE_PORT = int(os.environ.get("DATABASE_PORT", "27017"))
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "music_store")

    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')

    APP_HOST = os.environ.get('APP_HOST', '0.0.0.0')
    APP_PORT = int(os.environ.get('APP_PORT', '5000'))

    def to_dict(self):
        """
        Returns a dict representation of all configuration values.
        """
        return {
            attr: getattr(self, attr)
            for attr in dir(self)
            if not callable(getattr(self, attr)) and not attr.startswith("__")
        }
