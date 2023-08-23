import arxiv

with open("papers.txt", "r") as paper_list:

    for arXiv_id in paper_list:
        print(arXiv_id.replace("\n", ""))

        clean_id = arXiv_id.replace("\n", "")

        search = arxiv.Search(
            query = f'id:{clean_id}',
            max_results = 1,
            sort_by = arxiv.SortCriterion.SubmittedDate
        )

        for result in search.results():
            title = result.title
            authors = result.authors
            journal = result.journal_ref
            doi = result.doi

            print(title)
            print(authors)
            print(journal)
            print(doi)
