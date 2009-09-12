closestpair.so: closestpair.c
	gcc -shared -fPIC -O3 -I/usr/include/python2.6/ closestpair.c -o closestpair.so
closestpair.c: closestpair.pyx
	pyrexc closestpair.pyx
