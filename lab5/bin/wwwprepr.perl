#!/usr/bin/env perl
# Jussi Karlgren, jussi@sics.se, 1997
%abbs = ('&amp;','et','a\.', 'a', 'a\.m\.', 'am', 'apr\.', 'apr', 'ariz\.', 'ariz', 'aug\.', 'aug', 'b\.', 'b', 'c\.', 'c', 'calif\.', 'calif', 'co\.', 'co', 'col\.', 'col', 'colo\.', 'colo', 'conn\.', 'conn', 'corp\.', 'corp', 'cpl\.', 'cpl', 'd\.', 'd', 'd\.c\.', 'dc', 'dec\.', 'dec', 'deg\.', 'deg', 'dr\.', 'dr', 'e\.', 'e', 'f\.', 'f', 'feb\.', 'feb', 'fla\.', 'fla', 'fr\.', 'fr', 'g\.', 'g', 'gen\.', 'gen', 'gov\.', 'gov', 'h\.', 'h', 'i\.', 'i', 'ii\.', 'ii', 'ill\.', 'ill', 'inc\.', 'inc', 'j\.', 'j', 'j\.c\.', 'jc', 'j\.p\.', 'jp', 'jan\.', 'jan', 'jr\.', 'jr', 'k\.', 'k', 'l\.', 'l', 'l\.a\.', 'la', 'l\.p\.', 'lp', 'ltd\.', 'ltd', 'm\.', 'm', 'maj\.', 'maj', 'mar\.', 'mar', 'mass\.', 'mass', 'md\.', 'md', 'mich\.', 'mich', 'minn\.', 'minn', 'mo\.', 'mo', 'mr\.', 'mr', 'mrs\.', 'mrs', 'ms\.', 'ms', 'n\.', 'n', 'n\.a\.', 'na', 'n\.c\.', 'nc', 'n\.j\.', 'nj', 'n\.v\.', 'nv', 'n\.y\.', 'ny', 'no\.', 'no', 'non-u\.s\.', 'non-us', 'nov\.', 'nov', 'o\.', 'o', 'oct\.', 'oct', 'ore\.', 'ore', 'p\.', 'p', 'p\.m\.', 'pm', 'pa\.', 'pa', 'pct\.', 'pct', 'plc\.', 'plc', 'pres\.', 'pres', 'prof\.', 'prof', 'pvt\.', 'pvt', 'q\.', 'q', 'qtr\.', 'qtr', 'r\.', 'r', 'rep\.', 'rep', 'rev\.', 'rev', 's\.', 's', 's\.a\.', 'sa', 'sen\.', 'sen', 'sept\.', 'sept', 'sgt\.', 'sgt', 'st\.', 'st', 'supt\.', 'supt', 't\.', 't', 'u\.', 'u', 'u\.k\.', 'uk', 'u\.n\.', 'un', 'u\.s\.', 'us', 'v\.', 'v', 'va\.', 'va', 'vs\.', 'vs', 'w\.', 'w', 'wash\.', 'wash', 'x\.', 'x', 'y\.', 'y', 'z\.', 'z');



while($line = <STDIN>)
{
    $line =~ s/(<[^>]+>)//g;        # remove sgml/html tags
    $line =~ s/-\n/-/g;                # join hyphenated words at line breaks
    $line =~ s/&auml\;/ä/;
    $line =~ s/&aring\;/å/;
    $line =~ s/&ouml\;/ö/;
    $line =~ s/&Ouml\;/Ö/;
    $line =~ s/&Auml\;/Ä/;
    $line =~ s/&Aring\;/Å/;
    $line =~ s/[\}\{\[\],)(\"]/\ ,\ /g;        # remove punctuation (lesser)
    foreach $abb (keys %abbs) {$line =~ s/(\b )$abb/$1 $abbs{$abb}/ig;};
    $line =~ s/[;:!\?]/\ ;\ /g;         # remove punctuation (sentence break)
    $line =~ s/(\D)\.(\D)/$1\ ;$2/g; # remove punctuation (period - nondec)
    print $line;
}
