import ee

def addDate(image):
  img_date = ee.Date(image.date())
  img_date = ee.Image(ee.Number.parse(img_date.format('YYYYMMdd'))).rename('date').toInt()
  image = image.addBands(img_date)
  return(image)

def getNDVI(image):
  ndvi = image.normalizedDifference(['B8','B4']).rename("NDVI")
  image = image.addBands(ndvi)
  return(image)

def getGNDVI(image):
  gndvi = image.normalizedDifference(['B8','B3']).rename("GNDVI")
  image = image.addBands(gndvi)
  return(image)

def getNDSI(image):
  ndsi = image.normalizedDifference(['B3','B11']).rename("NDSI")
  image = image.addBands(ndsi)
  return(image)

def getReCl(image):
    ReCl = image.expression(
        '((NIR / RED) - 1)', {
            'NIR': image.select('B8'),
            'RED': image.select('B4')
        }).rename("ReCl")

    image = image.addBands(ReCl)

    return(image)

def getNDWI(image):
    ndwi = image.normalizedDifference(['B8','B11']).rename("NDWI")
    image = image.addBands(ndwi)
    return(image)

def getCWSI(image):
    # Compute the EVI using an expression.
    CWSI = image.expression(
        '(NDVI + NDWI)', {
            'NDWI': image.select('NDWI'),
            'NDVI': image.select('NDVI')
        }).rename("CWSI")

    image = image.addBands(CWSI)

    return(image)