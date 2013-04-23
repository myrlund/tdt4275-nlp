#!/usr/bin/env perl

require "getopts.pl";
&Getopts('s:i:');

if ($opt_s) {
    open(STOPLIST, "<$opt_s");
    while (<STOPLIST>) {
        chop;
        ($str = $_) =~ s/\s//;
        $str =~ tr/A-Z/a-z/;
        $stop{$str} = 1;
    }
    close STOPLIST;
}
$N=1;
if ($opt_i) {
    open(IDF, "<$opt_i");
    while (<IDF>) {
        chop;
        split;
        $df{$_[1]} = $_[0];
        if ($N < $_[0]) {$N=$_[0];}
    }
    close IDF;
}
$/="\n\n";

while($line = <>) {
    $line =~ s/(<[^>]+>)//mg;        # remove sgml/html tags
    $line =~ s/[\'\"\`\~]//mg; # remove quotes and other non-characters
    $line =~ s/\-\n//mg; # fix line breaks
    $line =~ s/[\\\/\-\_]/\ /mg; # remove hyphens and slashes
    $line =~ s/[\}\{\[\],)(\"]//mg;        # remove punctuation (lesser)
    $line =~ s/[;:!\?]//mg;         # remove punctuation (sentence break)
    $line =~ s/(\D)\.(\W)/$1\ $2/mg; # remove punctuation (period - nondec)
    $line =~ tr/ŒŠš/åäö/;            # lowercase
    $line =~ tr/A-Z/a-z/;            # lowercase
    @array = split(/\s+/,$line); # split line into words
    foreach $word (@array) {
        $tf{$word}++ unless $stop{$word};
        $dl++;
    }
}
$K1=2;
$b=0.75;
foreach $word (keys %tf) {
    if ($df{$word}) {
        $score{$word} = (log($N) - log($df{$word}));
    } else {
        $score{$word} = 1;
    }
    $score{$word} = $score{$word}*$tf{$word}*($K1+1);
    $score{$word} = $score{$word}/($K1*((1-$b)+$b*$dl+$tf{$word}));
}
foreach $word (sort {$score{$b} <=> $score{$a}} keys %score) {
    print "$score{$word}        $word\n";
}
