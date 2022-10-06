# PDF Data Scrapper for Blackstone's Criminal Practice 2022 (Part D - Procedure)

# WIP

## Introduction

**NOTE:** This tool was designed purely for Part D of the Blackstone's Criminal Practice 2022 Document from Lexis Library. The tool seems to work fine on Parts D, E, F and R from Blackstone's Criminal Practice 2022 from Lexis Library.

## How to use the tool

1. Download all the files into a folder and create a folder called `data` and `output`.

    * The `data` folder will be used to store all the PDF files downloaded from Lexis Library Blackstone's Criminal Practice 2022.
    * The `output` folder will be where all the word files are written to.

2. Create a JSON file called `topics.json` in the same directory as the `blackstone_scrapper.py` file. This will be used to tell the program which sections and subsections to scrape. The structure of the file is as follows:

    ```js

    {
        "doc_title": "",

        "doc_data": {

            "Topic Number": {

                "title": "",
                "sections": {

                    "D3": [],
                    "D4": []
                    
                }
            }
        }

    }

    ```


## File Naming Conventions

### Downloaded PDFs

Name the PDF file based on the Part and Section that it belongs to. For example:

*Part D5 - Starting a Prosecution and Preliminary Proceedings in Magistrates' Court should be named as **D5.pdf**.*

The file should be saved in a folder called `data`.

## Future Work

1. Handle key errors if a subsection outside the range of the pdf is requested.
2. Different log category classifications.
3. Introduce appropriate error codes to identify errors.
4. Update all hardcoded filepaths with `os.path.join()` for cross OS functionality.
