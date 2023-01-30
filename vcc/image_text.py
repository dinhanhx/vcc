from dataclasses import dataclass
from typing import List

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


@dataclass
class ImageDescription:
    image_url: str
    description: List[str]


@dataclass
class PhotoStory(JSONWizard):
    class _(JSONWizard.Meta):
        # Sets the target key transform to use for serialization;
        # defaults to `camelCase` if not specified.
        key_transform_with_load = LetterCase.SNAKE
        key_transform_with_dump = LetterCase.SNAKE

    contents: List[ImageDescription]
    article_url: str
    title: str

    def echo(self):
        print(self.title)
        print(self.article_url)
        for image_description in self.contents:
            print(image_description.image_url)
            for description in image_description.description:
                print(description)


if __name__ == '__main__':
    article = PhotoStory([
        ImageDescription(image_url='direct image link', description=[
            'Describe the image',
            'Describe the image more'
        ])
    ],
        article_url='article url',
        title='A title')
    print(article.to_dict())
    article.echo()
