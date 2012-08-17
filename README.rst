Chase The Cheshire Cat Dev Branch
=================================

Welcome, this is the source for a puzzle/scavenger hunt website. This site will allow users to form teams of max 5 members to compete.
Different challenges will be posted periodically and will be worth a number of points. Submissions will be text/video/audio/images. Judging will be done
manually and teams may be penalized and commented on by judges.

Wanna help?
**********
* Learn `Python <http://code.google.com/edu/languages/google-python-class/>`_
* Learn `Django <https://docs.djangoproject.com/en/1.4>`_
* Join the project and start committing :) 

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
* ``view_main_page`` - display the index of the site with latest announcements and links.
* ``view_info_page`` - display InfoPage
* ``view_announcement`` - display a single annoucement
* ``list_announcements`` - list all announcements
* ``create_info_page`` - display form to create a new info page.
* ``create_announcement`` - display form to create new announcement. 

-----------------------------------------------

``score``
---------
Models
~~~~~~
*no models needed?*

Views
~~~~~
* ``view_scores`` - display groups and their points. sortable.


-----------------------------------------------

``game``
--------
Models
~~~~~~
* ``Series`` - A list of challenges, unlocked by qrcode.
* ``Challenge`` - a contest challenge with name, description, dates, etc.
* ``Deliverable`` - a deliverable object. Could be linked to a file and has an owner/challenge.
* ``Submission`` - a submission, has a deliverable and dates, challenge. Could be valid/invalid as determined by judges.
* ``SubmitKeyForm`` - a form that handles key submissions (ex. codes from crypto/html challenges)
* ``SubmiFileForm`` - a submit form that handles file uploadloads.
* ``UnlockSeriesForm`` - a form to unlock a series given a qrcode.

Views
~~~~~
* ``list_challenges`` - list all challenges
* ``view_challenge`` - view single page for a challenge
* ``list_submissions`` - lists submissions by a group
* ``submit`` - display appropiate submit form for a given challenge.
* ``save_upload`` - called by ``submit`` to write an upload to the disk.
* ``unlock_series`` - display form to unlock a challenge series.

-----------------------------------------------

``judge``
---------
Models
~~~~~~
* ``JudgeSubmissionForm`` - form to comment on and validate/invalidate submission.
* ``NewSeriesForm`` - a form to add a new challenge series.
* ``NewChallengeForm`` - form to add a new challenge

Views
~~~~~
* ``list_submissions`` - list all submissions by all groups
* ``new_series`` - display form to create a new series.
* ``new_challenge`` - display form to create new challenge.
* ``judge_submission`` - display form to judge a submission and process it.


-----------------------------------------------

``player``
----------
Models
~~~~~~
* ``Player`` - a player in this game
* ``Team`` - a team of max 5 members with a name
* ``NewPlayerForm`` - form to register a new player
* ``PlayerNameField`` - a form field that must be unique (username)
* ``NewTeamForm`` - form to register a new team
* ``TeamNameField`` - a form field that must be unique (team name)
* ``TeamInfoForm`` - form to update team info
* ``JoinTeamForm`` - form to join a team, given a join key.
* ``RequestBanForm`` - form to handle a ban request
* ``PlayerNameBanField`` - a field that disables the banning of yourself and judges.
* ``BanRequest`` - a request to ban a user.
* ``UpdateTeamInfoForm`` - a form to handle updating team info.
* ``UpdatePlayerInfoForm`` - a form to handle updating player info.

Views
~~~~~
* ``view_player_info`` - view info about a player
* ``view_team_info`` - view info about a team
* ``player_home`` - a home page for the player.
* ``register_new_player`` - display a form to register a new player and process it.
* ``confirm_player`` - confirm a player into a team.
* ``gen_join_key`` - generate a unique join key for a team.
* ``register_new_team`` -  display a form to register a team and process it.
* ``join_team`` - display form to join a team and process it.
* ``leave_team`` - display a leave team confirmation message and remove player from current team.
* ``request_ban`` - display a ban request form and submit ban request to judges.
* ``update_team_info`` - display form to update a team's info and process it.
* ``update_player_info`` - display form to update a player's info and process it.

