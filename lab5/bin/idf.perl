#!/usr/bin/env perl
# Jussi Karlgren, jussi@sics.se, 1997


require "getopts.pl";
&Getopts('s:');

if ($opt_s) {
    open(STOPLIST, "<$opt_s");
    while ($_ = <STOPLIST>) {
        tr/öäå/oaa/;
        ($str = $_) =~ s/\s//;
        $str =~ tr/A-Z/a-z/;
        $stop{$str} = 1;
    }
    close STOPLIST;
}


$/="\n\n";


while($line = <>) {
    $line =~ s/(<[^>]+>)//g;               # remove sgml/html tags
    $line =~ s/[\'\"\`\~]//g;              # remove quotes and other non-characters
    $line =~ s/[\\\/\-\_]/\ /g;            # remove hyphens and slashes
    $line =~ s/[\}\{\[\],)(\"]/\ ,\ /g;    # remove punctuation (lesser)
    $line =~ s/[;:!\?§]/\ ;\ /g;           # remove punctuation (sentence break)
    $line =~ s/(\D)\.(\W)/$1\ ;$2/g;       # remove punctuation (period - nondec)
    $line =~ tr/A-Z/a-z/;                  # lowercase

    @array = split(/\s+/,$line);           # split line into words

    foreach $word (@array) {
        $this{$word}++ if !$stop{$word};
    }

    if (eof) {
        foreach (keys %this) {
            $df{$_}++;
        }

        %this = ();
    }
}

foreach (sort keys %df) {
    print 1/$df{$_}," $_\n";
}

exit(0);
