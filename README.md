
# Co-accessibility and Spatial segregation
### How could we assess how accessible a given destination is to people from different demographics (i.e., co-accessibility)?
This repo contains code for calculating the demographics of people who can walk to urban amenities in 5, 10, and 15 minutes.

If you prefer a visual representation of this concept check out [CTwalk Map](https://miliasv.github.io/CTwalkMap/info_page/), an interactive web tool that maps co-accessibility for the five most populous cities in the Netherlands.

<p align="center">
    <img src="https://github.com/MiliasV/coaccessibility/blob/main/img/poster.png" width="60%">
</p>

If you use the code or data shared in this repo in your work, please cite the journal article:

[Milias, V., & Psyllidis, A. (2022). Measuring spatial age segregation through the lens of co-accessibility to urban activities. Computers, Environment and Urban Systems, 95, 101829](https://doi.org/10.1016/j.compenvurbsys.2022.101829)

## Data
Under the data folder you can find data related to co-accessibility for urban amenities located in one of the five most populous Dutch cities: Amsterdam, Rotterdam, The Hague, and Eindhoven. To learn more about this data look at our paper.

### Structure of the data
| Geometry       | osm_id | children (0_15) | children_perc | adults (16_64)| adults_perc | elderly (65+)| elderly_perc |total_pop | age_entropy_index |wijk_age_entropy_index | buurt_age_entropy_index
| :---        |    :----   |          :--- |            :--- |    :--- |    :--- |  :--- |    :--- |     :--- | :--- | :--- | :--- | 
| EPSG:4326   | id of place from OpenStreetMap | Number of children who have access  | Percentage of children among the people who have access | Number of adults who have access | Percentage of adults among the people who have access | Number of elderly | Percentage of elderly among the people who have access | Total number of people who have access | age diversity of the people who have access | age diversity of the people who live in the same neighborhood (based on wijk) | age diversity of the people who live in the same neighborhood (based on buurt)

## Code
Currently, the code uses a PostgreSQL database enriched with the PostGIS add-on to store and query the data. 
Adaptations are needed to use the code with other type of files (e.g., CSV).

* notebooks/collect_osm_data..ipynb --> Collecting seleted urban amenities from OSM for different cities
* notebooks/get_cbs_data.ipynb --> Collecting population data from the Netherlands (CBS - 100x100m grid), clipping and storing the data per city and computing the areas that people can access by waalking for 15 minutes based on the walkable street network of OSM.
* calculate_walkable_isochrones.py --> Calculate the 5, 10, and 15 minutes walkable environments.
* calculate_place_isochrone_intersection --> Create a mapping based on the intersection of the walkable area of each population square and the location of the urban amenities 

## Research 
To learn more about the concept of co-accessibility and how the shared code and data have been used for research look at our open access paper:   https://doi.org/10.1016/j.compenvurbsys.2022.101829

<!-- <p align="center">
    <img src="https://github.com/MiliasV/coaccessibility/blob/main/img/children_access_ex.png" width="70%">
</p>
 -->

