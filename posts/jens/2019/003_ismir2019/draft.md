[ISMIR 2019](https://ismir2019.ewi.tudelft.nl/) was my first conference in a
long time, the first conference visit
during my PhD and also the first MIR-related conference visit for me. As such,
even though I didn't have anything submitted, there were a ton of new insights,
cool papers and interesting people. In this post, I would like to summarize some
of my highlights as well as main takeaways.


## About Delft

Here are some facts I learned about the city:
- It rains a lot, but apparently only while people are asleep. How considerate!
- Pedestrians are at the bottom of the food chain. What are sidewalks?
- ...that's pretty much it. We didn't really get a chance to see the city amidst
all the conferencing. The historical city center is very beautiful though!


## Tutorials

The first day of the conference mainly consisted of two tutorial sessions. There
were three topics for each slot, so you had to pick one. Since I was there with
Sebastian, we decided to split up and each visit different topics. Instead of
discussing the tutorials themselves, however, I would like to discuss my personal
takeaways as to how you (IMHO) should structure such a session (and what you
should avoid).

1. Know your audience. You cannot please everyone; if you try, you will most
likely please noone. What will probably happen that your "middle ground" compromise
is still too much/overwhelming for novices, while experts in the topic will be
bored. Instead, I believe you should focus on one of the two groups (or on a 
group somewhere inbetween -- but _be specific_).  
Now, you might say that it is
impossible to know your audience at such an event -- there's too much diversity
in people's background! This just needs a slight readjustment, however: You can
_determine_ your audience instead. E.g. if you offer a GAN-for-Music tutorial 
advertised at people already familiar with the basics of GANs, then you can assume
that the people in your tutorial fulfill those requirements. People who don't will
likely go to a different tutorial. This isn't ideal in terms of inclusiveness, of
course, but I believe it would lead to much more "useful" sessions overall.
2. Foster activity/interaction. This depends somewhat on the length of the session:
IMHO, the longer it is, the more important it becomes that you _do_ something
at some point. The big thing here is that _running pre-made IPython notebooks
doesn't qualify_. Rather, you should include activities that really force the
participants to actively engage with the material. If these activities also
involve cooperation between participants, this will also allow give people an
excuse to get to know their peers a little bit. This is particularly relevant
if tutorials are in the beginning of (or before) the "main" conference.  
Generally,
including interactive sessions will result in not covering as much ground, but
I believe this is worth it if it means that you do so much more thoroughly. It
should also make your tutorial "stick" more, which I believe is the most important
thing -- you can't cover a lot of content in two or three hours anyway.


## Highlight Papers

These aren't necessarily the "best papers", but colored by my own preferences or
things I just found "cool". Note that the order in this post is simply the order
in which the papers were presented.

### mirdata
[The paper](http://archives.ismir.net/ismir2019/paper/000009.pdf) by Bittner et 
al. is an interesting case of "meta research", showing
the phenomenon of different people working with differing version of the "same"
dataset, as well as the significant impact this can have on the results. While
they only sample a small number of exemplary datasets, it makes you wonder how
many research projects are/were affected by problems like this.

The authors also propose a Python library for unified distribution and verification
of MIR datasets. This is great, if only for the fact that datasets that do _not_
come from the same source often come in different formats requiring separate
preprocessing procedures etc. A common repository can reduce the load of having
to write new processing code for each new dataset.

### Informational Complexity in Music
[This paper](http://archives.ismir.net/ismir2019/paper/000019.pdf) by Parmer et
al. investigates the "complexity" in terms of information theory of various
western music styles and its development over time. While the methodology can
be questioned -- e.g. the information measure is limited and not verified with
regards to human perception of complexity -- there are some interesting findings
about how different genres seem to "prioritize" different areas of complexity,
how the different areas developed over time, and how Billboard Top 100 songs
differ (or don't) from the general population of songs.

### Unsupervised Drum Transcription
Choi et al. tackle the problem of unsupervised transcription in 
[this paper](http://archives.ismir.net/ismir2019/paper/000020.pdf), based on how
a human might do it: Listen to a piece of music, try to play it, and adjust your
play to fix any errors on your part (i.e. differences between what you heard and
what you played).

The core idea is to use an encoder-decoder approach with a fixed decoder (your
"instrument"). By limiting the decoder to essentially produce impulse responses
for certain instruments, the encoder is forced to produce the corresponding
transcriptions. This of course has many limitations, e.g. a limited set of "sounds"
the decoder can produce, as well as the decoder needing to be differentiable.
Making this approach work for non-drum sounds would probably need a lot of extra
work, but in my opinion it's still a cool idea.  
Another interesting thing is their use of the [sparsemax activation](https://arxiv.org/pdf/1602.02068.pdf),
which I didn't know about before -- a kind of sparse (but differentiable)
alternative to softmax.

A special shoutout goes to their training dataset, which apparently "was crawled
from various websites". Way to foster reproducibility!

### Transcription with Invertible Neural Networks
Invertible neural networks are, essentially, able to map back from their output
to the input. Kelz et al. introduce this concept to MIR tasks in 
[their paper](http://archives.ismir.net/ismir2019/paper/000044.pdf). The networks
are very close to flow-based generative models, but there is the problem that
in classification tasks, we usually don't want the output to carry all information
in the input (or even be the same size as the input), which makes inverting the
network rather difficult. To fix this issue, there is an "auxiliary" output
that carries the extra information needed for invertibility, but not for the
actual task of interest.

Invertible neural networks primarily promise better interpretability of trained
models, which is definitely needed in deep learning. For example, in the case
of transcription, a given symbolic (transcribed) piece of music can be inverted
to give an example sound that would be transcribed this way. This way, one can
check whether the concepts that the model learned make sense intuitively. As an
added bonus, we get a generative model "for free" by training a discriminative one.

### Resonance Equalization with Neural Networks
Grachten et al. propose a kind of "neural equalizer" that automatically attenuates
resonances in music. They show that a network working directly on raw audio
performs on par with hand-crafted feature pipelines. I suppose this isn't super
impressive to most people, but I like the idea of incorporating AI/ML into
music production. Possible future work includes processing a piece of music
such that it adheres to some desired spectral profile (i.e., which frequencies
should be present how strongly?). Check 
[the paper](http://archives.ismir.net/ismir2019/paper/000048.pdf).

### AIST Dance Video Database
Not my topic at all, but this dataset represents a huge effort: Thousands of
videos, 40 dancers, several genres, up to nine cameras... Plus, it's all free
and open. Cheers to [Tsuchida et al.](http://archives.ismir.net/ismir2019/paper/000060.pdf)!

### Google Scooped My Idea
The folks at Google Magenta presented [a paper](http://archives.ismir.net/ismir2019/paper/000063.pdf)
on efficient neural audio synthesis. What I find more relevant is 
[the follow-up](https://openreview.net/pdf?id=B1x1ma4tDr), currently under review
for ICLR, which is _basically_ what I wanted to do to kick-off my PhD. Oh well.
Check it out though, the examples are quite impressive. And yet, lots of work
still to be done...

### FMP Notebooks
Müller et al. probably didn't "need" to write 
[this paper](http://archives.ismir.net/ismir2019/paper/000069.pdf) since the notebooks
kind of stand on their own, but I suppose it is rather like a "companion
paper" since, unfortunately, papers are still the most important thing in
research. Read the paper, check out the notebooks, read the FMP book... it's all
good stuff.

### Invariance Through Complex Basis Functions
At a glance, [the paper](http://archives.ismir.net/ismir2019/paper/000085.pdf)
by Lattner et al. is a bit too complex for me (hahaha), but this is definitely
something I'll be playing around with in the near future in order to gain some
understanding. The idea is to learn invariances to several "simple" kinds of
transformations such as transposition or time-shifting, although the authors
also demonstrate uses in the image domain (e.g. rotation). Unfortunately, the
paper leaves out most ofthe visualizations of the learned filters that were on
the poster, which looked really intriguing.

### Mosaic Style Transfer with Autocorrelograms
[This paper](http://archives.ismir.net/ismir2019/paper/000109.pdf) by MacKinlay
et al. sounded super cool (and he was really nice to talk to at the poster!), but
I have to admit that this goes way over my head mathematically. Another one I'm
gonna have to do some tinkering with. :) Unfortunately they don't include sound
examples in the paper, but it provides a method doing "musical style transfer"
(i.e. transfering the timbre of one signal onto the melody of another). While this
isn't "new" per se, the approach sounds quite sensible, plus it's IMHO more
attractive than just "letting a neural network do it", which most style transfer
solutions nowadays seem to go for.


## Late-breaking Demos

The LBD session was for "experimental" stuff that wasn't ready in time for the
regular deadline; it was also "just" posters (and optional demos), no papers.
Unfortunately, there was very little time given the sheer amount of stuff, so
here are just some quick highlights:
- The guys from [this paper](https://arxiv.org/abs/1907.00971) seemed to have
finished their "intuitively controllable" synthesizer. Not sure when/if/where
they're gonna release it though...
- Apparently, differentiable synthesizers are getting more popular right now:
Hirata et al. tested "deep frequency modulation synthesis". Looks like this
was already published at [CMMR](https://cmmr2019.prism.cnrs.fr/Docs/Proceedings_CMMR2019.pdf)
so I'm not sure why it was in the session, and it looks like it needs a lot of
work, but I thought it was cool.
- There was a poster on cross-fading between two audio tracks in the time-frequency
domain, i.e. cross-fade different frequencies at different times. Unfortunately
I don't have a link!


## Unconference

There was an "unconference" session with some interesting topics. Unfortunately,
it overlapped with the LBD session so I ended up not going... Shame, the whole
conference was set up in a "single-track" way, but it seems like they just wanted
to do a bit too much on Friday, so this kinda fell under the wagon. Maybe next year!


## In Closing

A few more general takeaways:
- Deep Learning is taking over MIR (of course...), but the methodology seems
to be rather simple still. I.e. the models used are often fairly "vanilla" and
there is little in terms of interpretability/understanding what's going on inside.
I suppose this will become more relevant once the models really start
saturating on the main MIR tasks and progress will require new approaches. I feel
like a kind of meta-review on the state of DL in MIR could be useful.
- Please don't _read_ your _one-hour_ keynote presentation _in the evening_. Bad
combination.
- Five days is a bit much for me. Around the fourth day or so, I really felt my
mental capacities decreasing, and crowding around posters for hours a day became
really exhausting. For people for whom this is an issue, 
it might be necessary to plan your visit a bit
more, e.g. not going to all the events on the first days to conserve your energy.

Overall, ISMIR 2019 was a great time! Met plenty of nice people, ate some great food,
got lots of new input... And motivation to submit something to next one so we
can go to Montreal next year. :) See you there!
