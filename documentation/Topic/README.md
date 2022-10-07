## `class` Topic
A topic object to handle each topic found within `topics.json`. This object will contain the data that will be passed on to the `DocxWriter` class to write the data into the word document.

### 🔸 .topic
```py
Topic.topic -> str
```

The topic header for this topic. *(i.e. Topic 2)*

### 🔸 .data
```py
Topic.data -> dict
```

The data for this topic in a dictionary. Consists of:
* The topic title
* The sections required under this topic
* The subsections required under this topic

```py
dict({
     "title" : "",
     "sections" : {
          "[sub_section_one]" : [],
          "[sub_section_two]" : [],
          .
          .
          .
     }
})
```

### 🔸 .title
```py
Topic.title -> str
```
The title of this topic.

### 🔸 .sections_data
```py
Topic.sections_data -> dict
```

The dictionary for sections and subsections related to this topic.

```py
dict({
     "[sub_section_one]" : [],
     "[sub_section_two]" : [],
     .
     .
     .
})
```

### 🔸 .sections
```py
Topic.data -> List[str]
```

The list of sections that will be used for this topic.