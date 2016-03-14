#!/usr/bin/perl

require "$1/libraries.ph" if ($0=~/^(.*)\/[^\/]+$/);

$|=1;
#$/='}';

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

  s/([\[\]])/$libraries'colour{'Teal'}\1$libraries'colour{'Off'}/g;
  s/([{}])/$libraries'colour{'Purple'}\1$libraries'colour{'Off'}/g;

  # attribute=
  s/(['"])([^'"]*)(['"])(\s*:\s*)/\1$libraries'colour{'Red'}\2$libraries'colour{'Off'}\3\4/g;
  
  # "value"
  s/(['"])(\s*:\s*)([^,]*)/\1\2$libraries'colour{'Green'}\3$libraries'colour{'Off'}\4/g;

  print "$_\n";

}
