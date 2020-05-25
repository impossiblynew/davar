[<img src="https://upload.wikimedia.org/wikipedia/commons/2/20/Wikidata_stamp_rec.png" alt="Powered by Wikidata." width="150" height="41"/>](https://www.wikidata.org)
and by [Open Multilingual Wordnet](http://compling.hss.ntu.edu.sg/omw/)

0.2.0: Added Open Multilingual Wordnet synset as node type and as rel type
# davar

 An experimental interpreted international auxilliary language that aims to be extremely easy to translate into other languages, through the use of external databases (currently [Wikidata](https://www.wikidata.org) and [Open Multilingual Wordnet](http://compling.hss.ntu.edu.sg/omw/)) for translation strings and very minimal grammar.
This package contains both a class for containing writing in davar and describing[[1]](#footnote1) it in other languages and a command line tool which can do the same. 

## Purpose

Currently there is no reliable way to communicate cross-linguistically. Machine translation tries to solve this, but often runs into fundamental issues explained well [here](https://youtu.be/GAgp7nXdkLU). Rather than by solving that with a constructed auxilliary language like Esperanto or Volapük, *davar* aims to solve this by creating a notation for simple statements that is language-neutral, and that a computer can easily describe in any language. This is achieved through the minimization of grammar and use of external data sets as a source of translation strings.

## Syntax

The basic building blocks of davar are *Nodes* and *Rels*:

### Nodes
**Nodes** represent items or ideas, and can currently be **Wikidata items**, **Open Multilingual Wordnet (OMW) synsets**, or davar statements, which will be explained later. 
- **Wikidata items** are written with Wikidata item identifiers, ex: [`Q42`](https://www.wikidata.org/wiki/Q42).
- **OMW synsets** are written using a WordNet locator and offset, ex: [`02084071-n`](http://compling.hss.ntu.edu.sg/omw/cgi-bin/wn-gridx.cgi?usrname=&gridmode=grid&synset=02084071-n&lang=eng&lang2=eng). 

### Rels
Rels represent a specific type of relationship that can be had between nodes, and can currently either be **Wikidata properties** or **OMW synsets**. *Note that OMW synsets can be both nodes and rels, to allow for flexibility. This may be changed in later releases of davar.*
- **Wikidata properties** are written as Wikidata property identifiers, ex: [ `P828` ](https://www.wikidata.org/wiki/Property:P828)
 
Wikidata item and properties can be found by searching [Wikidata](https://www.wikidata.org), and OMW synsets can be found on the [OMW search interface](http://compling.hss.ntu.edu.sg/omw/cgi-bin/wn-gridx.cgi?gridmode=grid).

Nodes and rels can be combined to make *Statements*, of which there are currently three types:

### Singleton Statement

Singleton statements are the most basic type of statement:

``` 
(Subject)
```

where `Subject` is either a Node or another Statement. This statement is not very meaningful, but means something along the lines of " `Subject` exists". For example, `(Q2013)` will be described in English as `Wikidata.` , which can be understood as "consider Wikidata" or "Wikidata exists."

### Edge

Edges are statements that connect an `Subject` to an `Object` :

``` 
(Subject Object)
```

where `Subject` and `Object` can either be a Node or a Statement. This statement encodes an unspecified relationship between the `Subject` and the `Object` . For example, `(Q2 00217728-a)` will be described in English as `Earth → beautiful` which can be understood as "there is a relationship between Earth and beauty" or "Earth is beautiful".

### Labeled Edge

Labeled Edges are statements that connect an `Subject` to an `Object` in a way specified by a `Relationship` :

``` 
(Relationship Subject Object)
```

where `Subject` and `Object` can either be a Node or a Statement and `Relationship` is a Rel. This statement encodes a specified relationship between the `Subject` and the `Object` . For example, `(P31 Q42 Q5)` will be described in English as `Douglas Adams → human (instance of)` , which can be understood as "Douglas Adams is a human."

*Note that statements can themselves be nodes in other statements: `(Subject1 (Relationship Object Subject2))` is a valid construction.* 

## Examples

Some examples of more complex davar writing:

### Self-Description

#### davar:

``` 
(Q28865 (P31 Q3236990 Q5482740))
```

#### English Description:

> Python → \[self → programmer (instance of)\]

#### Meaning:

> When it comes to Python, I am a programmer.

or

> I am a python programmer.

### Analogy

#### davar:

``` 
(02664769-v (Q9128 Q204170) (Q11461 Q502261))
```

#### English Description:

> \[light → darkness] → \[sound → silence] (equal).

#### Meaning:

> The relationship between light and darkness is the same as the relationship between sound and silence.

or

> light is to darkness as sound is to silence

### Fiction:

#### davar:

``` 
(00060632-r (02612762-v Q3236990 Q8460327))
(00048475-r (P108 Q3236990 Q2599656))
```

#### English Description:

> previously → \[self → Unseen University (attend)].

> nowadays → \[self → Twoflower (employer)].

#### Meaning:

> In the past I went to Unseen University. Now I am employed by Twoflower.

## Usage

*Note: On first run of either the command line tool or the package, around 100mb of data will be downloaded to `./nltk_data` in order to allow OMW to be used.*

### Command Line Tool

To describe a string of davar in a language, use
 
``` 
 python -m davar DAVARTEXT -l LANG
 ```

where LANG is a two character language code and DAVARTEXT is a string consisting of statements written in davar. This will cause errors if the `LANG` is in the wrong format or isn't available for the given Wikidata item, which I will get around to handling later.

### Package

To change a string of davar into a `Davar` object, use `d = Davar.from_davartext(davartext)` . Then, to describe the `Davar` object in a readable language, use `d.describe(lang)` where `lang` is a string containing a two character language code. 

## Footnotes

<a name="footnote1">1</a>: We call it *describing* rather than *translating* because the output is not anything close to natural language. Rather, it is a mix of symbols and words that conveys the relationships described in the corresponding davar statements.

## Citations:
Powered by Wikidata.

```citation
Francis Bond and Kyonghee Paik (2012)
    A survey of wordnets and their licenses In Proceedings of the 6th Global WordNet Conference (GWC 2012). Matsue. 64–71
Francis Bond and Ryan Foster (2013)
    Linking and extending an open multilingual wordnet. In 51st Annual Meeting of the Association for Computational Linguistics: ACL-2013. Sofia. 1352–1362 
```
