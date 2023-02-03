# Precision Agriculture WebApp

Web application developed for precision agriculture. 
The application will have the functionality based on a set of input 
parameters and the use of Google Earth Engine to calculate crop indices, 
sowing and harvest periods, fertilizer measurement, etc.

## Current Funcionalities
- Login
- User/Role Registration
- View registered land
- Search a location
- Extract Index
- Search by land acres (Polygon)

## Next Funcionalities
- Fertilization calendars
- Export Data

## Images

### Home Page

![](https://github.com/benitezfj/WebApp/blob/master/WebApp/static/images/home.png?raw=true)

### Role registration

![](https://github.com/benitezfj/WebApp/blob/master/WebApp/static/images/role.png?raw=true)

### New user registration

![](https://github.com/benitezfj/WebApp/blob/master/WebApp/static/images/new_user.png?raw=true)

### View of lands

![](https://github.com/benitezfj/WebApp/blob/master/WebApp/static/images/parcelas.png?raw=true)

### Login Page

![](https://github.com/benitezfj/WebApp/blob/master/WebApp/static/images/login.png?raw=true)

### Farmland registration

![](https://github.com/benitezfj/WebApp/blob/master/WebApp/static/images/farmland.png?raw=true)

### Calculate indices

![](https://github.com/benitezfj/WebApp/blob/master/WebApp/static/images/index.png?raw=true)

### Calculated Index: GNDVI (Green Normalized Difference Vegetation Index) Imagery extracted by Google Earth Engine

![](https://github.com/benitezfj/WebApp/blob/master/WebApp/static/images/index_1.png?raw=true)

### Calculated Index: CWSI (Crop Water Stress Index) Imagery extracted by Google Earth Engine

![](https://github.com/benitezfj/WebApp/blob/master/WebApp/static/images/index_2.png?raw=true)

### Fertilizer Map

![](https://github.com/benitezfj/WebApp/blob/master/WebApp/static/images/posology.png?raw=true)

![](https://github.com/benitezfj/WebApp/blob/master/WebApp/static/images/posology_1.png?raw=true)

## Install
To install the Web App, clone the repository and install the dependency:

```shell
$ git clone https://github.com/benitezfj/WebApp.git
$ cd WebApp
$ pip install -r requirements.txt
```

Then, in the folder run the project:
```shell
$ python run.py
```

## Note
Keep in mind that in order to use the Google Earth Engine (GEE), users must give 
access to GEE services to their Google account. After that, locally install 
Google Cloud (gcloud) SDK and configure it, more information [here](https://cloud.google.com/sdk/docs/configurations?hl=es-419)
and [here](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)