# davar
 An experimental interpreted international auxilliary language based on and powered by WikiData that aims to be extremely easy to translate into other languages.
 Currently, this package is a command line tool that translates a single davar statement into a given language.

## syntax
 As of right now, the syntax is very simple: all statements are in the form
 ```
 (P{A} Q{B} Q{C})
 ```
 where `Q{B}` is the first entity's WikiData identifier, `Q{C}` is the second entity's WikiData identifier, and `P{A}` is the WikiData identifier for the property corresponding to the relationship between `Q{B}` and `Q{C}`. 

 For example, to say "I am a programmer, I might write `(P31 Q3236990 Q5482740)`

## usage
 ```
 davar -l LANG DAVARTEXT
 ```
 where LANG is a two character language code and DAVARTEXT is a statement written in davar.
 this will cause errors if the `LANG` is in the wrong format or isn't available for the given WikiData item, which I will get around to handling later.


 
