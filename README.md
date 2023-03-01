
# Co-ccessibility and Social segregation
### How could we measure how accessible a given destination is to individuals from different population groups (i.e. co-accessibility)?

This repo contains code to calculate the demographics of the people who have access to urban amenities within 0, 5, and 15 minutes walks.

<p align="center">
    <img src="https://github.com/MiliasV/coaccessibility/blob/main/img/meth.jpg" width="46%">
    <img src="https://github.com/MiliasV/coaccessibility/blob/main/img/concept.png" width="30%">
</p>

## Research 
To learn more about the concept of co-accessibility and how this code has been used for research look at our paper entitled "Measuring spatial age segregation through the lens of co-accessibility to urban activities"  https://doi.org/10.1016/j.compenvurbsys.2022.101829

<p align="center">
    <img src="https://github.com/MiliasV/coaccessibility/blob/main/img/children_access_per_location.jpg" width="50%">
</p>

## Data
Under the data folder you can find data relatred to co-accessibility for urban amenities locations in one of the five most populous Dutch cities: Amsterdam, Rotterdam, The Hague, and Eindhoven.

The structure of the data is the following:
| Geometry       | osm_id | children_(0-15) | children_perc | adults_(16-64)| adults_perc | elderly_(65+)| elderly_perc |total_pop | age_entropy_index |wijk_age_entropy_index | buurt_age_entropy_index
| :---        |    :----   |          :--- |            :--- |    :--- |    :--- |  :--- |    :--- |     :--- | :--- | :--- | :--- | 
| EPSG:4326   | id of place from OpenStreetMap | Number of children who have access  | Percentage of children among the people who have access | Number of adults who have access | Percentage of adults among the people who have access | Number of elderly | Percentage of elderly among the people who have access | Total number of people who have access | age diversity of theh people who have access | age diversity of the people who live in that neighborhood (based on wijk) | age diversity of the people who live in the same neighborhood (based on buurt)

## Code
Currently, the code uses a PostgreSQL database enriched with the PostGIS add-on to store and query the data. 
Adaptations are needed to use the code with other type of files (e.g., CSV).

* notebooks/collect_osm_data..ipynb --> Collecting seleted urban amenities from OSM for different cities
* notebooks/get_cbs_data.ipynb --> Collecting population data from the Netherlands (CBS - 100x100m grid), clipping and storing the data per city and computing the areas that people can access by waalking for 15 minutes based on the walkable street network of OSM.
* calculate_walkable_isochrones.py --> Calculate the 5, 10, and 15 minutes walkable environments.
* calculate_place_isochrone_intersection --> Create a mapping based on the intersection of the walkable area of each population square and the location of the urban amenities 
