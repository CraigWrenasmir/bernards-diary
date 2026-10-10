# Journey: sources and editorial decisions

Prepared 10 October 2026. The journey companion is an interpretation of the photographed notebook, with external sources used for geographic identification. It does not change the faithful transcription or supply missing handwriting.

## What the map means

- **Recorded movement:** a readable arrival, departure or passing statement in the notebook. This is diary evidence, not independent proof of every event.
- **Tentative destination:** an uncertain reading such as [Rehovoth?], plotted conditionally. “Left for” does not establish arrival.
- **Drawing or note:** a labelled sketch or dated heading, not proof of a visit. Jerusalem has no visit date; Gaza’s sketch date remains [22/6/41?].
- **No pin:** Kilo 89 and Romani are retained in the chronology, but no trustworthy exact locality point was established here. Other unlocated notes remain unlocated.

All pins indicate approximate port or town/locality areas, not Bernard’s exact position, berth, station, camp, cemetery or viewpoint. The distinction matters especially at Gaza, Julis and Jerusalem. The map uses rounded WGS84 coordinates. It is an illustrative archive guide, not a navigational map.

The outward-voyage curves are drawn for legibility and sequence. Their control points are graphic choices, not evidence of a ship’s course. They must not be used for distance or speed calculations. No lines join the later gaps. The main regional map leaves the canal and railway positions as reference points rather than tracing infrastructure that was not reconstructed.

“Palestine” follows the historical context of the notebook. Modern, generalised coastlines are used without political boundaries. Town and port identifications do not assert modern borders or sovereignty.

## Chronology and omissions

`data/journey-evidence.json` contains a full source-text audit with movement records, contextual records, exact excerpts, conflict notes and excluded categories. The 25 entries in `data/journey.json` group closely related arrivals/departures and incorporate selected contextual notes. `journey-record.html` exposes each included entry’s passages and photograph links without JavaScript.

The displayed Suez arrival follows the repeated 3 May statements. The adjacent Saturday/Sunday wording, inserted 4th and much fainter [7/5/41?] inside-cover note remain unresolved. The 7 May Gaza arrival and the same-day Kilo 89 note are distinct; their connecting movement is not described. The 25 May destination remains tentative. The 4 August departure gives no destination. The Gaza heading has a disputed month: 23 June or 23 September 1941. It is retained as an uncertain dated heading, not an arrival statement, and is not made into a certain September journey stop.

The June 12 service/order note has an inferred year and an uncertain date association. A 20 July pencil line, a 21 July funeral note and the 9/10 August note do not securely locate Bernard. News about the Syrian armistice, another man’s death date, memorial dates from 1917–1918, Australian addresses and personnel lists have not been converted into journey stops.

The gallery uses reduced, uncropped versions of three supplied photographs. Its headings and captions are editorial. No lettering or missing drawing content was reconstructed.

## Coastline and city reference data

The included `data/map-land.geojson` is Natural Earth’s 1:50m land data, obtained from the project author’s repository. The builder clips and projects these polygons to make the two SVG maps. Natural Earth makes this data public domain.

- [Natural Earth land dataset](https://www.naturalearthdata.com/downloads/50m-physical-vectors/50m-land/)
- [Natural Earth terms of use](https://www.naturalearthdata.com/about/terms-of-use/)
- [Source GeoJSON in the Natural Earth repository](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_50m_land.geojson)
- [Natural Earth populated places](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_10m_populated_places_simple.geojson): general city references for Gaza (31.53 N, 34.445 E) and Jerusalem (31.778 N, 35.207 E). These do not locate their cemeteries.

## Overview port references

- **Sydney:** [Port Authority of NSW’s harbour measurements](https://wavewindtide.portauthoritynsw.com.au/default) locates Fort Denison at 33°51.31′ S, 151°13.52′ E. The map uses this as a rounded harbour reference, not an embarkation berth.
- **Fremantle:** [Australian Border Force ports of entry](https://www.abf.gov.au/entering-leaving-australia/Pages/Ports-of-entry.aspx) supplies 32°3.955′ S, 115°44.760′ E. The map uses the general port area, not that modern boarding facility as Bernard’s landing point.
- **Trincomalee:** [Sri Lanka Ports Authority terminal information](https://www.slpa.lk/port-colombo/terminal-info/1000) supplies 8°33′ N, 81°13′ E. This identifies the port called TRINCOMILEE in the diary.
- **Aden:** [Port of Aden navigation data](https://www.portofaden.net/en/site/page/8/Navigation%20Data) supplies a reference at 12°44′ N, 44°57′ E near the port approaches. The diary says he passed Aden; the pin is a port reference, not a recorded ship position.

## Regional identifications

The structured research is retained in `data/journey-geography.json`, including NGA feature identifiers and queried records. NGA is the US National Geospatial-Intelligence Agency’s Geographic Names Server. A geographic name match supports identification; it does not independently establish Bernard’s presence.

### Port Tewfic / Suez

Port Tewfik / Port Tawfiq (Bur Tawfiq), at Suez and the southern Suez Canal entrance.

Approximate map reference: 29.94 N, 32.57 E. rounded settlement vicinity; not the ship anchorage, berth or 1941 landing point.

- Do not place the ship precisely at the modern shipyard. The date 4 August and place spelling remain as transcribed.

Sources:

- [US National Geospatial-Intelligence Agency (NGA): Geographic Names Server: Port Tewfik](https://geonames.nga.mil/geon-ags/rest/services/RESEARCH/GIS_OUTPUT/MapServer/0/query?where=ufi+%3D+-292713&outFields=ufi%2Cfull_name%2Clat_dd%2Clong_dd%2Cdesig_cd%2Call_names&returnGeometry=false&f=pjson)
- [Suez Canal Authority: Port Tawfik Shipyard](https://www.suezcanal.gov.eg/English/Shipyards/PTShipyard/Documents/PORTAWFIQ%20ENGLISH.pdf)

### El Kantara / Kantara East

Al Qantarah on the Suez Canal; the text explicitly mentions Kantara East.

Approximate map reference: 30.86 N, 32.32 E. rounded locality point; not the receiving depot, landing or Kantara East station.

- NGA variants combine Kantara and Kantara East; its precise point must not be treated as a 1941 east-bank station location. Use rounded town vicinity only.

Sources:

- [US National Geospatial-Intelligence Agency (NGA): Geographic Names Server: El Kantara](https://geonames.nga.mil/geon-ags/rest/services/RESEARCH/GIS_OUTPUT/MapServer/0/query?where=ufi+%3D+-290712&outFields=ufi%2Cfull_name%2Clat_dd%2Clong_dd%2Cdesig_cd%2Call_names&returnGeometry=false&f=pjson)
- [Suez Canal Authority: Rules of Navigation 2020, map page 150](https://www.suezcanal.gov.eg/FlipPDFFiles/RulesOfNavigation/files/basic-html/page150.html)

### Romani

Romani in northern Sinai, on the historic railway from Kantara towards El Arish.

No precise site pin supplied. A broad city reference may appear only where explicitly labelled.

- NGA station UFI -301357 returns latitude 31.916667 and longitude 32.663889. This lies in the Mediterranean, inconsistent with the northern-Sinai railway; reject this coordinate instead of silently correcting it. No Romani pin recommended yet.
- The nearby salt-flat record is a different feature and is not a substitute station coordinate.

Sources:

- [Australian Department of Veterans’ Affairs: Australian Light Horse—Palestine 1916–1918](https://anzacportal.dva.gov.au/resources/australian-light-horse-palestine-1916-1918)
- [US National Geospatial-Intelligence Agency (NGA): Geographic Names Server: Romani](https://geonames.nga.mil/geon-ags/rest/services/RESEARCH/GIS_OUTPUT/MapServer/0/query?where=ufi+%3D+-301357&outFields=ufi%2Cfull_name%2Clat_dd%2Clong_dd%2Cdesig_cd%2Call_names&returnGeometry=false&f=pjson)

### El Erich

Very likely El Arish (Al Arish) on the northern Sinai coast; this is an editorial identification, not a changed transcription.

Approximate map reference: 31.13 N, 33.8 E. rounded modern town point; not a located rail station.

- Preserve El Erich in quotations; label El Arish as identification. Do not infer an extended stay from passed through.

Sources:

- [US National Geospatial-Intelligence Agency (NGA): Geographic Names Server: Al ‘Arīsh](https://geonames.nga.mil/geon-ags/rest/services/RESEARCH/GIS_OUTPUT/MapServer/0/query?where=ufi+%3D+-289771&outFields=ufi%2Cfull_name%2Clat_dd%2Clong_dd%2Cdesig_cd%2Call_names&returnGeometry=false&f=pjson)
- [Australian Department of Veterans’ Affairs: Australian Light Horse—Palestine 1916–1918](https://anzacportal.dva.gov.au/resources/australian-light-horse-palestine-1916-1918)

### Kilo 89

Kilo 89 Camp, Gaza Ridge, Palestine.

No precise site pin supplied. A broad city reference may appear only where explicitly labelled.

- No precise camp position established. Gaza city coordinates must not be labelled as Kilo 89 camp.
- An AWM graves-unit index labels Kilo 89 as Egypt; contemporaneous photo catalogues and diary route support the Palestine camp. The conflicting index is not a basis for moving the pin to Egypt.

Sources:

- [Australian War Memorial: Kilo 89 Camp, Gaza Ridge, Palestine, c. December 1941 (P02480.002)](https://www.awm.gov.au/collection/C325901)
- [Australian War Memorial: Kilo 89 camp, Gaza, Palestine, 1942 (P02480.009)](https://www.awm.gov.au/collection/C325908)

### Julis / JULIUS; [Gellibrand?] lines

Southern Palestine Julis camp near Gaza, with Gellibrand one of its documented sections; locality corresponds to abandoned Julis/Julius rather than Galilee Julis.

Approximate map reference: 31.68 N, 34.65 E. rounded NGA abandoned-settlement point, used only for the surrounding locality; camp perimeter and Gellibrand Lines are unlocated.

- Gellibrand remains bracketed in the transcription; external corroboration belongs in the map annotation.
- Do not use the present-day Galilee Julis at about 32.94N,35.18E.
- Pin represents historical locality, not the exact Australian camp or lines.

Sources:

- [US National Geospatial-Intelligence Agency (NGA): Geographic Names Server: Julis](https://geonames.nga.mil/geon-ags/rest/services/RESEARCH/GIS_OUTPUT/MapServer/0/query?where=ufi+%3D+-780300&outFields=ufi%2Cfull_name%2Clat_dd%2Clong_dd%2Cdesig_cd%2Call_names&returnGeometry=false&f=pjson)
- [Australian War Memorial: To Benghazi, chapter 4](https://s3-ap-southeast-2.amazonaws.com/awm-media/collection/RCDIG1070226/document/5519524.PDF) — Printed p. 72; PDF page 3
- [Australian War Memorial: Main Tel Aviv–Gaza road through Julis Camp (023609)](https://www.awm.gov.au/collection/C7504)
- [Australian War Memorial: 2/1st Australian Infantry Battalion](https://www.awm.gov.au/collection/U56044)

### [Rehovoth?]

Probably Rehovot, with Rehovoth a documented variant; not securely identified from handwriting alone.

Approximate map reference: 31.89 N, 34.81 E. rounded modern town point; conditional identification, no camp or hospital located.

- Use an uncertain/dashed marker if plotted. Departure for a destination is not independent evidence of arrival.
- The renewed image review tentatively reads [7 AGH?]. AWM records document the 7th Australian General Hospital near Rehovot, but neither the initials nor that contextual match establish Bernard’s admission as a patient. The proposed expansion remains editorial context, not a silent change to the faithful text.

Sources:

- [US National Geospatial-Intelligence Agency (NGA): Geographic Names Server: Reẖovot](https://geonames.nga.mil/geon-ags/rest/services/RESEARCH/GIS_OUTPUT/MapServer/0/query?where=ufi+%3D+-781210&outFields=ufi%2Cfull_name%2Clat_dd%2Clong_dd%2Cdesig_cd%2Call_names&returnGeometry=false&f=pjson)
- [Australian War Memorial: 7th Australian General Hospital at Kafr Balu, near Rehovot (022693)](https://www.awm.gov.au/collection/C6754) — Hospital location only; no personal admission claim.
- [Museums Victoria: Main Street in Rehovot, 1941 (MM 129890)](https://collections.museumsvictoria.com.au/items/1918987)
- [Smithsonian National Postal Museum: Rehovoth cancelled postage stamps, 1939–1940](https://postalmuseum.si.edu/object/npm_0.270209.52.11)

### Gaza Cemetry / Gaza war cemetry

Gaza War Cemetery, supported by the explicit diary label; the specific LIV memorial identification has not been independently checked against an accessible primary image.

No precise site pin supplied. A broad city reference may appear only where explicitly labelled.

- Do not connect a cemetery sketch with a solid dated journey segment.
- City-level Gaza coordinate may be used as a clearly labelled broad reference, not a cemetery pin.
- CWGC cemetery detail webpage could not be directly verified due to HTTP 403; no coordinate taken from mirrors.
- An October 2024 CWGC report hosted by Parliament was found in search, but its PDF could not be opened (HTTP 403), so no claim about its exact contents is relied on.

Sources:

- [Australian War Memorial: Gaza War Cemetery dawn service, 25 April 1940 (007388)](https://www.awm.gov.au/collection/C28976)

### Jerusalem War Cemetery

Jerusalem War Cemetery; archival photograph directly corroborates its land-gift entrance inscription.

No precise site pin supplied. A broad city reference may appear only where explicitly labelled.

- Do not convert the sketch into a confirmed Jerusalem visit or assign a date from neighbouring photographs.
- CWGC direct page returned HTTP 403; a modern Jerusalem city point can be reference-only, not the precise cemetery.

Sources:

- [Australian War Memorial: Entrance to Jerusalem War Cemetery (H12705)](https://www.awm.gov.au/collection/H12705)
- [Australian Department of Veterans’ Affairs: Israel: Australian Memorial outside Jerusalem War Cemetery](https://www.dva.gov.au/recognition-and-commemoration/memorials/memorials-africa-and-middle-east/israel)

## Reproducibility

Run `python3 build.py` after editing the diary or companion masters. It rebuilds both readers, exports and SVG maps locally. Leaflet 1.9.4 is bundled locally. Online maps request standard raster tiles from OpenStreetMap and show its required attribution. No tiles are prefetched or bundled; local SVG maps provide the offline and no-JavaScript fallback. See the [OSM tile policy](https://operations.osmfoundation.org/policies/tiles/) and [Leaflet documentation](https://leafletjs.com/reference.html).

Natural Earth land source SHA-256: `e874b27a51d146452be360cafb3cc50c86001074a67d534113e6534682f9826b`.



## Reading-copy and map review, 10 October 2026

The newer reading-copy review identifies Rehovot / 7 AGH, Gaza Ridge / A.A.P.D., Gaza hospital and Port Tewfik, while preserving the faithful text. The map uses the reading copy for these selected quotations and labels it accordingly; the chronology retains exact faithful excerpts. Details and evidence are in `data/reading-revisions.json`. Earlier uncertainty assessments above document the original review rather than overruling these revisions. Gaza’s June/September heading remains unresolved.

The online map uses modern OpenStreetMap place labels. Dashed sea connections and solid Kantara–El Arish–Gaza connections show the sequence approximately, not a surveyed ship or railway track. Rehovot is a named destination; Jerusalem is an undated drawing. No land route to the Tel Aviv address has been inferred. The two local fallback maps use Natural Earth, as documented above.
