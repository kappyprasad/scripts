#!/usr/bin/perl

$colOrange = "\033[;33m";
$colGreen = "\033[;32m";
$colTeal = "\033[;34m";
$colBlue = "\033[;36m";
$colPurple = "\033[;35m";
$colRed = "\033[;31m";
$colOff = "\033[0m";


open (INDIR, "svn status @ARGV | ") || die "Can't execute svn diff @ARGV, $!\n";
while (<INDIR>) {
  s/\r//g;
  s/\n//g;

  if (/^A(.*)$/) {
	print "${colGreen}$_${colOff}\n";
  }
  elsif (/^M(.*)$/) {
	print "${colOrange}$_${colOff}\n";
  }
  elsif (/^\?(.*)$/) {
	print "${colPurple}$_${colOff}\n";
  }
  elsif (/^D(.*)$/) {
	print "${colRed}$_${colOff}\n";
  }
  elsif (/^I(.*)$/) {
	print "${colTeal}$_${colOff}\n";
  }
  else {
	print "$_\n";
  }
}
close(INDIR);
