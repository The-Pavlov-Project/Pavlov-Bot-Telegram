from pydantic import BaseModel
import json

BASE_CONFIG_ROOT: str = 'pavlov'


class SettingsBaseModel(BaseModel):
    """
        Internal model for settings,
        this will only provide names conversion between naming conventions
    """

    class Config:
        allow_mutation = True

        @classmethod
        def alias_generator(cls, string: str) -> str:
            """convert the data on load to snake_case from camelCase"""
            components = string.split('_')
            return components[0] + ''.join(x.title() for x in components[1:])

    def __init__(self, **data):
        super().__init__(**data)
        for getter, setter in self.get_properties():
            if getter in data and setter:
                getattr(type(self), setter).fset(self, data[getter])

    @classmethod
    def get_properties(cls):
        attributes = {prop: getattr(cls, prop) for prop in dir(cls)}
        properties = {
            name: attribute
            for name, attribute in attributes.items()
            if isinstance(attribute, property) and name not in ("__values__", "fields")
        }

        setters = {prop.fget: name for name, prop in properties.items() if prop.fset}
        return [(name, setters.get(prop.fget))
                for name, prop in properties.items()
                if prop.fget and not prop.fset]

    def dict(self, *args, **kwargs):
        """
        Workaround for serializing properties with pydantic until
        https://github.com/samuelcolvin/pydantic/issues/935
        is solved
        """
        self.__dict__.update(
            {getter: getattr(self, getter) for getter, setter in self.get_properties()})

        return super().dict(*args, **kwargs)


class SettingsLoaderModel(SettingsBaseModel):
    """
        Base model for auto file load all settings
        CONFIGURATIONS_MODEL_FILENAME will define the filename that will be automatically loaded
    """
    CONFIGURATIONS_MODEL_FILENAME: str = ''

    @staticmethod
    def _save(filename, data):
        """Save the local storage data to the settings file"""
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=4))

    @staticmethod
    def _load(filename):
        """Load data from the file"""
        with open(filename, 'r') as f:
            return json.loads(f.read())

    def load(self, data: dict = None):
        """Load the file and re-init the class"""
        if not data:
            data = self._load(f"{BASE_CONFIG_ROOT}/{self.CONFIGURATIONS_MODEL_FILENAME}")
        super().__init__(**data)
