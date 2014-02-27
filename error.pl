#!/usr/bin/perl

require "$1/libraries.ph" if ($0=~/^(.*)\/[^\/]+$/);

$|=1;
#$/ = '>';

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

  if (/Composition unit WebSphere:cuname=(\S+) in BLA WebSphere:blaname=\S+ (started|stopped)/) {
    ($name, $type) = ($1,$2);
    if ($type eq "started") {
      print "$libraries'colour{'Green'}";
      &libraries'doHorizontal("-");
      print "$libraries'colour{'Off'}";
      s/$name/$libraries'colour{'Orange'}$name$libraries'colour{'Off'}/;
      s/$type/$libraries'colour{'Green'}$type$libraries'colour{'Off'}/;
      print "$_\n";
      return;
    }
    else {
      s/$name/$libraries'colour{'Orange'}$name$libraries'colour{'Off'}/;
      s/$type/$libraries'colour{'Red'}$type$libraries'colour{'Off'}/;
      print "$_\n";
      print "$libraries'colour{'Red'}";
      &libraries'doHorizontal("-");
      print "$libraries'colour{'Off'}";
      return;
    }
  }

  s/(Caused by:.*)/$libraries'colour{'Red'}\1$libraries'colour{'Off'}/g;
  s/(\s[.A-Za-z]*Exception):(.*)$/$libraries'colour{'Purple'}\1$libraries'colour{'Off'}:$libraries'colour{'Orange'}\2$libraries'colour{'Off'}/g;
  s/\(([A-Za-z]*.java):(\d+)\)/\($libraries'colour{'Teal'}\1$libraries'colour{'Off'}:$libraries'colour{'Green'}\2$libraries'colour{'Off'}\)/g;

  s/^(invalid)$/$libraries'colour{'Red'}\1$libraries'colour{'Off'}/g; 
  s/^(valid)$/$libraries'colour{'Green'}\1$libraries'colour{'Off'}/g; 

  if (/FFDC Incident emitted on/) {
    s/\\([^\\]*.txt) /\\$libraries'colour{'Orange'}\1$libraries'colour{'Off'} /;
  }

  print "$_\n";

}
