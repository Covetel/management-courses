#!/usr/bin/env perl
use strict;
use warnings;
use lib 'lib/';
use 5.010;
use utf8;
use Template::Latex;

my $dbi_dsn = "dbi:SQLite:dbname=db/certificados.db";
my $schema = Certificados::Latex::Schema->connect($dbi_dsn);

my @personas = $schema->resultset('Persona')->all();
my @personas_id = map {$_->id} @personas;

sub certificados {
    my ($self, $curso) = @_;
    my @certificados = $self->search({id_curso => $curso});

    my $vars = {
            certificados => \@certificados,
            };
        
            my $nombre = $certificados[0]->id_curso->nombre;
        
            my $tt = Template::Latex->new;
        
            $tt->process('src/template.tt2', $vars, "$nombre.pdf", binmode => 1)
            || die $tt->error();
        
}

$schema->resultset('CursoParticipante')->dictar_curso(
    "18", 
    "22 de Noviembre de 2013",
    6, 
    @personas_id
);

$schema->resultset('CursoParticipante')->certificados(6);
