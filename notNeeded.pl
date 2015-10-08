#!/usr/bin/perl

# $Date: 2014-06-19 08:24:58 +1000 (Thu, 19 Jun 2014) $
# $Revision: 4728 $
# $Author: dedson $
# $HeadURL: https://slither/svn/repository/trunk/DavidEdson/Software/perl/notNeeded.pl $
# $Id: notNeeded.pl 4728 2014-06-18 22:24:58Z dedson $



if ($#ARGV == -1) {
  die "usage: <target-dir>";
}

$target = join(" ", @ARGV);

if ( ! -e "$target" ) {
  die "Can't find $target, $!\n";
}

open (IND, "find . |") || die "Can't run find, $!\n";
while (<IND>) {
  s/\r//g;
  s/\n//g;
  $file = $_;

  if ( -e "$file" && ! -e "$target/$file" ) {
    system("rm -vfr \"$file\"");
  }

}
close (IND);

