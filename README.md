# aiblog
Stuff for the blog at blog.ai.ovgu.de. This is just a repo/backup -- it doesn't 
actually host the site.


## Basic use
- do `npm install` in the main folder do get the required node modules or 
whatever (you need `npm` for this obviously)
- write your markdown text in `draft.md`
- write header info into `draft_header.html`
- write appendix into `draft_appendix.md`
- put bibliography into `draft_bib.html`
- run `./make` to compile everything into an index.html that you can use 
whichever way you want!
- obviously you can (have to!) adapt file paths to your needs -- this is just an
example
- a runnable example/template is in the `example` folder
- note that the "real" posts have different relative paths for the javascripts
in their HTML header than the example!
- note also that as stuff is set up right now, your working directory needs
to be the one with `make` in it!
- the navigation site is in `nav`, however the generated html will need to
be in the main folder to work properly


## Acknowledgements
The template/format is that used by [Distill](distill.pub). The precise 
implementation used here has been adapted from the 
[World Models github page](https://github.com/worldmodels/worldmodels.github.io).
