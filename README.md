# social_cities

### Accessibility and Social segregation
Calculating  15 minutes walking accessibility of urban amenities while accounting for the demographics of the people who have access to the same resources.

*** Code
* notebooks/collect_osm_data..ipynb --> Collecting seleted urban amenities from OSM for different cities
* notebooks/age_pois..ipynb --> Collecting population data from the Netherlands (CBS - 100x100m grid), clipping and storing the data per city and computing the areas that people can access by waalking for 15 minutes based on the walkable street network of OSM.
* calculate_place_isochrone_intersection --> Create a mapping based on the intersection of the walkable area of each population square and the location of the urban amenities 
