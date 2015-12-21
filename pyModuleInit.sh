#!/usr/bin/env bash

echo "#!/usr/bin/env python2.7" > __init__.py

for i in *.py
do
    if [ ! "$i" = "__init__.py" ]
    then
        j=$(echo "$i" | sed -e 's/.py$//')
        echo "from $j import $j" | tee -a __init__.py
    fi
done

