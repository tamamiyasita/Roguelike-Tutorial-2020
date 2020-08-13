from constants import *

def door_check(tiles, x, y):
    #北
    if tiles[x][y] == TILE.EMPTY and tiles[x][y+1] == TILE.EMPTY and tiles[x][y-1] == TILE.EMPTY\
        and tiles[x-1][y] == TILE.WALL and tiles[x+1][y] == TILE.WALL\
        and tiles[x-1][y+1] == TILE.EMPTY and tiles[x+1][y+1] == TILE.EMPTY:

        return "north"
    
    #南
    if tiles[x][y] == TILE.EMPTY and tiles[x][y+1] == TILE.EMPTY and tiles[x][y-1] == TILE.EMPTY\
        and tiles[x-1][y] == TILE.WALL and tiles[x+1][y] == TILE.WALL\
        and tiles[x-1][y-1] == TILE.EMPTY and tiles[x+1][y-1] == TILE.EMPTY:

        return "south"

    #東
    if tiles[x][y] == TILE.EMPTY and tiles[x+1][y] == TILE.EMPTY and tiles[x-1][y] == TILE.EMPTY\
        and tiles[x][y-1] == TILE.WALL and tiles[x][y+1] == TILE.WALL\
        and tiles[x+1][y+1] == TILE.EMPTY and tiles[x+1][y-1] == TILE.EMPTY:

        return "east"

    #西
    if tiles[x][y] == TILE.EMPTY and tiles[x+1][y] == TILE.EMPTY and tiles[x-1][y] == TILE.EMPTY\
        and tiles[x][y-1] == TILE.WALL and tiles[x][y+1] == TILE.WALL\
        and tiles[x-1][y+1] == TILE.EMPTY and tiles[x-1][y-1] == TILE.EMPTY:

        return "west"