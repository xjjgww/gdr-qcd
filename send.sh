source instance/path_to_root.shinc

file_list=(
    passenger_wsgi.py
    "mygdr/*.py"
    mygdr/templates
    "mygdr/static/*.*"
    mygdr/static/reward
)

[[ $# -gt 0 ]] && { file_list=($@) ; }

for f in "${file_list[@]}" ; do
    fescape=${f//\*/'___'}
    # [[ $fescape == *.sqlite ]] && { echo "Do not send sqlite to server." ; continue ; }
    filename=${fescape##*/}
    filepath=${fescape%%$filename}
    filename=${filename//'___'/'*'}

    echo "scp -P 21098 -r -O $f $path_to_root/$filepath"
    scp -P 21098 -r -O $f $path_to_root/$filepath
done
