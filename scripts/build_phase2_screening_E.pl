#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use JSON::PP qw(decode_json);
use File::Basename qw(basename);

my $dir = 'audit/phase2_raw_search_results/E';
my $out = 'audit/phase2_screening_E.csv';

sub read_json {
    my ($path) = @_;
    # decode_json accepts UTF-8 octets and performs exactly one decode.
    open my $fh, '<:raw', $path or die "$path: $!";
    local $/;
    return decode_json(<$fh>);
}

sub csv {
    my ($value) = @_;
    $value = '' unless defined $value;
    $value =~ s/\r?\n/ /g;
    $value =~ s/"/""/g;
    return qq{"$value"};
}

my @header = qw(
  discovery_id search_id source search_date title authors year
  doi_or_identifier url duplicate_group screening_state exclusion_reason
  software_name evidence_level final_corpus_id notes
);
my @rows;
my $next = 1;
my %software_id = (
    '13CFLUX(v3)' => 'S0009', 'mfapy' => 'S0004',
    'FreeFlux' => 'S0005', 'influx_s' => 'S0007',
    'Iso2Flux' => 'S0011', 'INCA' => 'S0002',
    'OpenMebius' => 'S0006', 'Metran' => 'S0008',
    'OpenMebius2' => 'S0010', 'BayFlux' => 'S0012',
    'Isodyn' => 'S0013', 'FluxPyt' => 'S0014',
    'FiatFlux' => 'S0015', 'WUFlux' => 'S0016',
    'WUflux' => 'S0016',
);

sub add_row {
    my (%r) = @_;
    $r{discovery_id} = sprintf('E-D%04d', $next++);
    # Rows without a software/version family are explicit singleton groups,
    # rather than ungrouped records.
    $r{duplicate_group} = "E-SINGLE-$r{discovery_id}"
        unless defined($r{duplicate_group}) && length($r{duplicate_group});
    $r{final_corpus_id} //= $software_id{$r{software_name} // ''} // '';
    push @rows, \%r;
}

# Official repository/project API lookups: one discovered project each.
my @repo_specs = (
    ['0041', 'JuGit project API', 'PHASE2-SEARCH-0041_jugit_projects.json', '13CFLUX(v3)'],
    ['0044', 'GitHub repository API', 'PHASE2-SEARCH-0044_github_repo.json', 'mfapy'],
    ['0045', 'GitHub repository API', 'PHASE2-SEARCH-0045_github_repo.json', 'FreeFlux'],
    ['0048', 'GitHub repository API', 'PHASE2-SEARCH-0048_github_repo.json', 'influx_s'],
    ['0050', 'GitHub repository API', 'PHASE2-SEARCH-0050_github_repo.json', 'Iso2Flux'],
);
for my $s (@repo_specs) {
    my ($n, $source, $file, $software) = @$s;
    my $j = read_json("$dir/$file");
    my @items = ref($j) eq 'ARRAY' ? @$j : ($j);
    for my $item (@items) {
        my $title = $item->{name_with_namespace} // $item->{full_name} // $software;
        my $url = $item->{web_url} // $item->{html_url} // '';
        add_row(
            search_id => "PHASE2-SEARCH-$n", source => $source,
            search_date => '2026-07-31', title => $title, authors => 'NR',
            year => substr(($item->{created_at} // ''), 0, 4),
            doi_or_identifier => ($item->{id} // $item->{node_id} // $url),
            url => $url, duplicate_group => $software,
            screening_state => 'FULL_TEXT_INCLUDED', exclusion_reason => 'NA',
            software_name => $software, evidence_level => 'LEVEL_1_LOAD_BEARING',
            notes => 'Official repository and versioned paths inspected.'
        );
    }
}

# PubMed searches; summaries are retrieval of the identifiers returned by the
# associated prospective search, not separate discovery searches.
for my $n (qw(0042 0043 0047)) {
    my $search = read_json("$dir/PHASE2-SEARCH-${n}_pubmed.json");
    my $summary = read_json("$dir/PHASE2-SEARCH-${n}_pubmed_summary.json");
    for my $pmid (@{$search->{esearchresult}{idlist}}) {
        my $x = $summary->{result}{$pmid} // {};
        my $title = $x->{title} // "PubMed record $pmid";
        my $software = $n eq '0042' ? 'INCA' : $n eq '0047' ? 'OpenMebius' :
            $title =~ /^([^:—-]+)(?:--|—|:)/ ? $1 : '13C-MFA software lead';
        my $included = $title =~ /(INCA|OpenMebius|13CFLUX|FreeFlux|software|tool|workflow)/i;
        add_row(
            search_id => "PHASE2-SEARCH-$n", source => 'PubMed',
            search_date => '2026-07-31', title => $title,
            authors => ($x->{sortfirstauthor} // 'NR'),
            year => substr(($x->{pubdate} // ''), 0, 4),
            doi_or_identifier => "PMID:$pmid",
            url => "https://pubmed.ncbi.nlm.nih.gov/$pmid/",
            duplicate_group => $included ? $software : '',
            screening_state => $included ? 'TITLE_ABSTRACT_INCLUDED' : 'TITLE_ABSTRACT_EXCLUDED',
            exclusion_reason => $included ? 'NA' : 'Not a software-method record relevant to Workstream E',
            software_name => $included ? $software : '',
            evidence_level => $included ? 'LEVEL_2_SUPPORTING' : 'LEVEL_3_DISCOVERY_ONLY',
            notes => $included ? 'Software paper; capability claims require repository/document inspection.' : ''
        );
    }
}

# Crossref exact-name searches. Results without the named package in the title
# are prospectively excluded with an explicit reason.
my %crossref_name = (
    '0046' => 'OpenFLUX', '0049' => 'Metran', '0051' => 'sysmetab',
    '0052' => 'Isodyn', '0053' => 'ScalaFlux', '0054' => 'MIA'
);
for my $n (sort keys %crossref_name) {
    my $name = $crossref_name{$n};
    my $j = read_json("$dir/PHASE2-SEARCH-${n}_crossref.json");
    for my $x (@{$j->{message}{items}}) {
        my $title = join('; ', @{$x->{title} // []});
        my $included = $title =~ /\Q$name\E/i ||
            ($name eq 'MIA' && $title =~ /Mass Isotopolome Analyzer/i);
        my $authors = join('; ', map {
            join(' ', grep { length } ($_->{given} // '', $_->{family} // ''))
        } @{$x->{author} // []});
        my $parts = $x->{published}{'date-parts'}[0] // [];
        add_row(
            search_id => "PHASE2-SEARCH-$n", source => 'Crossref',
            search_date => '2026-07-31', title => $title, authors => $authors || 'NR',
            year => ($parts->[0] // 'NR'), doi_or_identifier => ($x->{DOI} // 'NR'),
            url => ($x->{URL} // ''), duplicate_group => $included ? $name : '',
            screening_state => $included ? 'TITLE_ABSTRACT_INCLUDED' : 'TITLE_ABSTRACT_EXCLUDED',
            exclusion_reason => $included ? 'NA' : "Name-targeted result is not about $name software",
            software_name => $included ? $name : '',
            evidence_level => $included ? 'LEVEL_2_SUPPORTING' : 'LEVEL_3_DISCOVERY_ONLY',
            notes => $included ? 'Bibliographic support only; official implementation evidence assessed separately.' : ''
        );
    }
}

# Broad official GitHub repository discovery.
my $gh = read_json("$dir/PHASE2-SEARCH-0055_github_search.json");
for my $x (@{$gh->{items}}) {
    my $name = $x->{full_name} // '';
    my $included = $name =~ m{^(?:fumiomatsuda/mfapy|maranasgroup/SteadyState-MFA|JBEI/bayflux|metabolic-engineering/OpenMebius2|maranasgroup/Nonstationary-MFA)$}i;
    add_row(
        search_id => 'PHASE2-SEARCH-0055', source => 'GitHub repository search API',
        search_date => '2026-07-31', title => $name, authors => ($x->{owner}{login} // 'NR'),
        year => substr(($x->{created_at} // ''), 0, 4),
        doi_or_identifier => ($x->{node_id} // $x->{html_url} // 'NR'),
        url => ($x->{html_url} // ''), duplicate_group => $included ? $name : '',
        screening_state => $included ? 'TITLE_ABSTRACT_INCLUDED' : 'TITLE_ABSTRACT_EXCLUDED',
        exclusion_reason => $included ? 'NA' : 'Application-specific code, thesis code, or no general software platform',
        software_name => $included ? $name : '',
        evidence_level => $included ? 'LEVEL_2_SUPPORTING' : 'LEVEL_3_DISCOVERY_ONLY',
        notes => $included ? 'Official repository lead; versioned files inspected for selected load-bearing platforms.' : ''
    );
}

# Bounded official-only closure searches.
add_row(
    search_id => 'PHASE2-SEARCH-0069', source => 'Official Antoniewicz laboratory page',
    search_date => '2026-07-31', title => 'Metran Software', authors => 'Antoniewicz Laboratory',
    year => 'NR', doi_or_identifier => 'https://cheresearch.engin.umich.edu/mranton/metran.html',
    url => 'https://cheresearch.engin.umich.edu/mranton/metran.html',
    duplicate_group => 'Metran', screening_state => 'FULL_TEXT_INCLUDED',
    exclusion_reason => 'NA', software_name => 'Metran',
    evidence_level => 'LEVEL_1_LOAD_BEARING',
    notes => 'Official feature page inspected; licence-mediated distribution documented.'
);
add_row(
    search_id => 'PHASE2-SEARCH-0070', source => 'PubMed DOI lookup',
    search_date => '2026-07-31',
    title => 'Metabolic Flux Analysis in Isotope Labeling Experiments Using the Adjoint Approach',
    authors => 'Mottelet S; Gaullier G; Sadaka G', year => '2017',
    doi_or_identifier => '10.1109/TCBB.2016.2544299',
    url => 'https://pubmed.ncbi.nlm.nih.gov/28113867/',
    duplicate_group => 'sysmetab', screening_state => 'TITLE_ABSTRACT_INCLUDED',
    exclusion_reason => 'NA', software_name => 'sysmetab',
    evidence_level => 'LEVEL_2_SUPPORTING',
    notes => 'Primary abstract verifies stationary/nonstationary adjoint-gradient implementation and an open-source package claim; historical repository was not retrievable.'
);
add_row(
    search_id => 'PHASE2-SEARCH-0071', source => 'GitHub repository API',
    search_date => '2026-07-31', title => 'seliv55/isodyn',
    authors => 'Vitaly Selivanov', year => '2019',
    doi_or_identifier => 'R_kgDOGitHub_isodyn',
    url => 'https://github.com/seliv55/isodyn', duplicate_group => 'Isodyn',
    screening_state => 'FULL_TEXT_INCLUDED', exclusion_reason => 'NA',
    software_name => 'Isodyn', evidence_level => 'LEVEL_1_LOAD_BEARING',
    notes => 'Official repository README and source inspected at commit c4f15c4ddce751d20c84b1916901c590594892e4.'
);
add_row(
    search_id => 'PHASE2-SEARCH-0072', source => 'PMC full-text backward-citation pass',
    search_date => '2026-07-31',
    title => '13CFLUX(v3) software-paper citation network',
    authors => 'Stratmann et al.', year => '2025',
    doi_or_identifier => '10.1093/bioinformatics/btaf630',
    url => 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12696647/',
    duplicate_group => '13CFLUX(v3)', screening_state => 'DUPLICATE',
    exclusion_reason => 'Same software paper/platform already retained through PHASE2-SEARCH-0041',
    software_name => '13CFLUX(v3)', evidence_level => 'LEVEL_3_DISCOVERY_ONLY',
    notes => 'Bounded reference inspection found benchmarked FreeFlux, INCA and influx_si, all already represented; no new decision-software family.'
);
add_row(
    search_id => 'PHASE2-SEARCH-0073', source => 'bioRxiv API',
    search_date => '2026-07-31',
    title => 'OpenMebius2: GUI-based software for 13C-metabolic flux analysis with tracer labeling pattern suggestions for accurate flux predictions',
    authors => 'Imada T; Shimizu H; Toya Y', year => '2026',
    doi_or_identifier => '10.64898/2026.03.20.698926',
    url => 'https://doi.org/10.64898/2026.03.20.698926',
    duplicate_group => 'OpenMebius2', screening_state => 'FULL_TEXT_INCLUDED',
    exclusion_reason => 'NA', software_name => 'OpenMebius2',
    evidence_level => 'LEVEL_1_LOAD_BEARING',
    notes => 'Official preprint metadata and versioned repository inspected; flux-precision tracer suggestion, not mechanism discrimination.'
);
for my $paper (
    ['BayFlux', '10.1371/journal.pcbi.1011111', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10664898/', 'Backman et al.', '2023'],
    ['FreeFlux', '10.1021/acssynbio.3c00265', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10510750/', 'Wu et al.', '2023'],
) {
    add_row(
        search_id => 'PHASE2-SEARCH-0074', source => 'PMC full-text software-paper pass',
        search_date => '2026-07-31', title => "$paper->[0] primary software paper",
        authors => $paper->[3], year => $paper->[4],
        doi_or_identifier => $paper->[1], url => $paper->[2],
        duplicate_group => $paper->[0], screening_state => 'FULL_TEXT_INCLUDED',
        exclusion_reason => 'NA', software_name => $paper->[0],
        evidence_level => 'LEVEL_1_LOAD_BEARING',
        notes => 'Complete primary software paper and backward software comparisons inspected.'
    );
}
for my $lead (
    ['FluxPyt', '10.7717/peerj.4716', 'https://doi.org/10.7717/peerj.4716'],
    ['FiatFlux', '10.1186/1471-2105-6-209', 'https://doi.org/10.1186/1471-2105-6-209'],
    ['WUflux', 'NR', ''],
) {
    add_row(
        search_id => 'PHASE2-SEARCH-0074',
        source => 'Backward citation from FreeFlux primary software paper',
        search_date => '2026-07-31', title => "$lead->[0] software lead",
        authors => 'NR', year => 'NR', doi_or_identifier => $lead->[1],
        url => $lead->[2], duplicate_group => $lead->[0],
        screening_state => 'TITLE_ABSTRACT_INCLUDED', exclusion_reason => 'NA',
        software_name => $lead->[0], evidence_level => 'LEVEL_3_DISCOVERY_ONLY',
        notes => 'New software-family lead from FreeFlux Table 2/references; official implementation, licence and maintenance remain unverified.'
    );
}

# Named-lead closure after restoration: exact official repository or primary
# software paper only. These occurrences do not rewrite the earlier discovery
# occurrences; they prospectively record the verification route.
add_row(
    search_id => 'PHASE2-SEARCH-0090', source => 'SourceForge project REST API',
    search_date => '2026-07-31', title => 'FluxPyt official SourceForge project and code',
    authors => 'Desai Trunil Shamrao', year => '2018',
    doi_or_identifier => '10.7717/peerj.4716',
    url => 'https://sourceforge.net/p/fluxpyt/', duplicate_group => 'FluxPyt',
    screening_state => 'FULL_TEXT_INCLUDED', exclusion_reason => 'NA',
    software_name => 'FluxPyt', evidence_level => 'LEVEL_1_LOAD_BEARING',
    notes => 'Official repository inspected at commit beb86d8811941aaaed0a05bcb3f6ebc6f49003ec; version is conflicted: setup.cfg 0.1.7 versus package __version__ 0.1.8.'
);
add_row(
    search_id => 'PHASE2-SEARCH-0091', source => 'PMC primary full text',
    search_date => '2026-07-31',
    title => 'FiatFlux – a software for metabolic flux analysis from 13C-glucose experiments',
    authors => 'Zamboni N; Fischer E; Sauer U', year => '2005',
    doi_or_identifier => '10.1186/1471-2105-6-209',
    url => 'https://pmc.ncbi.nlm.nih.gov/articles/PMC1199586/',
    duplicate_group => 'FiatFlux', screening_state => 'FULL_TEXT_INCLUDED',
    exclusion_reason => 'NA', software_name => 'FiatFlux',
    evidence_level => 'LEVEL_1_LOAD_BEARING',
    notes => 'Complete primary software paper inspected; code is available from authors for academic use but no current public versioned repository was identified.'
);
add_row(
    search_id => 'PHASE2-SEARCH-0092', source => 'PMC primary full text',
    search_date => '2026-07-31',
    title => 'WUFlux: an open-source platform for 13C metabolic flux analysis of bacterial metabolism',
    authors => 'He L; Wu SG; Zhang M; Chen Y; Tang YJ', year => '2016',
    doi_or_identifier => '10.1186/s12859-016-1314-0',
    url => 'https://pmc.ncbi.nlm.nih.gov/articles/PMC5096001/',
    duplicate_group => 'WUFlux', screening_state => 'FULL_TEXT_INCLUDED',
    exclusion_reason => 'NA', software_name => 'WUFlux',
    evidence_level => 'LEVEL_1_LOAD_BEARING',
    notes => 'Complete primary software paper inspected; exact EMU, steady-state inverse fitting, GUI, UQ and multi-tracer-input locations recorded in the Workstream E analysis.'
);
add_row(
    search_id => 'PHASE2-SEARCH-0093', source => 'Official project URL access check',
    search_date => '2026-07-31', title => 'WUFlux project homepage access route',
    authors => 'WUFlux authors', year => 'NR',
    doi_or_identifier => 'http://www.13cmfa.org/',
    url => 'http://www.13cmfa.org/', duplicate_group => 'WUFlux',
    screening_state => 'FULL_TEXT_UNAVAILABLE',
    exclusion_reason => 'Official project host did not resolve during the documented access check',
    software_name => 'WUFlux', evidence_level => 'LEVEL_3_DISCOVERY_ONLY',
    notes => 'Paper-named official project host did not resolve on 2026-07-31; primary software paper remains accessible and is the capability evidence.'
);

my %allowed_state = map { $_ => 1 } qw(
  DISCOVERED_NOT_SCREENED TITLE_ABSTRACT_INCLUDED TITLE_ABSTRACT_EXCLUDED
  FULL_TEXT_INCLUDED FULL_TEXT_EXCLUDED DUPLICATE FULL_TEXT_UNAVAILABLE
  AWAITING_VERIFICATION
);
my %allowed_evidence_level = map { $_ => 1 } qw(
  LEVEL_1_LOAD_BEARING LEVEL_2_SUPPORTING LEVEL_3_DISCOVERY_ONLY
);
my %seen_discovery;
for my $r (@rows) {
    die "duplicate discovery ID $r->{discovery_id}\n"
        if $seen_discovery{$r->{discovery_id}}++;
    die "invalid state $r->{screening_state} for $r->{discovery_id}\n"
        unless $allowed_state{$r->{screening_state}};
    die "invalid evidence level $r->{evidence_level} for $r->{discovery_id}\n"
        unless $allowed_evidence_level{$r->{evidence_level}};
    if ($r->{screening_state} eq 'TITLE_ABSTRACT_EXCLUDED' ||
        $r->{screening_state} eq 'FULL_TEXT_EXCLUDED' ||
        $r->{screening_state} eq 'DUPLICATE') {
        die "excluded or duplicate occurrence is not discovery-only for $r->{discovery_id}\n"
            unless $r->{evidence_level} eq 'LEVEL_3_DISCOVERY_ONLY';
    }
    if ($r->{screening_state} eq 'TITLE_ABSTRACT_EXCLUDED' ||
        $r->{screening_state} eq 'FULL_TEXT_EXCLUDED') {
        die "missing exclusion reason for $r->{discovery_id}\n"
            unless defined($r->{exclusion_reason}) &&
                   length($r->{exclusion_reason}) &&
                   $r->{exclusion_reason} ne 'NA';
    }
}
open my $oh, '>:encoding(UTF-8)', $out or die "$out: $!";
print {$oh} join(',', map { csv($_) } @header), "\n";
for my $r (@rows) {
    print {$oh} join(',', map { csv($r->{$_}) } @header), "\n";
}
close $oh or die "$out: $!";
my %state_count;
$state_count{$_->{screening_state}}++ for @rows;
print scalar(@rows), " prospective discovery rows written to $out\n";
print "$_=$state_count{$_}\n" for sort keys %state_count;
