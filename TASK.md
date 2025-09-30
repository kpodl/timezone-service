Create a microservice that has the following endpoint

/timezones
** Delivers all available timezones
/timezones?lat=y&lon=x
** Deliver timezone for specified coordinate given a geographic latitude/longitude in EPSG:4326 coordinate reference system


As a data source the timezone world shapefile from http://efele.net/maps/tz/world/ should be used.
The endpoint shall return a meaningful timezones for uninhabited zones.

The microservice shall be developed in python and be install/runnable on ubuntu 24.04, ideally containerized.
You can use any frameworks/libraries you desire.