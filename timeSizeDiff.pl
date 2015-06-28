#!/usr/bin/perl 

# $Date: 2014-06-19 08:24:58 +1000 (Thu, 19 Jun 2014) $
# $Revision: 4728 $
# $Author: dedson $
# $HeadURL: https://slither/svn/repository/trunk/DavidEdson/Software/perl/timeSizeDiff.pl $
# $Id: timeSizeDiff.pl 4728 2014-06-18 22:24:58Z dedson $



require "$1/libraries.ph" if ($0=~/^(.*)\/[^\/]+$/);

use strict;
use Getopt::Long;

my $name;
$name = $0;
$name =~ s|^.*/([^/]+)$|\1|;

my $USAGE = <<EOU;
USAGE: $name -d <destination> [-s <source>] [-t <size>]
EOU

my %OPTIONS;
my $source;
my $destination;
my $count;
my $sourceSize;
my $destinationSize;
my $exec;
my $size;
my $runningCount = 0;
my $runningTotal = 0;

my $rc = GetOptions(\%OPTIONS, 's=s', 'd=s', 'c=s', 't=s');

if (! defined($OPTIONS{'c'}) and ! defined($OPTIONS{'s'}) and ! defined($OPTIONS{'d'}) ) {
  die $USAGE;
}

if (defined($OPTIONS{'c'})) {
  $count = $OPTIONS{'c'};
  &countInputStream($count);
  exit(0);
}

if (defined($OPTIONS{'d'})) {
  $destination=$OPTIONS{'d'};
  if ( ! -e "$destination" ) {
    die "Can't find destination=$destination, $!\n";
  } else {
    $destinationSize=&getSize($destination);
  }
} else {
  print STDERR "$USAGE\n\nplease set destination\n";
  exit 1;
}

if (defined($OPTIONS{'s'})) {
  $source=$OPTIONS{'s'};
  if (! -e "$source" ) {
    die "Can't find source=$source, $!\n";
  } else {
    $sourceSize=&getSize($source);
  }
}
else {
  $sourceSize = 0;
}

if (defined($OPTIONS{'t'})) {
  $sourceSize=$OPTIONS{'t'};
}


print "\n";
print "source=$source\n";
print "sourceSize=" . &libraries'num2commas($sourceSize) . " kb\n";
print "desitination=$destination\n";
print "destinationSize=" . &libraries'num2commas($destinationSize) . " kb\n";
print "\n";

$exec = "| $0 -c $sourceSize";
open (OUT, $exec) || die "Can't execute $exec, $!\n";

while ($sourceSize > $destinationSize) {
  $destinationSize = &getSize($destination);
  print OUT "$destinationSize\n";
  sleep 15;
}

print OUT "\nEND\n";
close(OUT);
exit 0;

sub getSize() {
  my $file = shift(@_);
  my $exec = "du -sk '$file' |";
  my $size;
  open (IN, $exec) || die "Can't execute $exec, $1\n";
  while (<IN>) {
    if (/^(\d+)\s/) {
      $size = $1;
      last;
    }
  }
  close(IN);
  return $size;
}

sub countInputStream() {
  my $target = ($#_ == -1 ? 0 : shift(@_));
  my $oldTime = &getTime();
  my $oldSize = 0;
  my $size;
  my $time;
  my $bps;
  my $ds;
  my $dt;
  my $eta;
  my $etas;

  print sprintf("%15s%15s%15s%15s\n", "source(kb)", "dest(kb)", "kbps", "eta");

  while (<>) {
    s/[\r\n]//g;

    if (/END/) {
      last;
    }

    $size = $_;
    $time = &getTime();
    $ds = $size-$oldSize;
    $dt = $time-$oldTime;

    if ($bps != 0) {
      $eta = int(($target-$size) / $bps);
      $etas = toHMS($eta);
    } else {
      $etas = "-";
    }

    if ($dt != 0) {
      $bps = int($ds / $dt);
    } else {
      $bps = "-";
    }

    print "                                                              \r";               
    print sprintf("%15s%15s%15s%15s\r", &libraries'num2commas($target), &libraries'num2commas($size), &libraries'num2commas($bps), $etas);

    $oldSize = $size;
    $oldTime = $time;
  }
}

sub getTime {
  my $timeExec = "date +\%s |";
  open (INT, "$timeExec") || die "Can't execute $timeExec, $!\n";
  my $time = <INT>;
  close(INT);
  $time =~ s/[\n\r]//g;
  return $time;
}

sub toHMS {
  my $epoc = shift(@_);
  my $seconds = $epoc % 60;
  my $minutes = (($epoc - $seconds) / 60) % 60;
  my $hours   = ($epoc - ($minutes * 60) - $seconds) / 3600;
  return sprintf("%02d:%02d:%02d", $hours, $minutes, $seconds);
}

