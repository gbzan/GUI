import multiprocessing

class Data(object):

    def __init__(self):
        self.file_dir = {}
        self.datacube = {}
        self.current_datacube = None
        self.current_filename = None
        self.only_content_widget = None
        self.current_file_tree_item = None
        self.current_roi = None
        self.content_widget_container = {}
        self.darkcount = 300
        self.core_percent = 0.8
        self.core_num = int(self.core_percent * multiprocessing.cpu_count())
        self.roi_names = set()
