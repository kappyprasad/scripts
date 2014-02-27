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

  # <!doctype>
  #s/<\!([^-\!>]+)(\-\-|)>/$libraries'colour{'Teal'}<\1$libraries'colour{'Off'}\2$libraries'colour{'Teal'}\3>$libraries'colour{'Off'}/g;

  # <?processing>
  s/<\?([^\?>]+)\?>/$libraries'colour{'Teal'}<?$libraries'colour{'Off'}\1$libraries'colour{'Teal'}?>$libraries'colour{'Off'}/g;

  $comment = 0;

  # <!comment>
  $comment += s/<(\!\-\-|\!)([^\-]+)(\-\-)>/$libraries'colour{'Teal'}<\1$libraries'colour{'Blue'}\2$libraries'colour{'Teal'}\3>$libraries'colour{'Off'}/g;

  if ($comment == 0) {
	# <element>
	s/<([^\?\!][^>]+)>/$libraries'colour{'Teal'}<$libraries'colour{'Purple'}\1$libraries'colour{'Teal'}>$libraries'colour{'Off'}/g;

	# &amp; etc
	s/(&[^;]+;)/$libraries'colour{'Purple'}\1$libraries'colour{'Off'}/g;
		
	# attribute=
	s/(\s+\S+)=(['"])/$libraries'colour{'Red'}\1=$libraries'colour{'Off'}\2/g;
		
	# "value"
	s/(['"])([^'"]*)(['"])/\1$libraries'colour{'Green'}\2$libraries'colour{'Off'}\3/g;

        # CDATA 
        s/(<\!\[CDATA\[)/$libraries'colour{'Teal'}\1$libraries'colour{'Off'}/g; 
        s/(\]\]>)/$libraries'colour{'Teal'}\1$libraries'colour{'Off'}/g; 

   }

  print "$_\n";

}
