#!/usr/bin/perl

use strict;

use REST::Client;
use XML::Simple;

sub get_current_weather {
    my $location_code = @_[0];
    my $rest_url =
      "https://w1.weather.gov/xml/current_obs/${location_code}.xml";

    my $client = REST::Client->new();
    $client->GET($rest_url);
    my $content = $client->responseContent();

    return $content;
}

if ( $#ARGV == -1 ) {
    print "You must specify a location code, e.g., 'KDAY'\n";
}
else {
    my $content = get_current_weather( $ARGV[0] );

    my $ref = XMLin($content);

    print
"$ref->{weather}, $ref->{temperature_string}\nWind: $ref->{wind_string}\n(Weather) $ref->{observation_time}\n";
}

