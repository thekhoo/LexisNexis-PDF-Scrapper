from enum import unique
import os
import json
from sys import stdout
import PyPDF2
import logging
import regex as re

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_BREAK

from typing import List

class Logger:
    
    def __init__(self) -> None:
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)

        handler = logging.StreamHandler(stdout)
        handler.setLevel(logging.INFO)
        self.log.addHandler(handler)

    def logInfo(self,text:str) -> None:
        self.log.info(text)

class General:

    """
    This class is built to handle potential issues that could be faced by different PDFs throughout Lexis Library.
    """

    def __init__(self) -> None:
        pass

    def removeNewLine(self,raw_text:str) -> List[str]:

        """
        Remove the newline character '\n' within the PDF text
        """

        linespace_regex = r'[\.;:]\n'                           # Regex to identify linespaces to be kept (New line after full stop etc.)
        delimiter_arr = re.findall(linespace_regex,raw_text)    # Getting an array of delimeters that should be kept
        text_arr = re.split(linespace_regex,raw_text)           # Getting an array of text to be rejoined to the delimiters
        
        text_arr_formatted = [s.replace('\n','') for s in text_arr]             # Replace '\n' with '' in the text array
        delimiter_arr_formatted = [s.replace('\n','') for s in delimiter_arr]   # Replace '\n' with '' in the delimiter array
        
        text_delim_zip = zip(text_arr_formatted,delimiter_arr_formatted)    # Zip both arrays together to form a dictionary
        
        # Using tuple unpacking, get the text and delimiter rejoined in an array where there should be a line break for every element within this array.
        text_arr = []
        for text, delimiter in text_delim_zip:
            text_arr.append(text + delimiter)
        
        return text_arr

class ProcedurePDF(General):

    """
    Class to handle a SINGLE (.pdf) file from the Procedure (Part D) from Blackstone's Criminal Practice 2022 from Lexis Library
    """

    def __init__(self,filename:str) -> None:
        self.filename = filename
        self.pdf_text = self._getPDFText()
        self.pdf_dict = self._getTextDict()

    def getSections(self,sections:List[int]) -> dict:
        """
        Returns a dictionary of the sections that are entered as a list of integers in this function.
        """
        all_section_dict = {}
        
        # Loop through all the section numbers provided
        for section in sections:
            key = f"{self.filename}.{section}"                      # Get the Section Heading
            section_text = self.removeNewLine(self.pdf_dict[key])   # Use the Section heading as the key and remove newline characters

            all_section_dict.update({key: section_text})    # Update the main dictionary with the section dictionary
        
        return all_section_dict

    # Get's the PDF file and converts the text into a string
    def _getPDFText(self) -> str:
        """
        Get all the text from the PDF file in a single string.
        """
        # Open the File
        filepath = os.path.join('data',f'{self.filename}.pdf')

        try:
            file = open(filepath,'rb')
        except FileNotFoundError:
            print('We cannot find the file that you are looking for. Please try again.')
            return None
        else:
            # Create Reader Object
            reader = PyPDF2.PdfFileReader(file)

            # Get the Text
            text = ''

            for i in range(reader.numPages):
                page = reader.getPage(i)                # Get the Current Page
                current_text = page.extract_text()      # Extract the text from the current page
                text += current_text                    # Append to master 'text' variable

            file.close()
            
            return text

    # Converts a string of text into a dictionary based on sections (i.e. D5.4)
    def _getTextDict(self) -> dict:
        """
        Splits the text by section to create a dictionary with each section as the key.
        """

        if self.pdf_text == None:
            return None

        section_regex = re.escape(self.filename) + r'\.\d{1,3}\n'       # Create a regex to idenfity section headers (i.e. D4.52)
        section_headers = re.findall(section_regex,self.pdf_text)       # Gets all the section headers
        section_text = re.split(section_regex,self.pdf_text)            # Gets all the text for the section headers

        sections = [s.strip('\n') for s in section_headers]             # Remove the linespace character from the section headers
        section_text.pop(0)                                             # Remove the first element in the section_text array (Before D#.1)    
        pdf_dict = dict(zip(sections,section_text))                     # Create a dictionary of the section headers and text
        
        return pdf_dict

class Topic:

    """
    This class is built to handle each topic that is given and the respective sections that need to be referenced for this particular topic. One topic can reference from multiple files.
    """

    def __init__(self,topic:str,data:dict) -> None:
        self.topic = topic                              # Topic Number [str]
        self.data = data                                # Topic Data [dict]
        self.title = data['title']                      # Topic Title [str]
        self.sections_data = data['sections']           # Topic Sections and Subsections [dict]
        self.sections = self.sections_data.keys()       # Topic Sections [List[str]]

class DocxWriter:

    """
    This class handles the writing of the information to a word document.
    """

    def __init__(self,data:dict) -> None:
        self.doc = Document()
        self.doc_title = data['doc_title']  # Title of the document to be saved.
        self.doc_data = data['doc_data']    # Data dictionary of the topics and respective sections and subsections to extract.

        self.topics = []        # "List[Topic]"" - List of topic objects
        self.pdfs = {}          # "dict" - Dictionary of section and the PDFs (key: "[section]" as str | item: "[pdf_str]" as str)

    def createDocument(self) -> int:
        """
        Generates a document based on the data that is passed into the object.
        """

        # << Get Topics and PDFs >>
        if self._getTopicsAndPDFs() != 0:
            return self._getTopicsAndPDFs() # Error with generating topics and PDFs, refer to ._getTopicsAndPDFs()

        # << Write the Data for Topics >>
        for topic in self.topics:
            if self._writeTopicData(topic) != 0:
                return self._writeTopicData(topic) # Error with writing topic to word file, refer to ._writeTopicData()

            # Add a Page Break unless it's the last topic
            if topic != self.topics[-1]:
                self.doc.add_page_break()

        # Save the Document
        self.doc.save(f'output/{self.doc_title}.docx')

        # Return with Code 0 - Successful Generation of Document
        return 0

    def _writeTopicData(self,topic:Topic) -> int:
        logging.info(f'[Writing]: Writing data for {topic.topic}: {topic.title}')

        # Add the Topic Number and Topic Title as a "Title"
        self.doc.add_heading(f"{topic.topic}",level=0)
        self.doc.add_heading(f"{topic.title}",level=1)

        topic_data = {}

        # Iterate through the Sections and Subsections
        for section, subsections in topic.sections_data.items():
            logging.info(f"[Writing]: Getting PDF for {section}")
            pdf = self.pdfs[section]

            section_dict = pdf.getSections(subsections)
            topic_data.update(section_dict)

        for section_heading, section_text in topic_data.items():

            # Writing the Section as a Level 1 Heading
            self.doc.add_heading(section_heading,level=2)

            # Writing the text data to the document
            for text_item in section_text:
                para = self.doc.add_paragraph(text_item)
                para.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
                para.paragraph_format.space_after = Pt(6)

        return 0

    def _getTopicsAndPDFs(self) -> int:
        """
        Fills the pdfs and topics property of this class.
        """
        sections = []

        for topic_name, topic_data in self.doc_data.items():
            # key: Topic # [str]
            # items: Topic Data [dict]
            
            topic = Topic(topic_name,topic_data)    # Create Topic Object
            self.topics.append(topic)               # Append Topic Object to Topic Array

            sections += topic.sections              # Get all the sections for the topic

        unique_sections = list(set(sections))       # Convert the list for all the sections into a unique list so no repetitions

        if self._getPDFObjects(unique_sections) != 0:               # Update self.pdfs 
            return 1                                                # Return 1 for unsuccessful PDF conversion

        return 0
    
    def _getPDFObjects(self,unique_sections:List[str]) -> int:

        for section in unique_sections:
            logging.info(f'[PDFs]: Loading PDF for {section}')
            current_pdf = {section: ProcedurePDF(section)}
            self.pdfs.update(current_pdf)

        logging.info("<< ALL PDF FILES LOADED >>")

        return 0

if __name__ == '__main__':

    # Handling the Logger
    log = Logger()

    with open('topics.json') as f:
        log.logInfo('Loading JSON Data.')
        data = json.load(f)
    
    writer = DocxWriter(data)
    writer.createDocument()