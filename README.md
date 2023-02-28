
# Co-ccessibility and Social segregation
Calculating the demographics of the people who have access to urban amenities within 0, 5, and 15 minutes walks.

<p align="center">
    <img src="https://github.com/MiliasV/coaccessibility/blob/main/img/concept.png" width="70%">
</p>

## Research 
To learn more about the concept of co-accessibility and an application of this code look at our paper entitled "Measuring spatial age segregation through the lens of co-accessibility to urban activities"  https://doi.org/10.1016/j.compenvurbsys.2022.101829

## Code
* notebooks/collect_osm_data..ipynb --> Collecting seleted urban amenities from OSM for different cities
* notebooks/get_cbs_data.ipynb --> Collecting population data from the Netherlands (CBS - 100x100m grid), clipping and storing the data per city and computing the areas that people can access by waalking for 15 minutes based on the walkable street network of OSM.
* calculate_walkable_isochrones.py --> Calculate the 5, 10, and 15 minutes walkable environments.
* calculate_place_isochrone_intersection --> Create a mapping based on the intersection of the walkable area of each population square and the location of the urban amenities 
