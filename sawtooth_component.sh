#!/bin/bash

run_devmode_consensus_engine(){
	printf "\n%s\n\n" "Run devmode consensus engine..."
	sudo devmode-engine-rust -vv --connect tcp://localhost:5050
}

run_poet_engine(){
	printf "\n%s\n\n" "Run poet consensus engine..."
	sudo poet-engine -C tcp://127.0.0.1:5050 --component tcp://127.0.0.1:4004
}

run_rest_api(){
	sudo fuser -n tcp -k 8008 ;
	printf "\n%s\n\n" "Run rest-api..."
	sudo sawtooth-rest-api -v --bind 0.0.0.0:8008
}

run_settings_tp(){
	printf "\n%s\n\n" "Run setting transaction processor..."
	sudo settings-tp -v
}

run_intkey_tp(){
	printf "\n%s\n\n" "Run intkey transaction processor..."
	sudo intkey-tp-python -v
}

run_xo_tp(){
	printf "\n%s\n\n" "Run xo transaction processor..."
	sudo xo-tp-python -v
}

run_poet_tp(){
	printf "\n%s\n\n" "Run poet validator registry transaction processor..."
	sudo poet-validator-registry-tp -v
}

kill_all_components(){
	sudo kill -9 $(pgrep devmode-engine) ;
	sudo kill -9 $(pgrep poet-engine) ;
	sudo kill -9 $(pgrep sawtooth-rest) ;
	sudo kill -9 $(pgrep settings-tp) ;
	sudo kill -9 $(pgrep intkey-tp) ;
	sudo kill -9 $(pgrep xo-tp) ;
	sudo kill -9 $(pgrep poet-validator) ;
	sleep 1 ;
}

run_all_of_above(){
	sudo su &&
	run_devmode_consensus_engine &
	#run_poet_engine &
	run_rest_api &
	run_settings_tp &
	run_intkey_tp &
	#run_xo_tp &
	#run_poet_tp &

	wait
}

help_options(){
	printf "%s\n" "Allowed options:
	[1]        Run devmode consensus engine.
	[2]        Run rest-api.
	[3]        Run setting transaction processor.
	[4]        Run intkey transaction processor.
	[5]        Run xo transaction processor.
	[a]ll      Run all of above.
	[k]ill     Kill all the components process"
}

main(){
    case $1 in
    	1*) run_devmode_consensus_engine ;;
        2*) run_rest_api ;;
        3*) run_settings_tp ;;
        4*) run_intkey_tp ;;
        5*) run_xo_tp ;;
        a*) run_all_of_above ;;
        k*) kill_all_components ;;
        *)  help_options ;;
    esac
}

main "$@" ;
