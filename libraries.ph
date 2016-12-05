
package libraries;

$colour{"Orange"} = "\033[;33m";
$colour{"Green"}  = "\033[;32m";
$colour{"Blue"}   = "\033[;34m";
$colour{"Teal"}   = "\033[;36m";
$colour{"Purple"} = "\033[;35m";
$colour{"Red"}    = "\033[;31m";
$colour{"Off"}    = "\033[0m";

sub doHorizontal {
  $char = shift(@_);
  $HORIZONTAL = "";
  $COLUMNS = $ENV{'COLUMNS'};

  $COUNT = 1;
  while ($COUNT < $COLUMNS) {
    $HORIZONTAL .= $char;
    $COUNT++;
  }

  print "$HORIZONTAL\n";
}

sub num2commas() {
  $number = shift(@_);
  $formatted = "";
  while ($number =~ /(\d*)(\d\d\d)$/) {
    $formatted = $2 . "," . $formatted;
    $number = $1;
  }
  $formatted = $number . "," . $formatted;
  $formatted =~ s/^,//;
  $formatted =~ s/,$//;
  return $formatted;
}

1;
