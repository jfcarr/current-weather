default:
	@echo 'Targets:'
	@echo '  format'
	@echo '  critic'
	@echo '  clean'

format:
	@perltidy -b current-weather.pl

critic:
	@perlcritic current-weather.pl

clean:
	-rm -f current-weather.pl.bak
