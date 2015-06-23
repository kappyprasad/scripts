#!/usr/bin/perl

# $Date: 2014-06-19 08:24:58 +1000 (Thu, 19 Jun 2014) $
# $Revision: 4728 $
# $Author: dedson $
# $HeadURL: https://slither/svn/repository/trunk/DavidEdson/Software/perl/ant.pl $
# $Id: ant.pl 4728 2014-06-18 22:24:58Z dedson $



require "$1/libraries.ph" if ($0=~/^(.*)\/[^\/]+$/);

$|=1;

open (IN, "ant @ARGV 2>&1 |") || die "Can't start ant, $!\n";

while (<IN>) {
  if (/(Tests run: )(\d+)(, Failures: )(\d+)(, Errors: )(\d+),/) {
    ($th,$t,$fh,$f,$eh,$e) = ($1,$2,$3,$4,$5,$6);
    if ($f == 0 && $e == 0) {
      s/$th$t/$libraries'colour{'Green'}$th$t$libraries'colour{'Off'}/;
    }
    if ($f > 0) {
      s/$fh$f/$libraries'colour{'Red'}$fh$f$libraries'colour{'Off'}/;
    }
    if ($e > 0) {
      s/$eh$e/$libraries'colour{'Purple'}$eh$e$libraries'colour{'Off'}/;
    }
  }
  if (/^(\S+)(\:)(.*)$/) {
    &libraries'doHorizontal("-");
    print "$libraries'colour{'Purple'}$1$libraries'colour{'Off'}$2$libraries'colour{'Red'}$3$libraries'colour{'Off'}\n";
  }
  elsif (/^([^[]*\[)([^]]+)(\].*)$/i) {
    print "$1$libraries'colour{'Orange'}$2$libraries'colour{'Off'}$3\n";
  }
  elsif (/^(build )(successful.*)/i) {
    &libraries'doHorizontal("-");
    print "$1\n\t$libraries'colour{'Green'}$2$libraries'colour{'Off'}\n\n";
  }
  elsif (/^(build )(failed.*)/i) {
    &libraries'doHorizontal("-");
    print "$1\n\t$libraries'colour{'Red'}$2$libraries'colour{'Off'}\n\n";
  }
  elsif (/^(Total time\:.*)/i) {
    print "$1\n";
    &libraries'doHorizontal("-");
  }
  else {
    print;
  }
}

