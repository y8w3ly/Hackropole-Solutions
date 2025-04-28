# **Description**
Lors de l’investigation d’un poste GNU/Linux, vous analysez un fichier qui semble être généré par un programme d’enregistrement de frappes de clavier (enregistrement de l’activité de chaque touche utilisée). Retrouvez ce qui a bien pu être écrit par l’utilisateur de ce poste à l’aide de ce fichier !
Note : Insérer le contenu tapé au clavier de ce poste entre FCSC{...} pour obtenir le flag.

# **Solution**

+ It looks like a keylogger challenge.
+ After observation we can deduce that there are two tipes of events 
	- Type 1
	- Type 4
+ All this is my own reasoning I'm not sure about it:
	- The events with Type 4 are MCS_SCAN I think it scans the keyboard and returns the code value that the key holds.
	- Type 1 Events has two possible values 0 or 1.
	- I think 0 when the user stops holding the key and 1 when he holds it.
	- In that line we kan see KEY_*
	- If we cunstruct all keys in all lines that have value 1 we get the string that can be wrapped with the flag format.

+ After some skilling with the code editor we get : `UNEGENTILLEINTRODUCTION`


