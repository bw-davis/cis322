git clone https://github.com/postgres/postgres.git
cd postgres
git checkout REL9_5_STABLE
./configure --prefix=$1
make
make install
cd ~
curl http://www-eu.apache.org/dist//httpd/httpd-2.4.25.tar.bz2 > httpd-2.4.25.tar.bz2
tar xvfj httpd-2.4.25.tar.bz2 
cd httpd-2.4.25.25
./configure --prefix=$1
make
make install
