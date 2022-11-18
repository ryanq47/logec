echo "Intentionally put in a bad password to create a failed authentication log:"

sudo su


echo "connecting to webserver to generate logs..."

sudo systemctl start apache2

for i in 1 2 3 4 5
do
    curl -X GET http://127.0.0.1 > /dev/null

done


echo "Running some commands as sudo to generate auth logs..."
for i in 1 2 3 4 5
do
    sudo echo "Hello There" $i

done


echo "Done! Go check logec and see what is has found"