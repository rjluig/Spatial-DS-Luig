import math

def mercX(lon,zoom = 1):
    """
    """
    lon = math.radians(lon)
    a = (256 / math.pi) * pow(2, zoom)
    b = lon + math.pi
    return a * b

def mercY(lat,zoom = 1):
    """
    """
    lat = math.radians(lat)
    a = (256.0 / math.pi) * pow(2, zoom)
    b = math.tan(math.pi / 4 + lat / 2)
    c = math.pi - math.log(b)
    return (a * c)

def mercToLL(point):
    lng,lat = point
    lng = lng / 256.0 * 360.0 - 180.0
    n = math.pi - 2.0 * math.pi * lat / 256.0
    lat = (180.0 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n))))
    return (lng, lat)
    
def toLL(point):
    x,y = point
    return mercToLL((x/4,y/4))

def adjust_point(self,p):

    lon,lat = p
    x = (mercX(lon) / 1024 * self.screen_width)
    y = (mercY(lat) / 512 * self.screen_height) - (self.screen_height/2)
    return (x,y)
    
if __name__=='__main__':
    # From lat lon to xy and back
    point = (-64,-75)
    print(point)
    x = mercX(point[0])
    y = mercY(point[1])
    print(x,y)
    lat,lon = toLL((x,y))
    print(lat,lon)

    # From click to lat lon
    click = (743, 575) 
    lat,lon = toLL(click)
    print(lat,lon)