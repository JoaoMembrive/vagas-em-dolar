"""VagasEmDolar.com.br (nome provisório) - agrega vagas remotas abertas a brasileiros e gera site estático.
Fontes: Remotive API e RemoteOK API (gratuitas, exigem atribuição + link para a vaga original; não bloquear vagas atrás de cadastro)."""
import json, re, html, datetime, urllib.request, pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "site"
UA = {"User-Agent": "VagasEmDolarBot/0.1 (+contato pendente)"}
OK_LOC = re.compile(r"worldwide|anywhere|global|latam|latin america|south america|americas|brazil|brasil", re.I)
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r: return json.load(r)
def remotive():
    for j in get("https://remotive.com/api/remote-jobs").get("jobs", []):
        yield dict(t=j["title"], c=j["company_name"], loc=j.get("candidate_required_location",""), sal=j.get("salary",""),
                   cat=j.get("category",""), url=j["url"], date=j.get("publication_date","")[:10], src="Remotive")
def remoteok():
    for j in get("https://remoteok.com/api")[1:]:
        yield dict(t=j.get("position",""), c=j.get("company",""), loc=j.get("location","") or "Worldwide",
                   sal=f"US$ {j['salary_min']:,}–{j['salary_max']:,}" if j.get("salary_min") else "",
                   cat=", ".join(j.get("tags",[])[:3]), url=j.get("url",""), date=j.get("date","")[:10], src="Remote OK")
def collect():
    jobs=[]
    for f in (remotive, remoteok):
        try: jobs += [j for j in f() if OK_LOC.search(j["loc"] or "")]
        except Exception as e: print("fonte falhou", f.__name__, e)
    seen=set(); out=[]
    for j in sorted(jobs, key=lambda x:x["date"], reverse=True):
        k=(j["t"].lower(), j["c"].lower())
        if k not in seen: seen.add(k); out.append(j)
    return out
def card(j):
    e=html.escape
    return f'<li><a href="{e(j["url"])}" target="_blank" rel="noopener"><b>{e(j["t"])}</b></a> — {e(j["c"])}<br><small>📍 {e(j["loc"])} · {e(j["cat"])} {("· 💵 "+e(j["sal"])) if j["sal"] else ""} · {e(j["date"])} · via {e(j["src"])}</small></li>'
def render(jobs):
    now=datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    tpl=(OUT.parent/"src/template.html").read_text()
    OUT.mkdir(exist_ok=True)
    (OUT/"index.html").write_text(tpl.replace("{{N}}",str(len(jobs))).replace("{{NOW}}",now).replace("{{JOBS}}","\n".join(map(card,jobs))))
    (OUT/"jobs.json").write_text(json.dumps(jobs,ensure_ascii=False,indent=1))
    top=jobs[:15]
    (OUT/"newsletter.md").write_text(f"# Vagas em Dólar — edição {now}\n\n{len(jobs)} vagas remotas abertas a brasileiros esta semana. Top 15:\n\n"+
        "\n".join(f"- **{j['t']}** — {j['c']} ({j['loc']}) {j['sal']} → {j['url']} (via {j['src']})" for j in top)+"\n")
if __name__=="__main__":
    j=collect(); render(j); print(len(j),"vagas")
