# Generic Brute Force McKeeman Form Grammar Parser
McKeeman form is a simplified Backus-Naur Form notation for expression grammars.

This repo has a recursive descent parser for validating arbitrary grammars specified in McKeeman form, and an example McKeeman form validator. It makes use of generators to retain state when trying invalid parses. It's way too slow to be practical at all, but I thought it was kind of interesting since I could't find any brute force top down parser examples online.

### Usage
To test it out, try
```console
python3 mckeeman_validator.py input.txt
```

To specify your own grammar see validator.py. (It's easy to produce grammars from the parser as well, but it's too slow to even parse the McKeeman form grammar itself lol)
