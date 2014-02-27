#!/usr/bin/perl

$colOrange = "\033[;33m";
$colGreen = "\033[;32m";
$colBlue = "\033[;36m";
$colPurple = "\033[;35m";
$colRed = "\033[;31m";
$colOff = "\033[0m";

open (INDIR, "/usr/bin/diff @ARGV | ") || die "Can't execute diff @ARGV, $!\n";
while (<INDIR>) {
  s/\r//g;
  s/\n//g;

  if (/^\<(.*)$/) {
	print "${colGreen}$_${colOff}\n";
  }
  elsif (/^\>(.*)$/) {
	print "${colPurple}$_${colOff}\n";
  }
  else {
	print "$_\n";
  }
}
close(INDIR);
