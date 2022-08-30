from enum import Enum
from io import BytesIO
import re
from typing import IO, Any, Optional, Union

from fntlib.utils import *


class Padding(DefaultClass):
    """Padding describes how textures are displaced in the texture."""
    
    up: int = IntValue(0)
    right: int = IntValue(0)
    down: int = IntValue(0)
    left: int = IntValue(0)

    def __init__(self, args: Union[dict[str, Any], str, None] = None) -> None:
        if type(args) == str:
            args = re.search(
                r"(?P<up>.+?),(?P<right>.+?),(?P<down>.+?),(?P<left>.+?)",
                args
            ).groupdict()

        super().__init__(args)

    def to_string(self) -> str:
        return f'{self.up},{self.right},{self.down},{self.left}'


class Spacing(DefaultClass):
    """Spacing describes how letters are displaced relative each other."""
    
    horizontal: int = IntValue(0)
    vertical: int = IntValue(0)

    def __init__(self, args: Union[dict[str, Any], str, None] = None) -> None:
        if type(args) == str:
            args = re.search(
                r"(?P<horizontal>.+?),(?P<vertical>.+?)",
                args
            ).groupdict()

        super().__init__(args)

    def to_string(self) -> str:
        return f'{self.horizontal},{self.vertical}'


class Info(DefaultClass):
    """This class contains information on how the font was generated.
    
    :param face: The name of the true type font.
    :type face: str
    :param size: The size of the true type font.
    :type size: int
    :param bold: Whether the font is bold.
    :type bold: bool
    :param italic: Whether the font is italic.
    :type italic: bool
    :param charset: The name of the OEM charset used (when not unicode).
    :type charset: str
    :param unicode: Whether charset is unicode.
    :type unicode: bool
    :param stretch_h: The font height stretch in percentage. 100% means no stretch.
    :type stretch_h: int
    :param smooth: Whether the smoothing was turned on.
    :type smooth: bool
    :param aa: The supersampling level used. 1 means no supersampling was used.
    :type aa: int
    :param padding: The padding for each character.
    :type padding: Padding
    :param spacing: The spacing for each character.
    :type spacing: Spacing
    :param outline: The outline thickness.
    :type outline: int"""

    face: str = StrValue()
    """The name of the true type font."""
    size: int = IntValue()
    """The size of the true type font."""
    bold: bool = BoolValue()
    """Whether the font is bold."""
    italic: bool = BoolValue()
    """Whether the font is italic."""
    charset: str = StrValue()
    """The name of the OEM charset used (when not unicode)."""
    unicode: bool = BoolValue()
    """Whether charset is unicode."""
    stretch_h: int = IntValue()
    """The font height stretch in percentage. 100% means no stretch."""
    smooth: bool = BoolValue()
    """Whether the smoothing was turned on."""
    aa: int = IntValue()
    """The supersampling level used. 1 means no supersampling was used."""
    padding: Padding = Padding()
    """The padding for each character."""
    spacing: Spacing = Spacing()
    """The spacing for each character."""
    outline: int = IntValue()
    """The outline thickness."""

    def __init__(self, args: Optional[dict[str, Any]] = None) -> None:
        super().__init__(args)

    def to_string(self) -> str:
        return super().to_string({'stretch_h': 'stretchH'})


class ChannelInfo(Enum):
    """The enum to represent what information holds a texture channel."""
    
    GLYPH_DATA = 0
    OUTLINE = 1
    GLYPH_AND_OUTLINE = 2
    ZERO = 3
    ONE = 4


class Common(DefaultClass):
    """This class contains information common to all characters.
    
    :param line_height: The distance in pixels between each line of text.
    :type line_height: int
    :param base: The number of pixels from the absolute top of the line to the base of the characters.
    :type base: int
    :param scale_w: The width of the texture, normally used to scale the x pos of the character image.
    :type scale_w: int
    :param scale_h: The height of the texture, normally used to scale the y pos of the character image.
    :type scale_h: int
    :param pages_num: The number of texture pages included in the font.
    :type pages_num: int
    :param packed: Whether the monochrome characters have been packed into each of the texture channels. In this case alphaChnl describes what is stored in each channel.
    :type packed: bool
    :param alpha_channel: Check enum `ChannelInfo`
    :type alpha_channel: ChannelInfo
    :param red_channel: Check enum `ChannelInfo`
    :type red_channel: ChannelInfo
    :param green_channel: Check enum `ChannelInfo`
    :type green_channel: ChannelInfo
    :param blue_channel: Check enum `ChannelInfo`
    :type blue_channel: ChannelInfo"""

    line_height: int = IntValue()
    """The distance in pixels between each line of text."""
    base: int = IntValue()
    """The number of pixels from the absolute top of the line to the base of the characters."""
    scale_w: int = IntValue()
    """The width of the texture, normally used to scale the x pos of the character image."""
    scale_h: int = IntValue()
    """The height of the texture, normally used to scale the y pos of the character image."""
    pages_num: int = IntValue()
    """The number of texture pages included in the font."""
    packed: bool = BoolValue()
    """Whether the monochrome characters have been packed into each of the texture channels. In this case alphaChnl describes what is stored in each channel."""
    alpha_channel: ChannelInfo = EnumValue(enum=ChannelInfo)
    """Check enum `ChannelInfo`"""
    red_channel: ChannelInfo = EnumValue(enum=ChannelInfo)
    """Check enum `ChannelInfo`"""
    green_channel: ChannelInfo = EnumValue(enum=ChannelInfo)
    """Check enum `ChannelInfo`"""
    blue_channel: ChannelInfo = EnumValue(enum=ChannelInfo)
    """Check enum `ChannelInfo`"""

    def __init__(self, args: Optional[dict[str, Any]] = None) -> None:
        super().__init__(args)

    def to_string(self) -> str:
        return super().to_string({'line_height': 'lineHeight', 'scale_w': 'scaleW', 'scale_h': 'scaleH', 'pages_num': 'pages'})


class Page(DefaultClass):
    """This class represents a page associated with a texture."""

    id: int = IntValue()
    """The page id."""
    tex_name: str = StrValue()
    """The texture file name."""

    def __init__(self, args: Optional[dict[str, Any]]) -> None:
        super().__init__(args)

    def to_string(self) -> str:
        return super().to_string({'tex_name': 'file'})


class Channel(Enum):
    """The texture channel where the character image is found."""
    
    BLUE = 1
    GREEN = 2
    RED = 4
    ALPHA = 8
    ALL = 15


class Char(DefaultClass):
    """This class describes a character in the font.
    
    :param id: The character id.
    :type id: int
    :param x: The left position of the character image in the texture.
    :type x: int
    :param y: The top position of the character image in the texture.
    :type y: int
    :param width: The width of the character image in the texture.
    :type width: int
    :param height: The height of the character image in the texture.
    :type height: int
    :param xoffset: How much the current position should be offset when copying the image from the texture to the screen.
    :type xoffset: int
    :param yoffset: How much the current position should be offset when copying the image from the texture to the screen.
    :type yoffset: int
    :param xadvance: How much the current position should be advanced after drawing the character.
    :type xadvance: int
    :param page: The texture page where the character image is found.
    :type page: int
    :param chnl: The texture channel where the character image is found.
    :type chnl: Channel"""

    id: int = IntValue()
    """The character id."""
    x: int = IntValue()
    """The left position of the character image in the texture."""
    y: int = IntValue()
    """The top position of the character image in the texture."""
    width: int = IntValue()
    """The width of the character image in the texture."""
    height: int = IntValue()
    """The height of the character image in the texture."""
    xoffset: int = IntValue()
    """How much the current position should be offset when copying the image from the texture to the screen."""
    yoffset: int = IntValue()
    """How much the current position should be offset when copying the image from the texture to the screen."""
    xadvance: int = IntValue()
    """How much the current position should be advanced after drawing the character."""
    page: int = IntValue()
    """The texture page where the character image is found."""
    chnl: Channel = EnumValue(enum=Channel)
    """The texture channel where the character image is found."""

    def __init__(self, args: Optional[dict[str, Any]]) -> None:
        super().__init__(args)


class Kerning(DefaultClass):
    """The kerning information is used to adjust the distance between certain characters, e.g. some characters should be placed closer to each other than others.
    
    :param first_id: The first character id.
    :type first_id: int
    :param second_id: The second character id.
    :type second_id: int
    :param amount: How much the x position should be adjusted when drawing the second character immediately following the first.
    :type amount: int"""

    first_id: int = IntValue()
    """The first character id."""
    second_id: int = IntValue()
    """The second character id."""
    amount: int = IntValue()
    """How much the x position should be adjusted when drawing the second character immediately following the first."""

    def __init__(self, args: Optional[dict[str, Any]]) -> None:
        super().__init__(args)

    def to_string(self) -> str:
        return super().to_string({'first_id': 'first', 'second_id': 'second'})


class FNT(DefaultClass):
    """The main class that represents the .fnt file structure.
    
    :param info: This variable represents the `info` section in the font.
    :type info: Info
    :param common: This variable represents the `common` section in the font.
    :type common: Common
    :param pages: This variable represents pages in the font.
    :type pages: list[Page]
    :param chars: This variable represents characters in the font.
    :type chars: list[Char]
    :param kernings: This variable represents kernings in the font.
    :type kernings: list[Kerning]"""

    info: Info = Info()
    """This variable represents the `info` section in the font."""
    common: Common = Common()
    """This variable represents the `common` section in the font."""
    pages: list[Page] = []
    """This variable represents pages in the font."""
    chars: list[Char] = []
    """This variable represents characters in the font."""
    kernings: list[Kerning] = []
    """This variable represents kernings in the font."""

    def __init__(
        self
    ) -> None:
        """
        :param fp: An opened readable bytes file.
        """

        self.info = Info()
        self.common = Common()
        self.pages = []
        self.chars = []
        self.kernings = []
        
    @classmethod
    def from_fp(cls, fp: IO[bytes]):
        obj = cls.__new__(cls)
        super(FNT, obj).__init__()
        
        obj.setup(fp)
        
        return obj

    def setup(
        self,
        fp: IO[bytes]
    ) -> None:
        if not fp:
            return

        for line in [x.decode().strip() for x in fp.read().splitlines()]:
            if line == "":
                continue

            if line.startswith("info"):
                groups = get_pairs(line)

                groups = replace_dict_key(groups, "stretchH", "stretch_h")

                self.info = Info(groups)

            elif line.startswith("common"):
                groups = get_pairs(line)

                groups = replace_dict_key(groups, 'lineHeight', 'line_height')
                groups = replace_dict_key(groups, 'scaleW', 'scale_w')
                groups = replace_dict_key(groups, 'scaleH', 'scale_h')
                groups = replace_dict_key(groups, 'pages', 'pages_num')

                self.common = Common(groups)

            elif line.startswith("page"):
                groups = get_pairs(line)

                groups = replace_dict_key(groups, 'file', 'tex_name')

                self.pages.append(Page(groups))

            elif line.startswith("char "):
                groups = get_pairs(line)

                self.chars.append(Char(groups))

            elif line.startswith("kerning "):
                groups = get_pairs(line)

                groups = replace_dict_key(groups, 'first', 'first_id')
                groups = replace_dict_key(groups, 'second', 'second_id')

                self.kernings.append(Kerning(groups))

    def __repr__(self) -> str:
        return f'<FNT info={"None" if not self.info else "<Info ...>"} common={"None" if not self.common else "<Common ...>"} ' \
               f'pages={"[]" if not self.pages else "[...]"} chars={"[]" if not self.chars else "[...]"} kernings={"[]" if not self.chars else "[...]"}>'

    def to_string(self) -> str:
        ret = ""

        ret += f'info {self.info.to_string()}\ncommon {self.common.to_string()}\n'

        for page in self.pages:
            ret += f'page {page.to_string()}\n'

        if self.chars:
            ret += f'chars count={len(self.chars)}\n'

            for char in self.chars:
                ret += f'char {char.to_string()}\n'

        if self.kernings:
            ret += f'kernings count={len(self.kernings)}\n'

            for k in self.kernings:
                ret += f'kerning {k.to_string()}\n'

        return ret.strip()


def load(
    fp: IO[bytes]
) -> FNT:
    """
    Load a fnt file into an object.
    
    :param fp: An opened bytes-like file.
    :type fp: IO[bytes]
    
    :returns: An object that represents the font.
    :rtype: FNT
    
    :raises AttributeError: if `fp` is not readable.
    """

    if not fp.readable():
        raise AttributeError(
            f'Specified "{type(fp).__name__}" is not readable.')

    return FNT.from_fp(fp)


def loads(
    value: bytes
) -> FNT:
    """
    Load a fnt file from bytes string into an object.
    
    :param value: A bytes string containing a fnt file.
    :type value: bytes
    
    :returns: An object that represents the font.
    :rtype: FNT
    """
    return load(BytesIO(value))


def dump(
    value: FNT,
    fp: IO[bytes]
) -> None:
    """
    Write an `FNT` object into a file.
    
    :param value: An `FNT` object to write.
    :type value: FNT
    :param fp: An opened bytes-like file.
    :type fp: IO[bytes]
    
    :raises AttributeError: if `fp` is not writable.
    """
    
    if not fp.writable():
        raise AttributeError(
            f'Specified "{type(fp).__name__}" is not writable.')

    fp.write(value.to_string().encode())


def dumps(
    value: FNT
) -> bytes:
    """
    Write an `FNT` object to a string in fnt format.
    
    :param value: An object to write.
    :type value: FNT
    
    :returns: a bytes .fnt representation of the python object
    :rtype: bytes
    """
    fp = BytesIO()
    
    dump(value, fp)
    
    return fp.getvalue()
