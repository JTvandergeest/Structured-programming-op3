# Structured-programming-op3
Repo for SP 3/3
huw_recommend_productid.py is de webshop.
main.py, is het algoritme.
products_sessions_datascript.py, laad de data vanuit mongoDB in postgres in.

De recommendations zijn niet gebaseerd op het profileid maar op een productid.
De recommendations zijn soortgelijke producten gebaseerd op wat anderen kochten en op producten met dezelfde sub_sub_categorie. 
Dit is omdat niet alle producten al eerder in gekocht zijn en de op basis van de sub_sub_categorie omdat ik de categorie niet specifiek genoeg vond.
Bij een tandenborstel zou dan condooms aangeraden worden als soortgelijk omdat het dezelfde categorie was. 
De recommendations zijn uniek en zullen dus niet dubbel weergegeven worden.

M.b.t. wat anderen kochten heb ik gezorgd dat de producten die het meest gekocht werden door anderen die ook het product waarnaar gekeken word hebben bekeken eerst getoont word.
Dus als anderen een tandenborstel in de winkelmand hadden dan zou tandenpasta vaker in de winkelmand voorkomen dan een borstel, alhoewel een borstel ook is voorgekomen.

http://localhost:5400/product/update runt het algoritme
