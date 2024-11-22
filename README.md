# Projects

The purpose of this repo is to sync teacher and student work to a repo
so it can be shared and so it will not get lost.

To add a new computer to this repo, run these commands:

    git config --global user.name slvusd-gitbot
    git config --global user.email "ebrown+gitbot@slvusd.org"
    git config --global credential.helper store

Then from pi's home directory, run

    git -c credential.helper= clone https://github.com/slvusd/projects.git src

You will be prompted for the username (slvusd-github) and password. Get the
password (token) from Mr. Brown.

Finally, run `crontab -e` and add the following entry:

    */5 * * * * /home/pi/src/git_sync.sh

That's it!
