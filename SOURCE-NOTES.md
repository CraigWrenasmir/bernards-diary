# Source and editorial notes

## Scope and attribution

Craig supplied 28 HEIC photographs of a notebook and identifies the writer as his great-grandfather, **Bernard Shambrook**. He confirmed that he has permission to have it transcribed. His initial dating was the 1940s, probably in connection with the Second World War. The notebook itself contains explicitly dated 1941 entries, as well as names, numbers, addresses, practical notes and drawings. Some copied inscriptions contain earlier dates; those are retained in their photographed positions.

The photographs run from `IMG_0903.HEIC` to `IMG_0935.HEIC`, with deliberate gaps at `IMG_0909` and `IMG_0918`–`IMG_0921`. Craig confirmed that the supplied set comprises all the intended photographs. The website preserves filename order. It does not claim that the physical notebook is paginated, chronologically arranged or free of missing original leaves.

The front and back covers are included. Each photograph is treated as one navigation item, with left/right page or other section labels where appropriate. Website titles, photograph numbers, section labels, drawing descriptions and editorial notes are editorial additions.

Craig separately supplied `IMG_0569.heic` and identified the pictured man as Bernard. This portrait accompanies the introduction and is not counted among the 28 diary photographs. Its date and location were not supplied. No military unit, rank or portrait date has been inferred from the photograph.

## How the text was prepared

Full-resolution photographs were visually read, with enlarged crops and deterministic greyscale/contrast adjustments where useful. Each photograph received a first transcription and a separate second visual check. Disagreements were compared against the image; a reading was left tentative when the strokes did not resolve it. Repeated names and parallel passages elsewhere in the notebook helped comparison, but one entry was not silently replaced by another. Review status is recorded per photograph in `data/diary.json`.

The photographs remain the source of record. Faded pencil, hurried abbreviations, small digits, overwritten text, damaged paper and show-through limit what can be recovered. Unresolved writing remains marked; gaps have not been filled from historical expectation.

External military and genealogical records are documented separately in the Historical records page and `data/history.json`. They provide corroboration and context for selected names, numbers and events; the remaining names and numbers have not all been independently authenticated. External expectation is not used to fill unreadable writing. Official catalogue descriptions, inspected documents and secondary sources are explicitly distinguished. The GitHub documentation used for hosting instructions is unrelated to the interpretation of the notebook.

## Faithful transcription

The faithful text retains the visible wording, spelling, capitals, abbreviations, numbers and line breaks as closely as they can be read. It is a visual text transcription, not a typographic facsimile: precise spacing, letter forms, baselines, underlining and placement remain visible in the photographs. Punctuation and word boundaries can themselves be uncertain.

- `[word?]`: a tentative reading.
- `[illegible]`, sometimes with an approximate extent: writing that could not be recovered securely.
- `[deleted: text]`: readable cancelled wording; cancelled unreadable text is marked as such.
- `[inserted: text]`: writing inserted above or between lines.
- `[drawing: …]`, `[blank]` and other descriptive brackets: editorial observations, not words attributed to Bernard.

Reverse-side show-through or mirrored transfer marks are not treated as new front-page text. Where text appears to be obscured by another object or damaged paper, it is not reconstructed. Dates, numbers, names and abbreviations are not silently harmonised across pages.

## Reading copy

The reading copy lightly modernises spelling and punctuation, joins prose lines and clarifies the presentation of lists and dates. Securely identified names and places use their standard spelling; these changes, and readings clarified by parallel entries, are documented in `data/reading-revisions.json`. The faithful text remains unchanged by these reading-copy revisions. It keeps unresolved words and digits marked and preserves substantive information. Readable cancelled wording remains in the faithful copy and is normally omitted from the reading copy. Military abbreviations are generally retained rather than expanded from assumption.

The reading copy is not a summary or historical retelling. Where a faded passage cannot be made into a complete sentence without invention, the gap remains visible.

## Photographs and provenance

Original HEIC files were kept unchanged. Working PNG conversions and inspection crops are separate from the website. No generative restoration, invented lettering, retouching or inpainting was used.

The website includes full-resolution JPEG conversions with embedded image orientation normalised, saved at quality 96 without chroma subsampling. These JPEGs are high-quality viewing derivatives, not byte-identical replacements for the original HEICs. Navigation thumbnails, a smaller cover image and uncropped gallery previews (at most 800 pixels on the longest side) are separate derivatives. The portrait has a full-resolution JPEG and an uncropped 840 × 1120 viewing copy. No restoration, retouching or colourisation was applied to the portrait. The on-screen contrast control applies a temporary display filter; it does not change the stored photograph.

`data/source-manifest.json` records each diary photograph’s original filename, original byte count and SHA-256 checksum, derivative dimensions, web-image path and derivative checksum. `data/portrait.json` separately records the portrait’s attribution, checksums, dimensions and conversion method. The website bundles copies of all 29 HEIC images in `assets/originals/`, linked from the gallery and portrait. GPS/location metadata was removed for publication, without recompressing the image data. The manifests record `originalDownloadSHA256` for these public copies separately from `sourceSHA256` for the supplied originals. The owner’s source files remain unchanged locally.

## Comparison review and finding aids

The comparison edition adds a continuous reading page, editorial theme filters, a searchable surname finding aid, and a dated correction register. Independent readings were considered against the supplied photographs rather than adopted for fluency. The register includes corrected readings and disputes deliberately left open.

The people index is generated from exact lines in the faithful master. Surname headings are search groups, not assertions that all occurrences identify one person. Different initials and spellings remain visible; uncertain name readings remain bracketed. The source order is retained in the continuous reader, including when a theme is selected.

Light (the default), Dark and System appearance choices change the surrounding interface, never the stored photographs. The reader and continuous reading page share a saved text-version preference where local browser storage is available.

## Review and future corrections

The scrolling archive and `journey.html` include a geographic map and dated entries. The archive also has selected lists, cemetery pages and the original-photo gallery. It draws on external geographic sources to locate names, separately from transcribing them. Those sources and the limits of each identification are documented in `JOURNEY-SOURCES.md`. Geographic identifications do not replace the wording of the notebook. During the comparison review, image-supported corrections were made to both text editions and their dependent journey excerpts; these changes are documented in `data/corrections.json` and the Editorial revisions page. Dates in memorial inscriptions, addresses and other people’s records are not treated as Bernard’s movements. Sketches and dated headings have distinct labels from arrivals and departures. Rehovot and 7 AGH have been identified in the reading-copy review; the entry records a departure for that destination. Unrecorded travel between later notes is not filled in. Gallery reproductions are reduced, uncropped versions of the supplied photographs. The reader also offers 28 deterministic left/right crops from 14 visually inspected spreads. These crops include a narrow overlap at the fold, use the existing upright JPEG derivatives, and do not change lettering or geometry. Their rectangles and source dimensions are recorded in `data/source-crops.json`; the complete photographs remain available beside them.

The full text and uncertainty register are available as `faithful-transcription.txt`, `reading-copy.txt` and `uncertain-readings.tsv`. The register groups related uncertainties; it is not an error count or a numerical measure of accuracy. The inline brackets in the transcription are the more detailed record of unresolved text.

To correct a reading, compare the word with the photograph and with other instances of the writer’s letter forms. Edit `data/diary.json`, retaining uncertainty when needed, and regenerate the readable files with `python3 build.py`. If later family knowledge or external historical evidence resolves a name, record that evidence separately from what is directly legible.

Prepared 10 October 2026 for Craig. The public edition is hosted through the Bernard’s Diary GitHub Pages repository.
