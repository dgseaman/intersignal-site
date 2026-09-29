# Intersignal country map asset

`countries-110m.compact.geojson` is a self-contained GeoJSON map for an offline dashboard. It contains 177 country polygons and 28 point markers for small countries or territories that lack a polygon at this scale. The file is 179,089 bytes and needs no runtime map service or network request.

## Source and terms

- Geometry and names: [Natural Earth 1:110m Admin 0 Countries](https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/) and [Admin 0 Tiny Countries](https://www.naturalearthdata.com/downloads/110m-cultural-vectors/).
- Fetched from the Natural Earth project's [country GeoJSON](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_admin_0_countries.geojson) (Git blob `1e6ab74c7042f97013be69ceec798be8e1aff27d`) and [tiny-country GeoJSON](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_admin_0_tiny_countries.geojson) (Git blob `e468bfde3af1fbc49741fcfea938dbbdd9a9c27d`) on 2026-09-28.
- [Natural Earth's terms](https://www.naturalearthdata.com/about/terms-of-use/) place its vector map data in the public domain. Attribution is optional; “Made with Natural Earth” is their suggested short credit.

## Format and joining

- GeoJSON `FeatureCollection`, geographic longitude/latitude coordinates (CRS84).
- Every feature has a unique top-level `id` and `properties.name`, `properties.iso3`.
- `id` uses Natural Earth's `ISO_A2_EH` two-letter code where available. `XK` for Kosovo is a user-assigned code, while `CYN` and `SOL` are Natural Earth fallback codes for Northern Cyprus and Somaliland. Check these exceptions when joining to a GeoIP provider's country codes.
- `geometry.type` is `Polygon`, `MultiPolygon`, or `Point`. Draw points as small markers; they represent places too small for a polygon at this scale.
- Polygon and point coordinates are rounded to 0.01 degrees except one tiny ring retained at six decimals to avoid collapsing it. Duplicate tiny-country points were removed when a polygon already covered the same `id`.

This is a small-scale visualization asset, not a complete territorial register or a legal boundary reference. Country codes with no matching feature should remain visible in a separate table or “Other” count.
