import requests
from PIL import Image
from io import BytesIO
import pandas as pd
from pathlib import Path


API_KEY = 'your api key here'

dLat, dLong = 0.010122000000002629, 0.013259999999988281

df = pd.read_excel('Cities500.xlsx')

no_of_cities = df.count()[0]

# check if the file exists before creating new one
my_file = Path('ImageDetails.csv')
if not(my_file.is_file()):

	image_name_list = []
	image_city = []
	image_state = []
	image_latitude = []
	image_longitude = []

	df3 = pd.DataFrame()

	df3['Image Name'] = image_name_list
	df3['City'] = image_city
	df3['State'] = image_state
	df3['Latitude'] = image_latitude
	df3['Longitude'] = image_longitude

   	df3.to_csv('ImageDetails.csv', header=True, mode='a', index=False)

no_of_cities = 100

for city_no in range(no_of_cities):

	print("-------------------------- started city = ",city_no)

	image_name_list = []
	image_city = []
	image_state = []
	image_latitude = []
	image_longitude = []

	image_count = 0

	scale = df.Scale[city_no]
	Lat0 = df.Latitude[city_no]
	Long0 = df.Longitude[city_no]
	LatLong0 = str(Lat0) + ','+str(Long0)

	Lat1 = Lat0 + scale*dLat
	Long1 = Long0 - scale*dLong
	LatLong1 = str(Lat1) + ','+str(Long1)

	for i in range(int(scale+1)):
	for j in range(int(scale+1)):

		Lati = Lat1 - i*dLat
		Longi = Long1 + j*dLong
		LatLongi = str(Lati) + ','+str(Longi)

		image_name_list.append('city_no_'+ str(city_no) +'_image_number_'+str(image_count))
		image_count = image_count + 1
		image_city.append(df.City[city_no])
		image_state.append(df.State[city_no])
		image_latitude.append(Lati)
		image_longitude.append(Longi)

		##############################################################################################

		roadmap_url = 'https://maps.googleapis.com/maps/api/staticmap?zoom=16&size=620x640&scale=2&maptype=roadmap&center='+LatLongi+'&key='+API_KEY

		response = requests.get(roadmap_url)            
		im = Image.open(BytesIO(response.content))
		image_name = 'city_no_'+ str(city_no) +'_roadmap_image_'+str(image_count)
		im.save('roadmap-images/'+image_name+'.png')

		##############################################################################################

		satellite_url = 'https://maps.googleapis.com/maps/api/staticmap?zoom=16&size=620x640&scale=2&maptype=satellite&center='+LatLongi+'&key='+API_KEY

		response = requests.get(satellite_url)
		im = Image.open(BytesIO(response.content))
		image_name = 'city_no_'+ str(city_no) +'_satellite_image_'+str(image_count)
		im.save('satellite-images/'+image_name+'.png')

		print("city_no = ", city_no," image_no = ", image_count)
	    
	print("-------------------------- finished city = ",city_no)


	df3 = pd.DataFrame()

	df3['Image Name'] = image_name_list
	df3['City'] = image_city
	df3['State'] = image_state
	df3['Latitude'] = image_latitude
	df3['Longitude'] = image_longitude
	df3.to_csv('ImageDetails.csv', header=True, mode='a', index=False)






