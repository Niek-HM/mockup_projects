from django.db import models

from .tagModel import Tag

import pdfplumber

class Archive(models.Model):
    """
    A list of all pdf's you can find on the website.
    To upload give a name, tag and pdf, title/description are auto generated!
    """
    name = models.CharField(max_length=64, blank=True)
    tag = models.ManyToManyField(to=Tag, blank=True)

    title = models.CharField(max_length=64, blank=True)
    description = models.TextField(max_length=512, blank=True)
    pdf = models.FileField(upload_to='archive/pdf/')

    def __str__(self):
        return self.name + ' | ' + self.title

    def save(self):
        super(Archive, self).save()
        self.title, self.description = self.extract_info()

        super(Archive, self).save()

    def extract_info(self): #TODO: Write own descriptions or improve code.
        """
        Extracts title and description from the first page of the PDF file.
        The method looks for bold text as potential titles and extracts the initial text for the description.
        """
        title, description = None, ''

        with pdfplumber.open(self.pdf.path) as pdf:
            try:
                page = pdf.pages[0] # Get the first page of the PDF
                text = page.extract_text() # Extract all text from the page

                # Find bold text which potentially indicates titles
                clean_title = page.filter(lambda obj: obj["object_type"] == "char" and "Bold" in obj["fontname"])
                titles = clean_title.extract_text().split('\n')

                # Split the text into lines
                lines = text.split('\n')
                title = titles[0]
                print(title)

                # Check for all uppercase (indicating potential headings) to build a complete title
                select = 1
                if title == title.upper():
                    while titles[select] == titles[select].upper():
                        title += ' ' + titles[select]
                        print(titles[select])
                        select += 1
                else:
                    while not titles[select].endswith('.') or not titles[select].endswith(')'):
                        title += ' ' + titles[select]
                        print(titles[select])
                        select += 1

                # Extract description from the text, skipping lines that are part of the title
                for line in lines[1:]:
                    if description == '' and line in title: continue
                    elif line not in title:
                        if line.upper() == line: break
                        description += line + ' '
            except IndexError:
                # Fallback in case of errors or if no text is extracted
                description = ''
                title = self.pdf.name.split('/')[-1]

        # Fallback for short or missing titles
        if title.__len__() < 10: title = self.pdf.name.split('/')[-1]

        # Return the extracted or fallback title and description, truncated to fit the field lengths
        return title[:64], description[:512]