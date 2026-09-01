#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use JSON::PP qw(decode_json);

my $dir = 'audit/phase2_raw_search_results/A';
my $out = 'audit/phase2_screening_A_closure.csv';
my $date = '2026-07-31';

sub read_json {
    open my $fh, '<:raw', $_[0] or die "Cannot read $_[0]: $!\n";
    local $/;
    return decode_json(<$fh>);
}
sub csv {
    my $x = $_[0] // '';
    $x =~ s/[\r\n]+/ /g;
    $x =~ s/"/""/g;
    return qq{"$x"};
}
sub doi {
    my $x = lc($_[0] // '');
    $x =~ s{^https?://doi\.org/}{};
    $x =~ s{^doi:\s*}{};
    return $x;
}
sub decision {
    my ($title, $id) = @_;
    my $t = lc($title // '');
    my $d = doi($id);
    return ('FULL_TEXT_INCLUDED', '', 'LEVEL_2_SUPPORTING')
        if $d eq '10.1186/1471-2105-9-152';
    return ('FULL_TEXT_UNAVAILABLE',
            'LOAD_BEARING_DYNAMIC_DESIGN_FULL_TEXT_NOT_LEGALLY_RETRIEVED',
            'LEVEL_2_SUPPORTING')
        if $d eq '10.1002/bit.20803';
    return ('TITLE_ABSTRACT_INCLUDED', '', 'LEVEL_2_SUPPORTING')
        if $t =~ /(experimental design|experiment design|optimal sampling|sampling time|tracer design|tracer selection|measurement uncertainty|pool size measurements|isotopically (?:nonstationary|instationary)|parallel labeling)/;
    return ('TITLE_ABSTRACT_EXCLUDED',
            length($title // '') ? 'NO_DIRECT_EXPERIMENTAL_DESIGN_METHOD' : 'REFERENCE_TITLE_UNAVAILABLE',
            'LEVEL_3_DISCOVERY_ONLY');
}

my @rows;
my %seen;
my $n = 0;
sub add_row {
    my (%r) = @_;
    ++$n;
    my $key = doi($r{identifier}) || lc($r{title} // '') || "$r{query}:$n";
    my ($state, $reason, $level) = decision($r{title}, $r{identifier});
    my $final_id = doi($r{identifier}) eq '10.1186/1471-2105-9-152'
        ? 'P0046' : '';
    my $group = $seen{$key} // sprintf('A-CLOSE-DUP-%04d', scalar(keys %seen) + 1);
    if ($seen{$key}) {
        ($state, $reason, $level) = ('DUPLICATE',
            'DUPLICATE_RECORD_RETURNED_EARLIER_IN_CLOSURE_PASS',
            'LEVEL_3_DISCOVERY_ONLY');
    } else {
        $seen{$key} = $group;
    }
    push @rows, [sprintf('AC%04d',$n), $r{source}, $r{query}, $date,
        $r{title}, $r{year}, $r{identifier}, $r{native_id}, $r{anchor},
        $group, $state, $reason, $level, $final_id, $r{notes}];
}

my $back = read_json("$dir/PHASE2-SEARCH-0056_backward_references.json");
for my $anchor (@{$back->{anchors}}) {
    for my $r (@{$anchor->{references}}) {
        add_row(source=>'Primary full-text reference list',
            query=>'PHASE2-SEARCH-0056', title=>$r->{title}, year=>'',
            identifier=>$r->{doi}, native_id=>'', anchor=>$anchor->{anchor_doi},
            notes=>'Prospective backward-reference occurrence.');
    }
}

my $sum = read_json("$dir/PHASE2-SEARCH-0057_pubmed_esummary.json");
for my $uid (@{$sum->{result}{uids}}) {
    my $r = $sum->{result}{$uid};
    my ($year) = ($r->{pubdate} // '') =~ /(\d{4})/;
    add_row(source=>'PubMed', query=>'PHASE2-SEARCH-0057',
        title=>$r->{title}, year=>$year, identifier=>doi($r->{elocationid}) || "PMID:$uid",
        native_id=>"PMID:$uid", anchor=>'', notes=>'Prospective dynamic-design query.');
}

for my $spec (
    ['PHASE2-SEARCH-0058','OpenAlex',"$dir/PHASE2-SEARCH-0058_openalex_dynamic_design.json"],
    ['PHASE2-SEARCH-0060','OpenAlex forward citations',"$dir/PHASE2-SEARCH-0060_openalex_noh_forward.json"],
) {
    my ($qid,$source,$path)=@$spec;
    my $j=read_json($path);
    for my $r (@{$j->{results}}) {
        add_row(source=>$source, query=>$qid, title=>$r->{title},
            year=>$r->{publication_year}, identifier=>doi($r->{doi}) || $r->{id},
            native_id=>$r->{id}, anchor=>($qid eq 'PHASE2-SEARCH-0060' ? '10.1002/bit.20803' : ''),
            notes=>'Prospective bounded API result.');
    }
}

my $cross=read_json("$dir/PHASE2-SEARCH-0059_crossref_dynamic_design.json");
for my $r (@{$cross->{message}{items}}) {
    add_row(source=>'Crossref', query=>'PHASE2-SEARCH-0059',
        title=>$r->{title}[0], year=>$r->{published}{'date-parts'}[0][0],
        identifier=>doi($r->{DOI}) || $r->{URL}, native_id=>$r->{DOI},
        anchor=>'', notes=>'Prospective bounded API result.');
}

open my $fh, '>:encoding(UTF-8)', $out or die "Cannot write $out: $!\n";
my @head=qw(workstream_record_id search_source query_id search_date title year
doi_or_identifier source_native_id citation_anchor duplicate_group screening_state
exclusion_reason evidence_level final_corpus_id notes);
print {$fh} join(',',map{csv($_)}@head),"\n";
print {$fh} join(',',map{csv($_)}@$_),"\n" for @rows;
close $fh or die "Cannot close $out: $!\n";
print "Wrote ".scalar(@rows)." occurrences; ".scalar(keys %seen)." unique.\n";
