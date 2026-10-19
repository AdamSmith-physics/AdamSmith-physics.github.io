import re
import arxiv
from datetime import date

today = date.today()

d2 = today.strftime("%d %B %Y")

header_text = f"""
<div class="header">
    Publications
    <hr class="nameUnderline">
</div>

<p> This list was last updated on {d2}. All of my publications are available on the 
    <a href="https://arxiv.org/a/smith_a_7.html">arXiv</a> and on my 
    <a href="https://scholar.google.co.uk/citations?user=0sCuBC4AAAAJ&hl=en">Google Scholar</a> page </p>
<br>
<p> Disorder-free localization. <em>Adam Smith</em>. <a href="https://www.springer.com/gb/book/9783030208509">Springer Thesis</a>  </p>
<br>
"""

def _strip_version(arxiv_id):
    return re.sub(r"v\d+$", "", arxiv_id)


def updateArxiv(directory = ""):

    with open(directory+"papers.txt", "r") as paper_list:
        ids = [line.strip() for line in paper_list if line.strip()]

    # One batched request (instead of one per paper) avoids arXiv's HTTP 429 rate limit.
    client = arxiv.Client(page_size=100, delay_seconds=10, num_retries=5)
    search = arxiv.Search(id_list=ids, max_results=len(ids))

    try:
        results = {_strip_version(r.get_short_id()): r for r in client.results(search)}
    except arxiv.HTTPError as err:
        # Keep the existing publications.html so the site build still works.
        print(f"WARNING: arXiv request failed ({err}). Keeping existing publications.html.")
        return

    entries = []
    for arXiv_id in ids:
        clean_id = _strip_version(arXiv_id)
        result = results.get(clean_id)
        if result is None:
            print(f"WARNING: {arXiv_id} not returned by arXiv, skipping.")
            continue

        authors = [author.name for author in result.authors]
        num_authors = len(authors)
        authors = authors[:6]
        if num_authors > 6:
            authors.append("et al.")
        authors = ", ".join(authors) + "."

        entry = f'<p> <b>•</b> {result.title}.\n'
        entry += f'\t<em> {authors} </em>\n'
        if result.journal_ref:
            entry += f'\t<a href="https://doi.org/{result.doi}">{result.journal_ref}</a>\n'
        entry += f'\t<a href="https://arxiv.org/abs/{clean_id}">[arXiv:{clean_id}]</a> </p>\n\n'
        entries.append(entry)
        print(result.title)

    with open(directory+"publications.html", "w", encoding="utf-8") as publications:
        publications.write(header_text)
        publications.writelines(entries)
        publications.write("<br>\n")

    print("ArXiv updated!")

if __name__ == "__main__":
    updateArxiv()
