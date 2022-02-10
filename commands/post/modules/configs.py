from .paginator import Resolutions, COLORS_COMBINATIONS
from .colors import *


class Configs:

    def __init__(self, data, default='pavlov'):
        """Automatically load the default object"""

        self.data = data
        self.config_item = data[default]

        # the logo path
        self.logo: str = self.config_item.get('logo')

        # the list of the operators that can use this command
        self.operators: list = self.config_item.get('operators')

        # the list of the guilds that can use this command
        # inside the guild all the users have the permission to use it
        self.guilds: list = self.config_item.get('guild')

        # the image resolution optimized for the social
        self.resolution: tuple = Resolutions.INSTAGRAM.value

        # the name tag in the post
        self.name_tag = self.config_item.get('name_tag')

    def _unpack(self):
        self.logo: str = self.config_item.get('logo')
        self.operators: list = self.config_item.get('operators')
        self.resolution: tuple = Resolutions['INSTAGRAM'].value
        self.name_tag = self.config_item.get('name_tag')

    def _get_subsection(self, configs_type: str, sub_section: str):
        """load the configs in the subsection"""
        cfg = self.config_item.get(configs_type)

        # there is no config
        if not cfg:
            raise Exception('post type not found')

        # get the subsection
        # or the first one available
        try:
            cfg = cfg[sub_section]
        except KeyError:
            cfg = cfg[list(cfg.keys())[0]]

        return cfg

    def get_by_code(self, code, code_type='operators'):
        """Load the right item based on the operator"""
        code = str(code)

        for key in self.data.keys():
            config_item = self.data[key]
            if code in config_item.get(code_type, []):
                self.config_item = config_item
                self._unpack()  # load data
                return True

        return False

    def get_by_name(self, name):
        """Load the right item based on the name of itself"""
        for key in self.data.keys():
            if name == key:
                self.config_item = self.data[key]
                self._unpack()  # load data
                return True

        return False

    def get_colors_setup(self, configs_type: str, sub_section: str):
        """the color setup for the post generator"""
        cfg = self._get_subsection(configs_type, sub_section)

        colors = COLORS_COMBINATIONS  # default colors

        colors_list = cfg.get('colors')
        if colors_list:
            colors = []
            for color_descriptor in colors_list:
                colors.append([name if name.startswith('#') else globals()[name] for name in color_descriptor])

        return colors

    def build_kwargs(self, configs_type: str, sub_section: str):
        """
        Create a kwargs dict to pass to the function
        :param configs_type: the type of configs you want: 'image' or 'text' etc
        :param sub_section: the subsection
        :return: kwargs dict
        """
        kwargs = {}

        cfg = self._get_subsection(configs_type, sub_section)

        # build the kwargs dict with the configs
        for key in cfg.keys():
            kwargs[key] = cfg.get(key)
        return kwargs
