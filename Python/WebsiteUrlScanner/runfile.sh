#!/bin/bash

echo "I am running this bash script"

function GetDirectory(){
namedom=~/Desktop/script/domains
dirs=($(find "$namedom" -type d))
for dir in "${dirs[@]}"; do
	cd "$namedom"
	cd "$dir"
	echo $PWD
	cd ..

done
}

#GetDirectory

#Dir1=~/Desktop/script/domains
#cd "${Dir1}"
#pwd

function SetDirectory(){
namedom="domains"
#cd "$namedom"
dirs=($namedom/*)
mkdir -p results
#cd results
for dir in "${dirs[@]}"; do
b=$(basename $dir)
echo "$b"
cd results
mkdir -p $b
cd ..
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/Domains0-9.txt -r results/$b/0-9Results.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsA.txt -r results/$b/AResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsB.txt -r results/$b/BResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsC.txt -r results/$b/CResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsD.txt -r results/$b/DResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsE.txt -r results/$b/EResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsF.txt -r results/$b/FResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsG.txt -r results/$b/GResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsH.txt -r results/$b/HResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsI.txt -r results/$b/IResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsJ.txt -r results/$b/JResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsK.txt -r results/$b/KResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsL.txt -r results/$b/LResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsM.txt -r results/$b/MResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsN.txt -r results/$b/NResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsO.txt -r results/$b/OResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsP.txt -r results/$b/PResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsQ.txt -r results/$b/RResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsR.txt -r results/$b/SResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsS.txt -r results/$b/SResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsT.txt -r results/$b/TResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsU.txt -r results/$b/UResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsV.txt -r results/$b/VResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsW.txt -r results/$b/WResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsX.txt -r results/$b/XResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsY.txt -r results/$b/YResults.csv &
python3.6 SearchDom.py -a auto -s search.txt -d domains/$b/DomainsZ.txt -r results/$b/ZResults.csv &
wait

done
}

SetDirectory





