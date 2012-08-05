Chase The Cheshire Cat Dev Branch
=================================

Welcome, this is the source for a puzzle/scavenger hunt website. This site will allow users to form teams of max 5 members to compete.
Different challenges will be posted periodically and will be worth a number of points. Submissions will be text/video/audio/images. Judging will be done
manually and teams may be penalized and commented on by judges.

Apps Summary
************

* ``inform`` - info pages, rules, and clues.
* ``score`` - list teams and their score.
* ``game`` - provides functionlity to list challenges and submit answers to them.
* ``judge`` - judge, reward points, and add challenges.
* ``player`` - represents a player in this game. its an extension of the user object in django. 

Detailed Plans for Apps
***********************

``inform``
----------
Models
~~~~~~
* ``InfoPage`` - page for rules or other static pages.
* ``Announcement`` - a definition for an announement
* ``NewInfoPageForm`` - form for a new info page
* ``NewAnnouncementForm`` - form for a new annoucement

Views
~~~~~
* ``view_info_page`` - display InfoPage
* ``view_announcement`` - display a single annoucement
* ``create_info_page`` - display form to create a new info page.
* ``create_announcement`` - display form to create new announcement. 
    
