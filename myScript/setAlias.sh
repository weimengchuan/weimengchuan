list=("cdw='cd_/home/weimengchuan'"\
        "cdm='cd_/home/weimengchuan/myCode'"\
        "cdmm='cd_/home/weimengchuan/myCode/myScript'"\
        "unZip='bash_/home/weimengchuan/myCode/myScript/unZip.sh'"\
        )

for i in ${list[@]}; do
    if [[ 0 -eq `grep "${i//_/\ }" -c ~/.bashrc` ]];then
        echo "alias "${i//_/\ } >> ~/.bashrc
    fi
done

source ~/.bashrc
echo done
