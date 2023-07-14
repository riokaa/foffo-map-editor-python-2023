import random
from collections import defaultdict
from PIL import Image

class Tile:
    tile_dir = "static/tile/"

    def __init__(self, name) -> None:
        self.name = name
        self.tiles = self._load_tiles()

    def _load_tiles(self):
        image = Image.open(f"{Tile.tile_dir}{self.name}.png")
        width, height = image.size
        num_squares = height // width
        tiles = []
        for i in range(num_squares):
            top = i * width
            bottom = top + width
            square_image = image.crop((0, top, width, bottom))
            tiles.append(square_image)
        # 地砖样式按照4位二进制分类(左上/右上/左下/右下)
        tiledict = defaultdict(list)
        for tile in tiles:
            loc_code = [int(tile.getpixel(pos)[3] > 127) for pos in [(0, 0), (-1, 0), (0, -1), (-1, -1)]]
            loc_code = int("".join(str(bit) for bit in loc_code), 2)
            tiledict[loc_code].append(tile)
        return tiledict
    
    def get_tile(self, id):
        """根据id获取地砖部位。

        Args:
            id (int): 地砖编号(1~15)
        """
        return random.choice(self.tiles[id])
    
    
class AnimatedTile(Tile):
    tile_dir = "static/tile/animated/"


if __name__ == "__main__":
    tile = Tile("王城砖地")
