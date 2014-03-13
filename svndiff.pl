#!/usr/bin/perl

require "$1/libraries.ph" if ($0=~/^(.*)\/[^\/]+$/);

$colOrange = "\033[;33m";
$colGreen = "\033[;32m";
$colBlue = "\033[;36m";
$colPurple = "\033[;35m";
$colRed = "\033[;31m";
$colOff = "\033[0m";

open (INDIR, "svn diff --force @ARGV | ") || die "Can't execute svn diff @ARGV, $!\n";
while (<INDIR>) {
    s/\r//g;
    s/\n//g;

    if (/^===================================================================/) {
        &libraries'doHorizontal("-");
    }
    elsif (/^Index: (.*)$/) {
        &libraries'doHorizontal("=");
        print "$1\n";
    }
    elsif (/^\+(.*)$/) {
        print "${colGreen}$_${colOff}\n";
    }
    elsif (/^\-(.*)$/) {
        print "${colPurple}$_${colOff}\n";
    }
    else {
        print "$_\n";
    }
}
close(INDIR);
