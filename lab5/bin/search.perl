#!/usr/bin/env perl
# Jussi Karlgren, jussi@sics.se, 1997

require "getopts.pl";
&Getopts('i:e:d');
if ($opt_d) {$debug = 1;}
if (! $opt_e) {$filesuffix = "tf"} else {$filesuffix = $opt_e}

#-----------------------------------------
# get all the files in DATADIR with suffix $filesuffix

opendir(DATADIR,".");
@DATAFILES = grep(/$filesuffix$/,readdir(DATADIR));
closedir(DATADIR);

# read all the files. term frequency in first column; the term itself in the second.

%tf = ();
foreach (@DATAFILES) {
    $doc = $_;
    @fnl = split(/\./,$_);
    $docs{$doc} = 1;
    open(TF, "<", $_);

    my $max = 0;
    my %thistf = ();

    while (<TF>) {
        ($f, $w) = split;
        $thistf{$doc,$w} = $f;

        $max = $f if $f > $max;
    }
    close TF;

    while (($key, $value) = each(%thistf)) {
        $tf{$key} = $value / $max;
    }
}


#------------------------------------------
# use idf if asked for

%idf = ();
if ($opt_i) {
    open(IDF, "<", $opt_i);
    while (<IDF>) {
        my @foo = split;

        $idf{$foo[1]} = $foo[0] * $#DATAFILES;
    }
    close IDF;
}

#------------------------------------------

while (<>) {        # for each line in the query file
    %score = ();    # reset %score

    print "$_\n";

    my @ords = split;          # split for query terms

    foreach $ord (@ords) {  # for each query term
        print "$ord IDF: $idf{$ord} " if $debug;

        foreach $doc (keys %docs) {   #  for each doc
            print "$doc: $tf{$doc,$ord} " if ($tf{$doc,$ord} && $debug);

            # this is the ugly bit: here's where you get to play!
            # 1. idf and tf are multiplied with no theoretical basis for that operation;
            # 2. all the weights are summed with no attention paid to how many terms
            #    are acted on.
            # this is stupid. modify this.

            if ($opt_i) {
                $score{$doc} += $idf{$ord}*$tf{$doc,$ord}
            } else {
                $score{$doc} += $tf{$doc,$ord}
            }
        }
        print "\n" if $debug;
    }

    @sorted_docs = sort byscore keys %docs;
    @best_docs = @sorted_docs[0 .. 10];

    print $#sorted_docs;

    # sort the document by their scores
    foreach $dokument (@best_docs) {
        if ($opt_i) {
            print "$score{$dokument} $dokument\n" if $score{$dokument} > 0;
        } else {
            print "$score{$dokument} $dokument\n" if $score{$dokument} > 0;
        }
    }

    print "\n\n";
}



# sorting subroutine.
sub byscore {$score{$b} <=> $score{$a}}


