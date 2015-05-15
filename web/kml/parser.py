import xml.etree.ElementTree as ET
import json
import os
import copy


class UpdateGeoJSONwithKML:

    def __init__(self, filename, kmldir):
        # Holds each polygon data
        self.polygon_dict = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                    ]
                ]
            },
            "properties": {
                "name": ""
            }
        }

        # Reading data back
        with open(filename, 'r') as f:
            cjson = json.load(f)
        # for each kml file, parse it and add to json
        for k in os.listdir(kmldir):
            if k.endswith(".kml"):
                i = ParseKMLtoGeoJSON(k)
                j = copy.deepcopy(self.polygon_dict)
                j["geometry"]["coordinates"][0] = i.polygon
                j["properties"]["name"] = "BEAT " +\
                    i.name.upper()
                print(j)
                cjson["features"].append(j)

        # Writing JSON data
        with open(filename, 'w') as f:
            json.dump(cjson, f)


class ParseKMLtoGeoJSON:

    def __init__(self, filename):
        doc = ET.parse(filename)
        root = doc.getroot()
        self.polygon = []
        placemark = self.findPlacemark(root)
        self.name, coords = self.extractData(placemark)
        self.parseCoords(coords)

    def findPlacemark(self, root):
        # find the tag that holds all the data for a place
        try:
            for i in root:
                for j in i:
                    if "placemark" in j.tag.lower():
                        return j
        except Exception:
            pass
        return -1

    def extractData(self, placemark):
        # get the coords and name of the place
        name = ""
        try:
            for i in placemark:
                if "name" in i.tag.lower():
                    name = i.text.lower()
                if "linestring" in i.tag.lower():
                    for j in i:
                        if "coord" in j.tag.lower():
                            coords = j.text
                            return name, coords
        except Exception:
            pass
        return -1

    def parseCoords(self, coords):
        # parse all the coords into geojson compatible list of coordinates for
        # a polygon
        data = coords.strip("\n\r\t").split(",0 ")
        for d in data:
            t = d.split(",")
            if len(t) > 1:
                self.polygon.append([float(t[0]), float(t[1]), 0])
        self.polygon.append(self.polygon[0])

if "__main__" == __name__:
    UpdateGeoJSONwithKML("../js/beats.geojson", "./")
