#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use JSON::PP;

my $out = 'audit/phase2_screening_B_audit.csv';

sub parse_csv {
    my ($s) = @_;
    $s =~ s/\r?\n\z//;
    my @v;
    while (length $s) {
        if ($s =~ s/^"((?:[^"]|"")*)"(?:,|\z)//) {
            my $x = $1;
            $x =~ s/""/"/g;
            push @v, $x;
        }
        elsif ($s =~ s/^([^,]*)(?:,|\z)//) {
            push @v, $1;
        }
        else {
            die "CSV parse error\n";
        }
    }
    return @v;
}

sub csvq {
    my ($x) = @_;
    $x //= '';
    $x =~ s/"/""/g;
    return qq{"$x"};
}

sub read_json {
    my ($path) = @_;
    # JSON::PP::decode_json expects UTF-8 octets and performs the decode.
    open my $fh, '<:raw', $path or die "cannot read $path: $!\n";
    local $/;
    my $raw = <$fh>;
    close $fh;
    return decode_json($raw);
}

sub normalise_identifier {
    my ($id) = @_;
    $id //= '';
    $id =~ s{^\s+|\s+$}{}g;
    $id =~ s{^https?://(?:dx\.)?doi\.org/}{}i;
    return lc $id;
}

sub corpus_doi_map {
    open my $fh, '<:encoding(UTF-8)', 'corpus/papers.csv'
      or die "cannot read corpus/papers.csv: $!\n";
    my @header = parse_csv(scalar <$fh>);
    my %at;
    @at{@header} = 0 .. $#header;
    die "corpus DOI or record_id column missing\n"
      unless exists $at{doi} && exists $at{record_id};
    my %map;
    while (my $line = <$fh>) {
        my @row = parse_csv($line);
        die "corpus column mismatch\n" unless @row == @header;
        my $doi = normalise_identifier($row[$at{doi}]);
        $map{$doi} = $row[$at{record_id}]
          if length($doi) && $doi ne 'nr';
    }
    close $fh;
    return %map;
}

my %corpus = corpus_doi_map();
my @records;

sub add_record {
    my (%r) = @_;
    $r{query_id} //= '';
    $r{source} //= '';
    $r{title} //= '';
    $r{authors} //= '';
    $r{year} //= '';
    $r{identifier} //= '';
    $r{source_native_id} //= '';
    $r{relation_note} //= '';
    push @records, \%r;
}

{
    my $j = read_json(
        'audit/phase2_raw_search_results/B/PHASE2-SEARCH-0100_crossref.json'
    );
    for my $r (@{$j->{message}{items}}) {
        my $authors = join '; ', map {
            join ' ', grep { length } ($_->{given} // '', $_->{family} // '')
        } @{$r->{author} // []};
        my $year = $r->{published}{'date-parts'}[0][0] // '';
        add_record(
            query_id => 'PHASE2-SEARCH-0100',
            source => 'Crossref',
            title => $r->{title}[0] // '',
            authors => $authors,
            year => $year,
            identifier => $r->{DOI} // '',
            source_native_id => $r->{DOI} // '',
            relation_note => 'First 50 results of broad prospective Crossref audit pass.'
        );
    }
}

for my $spec (
    [
        'PHASE2-SEARCH-0101',
        'audit/phase2_raw_search_results/B/PHASE2-SEARCH-0101_anchor_openalex.json',
        'anchor'
    ],
    [
        'PHASE2-SEARCH-0101',
        'audit/phase2_raw_search_results/B/PHASE2-SEARCH-0101_backward_openalex.json',
        'backward citation'
    ],
    [
        'PHASE2-SEARCH-0101',
        'audit/phase2_raw_search_results/B/PHASE2-SEARCH-0101_forward_openalex.json',
        'forward citation'
    ],
    [
        'PHASE2-SEARCH-0102',
        'audit/phase2_raw_search_results/B/PHASE2-SEARCH-0102_anchor_openalex.json',
        'anchor'
    ],
    [
        'PHASE2-SEARCH-0102',
        'audit/phase2_raw_search_results/B/PHASE2-SEARCH-0102_backward_openalex.json',
        'backward citation'
    ],
    [
        'PHASE2-SEARCH-0102',
        'audit/phase2_raw_search_results/B/PHASE2-SEARCH-0102_forward_openalex.json',
        'forward citation'
    ]
) {
    my ($qid, $path, $relation) = @$spec;
    my $j = read_json($path);
    my @items = $relation eq 'anchor' ? ($j) : @{$j->{results}};
    for my $r (@items) {
        my $authors = join '; ', map {
            $_->{author}{display_name} // ''
        } @{$r->{authorships} // []};
        add_record(
            query_id => $qid,
            source => 'OpenAlex',
            title => $r->{display_name} // $r->{title} // '',
            authors => $authors,
            year => $r->{publication_year} // '',
            identifier => $r->{doi} // $r->{id} // '',
            source_native_id => $r->{id} // '',
            relation_note => "$relation result from the stated anchor."
        );
    }
}

{
    my $j = read_json(
        'audit/phase2_raw_search_results/B/PHASE2-SEARCH-0110-0112_web_snapshot.json'
    );
    for my $search (@{$j->{searches}}) {
        for my $r (@{$search->{scholarly_records_visible}}) {
            add_record(
                query_id => $search->{query_id},
                source => $search->{source},
                title => $r->{title},
                authors => $r->{authors},
                year => $r->{year},
                identifier => $r->{identifier},
                source_native_id => $r->{url},
                relation_note =>
                  'Structured transcription; source did not expose a native export or total count.'
            );
        }
    }
}

{
    my $j = read_json(
        'audit/phase2_raw_search_results/B/PHASE2-SEARCH-0114_web_snapshot.json'
    );
    for my $r (@{$j->{scholarly_records_visible}}) {
        add_record(
            query_id => $j->{query_id},
            source => $j->{source},
            title => $r->{title},
            authors => $r->{authors},
            year => $r->{year},
            identifier => $r->{identifier},
            source_native_id => $r->{url},
            relation_note =>
              'Exact-title routing search followed by primary PMC verification.'
        );
    }
}

add_record(
    query_id => 'PHASE2-SEARCH-0113',
    source => 'PubMed/PMC',
    title =>
      'One-shot 13C15N-metabolic flux analysis for simultaneous quantification of carbon and nitrogen flux',
    authors =>
      'Khushboo Borah Slater; Martin Beyß; Ye Xu; Jim Barber; Catia Costa; Jane Newcombe; Axel Theorell; Melanie J. Bailey; Dany J. V. Beste; Johnjoe McFadden; Katharina Nöh',
    year => '2023',
    identifier => '10.15252/msb.202211099',
    source_native_id => 'PMID:36705093;PMCID:PMC9996240',
    relation_note => 'Exact DOI retrieval; complete PMC text inspected.'
);

add_record(
    query_id => 'PHASE2-SEARCH-0115',
    source => 'PMC BioC',
    title =>
      'Robust Optimal Design of Experiments for Model Discrimination Using an Interactive Software Tool',
    authors => 'Johannes Stegmaier; Dominik Skanda; Dirk Lebiedz',
    year => '2013',
    identifier => '10.1371/journal.pone.0055723',
    source_native_id => 'PMCID:PMC3563641',
    relation_note => 'Exact PMCID retrieval; complete PMC text inspected.'
);

add_record(
    query_id => 'PHASE2-SEARCH-0116',
    source => 'PMC BioC',
    title => 'Optimal experiment design for model selection in biochemical networks',
    authors =>
      'Joep Vanlier; Christian A. Tiemann; Peter A. J. Hilbers; Natal A. W. van Riel',
    year => '2014',
    identifier => '10.1186/1752-0509-8-20',
    source_native_id => 'PMCID:PMC3946009',
    relation_note => 'Exact PMCID retrieval; complete PMC text inspected.'
);

my %include_full = map { $_ => 1 } qw(
  10.15252/msb.202211099
  10.1016/j.mbs.2026.109710
  10.1093/bioinformatics/bts585
  10.1371/journal.pone.0055723
  10.1186/1752-0509-8-20
);

my %phase2_full_id = (
    '10.15252/msb.202211099' => 'P0047',
    '10.1093/bioinformatics/bts585' => 'P0048',
    '10.1371/journal.pone.0055723' => 'P0049',
    '10.1186/1752-0509-8-20' => 'P0050',
    '10.1016/j.mbs.2026.109710' => 'P0051'
);

my %phase2_group_id = (
    'B-ONE-SHOT-2023' => 'P0047',
    'B-LIU-MAINI-BAKER-2026' => 'P0051'
);

my %include_supporting = (
    '10.1186/1752-0509-3-105' => 'LEVEL_2_SUPPORTING',
    '10.1186/1752-0509-8-46' => 'LEVEL_3_DISCOVERY_ONLY',
    '10.1111/j.1467-9876.2004.05148.x' => 'LEVEL_3_DISCOVERY_ONLY',
    '10.1186/1752-0509-6-95' => 'LEVEL_3_DISCOVERY_ONLY',
    '10.1093/bioinformatics/btm607' => 'LEVEL_3_DISCOVERY_ONLY',
    '10.1002/btpr.3413' => 'LEVEL_3_DISCOVERY_ONLY',
    '10.1016/j.ymben.2024.03.005' => 'LEVEL_3_DISCOVERY_ONLY',
    '10.1007/978-3-032-01436-8_13' => 'LEVEL_3_DISCOVERY_ONLY',
    'arxiv:2309.01476' => 'LEVEL_3_DISCOVERY_ONLY',
    '10.1093/bioinformatics/btz445' => 'LEVEL_3_DISCOVERY_ONLY',
    '10.1093/bib/bbab387' => 'LEVEL_3_DISCOVERY_ONLY',
    '10.1021/ma00080a011' => 'LEVEL_3_DISCOVERY_ONLY',
    '10.1101/2025.05.12.653312' => 'LEVEL_3_DISCOVERY_ONLY',
    '10.3390/psf2025012005' => 'LEVEL_3_DISCOVERY_ONLY'
);

sub duplicate_group {
    my ($identifier, $title) = @_;
    my $id = normalise_identifier($identifier);
    if ($id =~ /(?:j\.mbs\.2026\.109710|arxiv:2506\.11311|ssrn\.5377217)/i
        || $title =~ /^Optimal experiment design for practical parameter identifiability and model discrimination$/i) {
        return 'B-LIU-MAINI-BAKER-2026';
    }
    if ($id =~ /(?:msb\.202211099|2022\.03\.08\.483448)/i
        || $title =~ /^One[\x{2010}-\x{2015}-]?shot 13C15N-metabolic flux analysis/i) {
        return 'B-ONE-SHOT-2023';
    }
    return length($id) ? "B-$id" : 'B-TITLE-' . lc($title);
}

sub is_ancillary {
    my ($id, $title) = @_;
    return 1 if $id =~ /\.s\d+\z/i;
    return 1 if $id =~ m{/v\d+/(?:review|decision|response)\d+\z}i;
    return 1 if $title =~ /^(?:Review for|Decision letter for|Author response for)/i;
    return 0;
}

my %seen_group;
my @out_rows;
my $serial = 0;

# The software is a distinct retained scientific-software record discovered
# inside the fully inspected P0049 primary paper and verified at the official
# project location. It is not counted as another bibliographic search result.
push @out_rows, {
    phase2_record_id => 'B-AUDIT-SOFTWARE-0001',
    workstream => 'B',
    search_source => 'PMC primary paper and official SourceForge project',
    query_id => 'PHASE2-SEARCH-0115',
    date => '2026-07-31',
    title => 'ModelDiscriminationToolkitGUI',
    authors => 'Stegmaier J; Skanda D; Lebiedz D',
    year => '2013',
    doi_or_identifier => 'https://sourceforge.net/projects/mdtgui/',
    source_native_id => 'PMCID:PMC3563641;SourceForge:mdtgui',
    duplicate_group => 'B-SOFTWARE-MDTGUI',
    screening_state => 'FULL_TEXT_INCLUDED',
    exclusion_reason => 'NA',
    evidence_level => 'LEVEL_1_LOAD_BEARING',
    final_record_id => 'S0017',
    notes =>
      'Distinct software record discovered and verified in P0049: GPL GUI implementing robust biochemical model-discrimination and measurement-time design; not a second paper occurrence.'
};

for my $r (@records) {
    ++$serial;
    my $id = normalise_identifier($r->{identifier});
    my $group = duplicate_group($r->{identifier}, $r->{title});
    my ($state, $reason, $level, $final) =
      ('TITLE_ABSTRACT_EXCLUDED',
       'OUT_OF_SCOPE_FOR_WORKSTREAM_B_AFTER_TITLE_ABSTRACT_SCREEN',
       'LEVEL_3_DISCOVERY_ONLY', '');

    if (!$seen_group{$group}
        && ($include_full{$id}
            || $group eq 'B-LIU-MAINI-BAKER-2026'
            || $group eq 'B-ONE-SHOT-2023')) {
        $state = 'FULL_TEXT_INCLUDED';
        $reason = 'NA';
        $level = 'LEVEL_1_LOAD_BEARING';
        $final = $phase2_full_id{$id} // $phase2_group_id{$group} // '';
        die "missing final corpus ID for retained full-text group $group\n"
          unless length $final;
    }
    elsif (exists $corpus{$id}) {
        $state = 'DUPLICATE';
        $reason = "DUPLICATE_OF_$corpus{$id}";
        $level = 'LEVEL_3_DISCOVERY_ONLY';
        $final = $corpus{$id};
    }
    elsif ($seen_group{$group}) {
        $state = 'DUPLICATE';
        $reason = "DUPLICATE_OF_$seen_group{$group}";
        $level = 'LEVEL_3_DISCOVERY_ONLY';
        $final = $phase2_group_id{$group} // $phase2_full_id{$id} // '';
    }
    elsif (exists $include_supporting{$id}) {
        $state = 'TITLE_ABSTRACT_INCLUDED';
        $reason = 'NA';
        $level = $include_supporting{$id};
    }
    elsif (is_ancillary($id, $r->{title})) {
        $state = 'TITLE_ABSTRACT_EXCLUDED';
        $reason = 'NOT_PRIMARY_ARTICLE_ANCILLARY_MATERIAL';
        $level = 'LEVEL_3_DISCOVERY_ONLY';
    }
    elsif ($r->{query_id} =~ /^PHASE2-SEARCH-010[12]$/) {
        $state = 'TITLE_ABSTRACT_EXCLUDED';
        $reason = 'CITATION_CONTEXT_ONLY_NO_NEW_MODEL_DISCRIMINATION_METHOD_FAMILY';
        $level = 'LEVEL_3_DISCOVERY_ONLY';
    }
    elsif ($r->{query_id} eq 'PHASE2-SEARCH-0100') {
        $state = 'TITLE_ABSTRACT_EXCLUDED';
        $reason = 'GENERAL_MFA_OR_APPLICATION_NO_MODEL_DISCRIMINATION_METHOD';
        $level = 'LEVEL_3_DISCOVERY_ONLY';
    }

    my $occurrence_id = sprintf('B-AUDIT-%06d', $serial);
    if ($id eq
        '10.1002/(sici)1097-0290(1999)66:2<86::aid-bit2>3.0.co;2-a') {
        # OpenAlex supplied U+FFFD in this author name. The spelling is
        # verified by curated record P0004. The raw response is unchanged.
        $r->{authors} =
          'Michael Möllney; Wolfgang Wiechert; Dirk Kownatzki; Albert A. de Graaf';
    }
    $seen_group{$group} //= $occurrence_id;
    push @out_rows, {
        phase2_record_id => $occurrence_id,
        workstream => 'B',
        search_source => $r->{source},
        query_id => $r->{query_id},
        date => '2026-07-31',
        title => $r->{title},
        authors => $r->{authors},
        year => $r->{year},
        doi_or_identifier => $r->{identifier},
        source_native_id => $r->{source_native_id},
        duplicate_group => $group,
        screening_state => $state,
        exclusion_reason => $reason,
        evidence_level => $level,
        final_record_id => $final,
        notes => $r->{relation_note}
    };
}

my @header = qw(
  phase2_record_id workstream search_source query_id date title authors year
  doi_or_identifier source_native_id duplicate_group screening_state
  exclusion_reason evidence_level final_record_id notes
);

open my $fh, '>:encoding(UTF-8)', $out or die "cannot write $out: $!\n";
print {$fh} join(',', map { csvq($_) } @header), "\n";
for my $r (@out_rows) {
    print {$fh} join(',', map { csvq($r->{$_}) } @header), "\n";
}
close $fh or die "cannot close $out: $!\n";
print "wrote ", scalar(@out_rows), " rows to $out\n";
