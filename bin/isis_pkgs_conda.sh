#!/bin/bash
# will query a conda environment for packages matching an input file with
# packagename version#
# on each line
# output is in json format

envname='isisbuild'
filename='./meta/isis_dep_list.txt'
action="status"
platform="osx-64"
envpath="/usr/local/anaconda/envs/${envname}"
dest="./recipies"
self=$(basename "$0")
skip=0
declare -a missing
declare -a found


function help(){
	echo -e "\n${self} [options] <action>"
	echo -e "\nIs a set of utilities for helping create an isis build environment with conda"
	echo -e "\n\t -d <path> path to tranfer recipies for isis build. Default $dest"
	echo -e "\t -e <envname> conda environment to probe. Default $envname"
	echo -e "\t -f <filename> path to a requirements list of packages, should have name and version. Default: $filename"
	echo -e "\t -n <packagename> package to tranfer recipe for isis build. If not set all packages will be offered"
	echo -e "\t -p <path> path to conda env for isis build. Default: $envpath"
	echo -e "\t -s automatically skip any existing recipies in Transfer"
	echo -e "\n Actions:\n---------------------------------------------"
	echo -e "\tStatus: will report all installed and missing package in json format"
	echo -e "\tMissing: will report only missing packages in json format"
	echo -e "\tInstalled: will report only installed packages in json format"
	echo -e "\tMismatched: will report only the installed packages whose versions do not match the requirements"
	echo -e "\tSearch: will search anaconda cloud for the missing packages and offer to install them"
	echo -e "\tTransfer: will copy the recipies from installed matches to a destination folder.\n"

}

function get_index(){
	  local val="$1"
		shift
		local src=("${@}")
		local ret="-1"
		for ((j=0;j<${#src[@]}; j++)) do
			if [ ${src[$j]} == ${val} ]; then
				ret=${j};
				break;
			fi
	  done
		echo $ret;
}

function scan_env(){
	for pkg in ${pkgs_isis_name[@]};
	do
			if [[ ${pkgs_inst_name[@]} =~ $pkg ]]; then
					found+=($pkg)
			else
					missing+=($pkg)
			fi
	done
}


# cross check for all those packages not yet in the envrionment
function missing(){
		echo -e "[\n"
		for pkg in ${missing[@]}; do
			i=$(get_index "${pkg}" "${pkgs_isis_name[@]}" )
			echo -e "\t{\n\t\tname: ${pkg},\n\t\trequired: ${pkgs_isis_ver[$i]}\n\t},"
		done
		echo -e "\n]"
}

# cross check for those packages requires already in the environment
function installed(){
		echo -e "[\n"
		for pkg in ${found[@]}; do
			i=$(get_index "${pkg}" "${pkgs_inst_name[@]}" )
			j=$(get_index "${pkg}" "${pkgs_isis_name[@]}" )
			echo -e  "\t{\n\t\tname: ${pkg},\n\t\tinstalled: ${pkgs_inst_ver[$i]},\n\t\trequired: ${pkgs_isis_ver[$j]}\n\t},"
		done
		echo -e "\n]"
}

function mismatched(){

		for pkg in ${found[@]}; do
			i=$(get_index "${pkg}" "${pkgs_inst_name[@]}" )
			j=$(get_index "${pkg}" "${pkgs_isis_name[@]}" )
			if [ ${pkgs_inst_ver[$i]} != ${pkgs_isis_ver[$j]} ]; then
				top=$(echo -e "${pkgs_inst_ver[$i]}\n${pkgs_isis_ver[$j]}" | sort -t . -k 1,1nr -k 2,2nr -k 3,3nr | head -n 1)
				if [ ${top} != ${pkgs_isis_ver[$j]} ]; then
					ahead="${ahead}\t{\n\t\tname: ${pkg},\n\t\tinstalled: ${pkgs_inst_ver[$i]},\n\t\trequired: ${pkgs_isis_ver[$j]}\n\t},\n"
				else
					behind="${behind}\t{\n\t\tname: ${pkg},\n\t\tinstalled: ${pkgs_inst_ver[$i]},\n\t\trequired: ${pkgs_isis_ver[$j]}\n\t},\n"
				fi
			fi
		done
		echo -e "{\nahead:\n[\n${ahead}\n],"
		echo -e "behind:\n[\n${behind}\n]\n}"
}
# here we lookin in conda-meta for the env
# and copy out the recipies to a new directory
# for modification and builds
function transfer(){
	 meta=${envpath}/conda-meta
	 if [ ! -d $dest ]; then
		 mkdir $dest
		 if [ $? -ne 0]; then
			 exit 1;
		 fi
	 fi
	 if [ -n "${packagename}" ]; then
		  copyrecipe ${packagename}
	 else
		 for pkg in ${found[@]}; do

			 	copyrecipe ${pkg}
		 done
	 fi
}

function copyrecipe(){
	apkg="$1"
	i=$(get_index ${apkg} ${pkgs_inst_name[@]})
	ver=${pkgs_inst_ver[$i]}
	fname=$(find ${meta} -name ${apkg}-${ver}*.json)
	recipe=$(jq -r '.link.source' ${fname})/info/recipe
	if [ ! -d  ${dest}/${apkg} ]; then
		 cp -a ${recipe} ${dest}/${apkg}
	else
		 if [ $skip -eq 0 ]; then
			 read -p "This recipie: ${apkg} already exists, do you want to overwrite? (y/N) " yn
			 case $yn in
				 [Yy]* ) cp -a ${recipe} ${dest}/${apkg};;
				 \?) ;;
			 esac
		fi
	fi
}

# here we search for missing packages and
# do our best to find and offer those
# to install as pkg in env or recipe in dest
function search(){
	for pkg in ${missing[@]}; do
		i=$(get_index "${pkg}" "${pkgs_isis_name[@]}" )
		ver=${pkgs_isis_ver[$i]}
		list=($(anaconda search -t conda ${pkg} 2>/dev/null | grep "osx-64" | cut -d "|" -f 1,2 | tr -d ' '))
		echo "We found the following options for ${pkg}@${ver}"
		echo -e "\n---------------------"
		declare -a names; declare -a forges; declare -a versions
		for canidate in ${list[@]}; do
				version=$(cut -d '|' -f 2 <<< $canidate)
				thispkg=$(cut -d '|' -f 1 <<< $canidate)
				forge=$(cut -d '/' -f 1 <<< $thispkg)
				name=$(cut -d '/' -f 2 <<< $thispkg)
				echo -e "\n${name}::${forge}::${version}"
				names+=($name); forges+=($forge); versions+=($version)
		done
		echo -e "\n---------------------"
		for ((i=0; i<${#names[@]}; i++)); do
			echo -e "\nOption: ${forges[$i]}/${names[$i]}: ${versions[$i]}"
			read -p "Do you wish to install this package or recipe? Package, Recipe, Skip, Next (P,R,S,N): " yn
			case $yn in
				[Pp]* ) installpkg ${names[$i]} ${forges[$i]} ${versions[$i]}; break;;
				[Rr]* ) installrcp ${names[$i]} ${forges[$i]} ${versions[$i]}; break;;
				[Ss]* ) break;;
				\? ) ;;
			esac
		done
		echo -e "---------------------\n"
		unset names; unset forges; unset versions;
	done
}

function installpkg(){
	echo "installing pkg: $1 from: $2 version: $3";
  conda install -n ${envname} -c ${2} ${1}=${3}
}

function installrcp(){
	echo "installing recipe: $1 from: $2 into ${dest}";
	url=$(conda search --json -c ${2} ${1} | jq -r ".${1}[0].url")
	if [ ! -d  ${dest}/${1} ]; then
		mkdir ${dest}/${1};
	  wget -O ${dest}/${1}/${1}.tar.bz2 $url
		tar --strip-components=2 -jxvf ${dest}/${1}/${1}.tar.bz2 -C ${dest}/${1} info/recipe/
	else
		echo "recipe ${1} already exists...."
	fi
}

function status(){
	 echo -e "{\nmissing:"
	 missing;
	 echo -e ",\n installed:\n"
	 installed;
	 echo -e ",\n mismatched:\n"
	 mismatched;
	 echo  -e "\n}"
}

############# Main ##################

while getopts ":he:f:d:p:n:s" opt; do
	case $opt in
	  e)  envname=$OPTARG;;
	  f) 	filename=$OPTARG;;
		d)  dest=$OPTARG;;
		p)  envpath=$OPTARG;;
		n)  packagename=$OPTARG;;
		s)  skip=1;;
    h)	help; exit 1;;
		\?) help; exit 1;;
	esac
done

shift $((OPTIND-1)) # Shift the input arguments, so that the input file (last arg) is $1 in the code below

if [ $# -ne 1 ]; then # If no command line arguments are left (that's bad: no target was passed)
    help # print usage help
    exit # and exit
fi

action=$1;

if [ ! -f $filename ]; then
	echo "$filename is invalid."
	exit 1;
fi

pkgs_inst_name=($(conda list -n $envname --json | jq -r '.[] | .name ' ))
pkgs_inst_ver=($(conda list -n $envname --json | jq -r '.[] | .version ' ))
pkgs_isis_name=($(cat $filename | cut -d ' ' -f 1 ))
pkgs_isis_ver=($(cat $filename | cut -d ' ' -f 2 ))

scan_env;

case $action in
	status) 	status;;
	missing) 	missing;;
	installed)	installed;;
	search)		search;;
	transfer) transfer;;
	mismatched) mismatched;;
	\?) help; exit 1;;
esac
