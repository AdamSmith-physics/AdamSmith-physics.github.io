from content.arXiv import updateArxiv

#updateArxiv(directory="content/")

header_file = open("content/header.html", "r")

header = header_file.read()
header_file.close()

footer_file = open("content/footer.html", "r")

footer = footer_file.read()
footer_file.close()


pages = [["index", "Home"], 
         ["research", "Research"], 
         ["publications", "Publications"], 
         ["group", "Group"],
         ["join", "Join Us"], 
         ["cirquit", "CirQuit"]]

for page in pages:

    # Add the header
    newFile = open(f"{page[0]}.html", "w")

    newFile.write(header)

    newFile.close()

    # add the navigation bar
    newFile = open(f"{page[0]}.html", "a")

    for link in pages:
        if link[0] == page[0]:
            newFile.write(f'<a href="{link[0]}.html" class="active">{link[1]}</a>\n')
        else:
            newFile.write(f'<a href="{link[0]}.html">{link[1]}</a>\n')

    newFile.write('\t\t</div>\n')
    newFile.write('\t</div>\n\n')
    newFile.write('\t<div class="container">\n')
    newFile.write('\t\t<div class="main">\n\n')

    # add the content
    #content = open(f"content/{page[0]}.html", "r")
    #newFile.write(content.read())
    #content.close()

    with open(f"content/{page[0]}.html", "r") as content:
        for line in content:
            newFile.write("\t\t\t" + line)

    newFile.write(footer)

    newFile.close()
