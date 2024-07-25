# SLDA-data-preprossor

By accepting multiple articles, it produces two files describing each aritcles statistics.

## Output Data format

### Data file

Under LDA, the words of each document are assumed exchangeable.  Thus,
each document is succinctly represented as a sparse vector of word
counts. The data is a file where each line is of the form:

     [M] [term_1]:[count] [term_2]:[count] ...  [term_N]:[count]
     ....

where [M] is the number of unique terms in the document, and the
[count] associated with each term is how many times that term appeared
in the document.  Note that [term_1] is an integer which indexes the
term; it is not a string.

### Label file
Each line contains a `true_narrative` value for the article.

```
1
1
2
...
```

## Input

### A json file with one or more articles with following format:

```json
[
    {
        "title": "Title",
        "body": "Content",
        "true_narrative": 1
    },
    ...
]
```

### Non-stop words 
(vocab.txt is provided for reference only)

```
hello
world
...
```

## Usage

`python3 process.py [json file path] [non-stop words path] [output directory]`

e.g. `python3 ./sample.json ./vocab.txt ./output`
