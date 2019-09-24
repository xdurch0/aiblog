# aiblog
Stuff for the blog at blog.ai.ovgu.de. This is just a repo/backup -- it doesn't actually host the site.


## Basic use
- do `npm install` in the main folder do get the required node modules or whatever (you need `npm` for this obviously)
- write your markdown text in `draft.md`
- write header info into `draft_header.html`
- write appendix into `draft_appendix.md`
- put bibliography into `draft_bib.html`
- run `bin/make` to compile everything into an index.html that you can use whichever way you want!
- you can also use `bin/make_noapp` if you don't want/need an appendix/bibliography
- obviously you can adapt file paths to your needs -- this is just an example
- to get a runnable example/template, copy the files from the `example` folder into the main folder and run `make`


## Acknowledgments
The template/format is that used by [Distill](distill.pub). The precise implementation used here has been adapted from the [World Models github page](https://github.com/worldmodels/worldmodels.github.io).
