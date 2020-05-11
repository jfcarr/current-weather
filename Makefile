default:
	@echo 'Targets:'
	@echo '  format'
	@echo '  clean'

format:
	perltidy -b current-weather.pl

clean:
	-rm -f current-weather.pl.bak
