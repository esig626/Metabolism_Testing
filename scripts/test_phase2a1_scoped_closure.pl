#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use open qw(:std :encoding(UTF-8));
use File::Temp qw(tempdir);
use Test::More;

my @screen_header = qw(
  phase2_record_id workstream search_source query_id date title authors year
  doi_or_identifier source_native_id duplicate_group screening_state
  exclusion_reason evidence_level final_record_id notes
);
my @triage_header = qw(
  unique_record_id title authors year doi_or_identifier source_occurrence_count
  workstream candidate_gap_affected methodological_family likely_load_bearing
  current_evidence_depth full_text_access_status screening_priority
  final_disposition exclusion_reason evidence_location notes
);
my @deferred_header = qw(
  unique_record_id title authors year doi_or_identifier source_occurrence_ids
  source_occurrence_count original_phase2_screening_state
  original_phase2_evidence_level phase2a1_scoped_disposition
  broader_review_relevance disposition_reason eligible_for_later_synthesis
  current_evidence_depth full_text_access_status likely_load_bearing
  methodological_family candidate_gap_affected evidence_location notes
);

sub csv_quote {
    my ($value) = @_;
    $value //= '';
    $value =~ s/"/""/g;
    return qq{"$value"};
}

sub write_csv {
    my ($path, $header, $rows) = @_;
    open my $fh, '>:encoding(UTF-8)', $path or die "$path: $!\n";
    print {$fh} join(',', map { csv_quote($_) } @$header), "\n";
    for my $row (@$rows) {
        print {$fh}
          join(',', map { csv_quote($row->{$_}) } @$header), "\n";
    }
    close $fh or die "$path: $!\n";
}

sub slurp {
    my ($path) = @_;
    open my $fh, '<:raw', $path or die "$path: $!\n";
    local $/;
    my $bytes = <$fh>;
    close $fh or die "$path: $!\n";
    return $bytes;
}

sub parse_csv_line {
    my ($line) = @_;
    $line =~ s/\r?\n\z//;
    my @values;
    while (length $line) {
        if ($line =~ s/^"((?:[^"]|"")*)"(?:,|\z)//) {
            my $value = $1;
            $value =~ s/""/"/g;
            push @values, $value;
        }
        elsif ($line =~ s/^([^,]*)(?:,|\z)//) {
            push @values, $1;
        }
        else {
            die "CSV parse failure\n";
        }
    }
    return @values;
}

sub read_first_row {
    my ($path) = @_;
    open my $fh, '<:encoding(UTF-8)', $path or die "$path: $!\n";
    my @header = parse_csv_line(scalar <$fh>);
    my @values = parse_csv_line(scalar <$fh>);
    close $fh or die "$path: $!\n";
    my %row;
    @row{@header} = @values;
    return \%row;
}

sub fixture {
    my (%args) = @_;
    my $dir = tempdir(CLEANUP => 1);
    my $screening = "$dir/screening.csv";
    my $triage = "$dir/triage.csv";
    my $deferred = "$dir/deferred.csv";
    my $papers = "$dir/papers.csv";
    my $log = "$dir/change_log.csv";

    write_csv($screening, \@screen_header, [{
        phase2_record_id => 'X0001',
        workstream => 'C',
        search_source => 'Fixture',
        query_id => 'PHASE2-SEARCH-9999',
        date => '2026-07-31',
        title => 'Fixture supporting paper',
        authors => 'Möllney',
        year => '2024',
        doi_or_identifier => '10.0000/fixture',
        source_native_id => 'fixture:1',
        duplicate_group => 'FIX-1',
        screening_state => 'TITLE_ABSTRACT_INCLUDED',
        exclusion_reason => '',
        evidence_level => 'LEVEL_2_SUPPORTING',
        final_record_id => '',
        notes => 'Original prospective relevance decision.',
    }]);
    write_csv($triage, \@triage_header, [{
        unique_record_id => 'U0001',
        title => 'Fixture supporting paper',
        authors => 'Möllney',
        year => '2024',
        doi_or_identifier => '10.0000/fixture',
        source_occurrence_count => '1',
        workstream => 'C',
        candidate_gap_affected => 'GAP-01',
        methodological_family => 'fixed_sample_testing',
        likely_load_bearing => 'SUPPORTING',
        current_evidence_depth => 'TITLE_ABSTRACT_LEVEL',
        full_text_access_status => 'NOT_ASSESSED',
        screening_priority => 'PRIORITY_4',
        final_disposition => $args{triage_disposition} // 'UNRESOLVED',
        exclusion_reason => $args{triage_reason} // '',
        evidence_location => '',
        notes => 'Occurrences=X0001. Query IDs=PHASE2-SEARCH-9999.',
    }]);
    my $mapping_rows = $args{mapping_rows} // [];
    write_csv($deferred, \@deferred_header, $mapping_rows);
    write_csv($papers, [qw(record_id doi)], []);
    return {
        dir => $dir,
        screening => $screening,
        triage => $triage,
        deferred => $deferred,
        papers => $papers,
        log => $log,
        mapping_count => scalar(@$mapping_rows),
    };
}

sub mapping {
    my (%args) = @_;
    return {
        unique_record_id => $args{unique_record_id} // 'U0001',
        title => 'Fixture supporting paper',
        authors => 'Möllney',
        year => '2024',
        doi_or_identifier => '10.0000/fixture',
        source_occurrence_ids => 'X0001',
        source_occurrence_count => '1',
        original_phase2_screening_state => 'TITLE_ABSTRACT_INCLUDED',
        original_phase2_evidence_level => 'LEVEL_2_SUPPORTING',
        phase2a1_scoped_disposition =>
          $args{disposition} // 'DEFERRED_RELEVANT_SUPPORTING',
        broader_review_relevance =>
          $args{broader_relevance} // 'RELEVANT_SUPPORTING',
        disposition_reason => $args{reason}
          // 'Explicitly deferred; broader-review relevance is preserved.',
        eligible_for_later_synthesis => $args{eligible}
          // 'yes_qualified_only',
        current_evidence_depth => 'TITLE_ABSTRACT_LEVEL',
        full_text_access_status => 'NOT_ASSESSED',
        likely_load_bearing => 'SUPPORTING',
        methodological_family => 'fixed_sample_testing',
        candidate_gap_affected => 'GAP-01',
        evidence_location => '',
        notes => 'Explicit fixture mapping.',
    };
}

sub run_closure {
    my ($fixture) = @_;
    local $ENV{PHASE2_SCREENING_PATH} = $fixture->{screening};
    local $ENV{PHASE2_TRIAGE_PATH} = $fixture->{triage};
    local $ENV{PHASE2_DEFERRED_PATH} = $fixture->{deferred};
    local $ENV{PHASE2_CLOSURE_CHANGE_LOG_PATH} = $fixture->{log};
    local $ENV{PHASE2_PAPERS_PATH} = $fixture->{papers};
    local $ENV{PHASE2_EXPECTED_TRIAGE_ROWS} = 1;
    local $ENV{PHASE2_EXPECTED_TRIAGE_OCCURRENCES} = 1;
    local $ENV{PHASE2_EXPECTED_DEFERRED_ROWS} =
      $fixture->{mapping_count};
    system($^X, 'scripts/apply_phase2a1_screening_closure.pl');
    return $? >> 8;
}

sub run_triage_builder {
    my ($fixture) = @_;
    local $ENV{PHASE2_SCREENING_PATH} = $fixture->{screening};
    local $ENV{PHASE2_TRIAGE_PATH} = $fixture->{triage};
    local $ENV{PHASE2_PAPERS_PATH} = $fixture->{papers};
    local $ENV{PHASE2_EXPECTED_TRIAGE_ROWS} = 1;
    local $ENV{PHASE2_EXPECTED_TRIAGE_OCCURRENCES} = 1;
    system($^X, 'scripts/build_phase2_unresolved_triage.pl');
    return $? >> 8;
}

{
    my $fixture = fixture();
    my $screen_before = slurp($fixture->{screening});
    my $triage_before = slurp($fixture->{triage});
    is(run_closure($fixture), 0,
       'unmapped supporting record does not make closure fail');
    is(slurp($fixture->{screening}), $screen_before,
       'SUPPORTING occurrence remains title/abstract included without mapping');
    is(slurp($fixture->{triage}), $triage_before,
       'non-priority triage record is not automatically reclassified');
    ok(!-e $fixture->{log},
       'no audit transition is invented when no explicit mapping exists');
}

{
    my $map = mapping();
    my $fixture = fixture(
        triage_disposition => 'FALSE_POSITIVE',
        triage_reason =>
          'Legacy automatic closure; known to require scoped correction.',
        mapping_rows => [$map],
    );
    is(run_closure($fixture), 0,
       'explicit deferred mapping applies successfully');
    my $screen_row = read_first_row($fixture->{screening});
    my $triage_row = read_first_row($fixture->{triage});
    is($screen_row->{screening_state}, 'DEFERRED_RELEVANT_SUPPORTING',
       'explicit mapping restores the supporting occurrence');
    is($screen_row->{evidence_level}, 'LEVEL_2_SUPPORTING',
       'original evidence level is restored');
    is($triage_row->{likely_load_bearing}, 'SUPPORTING',
       'original relevance classification survives');
    is($triage_row->{final_disposition}, 'DEFERRED_RELEVANT_SUPPORTING',
       'triage receives the explicit scoped disposition');

    my $screen_after_first = slurp($fixture->{screening});
    my $triage_after_first = slurp($fixture->{triage});
    my $log_after_first = slurp($fixture->{log});
    is(run_closure($fixture), 0, 'repeated explicit closure succeeds');
    is(slurp($fixture->{screening}), $screen_after_first,
       'repeat execution leaves screening bytes unchanged');
    is(slurp($fixture->{triage}), $triage_after_first,
       'repeat execution leaves triage bytes unchanged');
    is(slurp($fixture->{log}), $log_after_first,
       'repeat execution appends no audit changes');
}

{
    my $map = mapping(
        disposition => 'FALSE_POSITIVE_CONFIRMED',
        broader_relevance => 'NOT_RELEVANT_TO_ANY_REVIEW_QUESTION',
        eligible => 'no',
        reason => '',
    );
    my $fixture = fixture(
        triage_disposition => 'FALSE_POSITIVE',
        mapping_rows => [$map],
    );
    my $screen_before = slurp($fixture->{screening});
    my $triage_before = slurp($fixture->{triage});
    isnt(run_closure($fixture), 0,
         'confirmed false positive without a record-level reason aborts');
    is(slurp($fixture->{screening}), $screen_before,
       'failed false-positive validation does not replace screening');
    is(slurp($fixture->{triage}), $triage_before,
       'failed false-positive validation does not replace triage');
    ok(!-e $fixture->{log}, 'failed validation creates no change log');
}

{
    my $map = mapping(unique_record_id => 'UNKNOWN');
    my $fixture = fixture(mapping_rows => [$map]);
    my $screen_before = slurp($fixture->{screening});
    my $triage_before = slurp($fixture->{triage});
    isnt(run_closure($fixture), 0, 'unknown mapped record aborts');
    is(slurp($fixture->{screening}), $screen_before,
       'unknown record leaves screening unchanged');
    is(slurp($fixture->{triage}), $triage_before,
       'unknown record leaves triage unchanged');
}

{
    my $fixture = fixture();
    my $triage_before = slurp($fixture->{triage});
    isnt(run_triage_builder($fixture), 0,
         'triage candidate generator refuses a nonidentical curated target');
    is(slurp($fixture->{triage}), $triage_before,
       'candidate conflict leaves curated triage byte-for-byte unchanged');
}

done_testing();
