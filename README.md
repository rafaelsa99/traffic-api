# Traffic Monitoring API
REST API for traffic monitoring.

Traffic monitoring is done for road segments and, for each of them, measurements of the average speed of vehicles at a given instant are stored and the respective level of intensity and characterization of the traffic is determined.

## Installation
The deployment of the application and database is done using Docker. Therefore, it is necessary to setup docker before installing the application.

1. Clone the project from GitHub
  ```bash
git clone git@github.com:rafaelsa99/traffic-api.git
   ```
2. Create a virtual environment
  ```bash
mkvirtualenv --python=/usr/bin/python3 traffic_api
workon traffic_api
   ```
3. Build the containers
  ```bash
cd traffic-api/traffic_api/
docker-compose build
   ```
4. Run the containers
  ```bash
docker-compose up
   ```
 
 Once the containers are running, the API is available at: http://localhost:8000/
 
 **NOTE**: Default Admin user is ``admin`` (with pw: ``admin``)
 
 ## Tests
A Postman collection is available with test requests for testing the API endpoints.

For this, the file [Traffic REST API.postman_collection.json](Traffic%20REST%20API.postman_collection.json) must be imported into Postman.

## File Upload
The file [traffic_speed.csv](traffic_speed.csv) serves as a source of sample data for the API.

To load the provided file, an endpoint was created in the API that reads the file and, for each row, creates the corresponding road segment and speed measurement, determining the traffic characterization.

*NOTE: Some anomalies were detected in the Long_end, Lat_end and Length columns. It was considered that the Long_end column corresponds to Lat_end, the Lat_end column corresponds to Length, and the Length column corresponds to Long_end.*
