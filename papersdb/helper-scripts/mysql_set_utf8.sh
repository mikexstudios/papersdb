#!/bin/bash
#We need to run this before we run syncdb so that  all entries within our
#database will be set to utf8.
#To use:
#./mysql_set_utf8.sh dev  <- mysql user
#Some example strings:
#ALTER DATABASE  `picosong` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci
#ALTER TABLE  `songs_song` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci
#ALTER TABLE  `songs_song` CHANGE  `file`  `file` VARCHAR( 500 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL

#Check is user arg is set. -n means 'not empty':
if [ ! -n "$1" ]; then
    echo 'Sets the database to use utf8 encoding.'
    echo 'Usage: $0 [mysql user]'
    exit
fi

mysql_cmd='ALTER DATABASE papersdb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci'
#If the database already exists, and we want to make the file field accept
#utf8, then run this command:
mysql_cmd='ALTER TABLE `papers_paper` CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci'
echo "$mysql_cmd" | mysql papersdb -u $1 -p
