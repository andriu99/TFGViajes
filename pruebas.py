import timezonefinder
tf = timezonefinder.TimezoneFinder()

timezone_str = tf.certain_timezone_at(lat=28, lng=-15.1207)
print(timezone_str)

lista=[0,1,2,3,4]
print(lista[0:2])