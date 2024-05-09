-- Sql script that lists all bands with Glam rock as their style,
-- ranked by their longevity
-- Column names must be: band_name & lifespan

SELECT band_name, (2022 - year_formed - (2022 - year_disbanded)) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC
