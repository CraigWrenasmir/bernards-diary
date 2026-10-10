"""Regenerate the companion maps, reader data and plain chronology; standard library only."""
from pathlib import Path
import json
import math
import html
import csv

ROOT = Path(__file__).resolve().parent
esc = html.escape

def projector(bounds):
    west, south, east, north = bounds
    c = math.cos(math.radians((south+north)/2))
    scale = min(920 / ((east-west)*c), 535 / (north-south))
    return lambda lon, lat: (500+(lon-(west+east)/2)*c*scale, 305+((south+north)/2-lat)*scale)

def clip_ring(ring, bounds):
    pts = ring[:-1] if ring[0] == ring[-1] else ring
    for axis, edge, lower in [(0,bounds[0],True),(0,bounds[2],False),(1,bounds[1],True),(1,bounds[3],False)]:
        result=[]
        if not pts: break
        for start,end in zip(pts[-1:]+pts[:-1],pts):
            a = start[axis] >= edge if lower else start[axis] <= edge
            b = end[axis] >= edge if lower else end[axis] <= edge
            if a != b:
                ratio=(edge-start[axis])/(end[axis]-start[axis])
                result.append([start[0]+ratio*(end[0]-start[0]),start[1]+ratio*(end[1]-start[1])])
            if b: result.append(end)
        pts=result
    return pts

def map_svg(key, config, places, land):
    bounds=config['bounds']; project=projector(bounds)
    svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 630" role="img">',f'<title>{esc(config["description"])}</title>',
        '<desc>Bernard Shambrook’s diary. Approximate reference places, not exact personal positions. Coastline: Natural Earth. No political boundaries. Dashed lines, where shown, are schematic sequence connections.</desc>',
        '<rect width="1000" height="630" fill="#f0f0f0"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#222222}.place{font-size:21px;font-weight:600;paint-order:stroke;stroke:#fafafa;stroke-width:5px;stroke-linejoin:round}.sub{font-size:15px;fill:#666666}.region{font-size:21px;letter-spacing:4px;fill:#777777}.grid{fill:none;stroke:#dddddd;stroke-width:1}.coast{fill:#fafafa;stroke:#aaaaaa;stroke-width:.8}.route{fill:none;stroke:#666666;stroke-width:2.6;stroke-dasharray:6 8;stroke-linecap:round}</style>']
    west,south,east,north=bounds
    step=20 if key=='voyage' else 1
    for lon in range(math.ceil(west/step)*step,math.floor(east/step)*step+1,step):
        x1,y1=project(lon,south);x2,y2=project(lon,north)
        svg.append(f'<path class="grid" d="M{x1:.2f},{y1:.2f} L{x2:.2f},{y2:.2f}"/>')
    for lat in range(math.ceil(south/step)*step,math.floor(north/step)*step+1,step):
        x1,y1=project(west,lat);x2,y2=project(east,lat)
        svg.append(f'<path class="grid" d="M{x1:.2f},{y1:.2f} L{x2:.2f},{y2:.2f}"/>')
    for feature in land['features']:
        geom=feature['geometry']; polys=[geom['coordinates']] if geom['type']=='Polygon' else geom['coordinates']
        for polygon in polys:
            paths=[]
            for ring in polygon:
                pts=clip_ring(ring,bounds)
                out=[]
                for lon,lat in pts:
                    p=project(lon,lat)
                    if not out or math.dist(p,out[-1])>.65:out.append(p)
                if len(out)>2: paths.append('M'+' L'.join(f'{x:.2f},{y:.2f}' for x,y in out)+' Z')
            if paths:svg.append(f'<path class="coast" fill-rule="evenodd" d="{" ".join(paths)}"/>')
    if key=='voyage':
        # These control points are graphic layout guides, never claimed ship positions.
        for coords in [[(151.225,-33.855),(158,-49),(119,-49),(115.746,-32.066)],[(115.746,-32.066),(103,-34),(82,-15),(81.217,8.55)],[(81.217,8.55),(79,-4),(55,-1),(44.95,12.733)],[(44.95,12.733),(41,12),(35,26),(32.57,29.94)]]:
            p=[project(*c) for c in coords]
            svg.append('<path class="route" d="M'+f'{p[0][0]:.2f},{p[0][1]:.2f} C'+' '.join(f'{x:.2f},{y:.2f}' for x,y in p[1:])+'"/>')
        regions=[('AUSTRALIA',132,-24),('INDIAN OCEAN',71,-24)]
    else:
        regions=[('MEDITERRANEAN',32.6,32.45),('SEA',32.6,32.2),('SINAI',33.45,30.05)]
    for name,lon,lat in regions:
        x,y=project(lon,lat);svg.append(f'<text class="region" x="{x:.1f}" y="{y:.1f}" text-anchor="middle">{esc(name)}</text>')
    for pin in config['pins']:
        place=places[pin['place']];x,y=project(place['lon'],place['lat']);pin['x']=round(x,3);pin['y']=round(y,3)
        tx,ty=x+pin.get('dx',22),y+pin.get('dy',0)
        anchor=pin.get('anchor','start'); color='#555555' if pin.get('kind')=='uncertain' else '#222222'
        if abs(pin.get('dy',0))>35:svg.append(f'<path d="M{x:.1f},{y:.1f} L{tx:.1f},{ty:.1f}" stroke="#999999" fill="none"/>')
        if pin.get('kind')=='sketch':svg.append(f'<rect x="{x-10:.1f}" y="{y-10:.1f}" width="20" height="20" fill="#ffffff" stroke="{color}" stroke-width="2"/>')
        else:svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{color}" stroke="#ffffff" stroke-width="2"/>')
        svg.append(f'<text x="{x:.1f}" y="{y+4:.1f}" style="font-size:12px;fill:white;font-weight:bold" text-anchor="middle">{esc(pin["label"])}</text>')
        svg.append(f'<text class="place" x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}">{esc(pin.get("text",place["name"]))}</text>')
        if pin.get('date'):svg.append(f'<text class="sub" x="{tx:.1f}" y="{ty+22:.1f}" text-anchor="{anchor}">{esc(pin["date"])}</text>')
    svg.append('<text x="26" y="600" style="font-size:12px;fill:#666666">Approximate reference places · Modern coastline: Natural Earth · No political boundaries</text>')
    svg.append('<text x="26" y="619" style="font-size:12px;fill:#666666">'+('Dashed lines show sequence only; they are not recorded ship tracks.' if key=='voyage' else 'Later gaps are unconnected. Kilo 89 and Romani are recorded in the timeline without precise pins.')+'</text></svg>')
    return '\n'.join(svg)+'\n'

def main():
    data=json.loads((ROOT/'data/journey.json').read_text())
    land=json.loads((ROOT/'data/map-land.geojson').read_text())
    diary=json.loads((ROOT/'data/diary.json').read_text())
    texts={p['id']:'\n'.join(s['faithful'] for s in p['sections']) for p in diary['pages']}
    for e in data['events']:
        assert e['quote'] in texts[e['quoteSource']],(e['id'],'quote differs from source')
        for ref in e['evidence']:assert ref['excerpt'] in texts[ref['pageId']],(e['id'],ref)
    for key,config in data['maps'].items():
        (ROOT/f'assets/maps/{key}.svg').write_text(map_svg(key,config,data['places'],land))
    (ROOT/'journey-data.js').write_text('window.JOURNEY_DATA = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n')
    with (ROOT/'journey-chronology.tsv').open('w',newline='') as f:
        writer=csv.writer(f,delimiter='\t');writer.writerow(['Date label','Entry','Evidence type','Summary','Qualification','Source photographs'])
        for e in data['events']:writer.writerow([e['dateLabel'],e['title'],e['kindLabel'],e['description'],e['note'],', '.join(e['sources'])])
    out=['<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chronology — Bernard Shambrook</title><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="journey.css"><link rel="stylesheet" href="enhancements.css"><link rel="stylesheet" href="monochrome.css"><script src="preferences.js" defer></script></head><body class="journey-record"><header class="masthead"><a class="wordmark" href="index.html">Bernard Shambrook</a><nav aria-label="Main navigation"><a href="index.html">Diary</a><a href="reading.html">Reading</a><a href="index.html#scan-gallery">Photographs</a><a href="journey.html">Journey</a><a href="people.html">Names</a><a href="history.html">Records</a></nav></header><main class="complete">',
        '<h1>Chronology</h1><p class="intro-note">Dates, places and source excerpts. Memorial dates and addresses do not establish personal travel.</p><nav><a href="journey.html">Map</a><a href="index.html">Diary</a><a href="journey-chronology.tsv" download>Download chronology</a><a href="references.html">Geographic sources</a></nav>',
        '<p class="edition-note">The maps locate named places. Dashed connections show sequence, not a recovered sailing track. Use the source photographs to assess the readings; sketches and dated headings do not prove visits.</p>',
        '<img src="assets/maps/voyage.svg" alt="Schematic voyage overview from Sydney to Suez"><img src="assets/maps/regional.svg" alt="Approximate named localities in Egypt and Palestine">']
    for e in data['events']:
        out.append(f'<section class="record-entry" id="{esc(e["id"])}"><p class="eyebrow">{esc(e["dateLabel"])} · {esc(e["kindLabel"])}</p><h2>{esc(e["title"])}</h2><p>{esc(e["description"])}</p><p class="edition-note">{esc(e["note"])}</p>')
        extra_sources=set(e['sources'])-{ref['pageId'] for ref in e['evidence']}
        for sid in sorted(extra_sources):out.append(f'<p class="photo-ref">Additional source: <a href="index.html#{esc(sid)}">{esc(sid)}</a></p>')
        for ref in e['evidence']:
            out.append(f'<blockquote>{esc(ref["excerpt"])}</blockquote><p class="photo-ref"><a href="index.html#{esc(ref["pageId"])}">{esc(ref["pageId"])} — {esc(ref["section"])}</a></p>')
        out.append('</section>')
    out.append('</main></body></html>')
    (ROOT/'journey-record.html').write_text('\n'.join(out)+'\n')
    print(f'Generated two SVG maps, {len(data["events"])} companion entries and source-linked chronology.')

if __name__=='__main__':main()
