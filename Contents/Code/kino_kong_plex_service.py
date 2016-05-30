from kino_kong_service import KinoKongService
from plex_storage import PlexStorage

class KinoKongPlexService(KinoKongService):
    def __init__(self):
        storage_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'kinokong.storage'))

        self.queue = PlexStorage(storage_name)

        self.queue.register_simple_type('movie')
        self.queue.register_simple_type('serie')
        # self.queue.register_simple_type('selection')
