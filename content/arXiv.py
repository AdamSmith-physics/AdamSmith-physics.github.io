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

def updateArxiv(directory = ""):

    with open(directory+"publications.html", "w") as publications:
        publications.write(header_text)
    
    paper_list = open(directory+"papers.txt", "r")

    with open(directory+"publications.html", "a") as publications:
        for arXiv_id in paper_list:

            clean_id = arXiv_id.replace("\n", "")
            print(clean_id)

            search = arxiv.Search(
                query = f'id:{clean_id}',
                max_results = 1,
                sort_by = arxiv.SortCriterion.SubmittedDate
            )

            for result in search.results():
                title = result.title

                authors = [author.name for author in result.authors]
                num_authors = len(authors)
                authors = authors[:6]
                if num_authors > 6:
                    authors.append("et al.")
                authors = ", ".join(authors) + "."

                journal = result.journal_ref
                doi = result.doi

                publications.write(f'<p> <b>•</b> {title}.\n')

                publications.write(f'\t<em> {authors} </em>\n')

                if journal:
                    publications.write(f'\t<a href="https://doi.org/{doi}">{journal}</a>\n')

                publications.write(f'\t<a href="https://arxiv.org/abs/{clean_id}">[arXiv:{clean_id}]</a> </p>\n\n')

                print(title)
                print(authors)
                print(journal)
                print(doi)

        publications.write('<br>\n')

if __name__ == "__main__":
    updateArxiv()
