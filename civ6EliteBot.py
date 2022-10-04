from genericpath import isfile
from random import randint
from Levenshtein import distance as levenshtein_distance
from os import listdir
from os.path import isfile, join
from discord import file

class Leader:
    def __init__(self, name, image):
        self.name = name
        self.image = image

    def __str__(self):
        return self.name + " : " + self.image

    def image_path(self):
        return "images/" + self.image

def rand_ints(lower, upper, N):
    assert(upper > lower)
    assert(upper - lower >= N)

    res = []
    L = list(range(lower, upper))
    for _ in range(N):
        rand = randint(0, len(L)-1)
        res.append(L.pop(rand))
    return res

def get_image(name):
    w = (1, 1, 100)
    images = [f for f in listdir("images") if isfile(join("images", f))]
    minDist, minImage = levenshtein_distance(images[0], name, weights=w), images[0]
    for image in images[1:]:
        dist = levenshtein_distance(image, name, weights=w)
        if dist < minDist:
            minDist = dist
            minImage = image
    return minImage

def load_leaders():
    leaders = []
    with open("leaders.txt", encoding = "utf8", errors ='replace') as f:

        lines = f.readlines()    
        for line in lines:
            leaderName = line.replace('\n', "")
            leaderImage = get_image(leaderName)
            leaders.append(Leader(leaderName, leaderImage))
    return leaders

def random_leaders(leaders, N):
    res = []
    for rand_int in rand_ints(0, len(leaders), N):
        res.append(leaders[rand_int])
    return res

if __name__ == "__main__":
    leaders = load_leaders()
    for leader in random_leaders(leaders, 3):
        print(leader.name)