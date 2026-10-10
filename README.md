# Bernard Shambrook’s diary

A static website containing Bernard’s portrait, all 28 diary photographs, a faithful transcription, a reading copy, a journey map and referenced service records. The photographs, scripts, styles and Leaflet library are bundled locally. OpenStreetMap supplies the online map tiles; local SVG maps are included for offline use. No accounts, external fonts, analytics, CDN or build service are required.

## Appearance

The monochrome layout follows the restrained typography and spacing of [wrenasmir.com](https://wrenasmir.com/). It opens in Light mode, with Dark and System options in the navigation. Photographs retain their original colours. On desktop the navigation is a sidebar; on phones it opens through Menu.

## View locally

Open `index.html` for the complete scrolling archive: portrait, journey, all diary pages, lists and rolls, cemetery pages, searchable people, original photographs and background records. Each leaf crop sits beside its text on desktop and above it on phones. Reading copy is the initial edition; a remembered choice takes precedence. Filters retain photograph order, and direct links reveal the target even after filtering.

The map has voyage and Palestine views, 25 source-linked entries, dated step-through controls and geographic markers. On an HTTP(S) website, Leaflet loads OpenStreetMap tiles as needed. Direct `file:` viewing, missing tiles or no JavaScript use the bundled SVG maps. No tiles are prefetched, archived or bundled. The dashed sea and solid land connections are approximate. Addresses are not plotted as visits, and undocumented legs are not joined. `journey.html` opens the same map on its own; `journey-record.html` contains exact faithful source excerpts.

For local HTTP preview, run `python3 -m http.server 8765` from this folder and open `http://localhost:8765/`. Local-file viewing remains useful without a server.

`reader.html` is the detailed single-photograph inspector, with full/left/right views, zoom, contrast and faithful text. `reading.html` is a separate continuous reader with search and print selection. `complete-transcription.html` contains both full text versions and the detailed original notes, including without JavaScript. Plain-text editions and the uncertainty register are also included.

The gallery contains all 28 complete photographs, with keyboard browsing, zoom and HEIC downloads with location metadata removed. Each image links back to its place in the scrolling diary. The portrait has its own full-resolution image and original download. No-JavaScript image links still open the full JPEGs.

`history.html` has the service record comparison and 20 numbered references. `people.html` expands the surname finding aid with exact source lines. `corrections.html` preserves the earlier faithful-text revisions and the 18 later reading-copy clarifications. `data/reading-revisions.json` records each reading change and its image or published-source evidence; these changes leave the faithful master unchanged.

## Put it on GitHub Pages

1. Create or choose a GitHub repository for the diary.
2. Upload **the contents of this folder**, including `index.html`, `diary-data.js`, `app.js`, `style.css`, `assets/`, `data/` and the other included files, to the root of its `main` branch. Do not upload just the ZIP. Retain the empty `.nojekyll` file; using Git will preserve it.
3. In the repository, open **Settings → Pages**. Under **Build and deployment**, select **Deploy from a branch**, then `main` and `/ (root)`, and save.
4. GitHub will provide the site address after deployment. The relative asset paths also work for a project site under `/repository-name/`.

The repository is [CraigWrenasmir/bernards-diary](https://github.com/CraigWrenasmir/bernards-diary). GitHub Pages publishes `main` at [craigwrenasmir.github.io/bernards-diary/](https://craigwrenasmir.github.io/bernards-diary/). Publishing makes the notebook photographs and text publicly available.

These instructions follow [GitHub’s guidance for creating a Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site) and [configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), checked on 10 October 2026.

## Correct or extend the transcription

The editable master is `data/diary.json`. Each photograph has sections containing `faithful` and `reading` text, plus editorial notes and uncertain readings. Keep meaningful uncertainty visible in both versions. Preserve substantive corrections and unresolved comparison decisions in `data/corrections.json`, which generates `corrections.html`. Describe method changes in `SOURCE-NOTES.md`.

The companion’s editable master is `data/journey.json`. Its captions and geographic identifications are editorial and do not replace the diary transcription. The supporting evidence audit and geographic research are in `data/journey-evidence.json` and `data/journey-geography.json`. Keep these records and `JOURNEY-SOURCES.md` in step with substantive changes.

After editing the JSON, run `python3 build.py` from this folder. Python is needed only for regeneration, not for viewing or hosting. The script updates `diary-data.js`, the two downloadable text editions, the complete HTML edition and `uncertain-readings.tsv`. Upload the changed files together.

The same command also rebuilds the companion maps, chronology, reader data, photograph gallery, continuous reader, names index, history and editorial reference pages. `data/history.json` contains historical claims, citations and the limits of each source. `data/people-terms.json` contains editable name finding terms; exact occurrences are regenerated from the faithful text. `references.html` combines the method and geography notes into a readable page. The companion builder checks that quoted passages still match the faithful text. If you correct a passage quoted by the companion, update its evidence and caption as part of the same correction.

`data/source-manifest.json` records the diary photographs’ original HEIC filenames and SHA-256 hashes, plus hashes of the web conversions. `data/portrait.json` records the portrait’s attribution, original file and derivatives. All 29 HEIC images are included in `assets/originals/` with GPS/location metadata removed for publication, without recompressing the image data. The manifests record separate checksums for the supplied originals and the public downloads. The owner’s supplied files remain unchanged locally. Full-resolution JPEGs support browser viewing, while smaller, uncropped gallery and portrait derivatives keep the page responsive. Including the original files increases the package size.

## Files

- `index.html`, `archive.css`, `archive.js`, `build-archive.py`: the scrolling archive.
- `reader.html`, `app.js`: detailed single-photograph inspector.
- `reading.html`, `people.html`, `edition.css`, `edition.js`, `build-edition.py`: continuous reader and source-linked name finding aid.
- `enhancements.css`, `monochrome.css`, `preferences.js`: shared appearance, responsive navigation, reading preferences and accessible controls.
- `history.html`, `history.css`, `build-history.py`, `data/history.json`: historical context and source bibliography.
- `references.html`, `corrections.html`, `data/corrections.json`: source method and revision record.
- `data/people-terms.json`, `data/people-index.json`: name search terms and generated occurrences.
- `assets/crops/`, `crop-data.js`, `data/source-crops.json`: inspected left/right viewing crops and their provenance.
- `gallery.css`, `gallery.js`, `build-gallery.py`: the photograph gallery, enlargement controls and optional gallery regeneration.
- `portrait.css`, `data/portrait.json`: portrait layout, attribution and checksums.
- `diary-data.js`: generated reader content, also works when opened directly from disk.
- `data/diary.json`: editable transcription master.
- `data/source-manifest.json`: provenance and photograph checksums.
- `assets/photos/`: full-resolution photographs converted to JPEG.
- `assets/thumbs/`: lightweight navigation images.
- `assets/gallery/`: uncropped gallery previews, at most 800 pixels on the longest side.
- `assets/portrait/`: full-resolution and smaller viewing copies of Bernard’s portrait.
- `assets/originals/`: HEIC copies of all 28 diary photographs and the portrait, with location metadata removed.
- `complete-transcription.html`: full printable transcription in both versions.
- `faithful-transcription.txt`, `reading-copy.txt`: plain-text editions.
- `uncertain-readings.tsv`: review register, opens in a spreadsheet or text editor.
- `SOURCE-NOTES.md`: editorial method and limitations.
- `build.py`: optional regeneration script.
- `journey.html`, `map.js`, `map.css`, `build-map.py`, `data/map-routes.json`: geographic map and dated entries.
- `assets/vendor/leaflet/`: Leaflet 1.9.4, its licence and provenance.
- `data/history-summary.json`: concise cited records and additional sources.
- `data/reading-revisions.json`, `data/page-reading-notes.json`: reading-copy revisions and concise page notes.
- `journey-record.html`, `journey-chronology.tsv`: printable evidence and spreadsheet-friendly chronology.
- `assets/maps/`: two standalone SVG maps; `assets/companion/`: reduced, uncropped gallery photographs.
- `build-journey.py`: companion regeneration script, also called by `build.py`; uses the included Natural Earth `data/map-land.geojson` without network access.
- `JOURNEY-SOURCES.md`: geographic citations, uncertainty and map decisions.
- `.nojekyll`: serves the static files without Jekyll processing.

This family archive package does not assert a new copyright licence for the notebook or the photographs. Craig supplied the photographs and confirmed permission to transcribe them.
