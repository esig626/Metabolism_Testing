#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use open qw(:std :encoding(UTF-8));
use Unicode::Normalize qw(NFKC);

# Deterministically normalise the Phase 2 TITLE_ABSTRACT_INCLUDED occurrence
# ledger into a paper-level triage table.  This script intentionally does not
# change the source ledger or make a full-text screening decision.

my $screening_path = $ENV{PHASE2_SCREENING_PATH}
  // 'audit/phase2_screening.csv';
my $corpus_path = $ENV{PHASE2_PAPERS_PATH}
  // 'corpus/papers.csv';
my $output_path = $ENV{PHASE2_TRIAGE_PATH}
  // 'audit/phase2_unresolved_triage.csv';
my $expected_included =
  $ENV{PHASE2_EXPECTED_TRIAGE_OCCURRENCES} // 264;
my $expected_unique =
  $ENV{PHASE2_EXPECTED_TRIAGE_ROWS} // 241;

sub parse_csv_line {
    my ($line) = @_;
    $line =~ s/\r?\n\z//;
    my @values;
    pos($line) = 0;
    while (pos($line) < length($line)) {
        if ($line =~ /\G"((?:[^"]|"")*)"(?:,|\z)/gc) {
            my $value = $1;
            $value =~ s/""/"/g;
            push @values, $value;
        }
        elsif ($line =~ /\G([^,]*)(?:,|\z)/gc) {
            push @values, $1;
        }
        else {
            die "CSV parse error near byte position " . (pos($line) // 0) . "\n";
        }
    }
    push @values, '' if $line =~ /,\z/;
    return @values;
}

sub read_csv {
    my ($path) = @_;
    open my $fh, '<:encoding(UTF-8)', $path or die "$path: $!\n";
    my $header_line = <$fh>;
    defined $header_line or die "$path is empty\n";
    my @header = parse_csv_line($header_line);
    my @rows;
    my $line_number = 1;
    while (my $line = <$fh>) {
        $line_number++;
        my @values = parse_csv_line($line);
        die "$path:$line_number column count " . scalar(@values)
          . " != " . scalar(@header) . "\n"
          unless @values == @header;
        my %row;
        @row{@header} = @values;
        push @rows, \%row;
    }
    close $fh or die "$path: $!\n";
    return (\@header, \@rows);
}

sub csv_quote {
    my ($value) = @_;
    $value //= '';
    $value =~ s/"/""/g;
    return qq{"$value"};
}

sub canonical_identifier {
    my ($value) = @_;
    $value //= '';
    $value = NFKC($value);
    $value =~ s/^\s+|\s+$//g;
    return '' unless length $value;
    my $lower = lc $value;
    $lower =~ s{^https?://(?:dx\.)?doi\.org/}{};
    $lower =~ s/^doi:\s*//;
    if ($lower =~ /(10\.\d{4,9}\/\S+)/) {
        my $doi = $1;
        $doi =~ s/[.,;:]+\z//;
        return "doi:$doi";
    }
    $lower =~ s{^https?://openalex\.org/}{openalex:};
    $lower =~ s/^pmid:\s*/pmid:/;
    $lower =~ s/\s+//g;
    return "id:$lower";
}

sub normalised_title {
    my ($value) = @_;
    $value //= '';
    $value = lc NFKC($value);
    $value =~ s/<[^>]+>/ /g;
    $value =~ s/&(?:amp|lt|gt|quot|apos|#\d+);/ /g;
    $value =~ s/[^\p{L}\p{N}]+//g;
    return $value;
}

sub author_tokens {
    my ($value) = @_;
    $value //= '';
    $value = lc NFKC($value);
    return {} if $value =~ /not completely exposed/;
    my %tokens = map { $_ => 1 }
      grep { length($_) >= 3 }
      split /[^\p{L}\p{N}]+/, $value;
    return \%tokens;
}

sub authors_overlap {
    my ($left, $right) = @_;
    my $left_tokens  = author_tokens($left);
    my $right_tokens = author_tokens($right);
    return 0 unless keys(%$left_tokens) && keys(%$right_tokens);
    return scalar grep { $right_tokens->{$_} } keys %$left_tokens;
}

sub union_find_root {
    my ($parent, $index) = @_;
    while ($parent->[$index] != $index) {
        $parent->[$index] = $parent->[ $parent->[$index] ];
        $index = $parent->[$index];
    }
    return $index;
}

sub union_find_join {
    my ($parent, $left, $right) = @_;
    my $root_left  = union_find_root($parent, $left);
    my $root_right = union_find_root($parent, $right);
    $parent->[$root_right] = $root_left if $root_left != $root_right;
}

sub contains_any {
    my ($text, @patterns) = @_;
    return scalar grep { $text =~ $_ } @patterns;
}

sub classify_record {
    my ($title, $notes, $workstreams) = @_;
    my $text = lc NFKC(join ' ', $title // '', $notes // '');

    my $foundational_lower_bound = contains_any(
        $text,
        qr/\bfano\b/, qr/\bassouad\b/, qr/\ble cam\b/, qr/\bbirg[eé]\b/,
        qr/\bmetric entropy\b/, qr/\btesting affinity\b/
    );
    my $general_converse = contains_any(
        $text,
        qr/\blower bound\b/, qr/\bconverse\b/, qr/\bimpossibil/,
        qr/\bfundamental limit/, qr/\bminimax (?:rate|risk|bound)/,
        qr/\bsample complexit/
    );
    my $fixed_composite = contains_any(
        $text,
        qr/\bcomposite hypothes/, qr/\bcomposite testing\b/,
        qr/\btesting (?:between|of) (?:convex )?(?:sets|classes)/,
        qr/\bminimax hypothes/, qr/\bnonasymptotic\b/,
        qr/\bfinite[- ]sample\b/, qr/\btype i\b/, qr/\btype ii\b/,
        qr/\bgeneralized likelihood ratio/,
        qr/\bgeneralised likelihood ratio/, qr/\bmultiple hypothes/
    );
    my $nuisance = $text =~ /\bnuisance parameter/;
    my $nuisance_testing = $nuisance && contains_any(
        $text,
        qr/\btest(?:ing|s)?\b/, qr/\bdetection\b/, qr/\bhypothes/,
        qr/\blikelihood ratio\b/, qr/\bwald\b/, qr/\brao\b/,
        qr/\bp values?\b/, qr/\binvariant power\b/
    );
    my $robust_testing = contains_any(
        $text,
        qr/\brobust hypothes/, qr/\bdistributional(?:ly)? robust/,
        qr/\bcontamination\b/, qr/\buncertainty class/,
        qr/\bleast favou?rable/, qr/\bdistributional uncertainty/
    );
    my $heterogeneous = contains_any(
        $text,
        qr/\bnon[- ]?iid\b/, qr/\bnonidentical/, qr/\bheterogeneous observation/,
        qr/\bnot identically distributed\b/,
        qr/\bindependent(?:ly)? non[- ]identical/, qr/\bfixed design\b/
    );
    my $active = contains_any(
        $text,
        qr/\bactive hypothes/, qr/\bcontrolled sensing\b/,
        qr/\bsequential (?:design|test|hypothes)/, qr/\bchernoff\b/,
        qr/\bsequential [^\n.]{0,50}\bhypothes/,
        qr/\badaptive [^\n.]{0,50}\b(?:test|hypothes)/,
        qr/\bfixed[- ]budget\b/, qr/\bfixed[- ]confidence\b/
    );
    my $testing_context = contains_any(
        $text,
        qr/\bhypothes/, qr/\btesting\b/, qr/\btest\b/,
        qr/\bdistribution(?:s| classes| sets)?\b/, qr/\bdetection\b/
    );
    my $asymptotic_only = $text =~ /\basymptotic\b/;
    my $strong_fixed_error_signal = contains_any(
        $text,
        qr/\bnonasymptotic\b/, qr/\bfinite[- ]sample\b/,
        qr/\btype i\b/, qr/\btype ii\b/, qr/\bminimax hypothes/,
        qr/\btests? with invariant power\b/,
        qr/\bverifying composite hypotheses\b/
    );
    my $discrimination_design = contains_any(
        $text,
        qr/\bmodel discrimination\b/, qr/\bmodel-discrimination\b/,
        qr/\bdiscrimination design\b/, qr/\bt-optimal/,
        qr/\bkl-optimal/, qr/\bexperimental design.*(?:model|hypothes)/,
        qr/\bdesign.*(?:model|hypothes).*discrimin/
    );
    my $metabolic_model_selection = contains_any(
        $text,
        qr/\bmodel (?:validation|selection|comparison)\b/,
        qr/\bnetwork (?:validation|selection|comparison)\b/,
        qr/\bpathway (?:selection|discrimination|elucidation)\b/,
        qr/\bmechanism discrimination\b/
    );
    my $isotope_design = contains_any(
        $text,
        qr/\btracer design\b/, qr/\btracer selection\b/,
        qr/\bisotop.*experimental design\b/, qr/\blabel(?:l)?ing experiment/,
        qr/\bparallel tracer\b/, qr/\bparallel label/, qr/\bflux precision\b/
    );
    my $software = contains_any(
        $text,
        qr/\bsoftware\b/, qr/\btoolbox\b/, qr/\bpackage\b/, qr/\bworkflow\b/,
        qr/\bopenflux\b/, qr/\bisodesign\b/, qr/^[a-z0-9_.-]+\/[a-z0-9_.-]+\z/
    );
    my $secondary = contains_any(
        $text,
        qr/\breview\b/, qr/\bperspective\b/, qr/\bputting theory into practice\b/,
        qr/\bwhat .* tell us\b/, qr/\bchapter\b/
    );
    my $misspecification = contains_any(
        $text,
        qr/\bmisspecification\b/, qr/\bmodel inadequacy\b/,
        qr/\bincorrect model\b/, qr/\bmodel discrepancy\b/,
        qr/\bgross error\b/, qr/\bmeasurement error\b/
    );
    my $correction = $text =~ /\b(?:erratum|corrigendum)\b/;
    my $clear_false_positive = contains_any(
        $text,
        qr/\bsimulation study .*model fit indices\b/,
        qr/\binterpretable machine learning .*fit indices\b/,
        qr/\bfructose metabolism in humans\b/
    );

    if ($clear_false_positive) {
        return (
            'unrelated_to_gap01_or_gap03',
            'none',
            'FALSE_POSITIVE',
            'PRIORITY_5'
        );
    }
    if ($correction) {
        return (
            'correction_or_erratum',
            'none',
            'SUPPORTING',
            'PRIORITY_3'
        );
    }
    if ($foundational_lower_bound
        || ($general_converse && $testing_context && !$active)) {
        return (
            'minimax_lower_bounds_and_converses',
            'GAP-03',
            'LOAD_BEARING',
            'PRIORITY_1'
        );
    }
    if ($active) {
        return (
            'active_sequential_or_controlled_testing',
            'GAP-01;GAP-03',
            'SUPPORTING',
            'PRIORITY_3'
        );
    }
    if ($asymptotic_only && ($fixed_composite || $nuisance_testing)) {
        return (
            'asymptotic_composite_or_nuisance_testing',
            'GAP-01;GAP-03',
            'SUPPORTING',
            'PRIORITY_3'
        );
    }
    if ($robust_testing || ($heterogeneous && $testing_context)
        || ($fixed_composite && $strong_fixed_error_signal)) {
        return (
            ($heterogeneous && $testing_context)
              ? 'fixed_block_heterogeneous_composite_testing'
              : $robust_testing ? 'robust_composite_testing'
              : 'fixed_sample_composite_testing',
            'GAP-01;GAP-03',
            'LOAD_BEARING',
            'PRIORITY_1'
        );
    }
    if ($fixed_composite || $nuisance_testing) {
        return (
            $nuisance_testing
              ? 'fixed_sample_nuisance_parameter_testing'
              : 'composite_testing_regime_unverified',
            'GAP-01;GAP-03',
            'POTENTIALLY_LOAD_BEARING',
            'PRIORITY_2'
        );
    }
    if ($nuisance || $general_converse) {
        return (
            $nuisance
              ? 'nuisance_parameter_methods'
              : 'lower_bound_or_complexity_context',
            'GAP-01;GAP-03',
            'SUPPORTING',
            'PRIORITY_3'
        );
    }
    if ($discrimination_design) {
        return (
            'experimental_design_for_model_discrimination',
            'GAP-01',
            'SUPPORTING',
            'PRIORITY_3'
        );
    }
    if ($metabolic_model_selection) {
        return (
            'metabolic_model_validation_or_discrimination',
            'GAP-01',
            'SUPPORTING',
            'PRIORITY_3'
        );
    }
    if ($misspecification) {
        return (
            'model_misspecification_or_diagnostics',
            'GAP-01',
            'SUPPORTING',
            'PRIORITY_3'
        );
    }
    if ($isotope_design) {
        return (
            'isotope_tracer_or_measurement_design',
            'none',
            'SUPPORTING',
            'PRIORITY_3'
        );
    }
    if (contains_any($text, qr/\brobust experiment design\b/,
        qr/\bmaximin optimi[sz]ation\b/)) {
        return (
            'robust_experimental_design',
            'none',
            'SUPPORTING',
            'PRIORITY_3'
        );
    }
    if ($software) {
        return (
            'scientific_software_or_workflow',
            'none',
            'SUPPORTING',
            'PRIORITY_3'
        );
    }
    if ($secondary) {
        return (
            'secondary_review_or_discovery',
            'none',
            'PERIPHERAL',
            'PRIORITY_4'
        );
    }
    if ($workstreams eq 'C') {
        return (
            'adjacent_statistical_or_decision_theory',
            'none',
            'PERIPHERAL',
            'PRIORITY_4'
        );
    }
    if ($workstreams =~ /(?:^|;)B(?:;|$)/) {
        return (
            'metabolic_model_or_mechanism_analysis',
            'GAP-01',
            'SUPPORTING',
            'PRIORITY_3'
        );
    }
    if ($workstreams =~ /(?:^|;)D(?:;|$)/) {
        return (
            'model_misspecification_context',
            'none',
            'PERIPHERAL',
            'PRIORITY_4'
        );
    }
    return (
        'domain_context_or_application',
        'none',
        'PERIPHERAL',
        'PRIORITY_4'
    );
}

my ($screening_header, $screening_rows) = read_csv($screening_path);
my @included = grep {
    ($_->{screening_state} // '') eq 'TITLE_ABSTRACT_INCLUDED'
} @$screening_rows;
die "Expected $expected_included TITLE_ABSTRACT_INCLUDED occurrences; found "
  . scalar(@included) . "\n"
  unless @included == $expected_included;

my @parent = 0 .. $#included;
my (%identifier_owner, %title_members);
for my $index (0 .. $#included) {
    my $identifier = canonical_identifier($included[$index]{doi_or_identifier});
    my $title      = normalised_title($included[$index]{title});
    if (length $identifier) {
        union_find_join(\@parent, $index, $identifier_owner{$identifier})
          if exists $identifier_owner{$identifier};
        $identifier_owner{$identifier} = $index;
    }
    push @{ $title_members{$title} }, $index if length $title;
}

# Normalized-title matching is a fallback, not permission to merge distinct
# identified publications having a generic shared title.  Join title matches
# only when authors overlap, or when an unidentified occurrence can be linked
# conservatively by a long exact title and compatible year.
for my $title (keys %title_members) {
    my @members = @{ $title_members{$title} };
    next unless @members > 1;
    for my $left_position (0 .. $#members - 1) {
        for my $right_position ($left_position + 1 .. $#members) {
            my $left  = $members[$left_position];
            my $right = $members[$right_position];
            my $left_identifier =
              canonical_identifier($included[$left]{doi_or_identifier});
            my $right_identifier =
              canonical_identifier($included[$right]{doi_or_identifier});
            my $author_match = authors_overlap(
                $included[$left]{authors},
                $included[$right]{authors}
            );
            my $left_year  = $included[$left]{year}  // '';
            my $right_year = $included[$right]{year} // '';
            my $compatible_year =
                 !$left_year
              || !$right_year
              || ($left_year =~ /^\d{4}$/ && $right_year =~ /^\d{4}$/
                  && abs($left_year - $right_year) <= 1);
            my $unidentified_fallback =
                 (!$left_identifier || !$right_identifier)
              && length($title) >= 32
              && $compatible_year;
            union_find_join(\@parent, $left, $right)
              if $author_match || $unidentified_fallback;
        }
    }
}

my %groups;
for my $index (0 .. $#included) {
    my $root = union_find_root(\@parent, $index);
    push @{ $groups{$root} }, $included[$index];
}

my ($corpus_header, $corpus_rows) = read_csv($corpus_path);
my (%corpus_by_doi, @corpus_title_candidates);
for my $row (@$corpus_rows) {
    my $doi = canonical_identifier($row->{doi});
    push @{ $corpus_by_doi{$doi} }, $row if $doi =~ /^doi:/;
    push @corpus_title_candidates, [
        normalised_title($row->{full_citation}),
        $row
    ];
}

my @group_records;
for my $members (values %groups) {
    my @sorted = sort {
           ($a->{phase2_record_id} // '') cmp ($b->{phase2_record_id} // '')
    } @$members;
    my ($representative) = sort {
           length($b->{authors} // '') <=> length($a->{authors} // '')
        || length($b->{title} // '')   <=> length($a->{title} // '')
        || ($a->{phase2_record_id} // '') cmp ($b->{phase2_record_id} // '')
    } @sorted;

    my %identifiers = map {
        my $identifier = canonical_identifier($_->{doi_or_identifier});
        length($identifier) ? ($identifier => 1) : ()
    } @sorted;
    my %titles = map {
        my $title = normalised_title($_->{title});
        length($title) ? ($title => 1) : ()
    } @sorted;
    my %workstreams = map { ($_->{workstream} // '') => 1 } @sorted;
    delete $workstreams{''};
    my $workstream_text = join ';', sort keys %workstreams;

    my %corpus_links;
    my %software_links;
    for my $row (@sorted) {
        $corpus_links{$row->{final_record_id}} = 1
          if ($row->{final_record_id} // '') =~ /^P\d{4}$/;
        $software_links{$row->{final_record_id}} = 1
          if ($row->{final_record_id} // '') =~ /^S\d{4}$/;
    }
    for my $identifier (keys %identifiers) {
        next unless $identifier =~ /^doi:/;
        for my $row (@{ $corpus_by_doi{$identifier} // [] }) {
            $corpus_links{$row->{record_id}} = 1;
        }
    }
    for my $normal_title (keys %titles) {
        next if length($normal_title) < 24;
        for my $candidate (@corpus_title_candidates) {
            my ($normal_citation, $row) = @$candidate;
            my $author_match = scalar grep {
                authors_overlap($_->{authors}, $row->{full_citation})
            } @sorted;
            $corpus_links{$row->{record_id}} = 1
              if $author_match
              && index($normal_citation, $normal_title) >= 0;
        }
    }

    my @corpus_ids = sort keys %corpus_links;
    my @matched_corpus = grep {
        my $id = $_->{record_id};
        scalar grep { $_ eq $id } @corpus_ids
    } @$corpus_rows;

    my ($family, $gaps, $load_class, $priority) = classify_record(
        $representative->{title},
        join(' ', map { $_->{notes} // '' } @sorted),
        $workstream_text
    );

    my ($depth, $access, $disposition, $evidence_location);
    my @inspected = grep { ($_->{full_text_inspected} // '') eq 'yes' }
      @matched_corpus;
    if (@inspected) {
        $depth = 'FULL_TEXT_INSPECTED';
        my %accesses = map {
            (($_->{access_status} // '') || 'unclear') => 1
        } @inspected;
        $access = 'INSPECTED:' . join(';', sort keys %accesses);
        $disposition = 'FULL_TEXT_INCLUDED';
        my %locations = map {
            (($_->{evidence_location} // '') || 'NR') => 1
        } @inspected;
        $evidence_location = join ' | ', sort keys %locations;
    }
    elsif (@matched_corpus) {
        my %verification = map {
            (($_->{verification_status} // '') || 'unclear') => 1
        } @matched_corpus;
        $depth = scalar(grep {
            /abstract/
        } keys %verification) ? 'ABSTRACT_LEVEL' : 'METADATA_OR_LEAD_ONLY';
        my %accesses = map {
            (($_->{access_status} // '') || 'unclear') => 1
        } @matched_corpus;
        $access = 'NOT_INSPECTED:' . join(';', sort keys %accesses);
        $disposition = 'UNRESOLVED';
        $evidence_location = '';
    }
    else {
        my %levels = map { ($_->{evidence_level} // '') => 1 } @sorted;
        $depth = $levels{LEVEL_2_SUPPORTING}
          ? 'TITLE_ABSTRACT_LEVEL'
          : 'DISCOVERY_ONLY';
        $access = 'NOT_ASSESSED';
        $disposition = 'UNRESOLVED';
        $evidence_location = '';
    }

    my %query_ids = map { ($_->{query_id} // '') => 1 } @sorted;
    delete $query_ids{''};
    my @occurrence_ids = map { $_->{phase2_record_id} // '' } @sorted;
    my @identifier_values = sort keys %identifiers;
    s/^(?:doi|id):// for @identifier_values;

    my @notes = (
        'Prospective Phase 2A.1 paper-level triage; no new search performed.',
        'Occurrences=' . join(';', @occurrence_ids) . '.',
        'Query IDs=' . join(';', sort keys %query_ids) . '.',
        @corpus_ids
          ? 'Existing corpus ID(s)=' . join(';', @corpus_ids) . '.'
          : 'No stable corpus paper ID assigned at triage.',
        keys(%software_links)
          ? 'Existing software corpus ID(s)='
              . join(';', sort keys %software_links) . '.'
          : (),
        'Grouping used canonical DOI/identifier first. Exact normalized-title fallback required author overlap, or a missing identifier plus a long title and compatible year.'
    );
    push @notes,
      'Multiple corpus links require manual identity review before evidence migration.'
      if @corpus_ids > 1;

    push @group_records, {
        title                    => $representative->{title} // '',
        authors                  => $representative->{authors} // '',
        year                     => $representative->{year} // '',
        doi_or_identifier        => join(';', @identifier_values),
        source_occurrence_count  => scalar(@sorted),
        workstream               => $workstream_text,
        candidate_gap_affected   => $gaps,
        methodological_family    => $family,
        likely_load_bearing      => $load_class,
        current_evidence_depth   => $depth,
        full_text_access_status  => $access,
        screening_priority       => $priority,
        final_disposition        => $disposition,
        exclusion_reason         => 'NA',
        evidence_location        => $evidence_location,
        notes                    => join(' ', @notes),
        _sort_identifier         => join(';', @identifier_values),
        _normal_title            => normalised_title($representative->{title}),
        _corpus_represented      => @corpus_ids ? 1 : 0,
    };
}

@group_records = sort {
       ($a->{_sort_identifier} // '') cmp ($b->{_sort_identifier} // '')
    || ($a->{_normal_title} // '') cmp ($b->{_normal_title} // '')
} @group_records;
die "Expected $expected_unique unique triage records; found "
  . scalar(@group_records) . "\n"
  unless @group_records == $expected_unique;

my @output_header = qw(
  unique_record_id
  title
  authors
  year
  doi_or_identifier
  source_occurrence_count
  workstream
  candidate_gap_affected
  methodological_family
  likely_load_bearing
  current_evidence_depth
  full_text_access_status
  screening_priority
  final_disposition
  exclusion_reason
  evidence_location
  notes
);

my $temporary_path = "$output_path.tmp.$$";
open my $out, '>:encoding(UTF-8)', $temporary_path
  or die "$temporary_path: $!\n";
print {$out} join(',', map { csv_quote($_) } @output_header), "\n";
my $number = 0;
for my $record (@group_records) {
    $record->{unique_record_id} = sprintf 'P2UT-%04d', ++$number;
    print {$out} join(
        ',',
        map { csv_quote($record->{$_}) } @output_header
      ),
      "\n";
}
close $out or die "$temporary_path: $!\n";

my ($generated_header, $generated_rows) = read_csv($temporary_path);
die "$temporary_path header changed unexpectedly\n"
  unless join("\x1f", @$generated_header) eq join("\x1f", @output_header);
die "$temporary_path row count changed unexpectedly\n"
  unless @$generated_rows == @group_records;
my $generated_occurrence_total = 0;
my %generated_ids;
for my $index (0 .. $#$generated_rows) {
    my $row = $generated_rows->[$index];
    my $expected_id = sprintf 'P2UT-%04d', $index + 1;
    die "$temporary_path unstable ID order at row " . ($index + 2) . "\n"
      unless ($row->{unique_record_id} // '') eq $expected_id;
    die "$temporary_path duplicate unique_record_id $expected_id\n"
      if $generated_ids{$expected_id}++;
    $generated_occurrence_total += $row->{source_occurrence_count};
}
die "$temporary_path occurrence total $generated_occurrence_total "
  . "!= $expected_included\n"
  unless $generated_occurrence_total == $expected_included;

# This is a candidate generator, not permission to replace manually curated
# triage.  Preserve the authoritative file byte-for-byte unless the candidate
# is identical; otherwise fail closed and require an explicit merge.
if (-e $output_path) {
    open my $existing, '<:raw', $output_path or die "$output_path: $!\n";
    local $/;
    my $existing_bytes = <$existing>;
    close $existing or die "$output_path: $!\n";
    open my $candidate, '<:raw', $temporary_path
      or die "$temporary_path: $!\n";
    my $candidate_bytes = <$candidate>;
    close $candidate or die "$temporary_path: $!\n";
    if ($existing_bytes ne $candidate_bytes) {
        unlink $temporary_path if -e $temporary_path;
        die "triage candidate differs from curated $output_path; refusing "
          . "replacement and requiring an explicit record-level merge\n";
    }
    unlink $temporary_path
      or die "cannot remove identical triage candidate $temporary_path: $!\n";
}
else {
    rename $temporary_path, $output_path
      or die "rename $temporary_path -> $output_path: $!\n";
}

my (
    %workstream_count,
    %workstream_combination_count,
    %gap_count,
    %gap_combination_count,
    %depth_count,
    %priority_count,
    %load_count,
    %family_count,
    %disposition_count,
    %workstream_gap_count
);
my ($represented, $unassigned) = (0, 0);
for my $record (@group_records) {
    my @record_workstreams = split /;/, $record->{workstream};
    my @record_gaps = split /;/, $record->{candidate_gap_affected};
    $workstream_count{$_}++ for @record_workstreams;
    $workstream_combination_count{ $record->{workstream} }++;
    $gap_count{$_}++ for @record_gaps;
    for my $workstream (@record_workstreams) {
        for my $gap (@record_gaps) {
            $workstream_gap_count{"$workstream/$gap"}++;
        }
    }
    $gap_combination_count{ $record->{candidate_gap_affected} }++;
    $depth_count{ $record->{current_evidence_depth} }++;
    $priority_count{ $record->{screening_priority} }++;
    $load_count{ $record->{likely_load_bearing} }++;
    $family_count{ $record->{methodological_family} }++;
    $disposition_count{ $record->{final_disposition} }++;
    $record->{_corpus_represented} ? $represented++ : $unassigned++;
}

print "source_occurrences=", scalar(@included), "\n";
print "unique_records=", scalar(@group_records), "\n";
print "duplicate_occurrences=", scalar(@included) - scalar(@group_records), "\n";
print "represented_in_corpus=$represented\n";
print "without_stable_paper_id=$unassigned\n";
for my $spec (
    ['workstream', \%workstream_count],
    ['workstream_combination', \%workstream_combination_count],
    ['gap',        \%gap_count],
    ['gap_combination', \%gap_combination_count],
    ['depth',      \%depth_count],
    ['priority',   \%priority_count],
    ['triage',     \%load_count],
    ['family',     \%family_count],
    ['disposition', \%disposition_count],
    ['workstream_gap', \%workstream_gap_count],
) {
    my ($label, $counts) = @$spec;
    print "$label ",
      join(' ', map { "$_=$counts->{$_}" } sort keys %$counts), "\n";
}
