from earthengine.products import EE_PRODUCTS
# from WebApp.config.Config import EE_ACCOUNT, EE_PRIVATE_KEY_FILE
import logging
import ee
from ee.ee_exception import EEException

# if EE_ACCOUNT:
#     try:
#         credentials = ee.ServiceAccountCredentials(EE_ACCOUNT, EE_PRIVATE_KEY_FILE)
#         ee.Initialize(credentials)
#     except EEException as e:
#         print(str(e))
# else:
#     try:
#         ee.Initialize()
#     except EEException as e:
#         from oauth2client.service_account import ServiceAccountCredentials
#         credentials = ServiceAccountCredentials.from_p12_keyfile(
#             service_account_email='',
#             filename='',
#             private_key_password='notasecret',
#             scopes=ee.oauth.SCOPE + ' https://www.googleapis.com/auth/drive '
#         )
#         ee.Initialize(credentials)


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


# def calculo_ndvi(image):
#     result = image.expression('b(24) >= 0.9 ? (200*0.7) : (b(24) >= 0.7 ? (200*1) : (200 * 1.1))').rename('result1')

#     image = image.addBands(result)

#     return(image)

# def posology_ndvi(image, fos):
#     result = image.expression('b(24) >= 0.9 ? (fos * 0.7) : (b(24) >= 0.7 ? (fos * 1) : (fos * 1.1))', {'fos': fos}).rename('posology')
#     image = image.addBands(result)
#     return(image)
    
# def calculo_ndvi(image):
#     var result = image.expression(
#           "(b('b7') > hT) ? 3 : (b('b7')  > mean) ? 2 : (b('b7') < lT) ? 1 : 0 ",
#           {
#           'hT': hT ,
#           'mean': ee.Number(meanV.get('b7')),
#           'lT': lT
#           });

def fertilizer_ndvi(image):
    # result = image.expression('b(24) >= 0.9 ? (NDVI * 0.7) : (b(24) >= 0.7 ? (NDVI * 1) : (NDVI * 1.1))', {'NDVI': image.select('NDVI')}).rename('fertilizer')
    result = image.expression('b(24) >= 0.9 ? (0.7) : (b(24) >= 0.7 ? (1) : (1.1))', {'NDVI': image.select('NDVI')}).rename('fertilizer')
    image = image.addBands(result)
    return(image)

def image_to_map_id(image_name, vis_params={}):
  try:
    ee_image = ee.Image(image_name)
    map_id = ee_image.getMapId(vis_params)
    tile_url = map_id['tile_fetcher'].url_format
    return tile_url
  except EEException as e:
     logging.error('An error occurred while attempting to retrieve the map id.', e)

def get_image_collection_asset(platform, sensor, product, cloudy=None, date_from=None, date_to=None, roi=None, index=None, reducer='first'):
    """
    Get tile url for image collection asset.
    """
    ee_product = EE_PRODUCTS[platform][sensor][product]

    collection = ee_product['collection']
    # index = ee_product['index']
    vis_params = ee_product['vis_index']
            
    # collection =  ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    #     .filterDate(start_date, end_date) \
    #     .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE',coverage)) \
    #     .filterBounds(roi) \
    #     .sort('system:time_start', False) 
    
    #cloud_mask = ee_product.get('cloud_mask', None)
    try:
        # print(index)
        ee_collection = ee.ImageCollection(collection)
        
        if date_from is None:
            date_from = ee_product['start_date']
            
        if date_from and date_to:
            ee_filter_date = ee.Filter.date(date_from, date_to)
            ee_collection = ee_collection.filter(ee_filter_date)

        # if index:
            # ee_collection = ee_collection.select(index)
            
        if roi:
            ee_collection = ee_collection.filterBounds(roi)
            ee_collection = ee_collection.map(lambda image: image.clip(roi))
        
        if cloudy:
            ee_collection = ee_collection.filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE',cloudy))
        
        ee_collection = ee_collection.sort('system:time_start', False) 
        
        if reducer:
            ee_collection = getattr(ee_collection, reducer)()
            
        
        if index == 1:
            if reducer=='first':
                print(1)
                ee_collection = addDate(ee_collection)
                ee_collection = getNDVI(ee_collection)
            else:
                print(2)
                ee_collection = ee_collection.map(addDate).map(getNDVI)
            index = "NDVI"
        elif index == 2:
            if reducer=='first':
                ee_collection = addDate(ee_collection)
                ee_collection = getGNDVI(ee_collection)
            else:
                ee_collection = ee_collection.map(addDate).map(getGNDVI)
            index = "GNDVI"
        elif index == 3:
            if reducer=='first':
                ee_collection = addDate(ee_collection)
                ee_collection = getNDSI(ee_collection)
            else:
                ee_collection = ee_collection.map(addDate).map(getNDSI)
            index = "NDSI"
        elif index == 4:
            if reducer=='first':
                ee_collection = addDate(ee_collection)
                ee_collection = getReCl(ee_collection)
            else:
                ee_collection = ee_collection.map(addDate).map(getReCl)
            index = "ReCl"
        elif index == 5:
            if reducer=='first':
                ee_collection = addDate(ee_collection)
                ee_collection = getNDWI(ee_collection)
            else:
                ee_collection = ee_collection.map(addDate).map(getNDWI)
            index = "NDWI"
        else: 
            if reducer=='first':
                ee_collection = addDate(ee_collection)
                ee_collection = getNDVI(ee_collection)
                ee_collection = getNDWI(ee_collection)
                ee_collection = getCWSI(ee_collection)
            else:
                ee_collection = ee_collection.map(addDate).map(getNDVI).map(getNDWI)
                ee_collection = ee_collection.map(getCWSI)
            index = "CWSI"
            
        
       
        if reducer=='first':
            date_to = ee_collection.date().format('YYYY-MM-dd').getInfo() 
        
        '''
        if cloud_mask:
            cloud_mask_func = getattr(cm, cloud_mask, None)
            if cloud_mask_func:
                ee_collection = ee_collection.map(cloud_mask_func)
        '''
        # ee_collection = ee_collection.add_colorbar(vis_params, label=index, layer_name="Index")     
        tile_url = image_to_map_id(ee_collection.select(index), vis_params)

        return tile_url, index, date_to

    except EEException as e:
        logging.error("The following exception occured", e)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
def get_fertilizer_map(platform, sensor, product, cloudy=None, date_from=None, date_to=None, roi=None, posology=None, posology_data=None, reducer='first'):
    """
    Get tile url for image collection asset.
    """
    ee_product = EE_PRODUCTS[platform][sensor][product]

    collection = ee_product['collection']
    vis_params = ee_product['vis_fertilizer']
    # vis_params.update({'min': posology_data*1.1, 'max': posology_data*0.7})
    # vis_params.update({'min': 1.1, 'max': 0.7})
    try:
        ee_collection = ee.ImageCollection(collection)
        
        if date_from is None:
            date_from = ee_product['start_date']

        if date_to is None:
            date_to = ee_product['end_date']

        if date_from and date_to:
            print(date_from, "Start Date")
            print(date_to, "End Date")
            ee_filter_date = ee.Filter.date(date_from, date_to)
            ee_collection = ee_collection.filter(ee_filter_date)

        if roi:
            ee_collection = ee_collection.filterBounds(roi)
            ee_collection = ee_collection.map(lambda image: image.clip(roi))

        if cloudy:
            ee_collection = ee_collection.filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE',cloudy))

        ee_collection = ee_collection.sort('system:time_start', False)

        if reducer:
            ee_image = getattr(ee_collection, reducer)()

        # Posology Index added when require add more.
        # if posology is None:
        #    posology = 1;

        # if posology == 1:
            # Posology is calculated only for one image, through map function is not necessary
        ee_image = addDate(ee_image)
        ee_image = getNDVI(ee_image)
        ee_image = fertilizer_ndvi(ee_image)
        ee_image = ee_image.clip(roi)
        
        end_date = ee_image.date().format('YYYY-MM-dd').getInfo() 
        tile_url = image_to_map_id(ee_image.select('fertilizer'), vis_params)

        return tile_url, end_date

    except EEException as e:
        logging.error("The following exception occured", e)