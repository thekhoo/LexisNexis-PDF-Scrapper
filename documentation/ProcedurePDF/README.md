## `class` ProcedurePDF(filename)
* **filename : `str`**, *the PDF filename*

A PDF file object with functions specific to the scrapping of Blackstone's Criminal Practice 2022 - Part D Procedure.

> **Update:** The program seems to work for Sections D, E, F and R for Blackstone's Criminal Practice 2022. Other sections have not been tested.

### 🔸 .pdf_text
```py
ProcedurePDF.pdf_text -> str
```

The raw text for the entire PDF file.

### 🔸 .pdf_dict
```py
ProcedurePDF.pdf_dict -> dict
```

A dictionary of the PDF file separated by subsections as the keys.

```py
{
    "[subsection]": {
        "section_heading": "str",
        "section_subheading": "str",
        "section_text": [List[int]]
    }
}
```

### 🔸 .SECTION_MAIN_HEADING
```py
ProcedurePDF.SECTION_MAIN_HEADING -> str
```

A string constant - "section_heading".


### 🔸 .SECTION_SUB_HEADING
```py
ProcedurePDF.SECTION_SUB_HEADING -> str
```

A string constant - "section_subheading".


### 🔸 .SECTION_TEXT
```py
ProcedurePDF.SECTION_TEXT -> str
```

A string constant - "section_text".


### 🔹 .getSections()
```py
ProcedurePDF.getSections(
     sections : List[int]

) -> dict
```
* **sections : `List[int]`**
*List of subsections in int form.*

Returns a dictionary of the sections that are entered as a list of integers in this function.

```py
{
    "[subsection]": {
        "section_heading": "str",
        "section_subheading": "str",
        "section_text": [List[int]]
    },
    .
    .
    .
}
```

### 🔹 ._getPDFText()
```py
ProcedurePDF._getPDFText() -> str
```
Get all the text from the PDF file in a single string.

### 🔹 ._getPDFDict()
```py
ProcedurePDF._getPDFDict() -> dict
```
Splits the text by section to create a dictionary with each section as the key to another dictionary holding the main heading, subheading, and text.

```py
# Data in this format.
{
    "[subsection]": {
        "section_heading": "str",
        "section_subheading": "str",
        "section_text": [List[int]]
    }
}
```

### 🔹 ._getSectionDict()
```py
ProcedurePDF._getSectionDict(
     subsection : str,
     main_heading : str,
     sub_heading : str,
     subsection_text : List[str]

) -> dict
```
* **subsection : `str`**
*The subsection that will be used as a key for the dictionary.*

* **main_heading : `str`**
*The main heading for this subsection.*

* **sub_heading : `str`**
*The subheading for this subsection.*

* **subsection_text : `List[str]`**
*The array of text that is contained under this subsection.*

Creates a dictionary with the data in the required format to be added to the final PDF dictionary. 

**Data Output Format:**
```py
# Data in this format.
{
    "[subsection]": {
        "section_heading": "str",
        "section_subheading": "str",
        "section_text": [List[int]]
    }
}
```

### 🔹 ._formatSectionText()
```py
ProcedurePDF._formatSectionText(
     text : str,
     page_heading : str

) -> List[str]
```

* **text : `str`**
*Raw text for the subsection from the PDF before being cleaned.*

* **page_heading : `str`**
*The heading that's on the current page of the PDF file.*

Removes any occurrences of the page heading within the text and removes newline characters as deemed appropriate. For more information, look at the documentation for the function `ProcedurePDF._removePageHeadingInText()` and `General.removeNewLine()`.

### 🔹 ._getPageHeading()
```py
ProcedurePDF._getPageHeading(
     page_data : List[str]

) -> str
```

* **page_data : List[str]**
*The text array on the current page split by "Blackstone's Criminal Practice 2022".*

Gets the page heading from an array containing the page data that has already been split with "Blackstone's Criminal Procedure 2022". There's only one occurrence of "Blackstone's Criminal Practice 2022" on each page and the page heading will always be before this. Therefore, the page heading is always the first element in the array.

> **NOTE:** The term 'page' used in the explanation refers to the content between one 'End of Document' and the subsequent 'End of Document' found within the PDF.

### 🔹 ._isPageHeadingUpper()
```py
ProcedurePDF._isPageHeadingUpper(
     heading : str

) -> bool
```

* **heading : str**
*The current page heading.*

Checks if a large portion of the heading is in capital letters. This is because some headings that include sections will have a lower case 's' or numbers. If more than 80% of the characters are upper case, this will be considered as a main heading and return True.

### 🔹 ._getPageText()
```py
ProcedurePDF._getPageText(
     page_data : List[str]

) -> str
```

* **page_data : List[str]**
*The text array on the current page split by "Blackstone's Criminal Practice 2022".*

Gets the page text from an array containing the page data that has already been split with "Blackstone's Criminal Procedure 2022". There's only one occurrence of "Blackstone's Criminal Practice 2022" on each page and the page heading will always be before this. Therefore, the page heading is always the first element in the array.

> **NOTE:** The term 'page' used in the explanation refers to the content between one 'End of Document' and the subsequent 'End of Document' found within the PDF.

### 🔹 ._getPageSections()
```py
ProcedurePDF._getPageSections(
     regex : str,
     text : str

) -> List[str]
```

* **regex : str**
*The regex used to identify subsections within the text (i.e. D5.32)*

* **text : str**
*The text on the current page without the page heading.*

Gets the list of sections that are in the page text.

```py
# The regex used to identify the sections.
# The sections can go up to 3 numbers.
section_regex = re.escape(self.filename) + r'\.\d{1,3}\n'
```
> To avoid confusion with normal section references within the text, the regex is programmed to look for a newline character '\n' as all these section headings are standalone with the text for the section starting on a new line.

### 🔹 ._getPageSectionTexts()
```py
ProcedurePDF._getPageSectionTexts(
     regex : str,
     text : str

) -> List[str]
```

* **regex : str**
*The regex used to identify subsections within the text (i.e. D5.32)*

* **text : str**
*The text on the current page without the page heading.*

Gets the list of section texts that are in the page text.

> The PDF is structured in a way where there is some text before the first section heading on the page. This text is a visual indicator to inform the user which section and subsection they're currently in. This information will be the first item in the text array when it is split by section and should be removed. **This results in a section array and section text array that are the same length.** 

> **See Also:** `ProcedurePDF._getPageSections()` for the section array.

```py
# The regex used to identify the sections.
# The sections can go up to 3 numbers.
section_regex = re.escape(self.filename) + r'\.\d{1,3}\n'
```
> To avoid confusion with normal section references within the text, the regex is programmed to look for a newline character '\n' as all these section headings are standalone with the text for the section starting on a new line.

### 🔹 ._splitTextByEOD()
```py
ProcedurePDF._splitTextByEOD() -> List[str]
```

Splits a string of text by the "End of Document" string into a List of strings.

> No text is required to be passed into this function because it references the property of the class `self.pdf_text`.

```py
# The regex used to identify "End of Document".
eod_regex = r"End\sof\sDocument"
```

### 🔹 ._splitPageContentByBlackstone()
```py
ProcedurePDF._splitPageContenttByBlackstone(
     page : str

) -> List[str]
```

Splits a string of text by the "Blackstone's Criminal Practice 2022" string into a List of strings.

```py
# The regex used to identify "Blackstone's Criminal Practice 2022".
title_regex = r"\nBlackstone's\sCriminal\sPractice\s2022"
```

### 🔹 ._removePageHeadingInText()
```py
ProcedurePDF._removePageHeadingInText(
     text : str,
     heading : str

) -> str
```

Removes any occurrences of the page heading followed by a newline character within the text. 

> For documents *(Sections between the phrase "End of Document")* that are longer than one page, the page heading is repeated at the top of the page. When scraping the PDF file, this will end up in the section text and has to be removed using this function.

### 🔹 ._removeNewLine()
```py
ProcedurePDF._removeNewLine(
     text : str

) -> List[str]
```

Identifies newline characters that are appropriately placed and removes all other newline characters '\n'. 

> **Why this is required:** The issue with scraping the text is that the newline characters in the original PDF do not match up with the newline characters that should be implemented in the word document due to the difference in formatting. This results in choppy text. 

> **How it works:** Using regex pattern matching, the newline characters that are preceded by a period (.), a dash (-), a colon (:), a semicolon (;), the phrase "or", and the phrase "and" will be kept as these are likely to be the end of bullet points or paragraphs. The rest of the newline characters are removed. 

The string will be separated by these 'correct' newline characters into an array. Two arrays will be generated using `re.findall()` and `re.split()`. This will be the `delimiter_arr` and `text_arr` respectively.

The text within the `text_arr` array will have its newline characters removed. Due to how the `docx` module works, the array of 'correct' newline characters in `delimiter_arr` will also have the '\n' part removed.

The `text_arr` and `delimiter_arr` are then zipped and appended together into one List of strings where each item within that list will be a paragraph or bullet points on its own. The function `.add_paragraph()` within the `docx` module will be used to add a linebreak between each item within this array.

```py
# The regex used to identify newline characters that should be kept in place.
linespace_regex = r'[\.;:—]\n|or\n|and\n'
```