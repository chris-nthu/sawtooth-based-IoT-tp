#!/bin/bash

HOST_IP="127.0.0.1"
#[[ -z "$EXTERNAL_IP" ]] && printf "\n\n%s\n\n" "Please set EXTERNAL_IP" && exit 1
EXTERNAL_IP="140.114.93.102"

yn() { read -rn 1 -p "$1 [y/n]: " printf '\n'; }

clean(){
	printf "\n"
	
	sudo rm -rf /var/lib/sawtooth/* && echo "Remove blockchain data from /var/lib/sawtooth/..." ;
	sudo rm -rf /var/log/sawtooth/* && echo "Remove log files from /var/log/sawtooth/..." ;
	sudo rm -rf /etc/sawtooth/keys/* && echo "Remove validator keys from /etc/sawtooth/keys/..." ;
	sudo rm -rf ~/.sawtooth/keys/* && echo "Remove user keys from ~/.sawtooth/keys/..." ;
	sudo rm *.batch && echo "Remove all the batch files.";

	printf "\n"
}

generate_user_keys(){
	printf "\n%s\n\n" "Generate a user key..."
	sawtooth keygen && printf "\n%s\n\n" "Successfully."
}

generate_root_keys_for_validator(){
	printf "\n%s\n\n" "Generate a validator key..."
	sudo sawadm keygen && printf "\n%s\n\n" "Successfully."
}

create_genesis_block(){
	printf "\n%s\n\n" "Create a genesis block..."
	sawset genesis ;
	sudo sawadm genesis config-genesis.batch && printf "\n%s\n\n" "Successfully."
}

create_genesis_block_for_multi_node(){
	sudo sawset genesis -k /etc/sawtooth/keys/validator.priv -o config-genesis.batch ;
	
	sudo sawset proposal create -k /etc/sawtooth/keys/validator.priv \
	-o config.batch \
	sawtooth.consensus.algorithm.name=PoET \
	sawtooth.consensus.algorithm.version=0.1 \
	sawtooth.poet.report_public_key_pem="$(cat /etc/sawtooth/simulator_rk_pub.pem)" \
	sawtooth.poet.valid_enclave_measurements=$(poet enclave measurement) \
	sawtooth.poet.valid_enclave_basenames=$(poet enclave basename) ;

	sudo poet registration create -k /etc/sawtooth/keys/validator.priv -o poet.batch ;

	sudo sawset proposal create -k /etc/sawtooth/keys/validator.priv sawtooth.poet.target_wait_time=5 sawtooth.poet.initial_wait_time=25 sawtooth.publisher.max_batches_per_block=100 -o poet-settings.batch
	
	sudo sawadm genesis config-genesis.batch config.batch poet.batch poet-settings.batch ;
}

run_new_single_node_validator(){
	sudo fuser -n tcp -k 4004 ;
	printf "\n%s\n\n" "Run a new single-node validator."

	clean ;
	generate_user_keys ;
	generate_root_keys_for_validator ;
	create_genesis_block ;

	# Start single-node validator.
	sudo sawtooth-validator -vv
}

run_existing_single_node_validator(){
	sudo fuser -n tcp -k 4004 ;
	printf "\n%s\n\n" "Run a existing single-node validator."

	# Start single-node validator.
	sudo sawtooth-validator -vv
}

run_new_multi_node_validator(){
	sudo fuser -n tcp -k 4004 ;
	printf "\n%s\n\n" "Run a new multi-node validator."

	clean ;
	generate_user_keys ;
	generate_root_keys_for_validator ;
	create_genesis_block_for_multi_node ;

	sudo sawtooth-validator -v \
	--bind component:tcp://"$HOST_IP":4004 \
	--bind network:tcp://"$EXTERNAL_IP":8800 \
	--bind consensus:tcp://"$HOST_IP":5050 \
	--endpoint tcp://"$EXTERAL_IP":8800 \
	#--peering dynamic
	--peers tcp://140.114.26.149:8800 \
	#--seeds tcp://140.114.26.149:8800
	#--minimum_peer_connectivity 2
}

help_options(){
	printf "%s\n" "Allowed options:
	[1]        Generate a user key.
	[2]        Generate a root key for validator.
	[3]        Run a new single-node validator.
	[4]        Run an existing single-node validator.
	[5]        Run a new multi-node validator.
	[6]        Rum an existing multi-node validator.
	[c]        Clean up all files to reset blockchain.
	"
}

main(){
	case $1 in
		1*) generate_user_keys ;;
		2*) generate_root_keys_for_validator ;;
		3*) run_new_single_node_validator ;;
		4*) run_existing_single_node_validator ;;
		5*) run_new_multi_node_validator ;;
		6*) run_existing_multi_node_validator ;;
		c*) clean ;;
		*)  help_options ;;
	esac
}

main "$@" ;