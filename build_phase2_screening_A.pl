#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use JSON::PP qw(decode_json);
use File::Basename qw(basename);

my $dir = 'audit/phase2_raw_search_results/A';
my $out = 'audit/phase2_screening_A.csv';
my $date = '2026-07-31';

sub read_json {
    my ($path) = @_;
    open my $fh, '<:raw', $path or die "Cannot read $path: $!\n";
    local $/;
    return decode_json(<$fh>);
}

sub csv {
    my ($value) = @_;
    $value //= '';
    $value =~ s/"/""/g;
    return qq{"$value"};
}

sub canonical_doi {
    my ($doi) = @_;
    $doi //= '';
    $doi =~ s{^https?://doi\.org/}{}i;
    $doi =~ s{^doi:\s*}{}i;
    return lc $doi;
}

my $summary = read_json("$dir/pubmed_esummary_union.json");
my %pubmed;
for my $uid (@{$summary->{result}{uids}}) {
    my $r = $summary->{result}{$uid};
    my $doi = canonical_doi($r->{elocationid});
    my $authors = join '; ', map { $_->{name} } @{$r->{authors} || []};
    $pubmed{$uid} = {
        title => $r->{title} // '',
        authors => $authors,
        year => (($r->{pubdate} // '') =~ /(\d{4})/ ? $1 : ''),
        identifier => $doi || "PMID:$uid",
    };
}

my @sources = (
    [ 'PHASE2-SEARCH-0001', 'PubMed', "$dir/PHASE2-SEARCH-0001_pubmed_esearch.json" ],
    [ 'PHASE2-SEARCH-0002', 'OpenAlex', "$dir/PHASE2-SEARCH-0002_openalex.json" ],
    [ 'PHASE2-SEARCH-0003', 'PubMed', "$dir/PHASE2-SEARCH-0003_pubmed_esearch.json" ],
    [ 'PHASE2-SEARCH-0004', 'OpenAlex', "$dir/PHASE2-SEARCH-0004_openalex.json" ],
    [ 'PHASE2-SEARCH-0005', 'PubMed', "$dir/PHASE2-SEARCH-0005_pubmed_esearch.json" ],
    [ 'PHASE2-SEARCH-0006', 'Crossref', "$dir/PHASE2-SEARCH-0006_crossref.json" ],
    [ 'PHASE2-SEARCH-0007', 'PubMed', "$dir/PHASE2-SEARCH-0007_pubmed_esearch.json" ],
    [ 'PHASE2-SEARCH-0008', 'OpenAlex', "$dir/PHASE2-SEARCH-0008_openalex.json" ],
    [ 'PHASE2-SEARCH-0009', 'OpenAlex forward citations', "$dir/PHASE2-SEARCH-0009_openalex_forward_citations.json" ],
    [ 'PHASE2-SEARCH-0010', 'Crossref', "$dir/PHASE2-SEARCH-0010_crossref.json" ],
);

my %full_text = map { $_ => 1 } qw(
  10.3389/fbioe.2021.685323
  10.1371/journal.pcbi.1006533
  10.1186/1752-0509-6-43
  10.1016/j.ymben.2011.12.005
  10.1016/j.ymben.2011.12.004
  10.1016/j.ymben.2016.06.001
);
my %corpus_id = (
  '10.3389/fbioe.2021.685323' => 'P0009',
  '10.1371/journal.pcbi.1006533' => 'P0036',
  '10.1186/1752-0509-6-43' => 'P0006',
  '10.1016/j.ymben.2011.12.005' => 'P0005',
  '10.1016/j.ymben.2011.12.004' => 'P0007',
  '10.1016/j.ymben.2016.06.001' => 'P0037',
  '10.1186/1471-2105-9-152' => 'P0046',
  '10.1371/journal.pcbi.1009999' => 'P0030',
  '10.1016/j.ymben.2012.06.003' => 'P0033',
  '10.1016/j.ymben.2013.08.006' => 'P0008',
  '10.1006/mben.2001.0187' => 'P0001',
);

# Explicit audit decisions. These identifiers were false negatives under the
# broad title heuristic but are relevant design, measurement, replication, or
# parallel-experiment leads. They remain supporting/discovery evidence unless
# the primary full text was inspected separately.
my %audited_inclusion = (
  '10.1002/bit.24997' => [
    'LEVEL_2_SUPPORTING',
    'Abstract-level software/design lead; no load-bearing claim.'
  ],
  '10.1002/bit.24344' => [
    'LEVEL_2_SUPPORTING',
    'Direct measurement-fragmentation lead relevant to measurement design.'
  ],
  '10.1021/acs.analchem.6b00188.s001' => [
    'LEVEL_3_DISCOVERY_ONLY',
    'Adjacent sample-size/power lead; supplemental record cannot support a substantive claim.'
  ],
  '10.1039/9781849735162-00035' => [
    'LEVEL_3_DISCOVERY_ONLY',
    'Adjacent metabolomics sample-size/design chapter retained for discovery only.'
  ],
  '10.1016/j.copbio.2013.02.003' => [
    'LEVEL_3_DISCOVERY_ONLY',
    'Secondary isotope-design review retained for primary-source discovery only.'
  ],
  '10.1016/j.ymben.2013.08.006' => [
    'LEVEL_2_SUPPORTING',
    'Abstract-level parallel-experiment method; no load-bearing claim.'
  ],
  '10.1016/j.ymben.2015.01.001' => [
    'LEVEL_2_SUPPORTING',
    'Direct multi-experiment isotope-analysis lead; design implications remain provisional.'
  ],
  '10.1016/j.copbio.2012.10.011' => [
    'LEVEL_3_DISCOVERY_ONLY',
    'Measurement-method review retained for primary-source discovery only.'
  ],
  '10.1039/c2mb25253h' => [
    'LEVEL_2_SUPPORTING',
    'Direct isotope-design lead; full method not inspected.'
  ],
  '10.1016/j.meteno.2016.06.001' => [
    'LEVEL_2_SUPPORTING',
    'Direct tracer-design lead; full method not inspected.'
  ],
);

# Crossref returned separate supplemental/review/decision objects that contain
# no distinct methodological record. Alias only the explicitly audited later
# occurrences so they inherit the first occurrence's duplicate group.
my %duplicate_alias = (
  '10.1021/acs.analchem.5c03905.s001' => '10.1021/acs.analchem.5c03905.s004',
  '10.1021/acs.analchem.5c03905.s002' => '10.1021/acs.analchem.5c03905.s004',
  '10.1021/acs.analchem.5c03905.s003' => '10.1021/acs.analchem.5c03905.s004',
  '10.1002/cjce.25733/v1/review2' => '10.1002/cjce.25733/v1/review1',
  '10.1002/cjce.25733/v2/decision1' => '10.1002/cjce.25733/v1/decision1',
);
my %seen;
my @rows;
my $sequence = 0;

sub disposition {
    my ($title, $identifier) = @_;
    my $lc = lc $title;
    my $doi = canonical_doi($identifier);
    return ('TITLE_ABSTRACT_INCLUDED', '', $audited_inclusion{$doi}[0])
        if $audited_inclusion{$doi};
    return ('FULL_TEXT_INCLUDED', '', 'LEVEL_1_LOAD_BEARING')
        if $full_text{$doi};
    if ($lc =~ /(review|guide to|roadmap|past, present|perspective)/) {
        return ('TITLE_ABSTRACT_EXCLUDED', 'SECONDARY_SOURCE_NOT_RETAINED_FOR_PRIMARY_METHOD_EVIDENCE', 'LEVEL_3_DISCOVERY_ONLY');
    }
    if ($lc =~ /(13c|carbon labeling|isotopic|isotope)/ &&
        $lc =~ /(tracer|experimental design|experiment design|parallel labeling|measurement|fragment|instationary|nonstationary)/) {
        return ('TITLE_ABSTRACT_INCLUDED', '', 'LEVEL_2_SUPPORTING');
    }
    if ($lc =~ /(metabolic flux|metabolism|metabolom|label)/) {
        return ('TITLE_ABSTRACT_EXCLUDED', 'NO_GENERALISABLE_EXPERIMENTAL_DESIGN_METHOD', 'LEVEL_3_DISCOVERY_ONLY');
    }
    return ('TITLE_ABSTRACT_EXCLUDED', 'UNRELATED_TO_13C_MFA_EXPERIMENTAL_DESIGN', 'LEVEL_3_DISCOVERY_ONLY');
}

for my $spec (@sources) {
    my ($qid, $source, $path) = @$spec;
    my $j = read_json($path);
    my @records;
    if ($j->{esearchresult}) {
        @records = map { +{ %{$pubmed{$_}}, native_id => "PMID:$_" } }
                   @{$j->{esearchresult}{idlist}};
    } elsif ($j->{results}) {
        @records = map {
            my $authors = join '; ', map { $_->{author}{display_name} // '' } @{$_->{authorships} || []};
            +{
                title => $_->{title} // '',
                authors => $authors,
                year => $_->{publication_year} // '',
                identifier => canonical_doi($_->{doi}) || ($_->{id} // ''),
                native_id => $_->{id} // '',
            }
        } @{$j->{results}};
    } elsif ($j->{message}{items}) {
        @records = map {
            my $authors = join '; ', map {
                join(' ', grep { length } ($_->{given} // '', $_->{family} // ''))
            } @{$_->{author} || []};
            +{
                title => $_->{title}[0] // '',
                authors => $authors,
                year => $_->{published}{'date-parts'}[0][0] // '',
                identifier => canonical_doi($_->{DOI}) || ($_->{URL} // ''),
                native_id => $_->{DOI} // $_->{URL} // '',
            }
        } @{$j->{message}{items}};
    }
    for my $r (@records) {
        ++$sequence;
        my $doi = canonical_doi($r->{identifier});
        my $key = $duplicate_alias{$doi} || $doi || lc($r->{title});
        my ($state, $reason, $level) = disposition($r->{title}, $r->{identifier});
        my $dup_group = $seen{$key} // sprintf('A-DUP-%04d', scalar(keys %seen) + 1);
        if ($seen{$key}) {
            $state = 'DUPLICATE';
            $reason = 'DUPLICATE_RECORD_RETURNED_BY_EARLIER_PHASE2A_QUERY';
            $level = 'LEVEL_3_DISCOVERY_ONLY';
        } else {
            $seen{$key} = $dup_group;
        }
        my $audit_note = $audited_inclusion{$doi}
            ? ' ' . $audited_inclusion{$doi}[1]
            : '';
        push @rows, [
            sprintf('A%04d', $sequence), $source, $qid, $date,
            $r->{title}, $r->{authors}, $r->{year}, $r->{identifier},
            $r->{native_id}, $dup_group, $state, $reason, $level,
            ($corpus_id{$doi} // ''),
            'Prospective Workstream A screening; API result-rank set preserved in raw snapshot.' . $audit_note
        ];
    }
}

open my $fh, '>:encoding(UTF-8)', $out or die "Cannot write $out: $!\n";
my @header = qw(
  workstream_record_id search_source query_id search_date title authors year
  doi_or_identifier source_native_id duplicate_group screening_state
  exclusion_reason evidence_level final_corpus_id notes
);
print {$fh} join(',', map { csv($_) } @header), "\n";
for my $row (@rows) {
    print {$fh} join(',', map { csv($_) } @$row), "\n";
}
close $fh or die "Cannot close $out: $!\n";
print "Wrote ", scalar(@rows), " result occurrences; ", scalar(keys %seen), " unique records.\n";
