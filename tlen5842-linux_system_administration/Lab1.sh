#!/bin/bash

space_root=`df / | awk 'FNR == 2 {print $5}'`
let space_root=${space_root%?};
space_boot=`df /boot | awk 'FNR == 2 {print $5}'`
let space_boot=${space_boot%?};

let threshold=80
subject="space exceeded $threshold"
body="do something"

if [ $space_boot -gt $threshold ] || [ $space_root -gt $threshold ];
then
	`mail -s "$subject" root@localhost <<< "$body"`
fi
