source ~/.bash_profile
for f in ` ls $1 `
do
        f=$1"/"$f
        file=$f
        if [ "${file##*.}"x = "js"x ];then
                grun JavaScript program -tree $file > testjs.txt
                s="JavaScript"
        elif [ "${file##*.}"x = "java"x ];then
                grun Java8 compilationUnit -tree $file > testj8.txt
                s="Java8"
        elif [ "${file##*.}"x = "cpp"x ];then
                grun CPP14 translationunit -tree $file > testc14.txt
                s="CPP14"
        fi
        python3 data_prepare.py $f $s
		python3 feature.py
done
python3 siamese.py
python3 training.py