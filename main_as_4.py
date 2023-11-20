# Import following
from pathlib import Path
import ifcopenshell
import selectors

# Call in your Ifc-File with the name
modelname = "LLYN - ARK"

# A check is made. 
# If the code do not make an error when running this everything is fine.
try:
    dir_path = Path(__file__).parent
    model_url = Path.joinpath(dir_path, 'model', modelname).with_suffix('.ifc')
    model = ifcopenshell.open(model_url)
except OSError:
    try:
        import bpy
        model_url = Path.joinpath(Path(bpy.context.space_data.text.filepath).parent, 'model', modelname).with_suffix('.ifc')
        model = ifcopenshell.open(model_url)
    except OSError:
        print(f"ERROR: please check your model folder : {model_url} does not exist")

# Lets see what type of IFC-file you have
print(f"The type of IFC model is as following: {model.schema}")

# Check the number of windows in the IFC-model.
# The name 'windows' will refer to all windows in the model.
windows = model.by_type('IfcWindow')
# Now a output of the number of windows will be displayed when the code are running.
print(f"the numbers of windows are: {len(windows)}")

# Now checking what kind of properties the windows have.
# Since the code displaced 81 for the amount of windows this window will be looked into. 
window = model.by_type('IfcWindow')[50]

# Now looking if the window is related to spaces
print(f"Does the window no. 50 have a IfcElement inside?: {window.is_a('IfcElement')}") #Return true if related.
# Now looking for the Global Id for window no. 50
print(f"The Global Id for the window no. 50 is: {window.GlobalId}")

# Now the area of the window needs to be found. Here the height and width is found
h = window.OverallHeight
b = window.OverallWidth
# The area of the window is found. no. 2 means that you will see the area with 2 digits.
A = round(h * b, 2)
# When running the code a output of the window area of window no. 50 is shown.
print(f"The total window area for no. 50 is: {A}")

# Now the total area of all windows would like to be found
# Therefore following libraries needs to be imported
import ifcopenshell.util
import ifcopenshell.util.element

# Below line will print a lot of properties and quentites about window no. 50
print(f"The quentitites and properties as a dictionary for Window no. 50 is as following:{ifcopenshell.util.element.get_psets(window)}")

# Making a start value for the total sum of windows
total_sum_window = 0

# Using the hasttr command to see if the window does have a OverallHeight & OverallWidth, if so, it collect them
# and use them to find the area and at the end add them all together.
for window1 in windows:
    if hasattr(window1, 'OverallHeight') and hasattr(window1, 'OverallWidth'):
        product = window1.OverallHeight * window1.OverallWidth
        total_sum_window += (product * 10**(-6)) # Going from mm^2 to m^2
# The total window area will be shown when running the code
print(f"The total window area is: {round(total_sum_window,2)}") # Area will be shown with 2 digits.

# It is also seen that the windows have information about being an external or internal window (from line 55)
# From line 55 the output says 'IsExternal' : False or True, which leads to the position of the window. 
# The 10% rule is only applicable for external windows which therefore needs to be found now.

# Making an empty list to safe the windows that are external.
external_windows = []
# Going though all the windows to see if they are 'IsExternal'
for window in windows:
    psets2 = ifcopenshell.util.element.get_psets(window)
    # From line 55 is it seen that 'IsExternal is inside a dictionary in this case called 'Pset_WindowCommon'
    # Below line looks for 'Pset_WindowCommon' and then afterwards 'IsExternal'
    if 'Pset_WindowCommon' in psets2 and 'IsExternal' in psets2['Pset_WindowCommon']: 
        is_external = psets2['Pset_WindowCommon']['IsExternal']
        # From above line is it assumed a 'boolsk value' which means you only have True or False values.
        if is_external:
            # If 'IsExternal' is true will they be added to the new list below
            external_windows.append(window) # Now the 'external_windows' only have the rooms with 'IsExternal': True

# To validate the IFC information following comparison will happen:
# The output of the number of external windows and total windows will be shown. Here the person needs to be critical if these two numbers
# are correct due to the IFC model. If this is incorrect will there be errors in the IFC-file that needs to be fixed.
# This error can be found if e.g., all windows are external but is known that there are some IFC windows inside the building.
print(f"Numbers of external windows: {len(external_windows)}")
print(f"Numbers of windows in total: {len(windows)}")

# Assuming that the numbers of external windows are correct this window area needs to be found. 

# The area of the external windows would like to be found, just with the priciple as before. 
total_external_window_area = 0

# Every window that are external is now going though to find the area.  
for window in external_windows:  
    if hasattr(window, 'OverallHeight') and hasattr(window, 'OverallWidth'):
        product = (window.OverallHeight * window.OverallWidth) * 10**(-6)# From mm^2 to m^2
        total_external_window_area += round(product, 2) # Only having 2 digits.

# The total area of external windows are
print(f"The total area of external windows are: {round(total_external_window_area,2)}")

# The area below is found manually, which can be done by measuring inside the IFC model by e.g., BlenderBIM. 
# However, the information below is not needed.
Curtain_Wall_area = 389.66 #m2
Facade_area = 2193.88 # m2
Window_area = total_sum_window #m2
print(f"the total area of the facade is: {round(Curtain_Wall_area + Facade_area - Window_area,2)}")

# Having the window area, then the space area needs to be found to see if the BR18 reqiurement about windowarea is complied.
import ifcopenshell.util.element
# First, one space is investigated, in this case no. 2. 
space = model.by_type("IfcSpace")[2]
# Now all quantities and properties as a dictionary is found for space no. 2.
psets = ifcopenshell.util.element.get_psets(space)
# When running the code the quentatites and properties for the space will be shown.
print(f"The quentitites and properties as a dictionary for space no. 2 is as following:{psets}")

# From above is it seen that the space has a dictonary called 'Qto_SpaceBaseQuantities' and inside it information about
# the floor area is seen (GrossFloorArea). This area is needed.

# The floor area will now be found by following code which is the same loop as the one with windows.
import ifcopenshell.util.element
# Looking for all the spaces
spaces = model.by_type("IfcSpace")
# Making a list equal to 0 to have all variables for the total GrossFloorArea
total_gross_floor_area = 0.0

# Loop to go through all the spaces in the model
for space in spaces:
    # psets for every room
    psets = ifcopenshell.util.element.get_psets(space)
    # As mentioned before is the GrossFloorArea inside the dictionary called Qto_SpaceBaseQuantites
    # First checking if the space have the Qto_SpaceBaseQuantites.
    if "Qto_SpaceBaseQuantities" in psets:
        try:
            # Getting the GrossFloorArea for the certain spcae.
            gross_floor_area = float(psets["Qto_SpaceBaseQuantities"]["GrossFloorArea"])
            
            # Adding the all GrossFloorArea to the total area.
            total_gross_floor_area += gross_floor_area
        except KeyError:
            # Now checking if some of the spaces do no have any dimensions which will be shown when running the code.
            print(f"Error: GrossFloorArea is not found for room {space.id()}")

# Now the total GrossFloorArea is found with two decimals.
print("The total GrossFloorArea for the rooms are:", round(total_gross_floor_area,2))
# It must be noted that this total area have an error. Since some of the spaces do not have any GrossFloorArea and the 
# 10% rule is only for a space that is connected to a certain external window.
# Therefore is this tutorial for a start up for the calculation.

# It will now be checked if the BR18 requirement is statified for the foundend floor area and with the external window area.
if total_sum_window >= 0.1*total_gross_floor_area:
    print("The BR18 requirment about 10% window area for the corresponding floor area is complied")
else: 
    print("The BR18 requirement about 10% window area for the correspnding is not observed")

# Since it has been discovered that some IFC models have some errors is it important to make some checks for the calculation.
# For this check is it investigated if the spaces are internal, which leads to 'IsExternal' needs to be False.

# The list that will save the spaces that retrun false for the external.
no_external_spaces = []

# Now all spaces are looked at for the 'IsExternal' which is inside the dictionary called 'Pset_SpaceCommon'
for space in spaces:
    psets = ifcopenshell.util.element.get_psets(space)
    if 'Pset_SpaceCommon' in psets and 'IsExternal' in psets['Pset_SpaceCommon']:
        is_external = psets['Pset_SpaceCommon']['IsExternal']
        if not is_external:
            #If 'IsExternal' is false, is it added below
            no_external_spaces.append(space)

#Now looking at the results
print(f"The numbers of spaces that are not external is: {len(no_external_spaces)}")
print(f"the numbers of spaces are: {len(spaces)}")
# It is seen that no spaces are external, however, this might not be true.
# When looking into the 3D model is it seen that it is not true. 
# Here is it observed that some of the facade elements is a IfcSpace and should therefore be external. 

# In some models there will be certain walls which also needs to be count as a window. 
# For this model the curtain walls are named 'IfcPlate'.
# Therefore the number of IfcPlate are counted below. 

CurtainWalls = model.by_type('IfcPlate')
print(f"the numbers of Curtain walls are: {len(CurtainWalls)}")
import ifcopenshell.util.element

# Since the area of the curtain wall is needed the same procedure about checking the information for one element is done below.
CurtainWall = model.by_type("IfcPlate")[2]
psets3 = ifcopenshell.util.element.get_psets(CurtainWall)
print(f"The quentitites and properties as a dictionary for plate no. 2 is as following::{psets3}")
print(CurtainWall.get_info)
# Since above output do not give any information about the dimensions of the curtain panel they are not used in the calculation.
print("No dimensions on the Plate eventough it gives postion of external")

# Now the second part of the code will be introduced.

# Now we would like to update the missing information for our calculation.
# Remeber that following still needs to be imported.
import ifcopenshell
import ifcopenshell.api
import ifcopenshell.util.element

# Another way to open your IFC-file is like following 
model = ifcopenshell.open(r"C:\Users\Clara\Desktop\Main Folder\ifcopenshell-python-311-v0.7.0-dadcbe6-win64 (1)\model\LLYN - ARK.ifc")

# It was seen that some of the spaces did not have any information about their floor area, so now we would like to add this information.
# We make a check about the IfcSpace information to see if the following will change
space = model.by_type("IfcSpace")[1]
# Seeing the orginal information
print(ifcopenshell.util.element.get_psets(space))
# Now taken all the spaces
spaces = model.by_type("IfcSpace")
# Making a for loop since we would like to go though all the spaces in the IFC-file.
for space in spaces:

    psets = ifcopenshell.util.element.get_psets(space)

    # It is seen that the floor area (GrossFloorArea) are inside the dictionary called "Qto_SpaceBaseQuantites" 
    # since this is a standard buildingSMART property set we just add "Qto_SpaceBaseQuantites" to the space. 
    # The 'model' is what we called the IFC-file.
    qto = ifcopenshell.api.run("pset.add_qto",model, product=space, name ="Qto_SpaceBaseQuantities")
    
    # Since this is a part of built-in buildingSMART templates results that making the "GrossFloorArea" 
    # will automatically be in "Qto_SpaceBaseQuantites"
    # For a refrence we insert the GrossFloorArea to 120. 
    # Now IfcSpace will have the value of 120 but it will be easier just to change it e.g., inside
    # the IFC-File when the quantity will be there. 
    ifcopenshell.api.run("pset.edit_qto", model, qto=qto, properties={"GrossFloorArea": 120})

    psets = ifcopenshell.util.element.get_psets(space)
# Since IfcSpace [1] already had the value of GrossFloorArea it will be change back to the orginal value
# This can easily be done like following.
space1 = model.by_type("IfcSpace")[1]
qto1 = ifcopenshell.api.run("pset.add_qto",model, product=space1, name ="Qto_SpaceBaseQuantities")
    
ifcopenshell.api.run("pset.edit_qto", model, qto=qto1, properties={"GrossFloorArea": 4.396})
# When running the code below line will show that it changed again.
print(f"Space [1] is changed into correct value again:{ifcopenshell.util.element.get_psets(space1)}")

# Windows
# It was also observed eailer that some of the windows are registered as an internal window eventhough it is an external window.
# On of the windows that have this error is following window the ID of "1I5_7E6Iz4rhZEaQfJMyE"
element = model.by_id("1I5_7E6Iz4rhZEaQfJMyEm")

# Making a check to see if the window is IsExternal: False
print(ifcopenshell.util.element.get_psets(element))
# The check was as expected. 

# The information of internal or external is inside the dictionary of "Pset_WindowCommon"
# Now collecting the pset_WindowCommon PropertySet for the element.
win_common = ifcopenshell.util.element.get_pset(element, "Pset_WindowCommon", should_inherit=False)

# Now chaning the IsExternal from False to True by taken the previously fetched property set
# and finding the object by using the ID.
ifcopenshell.api.run("pset.edit_pset", model,
    pset=model.by_id(win_common["id"]), properties={"IsExternal": "True"})
print(win_common)

# Now checking if the window is True for IsExternal
print(ifcopenshell.util.element.get_psets(element))

# Now we would like to update the ifc-file with the new values.
model.write(r"C:\Users\Clara\Desktop\Main Folder\ifcopenshell-python-311-v0.7.0-dadcbe6-win64 (1)\model\LLYNARK2.ifc")
