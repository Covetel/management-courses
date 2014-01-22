#!/usr/bin/env perl
use strict;
use warnings;
use 5.010;
use utf8;
use Template::Latex;
use Data::Dumper;

my @certificados = qw/ /;

open DATA, "<", "course_data.txt" or die "Error con el archivo";
while(<DATA>) {
    my @course_info = split(/,/, $_);
    my @person_info = split(/:/, $course_info[5]);
    my $data = {
        nombre_curso => $course_info[0],
	desde => $course_info[1], 
	hasta => $course_info[2],
        duracion => $course_info[3],
        instructor => $course_info[4],
        id_persona => { 
            nombre => $person_info[0],
            cedula => $person_info[1]
        }
    };
    push @certificados, $data;
}
close DATA;

my $nombre_curso = $certificados[0]->{"nombre_curso"};

my $vars = {
    certificados => \@certificados,
};

my $tt = Template::Latex->new;

$tt->process('template.tt2', $vars, "$nombre_curso.pdf", binmode => 1)
|| die $tt->error();
