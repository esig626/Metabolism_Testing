#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use open qw(:std :encoding(UTF-8));
use Test::More;

sub parse_csv_row {
    my ($text) = @_;
    $text =~ s/\r?\n\z//;
    my @values;
    while (length $text) {
        if ($text =~ s/^"((?:[^"]|"")*)"(?:,|\z)//) {
            my $value = $1;
            $value =~ s/""/"/g;
            push @values, $value;
        }
        elsif ($text =~ s/^([^,]*)(?:,|\z)//) {
            push @values, $1;
        }
        else {
            die "CSV parse failure near: $text\n";
        }
    }
    return @values;
}

sub read_csv {
    my ($path) = @_;
    open my $fh, '<:encoding(UTF-8)', $path or die "$path: $!\n";
    my @header = parse_csv_row(scalar <$fh>);
    my @rows;
    my $line_number = 1;
    while (my $line = <$fh>) {
        ++$line_number;
        my @values = parse_csv_row($line);
        die "$path:$line_number column mismatch\n"
          unless @values == @header;
        my %row;
        @row{@header} = @values;
        push @rows, \%row;
    }
    close $fh;
    return (\@header, \@rows);
}

sub vocabulary {
    return map { $_ => 1 } @_;
}

my ($paper_header, $papers) = read_csv('corpus/papers.csv');
my ($software_header, $software) = read_csv('corpus/software.csv');

is(scalar(@$papers), 74, 'paper corpus has 74 stable records');
is_deeply(
    [map { $_->{record_id} } @$papers],
    [map { sprintf 'P%04d', $_ } 1 .. 74],
    'paper stable IDs are complete and ordered'
);
is(scalar(@$software), 17, 'software corpus has 17 stable records');
is_deeply(
    [map { $_->{record_id} } @$software],
    [map { sprintf 'S%04d', $_ } 1 .. 17],
    'software stable IDs are complete and ordered'
);

my %doi_seen;
for my $paper (@$papers) {
    my $doi = lc($paper->{doi} // '');
    $doi =~ s{^https?://(?:dx\.)?doi\.org/}{};
    next if $doi eq '' || $doi eq 'nr';
    ok(!$doi_seen{$doi}++, "paper DOI is unique: $doi");
}

my %boolean = vocabulary(qw(yes no partial unclear NA));
my %paper_vocab = (
    publication_type => {vocabulary(qw(
      journal_article conference_paper book book_chapter thesis preprint
      technical_report software_paper software_documentation review
      perspective tutorial other
    ))},
    publication_status => {vocabulary(qw(
      peer_reviewed preprint accepted published_not_peer_reviewed
      thesis_examined retracted withdrawn superseded unclear
    ))},
    primary_or_secondary_source => {vocabulary(qw(primary secondary mixed unclear))},
    criterion_family => {vocabulary(qw(
      D_optimality T_optimality KL_optimality Bayesian_discrimination
      Chernoff Fisher_information likelihood posterior other NR unclear
    ))},
    guarantee_regime => {vocabulary(qw(
      none heuristic simulation_based local_asymptotic global_asymptotic
      non_asymptotic exact_finite_sample unclear
    ))},
    robustness_scope => {vocabulary(qw(
      none local_neighbourhood sampled_flux_maps finite_scenario_set
      continuous_parameter_set structural_uncertainty_set
      distributional_uncertainty model_misspecification unclear
    ))},
    converse_type => {vocabulary(qw(
      none identifiability_obstruction rank_obstruction lower_bound
      error_exponent_converse sample_complexity_converse other unclear
    ))},
    stopping_rule => {vocabulary(qw(fixed_sample sequential adaptive unspecified NA))},
    structural_alternative_subtype => {vocabulary(qw(
      reaction_presence_absence pathway_alternative compartment_structure
      atom_mapping kinetic_mechanism mechanism_class other NA unclear
    ))},
    parameter_sharing => {vocabulary(qw(
      shared_across_conditions condition_specific partially_shared unspecified NA
    ))},
    retrieval_status => {vocabulary(qw(
      not_attempted metadata_retrieved abstract_retrieved retrieved_full_text
      retrieval_failed unclear
    ))},
    access_status => {vocabulary(qw(
      open_access author_manuscript user_supplied paywalled_or_inaccessible
      not_retrieved unclear
    ))},
    screening_disposition => {vocabulary(qw(retained excluded duplicate pending unclear))},
);

my @boolean_fields = qw(
  finite_sample uniform_or_worst_case minimax converse_or_impossibility
  structural_alternatives multiple_experiments non_iid sample_size_design
  model_misspecification full_text_inspected
);

for my $paper (@$papers) {
    for my $field (@boolean_fields) {
        ok($boolean{$paper->{$field}},
            "$paper->{record_id} has valid boolean $field=$paper->{$field}");
    }
    for my $field (sort keys %paper_vocab) {
        for my $value (split /;/, $paper->{$field}) {
            ok($paper_vocab{$field}{$value},
                "$paper->{record_id} has valid $field=$value");
        }
    }

    my $gated =
         $paper->{finite_sample} eq 'yes'
      || $paper->{uniform_or_worst_case} eq 'yes'
      || $paper->{minimax} eq 'yes'
      || $paper->{converse_or_impossibility} eq 'yes'
      || $paper->{structural_alternatives} eq 'yes'
      || $paper->{non_iid} eq 'yes'
      || $paper->{sample_size_design} eq 'yes'
      || $paper->{converse_type} !~ /^(?:none|unclear)$/;
    if ($gated) {
        is($paper->{full_text_inspected}, 'yes',
            "$paper->{record_id} gated claims have inspected full text");
        ok(length($paper->{evidence_location}) > 12
              && $paper->{evidence_location} !~ /^(?:NR|unclear)$/i,
            "$paper->{record_id} gated claims have an exact evidence location");
    }
    if ($paper->{full_text_inspected} ne 'yes') {
        is($paper->{finite_sample}, 'no',
            "$paper->{record_id} uninspected source has no finite-sample yes");
        is($paper->{uniform_or_worst_case}, 'no',
            "$paper->{record_id} uninspected source has no uniform yes");
        is($paper->{minimax}, 'no',
            "$paper->{record_id} uninspected source has no minimax yes");
        is($paper->{converse_or_impossibility}, 'no',
            "$paper->{record_id} uninspected source has no converse yes");
    }
}

my @software_capabilities = qw(
  forward_EMU_simulation inverse_flux_estimation steady_state_support
  isotopically_nonstationary_support tracer_design measurement_design
  replicate_allocation multi_experiment_support model_comparison
  uncertainty_quantification finite_sample_certification graphical_interface
  command_line_interface
);
for my $row (@$software) {
    for my $field (@software_capabilities, 'full_text_inspected') {
        ok($boolean{$row->{$field}},
            "$row->{record_id} has valid software capability $field=$row->{$field}");
        if ($row->{$field} eq 'yes') {
            is($row->{full_text_inspected}, 'yes',
                "$row->{record_id} yes-level $field has inspected evidence");
            ok(length($row->{notes}) > 30
                  && $row->{verification_status} !~ /^(?:lead_only|metadata_only)$/,
                "$row->{record_id} yes-level $field has direct evidence notes");
        }
    }
}

my ($screen_header, $screening) = read_csv('audit/phase2_screening.csv');
my %screen_state = vocabulary(qw(
  DISCOVERED_NOT_SCREENED TITLE_ABSTRACT_INCLUDED TITLE_ABSTRACT_EXCLUDED
  FULL_TEXT_INCLUDED FULL_TEXT_EXCLUDED DUPLICATE FULL_TEXT_UNAVAILABLE
  AWAITING_VERIFICATION FALSE_POSITIVE
  DEFERRED_RELEVANT_SUPPORTING DEFERRED_RELEVANT_ADJACENT
  OUT_OF_SCOPE_FOR_PHASE2A1 FALSE_POSITIVE_CONFIRMED
));
my %evidence_level = vocabulary(qw(
  LEVEL_1_LOAD_BEARING LEVEL_2_SUPPORTING LEVEL_3_DISCOVERY_ONLY
));
my %workstream = vocabulary(qw(A B C D E));
my %screen_id;
my %paper_by_id = map { $_->{record_id} => $_ } @$papers;
my %software_by_id = map { $_->{record_id} => $_ } @$software;
my %corpus_id = map { $_ => 1 } (keys %paper_by_id, keys %software_by_id);
my %screening_by_id = map { $_->{phase2_record_id} => $_ } @$screening;
is(
    $screening_by_id{'ROOT-D0177'}{authors},
    'Kristen M. DeAngelis; Grace Pold; Begüm D. Topçuoğlu; Linda T. A. van Diepen; Rebecca Varney; Jeffrey L. Blanchard; Jerry M. Melillo; Serita D. Frey',
    'known OpenAlex mojibake is normalized in the authoritative ledger'
);
for my $row (@$screening) {
    ok(!$screen_id{$row->{phase2_record_id}}++,
        "unique Phase 2 occurrence ID $row->{phase2_record_id}");
    ok($workstream{$row->{workstream}},
        "$row->{phase2_record_id} has controlled workstream");
    like($row->{query_id}, qr/^PHASE2-SEARCH-\d{4}$/,
        "$row->{phase2_record_id} has prospective query ID");
    ok($screen_state{$row->{screening_state}},
        "$row->{phase2_record_id} has controlled screening state");
    ok($evidence_level{$row->{evidence_level}},
        "$row->{phase2_record_id} has controlled evidence level");
    if ($row->{screening_state} =~ /_EXCLUDED$/
        || $row->{screening_state} eq 'FALSE_POSITIVE'
        || $row->{screening_state} eq 'FALSE_POSITIVE_CONFIRMED') {
        ok(length($row->{exclusion_reason})
              && $row->{exclusion_reason} ne 'NA',
            "$row->{phase2_record_id} prospective exclusion has a reason");
    }
    if ($row->{screening_state} =~
          /^(?:DEFERRED_RELEVANT_SUPPORTING|DEFERRED_RELEVANT_ADJACENT|OUT_OF_SCOPE_FOR_PHASE2A1)$/) {
        ok(length($row->{exclusion_reason})
              && $row->{exclusion_reason} ne 'NA',
            "$row->{phase2_record_id} scoped deferral has a reason");
    }
    if ($row->{screening_state} eq 'FULL_TEXT_INCLUDED') {
        ok($corpus_id{$row->{final_record_id}},
            "$row->{phase2_record_id} full-text inclusion maps to corpus");
    }
    if ($row->{evidence_level} eq 'LEVEL_1_LOAD_BEARING') {
        ok($corpus_id{$row->{final_record_id}},
            "$row->{phase2_record_id} load-bearing occurrence maps to corpus");
        if (my $paper = $paper_by_id{$row->{final_record_id}}) {
            is($paper->{full_text_inspected}, 'yes',
                "$row->{phase2_record_id} load-bearing paper has full text");
            ok(length($paper->{evidence_location}) > 12,
                "$row->{phase2_record_id} load-bearing paper has location");
        }
        elsif (my $platform = $software_by_id{$row->{final_record_id}}) {
            is($platform->{full_text_inspected}, 'yes',
                "$row->{phase2_record_id} load-bearing software has inspected evidence");
            ok(length($platform->{notes}) > 30,
                "$row->{phase2_record_id} load-bearing software has evidence notes");
        }
    }
}

is(
    scalar(grep { $_->{screening_state} eq 'TITLE_ABSTRACT_INCLUDED' }
                 @$screening),
    0,
    'no Phase 2 title/abstract-included occurrence remains unresolved'
);

open my $gaps, '<:encoding(UTF-8)', 'synthesis/candidate_gaps.md'
  or die $!;
local $/;
my $gap_text = <$gaps>;
close $gaps;
for my $number (1 .. 7) {
    my $id = sprintf 'GAP-%02d', $number;
    like($gap_text, qr/^## \Q$id\E\b/m, "$id is present");
}
unlike($gap_text, qr/\bUNTESTED\b/, 'no Phase 2 gap remains untested');
unlike($gap_text, qr/\bnovel\b/i, 'no candidate gap is described as novel');

open my $transfer, '<:encoding(UTF-8)',
  'analyses/adjacent_method_transfer.md' or die $!;
my $transfer_text = <$transfer>;
close $transfer;
for my $spec (
    ['T-optimal', qr/T-optimal/i],
    ['KL-optimal', qr/KL-optimal/i],
    ['robust/maximin', qr/Robust (?:or|maximin).*maximin|Robust or maximin/i],
    ['Bayesian discrimination', qr/Bayesian discrimination/i],
    ['active hypothesis testing', qr/Active hypothesis testing/i],
    ['controlled sensing', qr/Controlled sensing/i],
    ['sequential experimental design', qr/Sequential experimental design/i],
    ['composite hypothesis testing', qr/Composite (?:or compound )?hypothesis testing/i],
) {
    like($transfer_text, $spec->[1],
        "transfer analysis includes $spec->[0]");
}

done_testing();
