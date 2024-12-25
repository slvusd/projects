#!/bin/sh
libcamera-jpeg -n -o - 2>/dev/null |\
      convert - -distort SRT 183 -resize 1920x \
      	-gravity southeast -pointsize 24 -fill white -annotate +10+10 "$(date +'%Y-%m-%d %H:%M:%S')" \
	$HOME/images/img$(date +'%Y%m%dT%H%M%S').jpg

