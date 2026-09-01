#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use open qw(:std :encoding(UTF-8));
use Encode qw(decode FB_CROAK);
use Test::More;

sub parse_csv_row {
    my ($text) = @_;
    defined $text or die "Unexpected end of CSV\n";
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
    close $fh or die "$path: $!\n";
    return (\@header, \@rows);
}

sub slurp_bytes {
    my ($path) = @_;
    open my $fh, '<:raw', $path or die "$path: $!\n";
    local $/;
    my $bytes = <$fh>;
    close $fh;
    return $bytes;
}

my @source_paths = (
    'audit/phase2a1_screening_AC.csv',
    'audit/phase2a1_screening_DEF.csv',
);
my %source_before = map { $_ => slurp_bytes($_) } @source_paths;
my $corpus_before = slurp_bytes('corpus/papers.csv');
my $consolidated_before = slurp_bytes('audit/phase2a1_screening.csv');

is(
    system($^X, 'scripts/build_phase2a1_screening.pl'),
    0,
    'deterministic consolidation script succeeds'
);
for my $path (@source_paths) {
    is(slurp_bytes($path), $source_before{$path},
       "source ledger remains byte-for-byte unchanged: $path");
}
is(slurp_bytes('corpus/papers.csv'), $corpus_before,
   'paper corpus remains byte-for-byte unchanged by audit consolidation');
is(
    slurp_bytes('audit/phase2a1_screening.csv'),
    $consolidated_before,
    'consolidated ledger is byte-for-byte reproducible'
);

my ($header, $rows) = read_csv('audit/phase2a1_screening.csv');
my @expected_header = qw(
  phase2a1_record_id workstream_families query_id search_date search_source
  title authors year doi_or_identifier source_native_id duplicate_group
  canonical_record_id deduplication_basis source_ledger source_duplicate_group
  source_screening_state screening_state source_exclusion_reason
  exclusion_reason evidence_depth full_text_access_status evidence_location
  final_record_id corpus_action source_proposed_corpus_record raw_snapshot
  notes
);
is_deeply($header, \@expected_header, 'consolidated schema is exact');
is(scalar(@$rows), 959, 'all 959 prospective occurrences are retained');

my (%state, %ledger, %record_id, %group, %query_in_screening);
my %allowed_state = map { $_ => 1 } qw(
  FULL_TEXT_INCLUDED FULL_TEXT_EXCLUDED FULL_TEXT_UNAVAILABLE DUPLICATE
  FALSE_POSITIVE
);
my %allowed_depth = map { $_ => 1 } qw(
  LEVEL_1_LOAD_BEARING LEVEL_2_SUPPORTING LEVEL_3_DISCOVERY_ONLY
);
my %allowed_action = map { $_ => 1 } qw(
  NONE NEW_CORPUS_CANDIDATE EXISTING_CORPUS_RECORD
  DUPLICATE_OF_EXISTING_CORPUS DUPLICATE_OF_NEW_CORPUS_CANDIDATE
);

my ($paper_header, $paper_rows) = read_csv('corpus/papers.csv');
my %paper_id = map { $_->{record_id} => 1 } @$paper_rows;

my (
    @bad_occurrence_id, @bad_query_id, @bad_state, @bad_source_state,
    @bad_depth, @bad_action, @missing_raw, @missing_group,
    @missing_canonical, @missing_reason, @bad_inclusion_location,
    @bad_inclusion_depth, @bad_inclusion_access, @bad_duplicate_reason,
    @bad_final_id, @missing_final_id, @bad_final_action
);
for my $row (@$rows) {
    push @bad_occurrence_id, $row->{phase2a1_record_id}
      if $record_id{$row->{phase2a1_record_id}}++;
    push @bad_query_id, $row->{phase2a1_record_id}
      unless $row->{query_id} =~ /^PHASE2A1-SEARCH-\d{4}$/;
    ++$query_in_screening{$row->{query_id}};
    push @bad_state, $row->{phase2a1_record_id}
      unless $allowed_state{$row->{screening_state}};
    push @bad_source_state, $row->{phase2a1_record_id}
      unless $allowed_state{$row->{source_screening_state}};
    push @bad_depth, $row->{phase2a1_record_id}
      unless $allowed_depth{$row->{evidence_depth}};
    push @bad_action, $row->{phase2a1_record_id}
      unless $allowed_action{$row->{corpus_action}};
    push @missing_raw, $row->{phase2a1_record_id}
      unless -e $row->{raw_snapshot};
    push @missing_group, $row->{phase2a1_record_id}
      unless length($row->{duplicate_group}) > 0;
    push @missing_canonical, $row->{phase2a1_record_id}
      unless length($row->{canonical_record_id}) > 0;

    if ($row->{screening_state} ne 'FULL_TEXT_INCLUDED') {
        push @missing_reason, $row->{phase2a1_record_id}
          unless length($row->{exclusion_reason}) > 0
          && $row->{exclusion_reason} ne 'NA';
    }
    else {
        push @bad_inclusion_location, $row->{phase2a1_record_id}
          unless length($row->{evidence_location}) > 12;
        push @bad_inclusion_depth, $row->{phase2a1_record_id}
          if $row->{evidence_depth} eq 'LEVEL_3_DISCOVERY_ONLY';
        push @bad_inclusion_access, $row->{phase2a1_record_id}
          unless $row->{full_text_access_status} =~ /INSPECTED/;
    }
    if ($row->{screening_state} eq 'DUPLICATE') {
        push @bad_duplicate_reason, $row->{phase2a1_record_id}
          unless $row->{exclusion_reason} =~ /duplicate/i;
    }
    if ($row->{final_record_id} ne '') {
        push @bad_final_id, $row->{phase2a1_record_id}
          unless $row->{final_record_id} =~ /^P\d{4}$/;
        push @missing_final_id, $row->{phase2a1_record_id}
          unless $paper_id{$row->{final_record_id}};
        push @bad_final_action, $row->{phase2a1_record_id}
          unless $row->{corpus_action} eq 'EXISTING_CORPUS_RECORD'
          && $row->{screening_state} eq 'FULL_TEXT_INCLUDED'
          && $row->{phase2a1_record_id} eq $row->{canonical_record_id};
    }

    ++$state{$row->{screening_state}};
    ++$ledger{$row->{source_ledger}};
    push @{$group{$row->{duplicate_group}}}, $row;
}

for my $check (
    ['duplicate occurrence IDs', \@bad_occurrence_id],
    ['invalid query IDs', \@bad_query_id],
    ['invalid final states', \@bad_state],
    ['invalid preserved source states', \@bad_source_state],
    ['invalid evidence depths', \@bad_depth],
    ['invalid corpus actions', \@bad_action],
    ['missing raw snapshots', \@missing_raw],
    ['missing duplicate groups', \@missing_group],
    ['missing canonical IDs', \@missing_canonical],
    ['non-inclusions without reasons', \@missing_reason],
    ['inclusions without exact locations', \@bad_inclusion_location],
    ['discovery-only inclusions', \@bad_inclusion_depth],
    ['inclusions without inspected access', \@bad_inclusion_access],
    ['duplicates without duplicate reasons', \@bad_duplicate_reason],
    ['malformed final record IDs', \@bad_final_id],
    ['final record IDs absent from corpus', \@missing_final_id],
    ['mapped records with wrong corpus action', \@bad_final_action],
) {
    is(scalar(@{$check->[1]}), 0, $check->[0])
      or diag(join(', ', @{$check->[1]}));
}

is_deeply(
    \%ledger,
    { AC => 444, DEF => 515 },
    'source occurrence counts are preserved'
);
is_deeply(
    \%state,
    {
        DUPLICATE             => 180,
        FALSE_POSITIVE        => 727,
        FULL_TEXT_INCLUDED    => 22,
        FULL_TEXT_UNAVAILABLE => 30,
    },
    'consolidated final-state counts are exact'
);
is(scalar(keys %group), 781, '781 conservative bibliographic groups');

my ($cross_groups, $doi_cross_groups, $title_cross_groups) = (0, 0, 0);
my @bad_canonical_membership;
for my $group_id (sort keys %group) {
    my @members = @{$group{$group_id}};
    my %member_id = map { $_->{phase2a1_record_id} => 1 } @members;
    my %ledgers = map { $_->{source_ledger} => 1 } @members;
    ++$cross_groups if keys(%ledgers) > 1;
    ++$doi_cross_groups
      if keys(%ledgers) > 1
      && grep { $_->{deduplication_basis} =~ /NORMALIZED_DOI/ } @members;
    ++$title_cross_groups
      if keys(%ledgers) > 1
      && grep {
          $_->{deduplication_basis} =~ /EXACT_TITLE_AUTHOR_YEAR_NO_DOI/
      } @members;
    for my $row (@members) {
        push @bad_canonical_membership, $row->{phase2a1_record_id}
          unless $member_id{$row->{canonical_record_id}};
    }
}
is(scalar(@bad_canonical_membership), 0,
   'every canonical occurrence belongs to its duplicate group')
  or diag(join(', ', @bad_canonical_membership));
is($cross_groups, 54, '54 cross-workstream duplicate groups');
is($doi_cross_groups, 54, 'all cross-workstream joins use normalized DOI');
is($title_cross_groups, 0, 'no unsafe title-only join was needed');

my @independent_full_text_duplicates = grep {
       $_->{source_screening_state} eq 'FULL_TEXT_INCLUDED'
    && $_->{screening_state} eq 'DUPLICATE'
} @$rows;
is(scalar(@independent_full_text_duplicates), 2,
   'two cross-stream full-text verifications are deduplicated');
for my $row (@independent_full_text_duplicates) {
    ok(length($row->{evidence_location}) > 12,
       "$row->{phase2a1_record_id} duplicate retains exact source evidence");
    like($row->{exclusion_reason}, qr/CROSS_WORKSTREAM_DUPLICATE_OF=/,
         "$row->{phase2a1_record_id} points to the consolidated representative");
}

my $operation_text =
    decode('UTF-8', slurp_bytes('audit/phase2a1_search_log_AC.md'), FB_CROAK)
  . decode('UTF-8', slurp_bytes('audit/phase2a1_search_log_DEF.md'), FB_CROAK)
  . decode('UTF-8',
      slurp_bytes(
        'audit/phase2a1_raw_search_results/root/'
        . 'supplementary_web_search_snapshots.csv'
      ),
      FB_CROAK);
my %operation_id = map { $_ => 1 }
  ($operation_text =~ /(PHASE2A1-SEARCH-\d{4})/g);
my @expected_operations = (
    (map { sprintf 'PHASE2A1-SEARCH-%04d', $_ } (1 .. 19)),
    (map { sprintf 'PHASE2A1-SEARCH-%04d', $_ } (21 .. 39)),
    (map { sprintf 'PHASE2A1-SEARCH-%04d', $_ } (41 .. 75)),
);
is(scalar(keys %operation_id), 73, '73 prospective search/access IDs logged');
for my $query_id (@expected_operations) {
    ok($operation_id{$query_id}, "$query_id has an exact operation record");
}
for my $query_id (keys %query_in_screening) {
    ok($operation_id{$query_id},
       "$query_id screening occurrences link to a logged operation");
}
ok(!$operation_id{'PHASE2A1-SEARCH-0020'},
   'unassigned query ID 0020 was not manufactured');
ok(!$operation_id{'PHASE2A1-SEARCH-0040'},
   'unassigned query ID 0040 was not manufactured');

my ($root_header, $root_rows) = read_csv(
    'audit/phase2a1_raw_search_results/root/'
    . 'supplementary_web_search_snapshots.csv'
);
is(scalar(@$root_rows), 25, '25 supplementary root operations preserved');
my %root_by_id = map { $_->{query_id} => $_ } @$root_rows;
for my $query_id (qw(PHASE2A1-SEARCH-0074 PHASE2A1-SEARCH-0075)) {
    ok($root_by_id{$query_id}, "$query_id POMDP access check is preserved");
    is($root_by_id{$query_id}{result_count},
       'NOT_EXPOSED_BY_INTERFACE',
       "$query_id does not invent a result count");
    like($root_by_id{$query_id}{use}, qr/no full text obtained/,
         "$query_id records the access boundary");
}

my $screening_bytes = slurp_bytes('audit/phase2a1_screening.csv');
my $screening_text =
  eval { decode('UTF-8', $screening_bytes, FB_CROAK) };
ok(defined $screening_text, 'consolidated ledger is strict valid UTF-8');
unlike($screening_text, qr/(?:Ã|Â|â€|â€™|\x{FFFD})/,
       'consolidated ledger has no common mojibake pattern');
like($screening_text, qr/Laëtitia/, 'Laëtitia remains correctly encoded');
like($screening_text, qr/Birgé/, 'Birgé remains correctly encoded');

for my $path (
    'audit/phase2a1_search_log.md',
    'audit/phase2a1_deduplication_log.md',
    'audit/phase2a1_raw_search_results/README.md',
) {
    ok(-f $path, "$path exists");
    my $text = decode('UTF-8', slurp_bytes($path), FB_CROAK);
    ok(length($text) > 300, "$path is nontrivial UTF-8 audit documentation");
}

my $candidate_gap_text = decode(
    'UTF-8', slurp_bytes('synthesis/candidate_gaps.md'), FB_CROAK
);
my $transfer_text = decode(
    'UTF-8', slurp_bytes('analyses/adjacent_method_transfer.md'), FB_CROAK
);
my $matrix_text = decode(
    'UTF-8', slurp_bytes('synthesis/old_vs_new_matrix.md'), FB_CROAK
);
my $completion_text = decode(
    'UTF-8', slurp_bytes('audit/phase2a1_completion_report.md'), FB_CROAK
);
unlike(
    $candidate_gap_text . $transfer_text,
    qr/REQUIRES A NONTRIVIAL THEORETICAL EXTENSION/,
    'bounded evidence does not silently imply a necessary theory extension'
);
like(
    $candidate_gap_text,
    qr/GAP-06[\s\S]+?Transfer:\*\* \*\*UNRESOLVED FROM CURRENT EVIDENCE\*\*/,
    'GAP-06 transfer remains unresolved until a discrepancy class is specified'
);
like(
    $matrix_text,
    qr/Every negative entry[\s\S]+?not a universal absence claim/,
    'old-versus-new negative entries are explicitly evidence-bounded'
);
like(
    $completion_text,
    qr/Review state: COMPLETE WITHIN THE DOCUMENTED EVIDENCE BOUNDARY/,
    'completion report records bounded rather than exhaustive completion'
);

done_testing();
