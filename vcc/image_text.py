from dataclasses import dataclass

from dataclass_wizard import JSONWizard
from dataclass_wizard.enums import LetterCase


@dataclass
class ImageCaption(JSONWizard):
    class _(JSONWizard.Meta):
        # Sets the target key transform to use for serialization;
        # defaults to `camelCase` if not specified.
        key_transform_with_load = LetterCase.SNAKE
        key_transform_with_dump = LetterCase.SNAKE

    image_url: str
    caption: str
    article_url: str


if __name__ == '__main__':
    example = ImageCaption(image_url='http://example.com',
                           caption='This is a caption',
                           article_url='http://example.com')
    print(example.to_dict())
