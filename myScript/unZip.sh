file=$1
if [[ ${file:0-6:6} = "tar.xz" ]]; then
	xz -d $file
	tar -xvf  ${file:0:$((${#file}-3))}
fi
