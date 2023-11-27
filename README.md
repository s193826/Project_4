# Project_4

##Target

The ones that are going to use this script are people who might be new to this library and working with IFC files. However, it is expected that they are used to working in Python since is anticipated that people can work further with the script and just need an introduction and some examples.
It is assessed that users need to understand BIM, so for the OpenBIM Modeller part, you need to be at Level 2 since there more likely must be some checks inside the BIM model.
For the OpenBM Analyst is it important that the person have a further understanding of Level 1 since it might not be enough to be able to make an analysis of the IFC file inside Excel. This tutorial will help people to be confident in Level 2.
For the OpenBIM Modeller Level 2 is not required but with this tutorial, you might be able to understand it afterwards.
For OpenBIM Ontologist is it assumed that Level 1 is known since this will not be go through for this tutorial. The OpenBIM Guru is only assessed to be at Level 1.
Overall is it assumed that the user understands what BIM is and how you can read and analyse the information inside Excel. It is not required that the user know how to work with the data inside Python (IfcOpenshell) which is going to be learned with the tutorial. However, it is expected that the person knows how to work inside Python to have a general understanding of the Python script. This is a tutorial meant to be for people who would like to be confident at Level 2.
It must be emphasized that people on Level 1 might still understand this tutorial however, there might be some learning gaps that can be looked into afterwards.


##Validation of Python script

The Python that is developed for this case should work. The last part (working with the windows) is overall correct but in this case, it does not work correctly. The aim of the script was to correct the error for a certain window. As described earlier some external windows are registered as internal which the script should change. Instead of only changing the window that is mentioned in the script (with GlobalId) the script changes all windows to external windows. This error is not acceptable since there can be some internal windows and these windows must not come into the 10% calculation. 

The reason why this is not working is that the property “IsExternal” has the Id 420 which the IFC file has collected to one property for all windows. So, when changing Id 420 for one GlobaldId it changes all Id 420 for the whole model.

Aiming for only changing “IsExternal” for a certain window with GlobalId can still be done with an updated version of ‘ifcopenshell.api.pset.edit_pset’ but Ifcopenshill Pip is only updated once a month. However, this can still be changed if the following two files can be found on a certain computer:
fcOpenShell/src/ifcopenshell-python/ifcopenshell/api/pset/edit_pset.py src/ifcopenshell-python/test/api/pset/test_edit_pset.py 
These two files then need to be replaced with the following two links:
https://github.com/IfcOpenShell/IfcOpenShell/blob/20b7ee009de1ddcb8d5e44402e4cd886ace36e44/src/ifcopenshell-python/ifcopenshell/api/pset/edit_pset.py, https://github.com/IfcOpenShell/IfcOpenShell/blob/20b7ee009de1ddcb8d5e44402e4cd886ace36e44/src/ifcopenshell-python/test/api/pset/test_edit_pset.py

Since the user cannot be expected to have the updated version, the code may still fail and due to time, this is not done. The attached Python code should therefore work for only a certain window with the updated version. 
