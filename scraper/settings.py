try:
    from scraper.localconfig import Config
except ImportError:
    from scraper.config import Config
Config
