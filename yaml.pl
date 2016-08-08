#!/usr/bin/perl

require "$1/libraries.ph" if ($0=~/^(.*)\/[^\/]+$/);

$|=1;
#$/='}';

$off    = $libraries'colour{'Off'};
$green  = $libraries'colour{'Green'};
$red    = $libraries'colour{'Red'};
$blue   = $libraries'colour{'Blue'};
$teal   = $libraries'colour{'Teal'};
$purple = $libraries'colour{'Purple'};
$orange = $libraries'colour{'Orange'};

if ($#ARGV == -1 ) {
  while (<>) {
    &processLine();
  }
}
else {
  if ($ARGV[0] eq "-t" && -e $ARGV[1]) {
    open (IN, "tail -f $ARGV[1] |") || die "Can't tail -f $ARGV[1], $!\n";
    while (<IN>) {
      &processLine();
    }
    close(IN);
  }
  else {
    foreach $file (@ARGV) {
      if ( -f $file ) {
	open (IN, $file) || die "Can't open $file, $!\n";
	while (<IN>) {
	  &processLine();
	}
      }
    }
  }
}

sub processLine {
  s/[\r\n]//gi;

  s/([\[\]])/${teal}\1${off}/g;
  s/([{}])/${purple}\1${off}/g;

  # element
  s/([^:]+)(:\s*)$/${orange}\1${off}\2/g;

  # attribute/value
  s/([^:]*):([^:]+)/${red}\1${off}:${green}\2${off}/g;

  print "$_\n";

}
