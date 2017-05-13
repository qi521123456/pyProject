# splitting strings
string1 = "A, B, C, D, E, F"
print ("String is:", string1)
print ("Split string by spaces:", string1.split(" "))
print ("Split string by commas:", string1.split( "," ))
print ("Split string by commas, max 2:", string1.split( ",", 2 ))
print ("Split string by commas, max 3:", string1.split( ",", 3 ))
print("\n")
# joining strings
list1 =  [ "A", "B", "C", "D", "E", "F" ]
string2 = "___"
print ("List is:", list1)
print(( 'Joining with "%s": %s' )% ( string2, string2.join ( list1 ) ))
print ('Joining with "-.-":', "-.-".join( list1 ))