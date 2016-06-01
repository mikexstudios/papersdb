PapersDB
==========

PapersDB is an elegant scientific paper management webapp similar to [Mendeley][m]
or [Papers][p] but operating completely in browser.

This was my entry to MIT's 2011 iCampus prize. The submission was well-received
but did not win since it was more geared towards researchers rather than 
addressing living and learning topics at MIT. I meant to further develop this
app for my personal usage, but my doctoral research projects took over any
free time. I moved to Mendeley instead, and it works pretty well.

[m]: https://www.mendeley.com/
[p]: http://papersapp.com/


## Motivation

As scientists and engineers, reading scientific literature is part of our daily
routine. However, these papers start piling up and keeping track of all of them
is a chore.

One solution is to keep a digital library of papers. This concept is not new,
and there are many existing software and websites to address the paper
management problem. However, none of them do it well. The software that gets it
mostly "right" is "Papers", a mac software that provides a minimalistic but
powerful interface for a papers library. However, it is platform dependent
(only mac), does not have the ability to sync libraries across computers, and
suffers from weak paper searching ability.

Some of the mentioned deficiencies can be addressed by putting the software "in
the cloud" (in other words, making a web application). However, current
web-based solutions lack the usability and feel of a well-designed web
application. For example, zotero is a "web application" that tries very hard to
mimic a desktop application! Because it attempts to bridge two disparate design
principles, zotero fails to be good at either. CiteULike is a very functional
web application, but lacks usability. Mendeley lacks focus and sacrifices its
online interface for social features and a kludgy desktop client.

Therefore, there is a need for a better paper management web application.

## Goals

PapersDB's focus is building an excellent and elegant paper management web
application. It attempts to reach this goal by:

1. Having less unnecessary features. Components such as "social networks" and
desktop clients is unimportant. The most important feature of PapersDB is to
manage papers well.

2. Designing a good user interface. The software should be minimalistic and get
out of the user's way. The papers library should be the most prominent part of
the application. Users should be able to immediately use the application
because it is intuitive.

3. Designing from a web application approach. A big mistake that destroys the
usability of a web application is to design it like desktop software. An
example would be Microsoft's Web Outlook vs. Google's Gmail. The desktop
version of Outlook is a usable program. However, Microsoft tried to apply the
same desktop design principles to their web version of Outlook. The result is a
confusing and unresponsive application that lacks elegance. In contrast,
Google's approach to building an online email client is to start from the
browser and design the application to look and feel like a website. Similarly,
PapersDB approaches the user interface from a web point of view, avoiding
browser limitations while capitalizing on browser strengths.

As a web application, PapersDB can be accessed on any computer with a modern web
browser. Users can work from any computer/platform, and all library changes are
synced automatically between computers. Users can search for papers like they
naturally do on Google or on the journal websites. Importing papers into the
website is envisioned as a single click from the browser.

## Usage

1. After cloning this repository, copy `local_settings.py.sample` to 
   `local_settings.py`.

2. Build the `Dockerfile`. Note, this `Dockerfile` uses SQLite and Django's
   development server:

   `docker build -t mikexstudios/papersdb .`

2. Run it like:

   `docker run -d -p 80:80 -v .:/usr/src/app mikexstudios/papersdb`

   If you want to develop while running the script, mount the current 
   directory by:

   `docker run -d -p 80:80 -v `pwd`:/usr/src/app mikexstudios/papersdb`

## Additional work

The following major features needs to be completed before the application is
considered stable:

1. Fulltext searching - the ability to search through all citation and document
text in the papers library.

2. Bookmarklet paper adding - the ability to click on a small button/link on
the browser when visiting a publisher's website to import a paper into the
database.

3. More robust automatic citation grabber - only certain popular journals are
currently supported for automatic paper adding. This list needs to be further
expanded and tested.

4. Better UI for viewing individual papers - when individual papers are
clicked, the resulting page is not very useful and look crude. Improvements to
the UI is necessary.

