"""Documented literature search through the Crossref REST API (the only bibliographic index with open programmatic access here; Scopus and Web of Science were not available). Date of search is stored in the output. Records title, DOI, year, venue; screening is done afterwards by title/abstract with the inclusion rules in results/litsearch/PROTOCOL.md."""
import json, urllib.parse, urllib.request, datetime, time
Q = {
 "Q1": "steganography genetic algorithm pixel selection LSB",
 "Q2": "steganography particle swarm optimization embedding location LSB",
 "Q3": "metaheuristic optimization pixel selection image steganography security steganalysis",
 "Q4": "LSB PVD hybrid steganography genetic algorithm",
 "Q5": "steganography medical image optimization steganalysis",
 "Q6": "steganalysis brain MRI deep learning",
 "Q7": "content-adaptive steganography random key comparison optimized embedding location steganalysis SRM",
 "Q8": "evolutionary algorithm embedding path LSB matching steganalysis resistance",
}
out = {"date": datetime.date.today().isoformat(), "index": "Crossref REST API, field query.bibliographic, rows=60, filter from-pub-date:2010-01-01,type:journal-article|proceedings-article", "queries": {}}
for k, q in Q.items():
    items = []
    for typ in ("journal-article", "proceedings-article"):
        url = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query.bibliographic": q, "rows": 60, "filter": f"from-pub-date:2010-01-01,type:{typ}", "select": "DOI,title,issued,container-title,type"})
        try: items += json.load(urllib.request.urlopen(url, timeout=40))["message"]["items"]
        except Exception as e: print(k, typ, "ERR", e)
        time.sleep(1)
    out["queries"][k] = dict(query=q, n=len(items), records=[dict(doi=i.get("DOI"), title=(i.get("title") or [""])[0], year=(i.get("issued", {}).get("date-parts") or [[None]])[0][0], venue=(i.get("container-title") or [""])[0]) for i in items])
    print(k, len(items))
json.dump(out, open("results/litsearch/crossref_raw.json", "w"), indent=1)
