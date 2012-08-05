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
* ``InfoPage`` -  a page for rules or other static pages.
* ``Announcement`` -  an announement
* ``NewInfoPageForm`` - form for a new info page
* ``NewAnnouncementForm`` - form for a new annoucement

Views
~~~~~
* ``view_info_page`` - display InfoPage
* ``view_announcement`` - display a single annoucement
* ``create_info_page`` - display form to create a new info page.
* ``create_announcement`` - display form to create new announcement. 

``score``
---------
Models
~~~~~~
*no models needed?*

Views
~~~~~
* ``view_scores`` - display groups and their points. sortable.

``game``
--------
Models
~~~~~~
* ``Challenge`` - a contest challenge with name, description, dates, etc.
* ``Deliverable`` - a deliverable object. Could be linked to a file and has an owner/challenge.
* ``Submission`` - a submission, has a deliverable and dates, challenge. Could be valid/invalid as determined by judges.
* ``SubmitKeyForm`` - a submit form that handles text
* ``SubmitImageForm`` - a submit form that handles images
* ``SubmitAudioForm`` - a submit form that handles audio
* ``SubmitVideoForm`` - a submit form that handles video

Views
~~~~~
* ``list_challenges`` - list all challenges
* ``view_challenge`` - view single page for a challenge
* ``list_submissions`` - lists submissions by a group
* ``submit`` - display appropiate submit form for a given challenge.

``judge``
---------
Models
~~~~~~
* ``JudgeSubmissionForm`` - form to comment on and validate/invalidate submission.
* ``NewChallengeForm`` - form to add a new challenge

Views
~~~~~
* ``list_submissions`` - list all submissions by all groups
* ``judge_submission`` - display form to judge a submission and process it.

``player``
----------
Models
~~~~~~
* ``Player`` - a player in this game
* ``Team`` - a team of max 5 members with a name
* ``NewPlayerForm`` - form to register a new player
* ``NewTeamForm`` - form to register a new team
* ``TeamInfoForm`` - form to update team info

Views
~~~~~
* ``view_player_info`` - view info about a player
* ``view_team_info`` - view info about a team
* ``register_new_player`` - display a form to register a new player and process it.
* ``register_new_team`` -  display a form to register a team and process it. 
* ``update_team_info`` - display form to update a team's info and process it.
