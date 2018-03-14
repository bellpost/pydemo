内存#内存比率#free -m|grep 'Mem:' | awk '{printf("%d%\n", $3/$2*100)}'#<80%
swap#swap使用情况# free -m|grep 'Swap:'|awk '{printf("%d%\n",  $3/$2*100)}'#<20%
存储空间#root空间#df -lP | grep -e 'centos-root' | awk '{print $5}'#<85%
存储空间#sda1空间#df -lP | grep -e 'sda1' | awk '{print $5}'#<85%
存储空间#sdb1空间#df -lP | grep -e 'sdb1' | awk '{print $5}'#<85%
存储空间#home空间#df -lP | grep -e 'centos-home' | awk '{print $5}'#<85%