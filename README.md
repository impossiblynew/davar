# davar
 An experimental interpreted international auxilliary language based on and powered by WikiData that aims to be extremely easy to translate into other languages.
 Currently, this package is a command line tool that describes a series of davar statements in a given language.

## Purpose
Currently there is no reliable way to communicate cross-linguistically. Machine translation tries to solve this, but often runs into fundamental issues explained well [here](https://youtu.be/GAgp7nXdkLU). Rather than by solving that with a constructed auxilliary language like Esperanto or Volapük, *davar* aims to solve this by creating a notation for simple statements that is language-neutral, and that a computer can easily describe[[1](#footnote1)] in any language. This is achieved through the minimization of grammar and use of WikiData as a source of translation strings.

## Syntax
The basic building blocks of davar are *Nodes* and *Rels*:

***Nodes*** represent WikiData items and are written as WikiData item identifiers, in the form `Q#`, where `#` can be a number of any length. For example, [`Q42`](https://www.wikidata.org/wiki/Q42) is Douglas Adams.

***Rels*** represent WikiData properties, and are written as WikiData property identifiers, in the form `P#` where `#` can be a number of any length. For example, [`P828`](https://www.wikidata.org/wiki/Property:P828) represents the property of causing something.

These can be combined to make *Statements*, of which there are currently three types:
### Singleton Statement
Singleton statements are the most basic type of statement:
```
(Subject)
```
Where `Subject` is either a Node or another Statement. This statement is not very meaningful, but means something along the lines of "`Subject` exists". For example, `(Q2013)` will be described in English as `WikiData.`, which can be understood as "consider WikiData" or "WikiData exists."

### Edge
Edges are statements that connect an `Subject` to an `Object`:
```
(Subject Object)
```
Where `Subject` and `Object` can either be a Node or a Statement. This statement encodes an unspecified relationship between the `Subject` and the `Object`. For example, `(Q2 Q5)` will be described in English as `Earth → human` which can be understood as "there is a relationship between Earth and humans" or "At Earth, there are humans".

### Labeled Edge
Labeled Edges are statements that connect an `Subject` to an `Object` in a way specified by a `Relationship`:
```
(Relationship Subject Object)
```
Where `Subject` and `Object` can either be a Node or a Statement and `Relationship` is a Rel. This statement encodes a specified relationship between the `Subject` and the `Object`. For example, `(P31 Q42 Q5)` will be described in English as `Douglas Adams → human (instance of)`, which can be understood as "Douglas Adams is a human."

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

### Analogy[[2](#footnote2)]
#### davar:
```
(P460 (Q9128 Q204170) (Q11461 Q502261))
```
#### English Description:
> \[light → darkness] → \[sound → silence] (said to be the same as).

#### Meaning:
> The relationship between light and darkness is the same as the relationship between sound and silence.

or

> light is to darkness as sound is to silence

### Fiction:
#### davar:
```
(Q192630 (P69 Q3236990 Q8460327))
(Q193168 (P108 Q3236990 Q2599656))
```
#### English Description:
> past → \[self → Unseen University (educated at)].

> present → \[self → Twoflower (employer)].

#### Meaning:
> In the past I went to Unseen University. Now I am employed by Twoflower.

 ## Usage
To describe a string of davar in a language, use
 ```
 python -m davar DAVARTEXT -l LANG
 ```
where LANG is a two character language code and DAVARTEXT is a string consisting of statements written in davar. This will cause errors if the `LANG` is in the wrong format or isn't available for the given WikiData item, which I will get around to handling later.


## Footnotes
<a name="footnote1">1</a>: We call it *describing* rather than *translating* because the output is not anything close to natural language. Rather, it is a mix of symbols and words that conveys the relationships described in the corresponding davar statements.

<a name="footnote2">2</a>: You may notice that [`P460`](https://www.wikidata.org/wiki/Property:P460) does not represent being "the same as", and instead is labeled as "is said to be the same as". This is because there is no WikiData Property for being the same as something else, as it is far to vague to be useful in a database such as WikiData. This lack of subjective or abstract properties is a fundamental problem with using WikiData as a source, and I am exploring a number of solutions to it.
