#!/usr/bin/perl
# Jussi Karlgren, jussi@sics.se, 1997


while (<>) {
    next unless $_;
    split;
    foreach ($_) {
        s/[\.;:"-@,!\?§]//g;
        next unless $_;
        tr/A-Z/a-z/;
        tr/\\\[\]/öäå/;
        tr/|\{\}/öäå/;
        tr/”„†/öäå/;
        print;
        print "\n";
    };
};
