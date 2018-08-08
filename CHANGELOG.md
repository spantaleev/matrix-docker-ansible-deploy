# 2018-08-08


## Docker container linking

Changed the way the Docker containers are linked together. The ones that need to communicate with others operate in a `matrix` network now and not in the default bridge network.