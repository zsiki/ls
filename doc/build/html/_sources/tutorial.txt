========================================
SurveyingCalculation plugin for QGIS 2.x
========================================
Tutorial
--------

In this tutorial the functionality of the plugin is demonstrated through 
sample datasets, which can be found in the sample directory after the 
installation of the plugin. To use this tutorial you have to have QGIS 2.x
installed on your machine. Linux or Windows operating system can be used.

Enable SurveyingCalculation plugin in QGIS
::::::::::::::::::::::::::::::::::::::::::

Before using the installed SurveyingCalculation plugin, it has to be enabled in 
QGIS. The installation process of the plugin can be found in the User\'s Guide.


.. figure:: images/t001.png
   :scale: 80 %
   :align: center

   *(1.) From the Plugins menu select Manage and Install Plugins...*


.. figure:: images/t002.png
   :scale: 80 %
   :align: center

   *(2.) Enabling SurveyingCalculation plugin*

After enabling the plugin a new pulldown menu (SurveyingCalculation) and a
toolbar are visible in the main window of QGIS.

Preparing the work
::::::::::::::::::

The SurveyingCalculation plugin is fully integrated into QGIS. We will use a
QGIS project to save our working environment. Some plug-in specific data sets 
have to be
added to the project before using the different calculations (e.g.
traversing, network adjustment).


.. figure:: images/t003.png
   :scale: 80 %
   :align: center

   *(3.) From the SurveyingCalculation menu select New coordinate list ...*

Let\'s create a new empty 2D point shape file to store benchmarks (points with
known coordinates). Select the sample subdirectory of the plug-in, use the *test1* name for the file.  The plugin adds *coord_* to the beginning of the
name to distinguish it from the other elements of the project.
Besides the point identifier, the coordinates (easting, 
northing, elevation), a point code and a point type can be stored in the 
attribute table of the shape file.


.. figure:: images/t005.png
   :scale: 80 %
   :align: center

   *(4.) The attribute table of the coordinate file is empty*

To demonstrate the calculations we have to load some benchmarks and observations.
During the next step an electric fieldbook will be imported. Electric fieldbooks 
from total stations can contain observations (direction, distance) and
coordinates, too.

For the easier readability of the fieldbooks the representation of NULL values should
be changed before importing.


.. figure:: images/t008.png
   :scale: 80 %
   :align: center

   *(5.) From the Settings menu select Options...*


.. figure:: images/t009.png
   :scale: 80 %
   :align: center

   *(6.) Select Data Sources, and set the Representation for NULL values from "NULL" to empty string*


.. figure:: images/t006.png
   :scale: 80 %
   :align: center

   *(7.) From the SurveyingCalculation menu select Import fieldbook ...*

In the file selection dialog navigate to sample directory of the installed 
plugin, select the *Geodimeter JOB/ARE* file type and the *test1.job* file.
You must give a name and a directory for the imported fieldbook in a second
output file selection dialog. Save the imported observations into the sample 
directory with the name test1. The plugin adds *fb_* to the beginning of the
name to distinguish it from the other elements of the project.

The records of the fieldbook should be ordered by *id* column to get the logical
order of observations. The *id* values are  incremented by ten to left space 
manually added rows.


.. figure:: images/t010.png
   :scale: 80 %
   :align: center

   *(8.) The attribute table of the fieldbook*

The coordinates for the sample project can be imported from the *test1.are* 
file, similar to the import of the job file. The points are added to the
coordinate list file.


.. figure:: images/t011.png
   :scale: 80 %
   :align: center

   *(9.) The attribute table of the coordinate file*


.. figure:: images/t0111.png
   :scale: 80 %
   :align: center

   *(10.) To view the points in the map window, right click on the coordinate file and select Zoom to Layer*

Points can be labeled with *point_id* column in the map window using the 
standard QGIS labeling tools.


.. figure:: images/t055.png
   :scale: 80 %
   :align: center

   *(11.) Points labeled by point id in the map window*

QGIS project can be saved by clicking on the save (floppy disk) icon.

Single Point Calculations
:::::::::::::::::::::::::

Now we are able to start the coordinate calculations from the observations.


.. figure:: images/t012.png
   :scale: 80 %
   :align: center

   *(12.) Click Single point calculations icon on SurveyingCalculation toolbar*


.. figure:: images/t013.png
   :scale: 80 %
   :align: center

   *(13.) First select the type of calculation*

Before starting the coordinate calculation the orientation angles have to be calculated for known stations.


.. figure:: images/t014.png
   :scale: 80 %
   :align: center

   *(14.) Selecting station 10001* 

Let\'s start with station 10001. Select the point from the *Station (1)* list.
In the *Station (1)* list the fieldbook name and the id in fieldbook are shown 
in brackets.


.. figure:: images/t015.png
   :scale: 80 %
   :align: center

   *(15.) Selecting target points for orientation*
   
Select both target points and add them to used points (the id in fieldbook is shown in brackets).


.. figure:: images/t016.png
   :scale: 80 %
   :align: center

   *(16.) Starting the calculation*

Click on the *Calculate* button and the orientation angle will be calculated.
Results can be seen in the *Result of calculations* widget. 
The results are also written to the log file. The name and location of the 
log file can be set in *config.py*.
The orientation angle is stored in the fieldbook too, in the *hz* column of the 
station record.


.. figure:: images/t018.png
   :scale: 80 %
   :align: center

   *(17.) Orientation for station 10002*

Repeat the orientation calculation for all known stations (231, 10006).

There are observations to point 5002 and 5004 from station 10001 and 10002.
So coordinates can be calculated as an intersection for them.


.. figure:: images/t019.png
   :scale: 80 %
   :align: center

   *(18.) Starting intersection*

For the intersection two oriented stations must be selected in *Station (1)* and
*Station (2)* lists.
The fieldbook name and the id in fieldbook is shown in brackets in the station 
list.


.. figure:: images/t020.png
   :scale: 80 %
   :align: center

   *(19.) Intersection of points 5002 and 5004*

Select both target points and add them to used points. In all lists
points in bold face have coordinates. Click calculate 
and coordinates will be calculated. Results of the calculation can be 
seen in the result widget. Calculated coordinates are added to the coordinate 
list, too.

In the next step coordinates of point 5001 and 5003 will be calculated using
resection.


.. figure:: images/t021.png
   :scale: 80 %
   :align: center

   *(20.) Preparing resection*

Using the resection select the station 5001 (the fieldbook name and the id in 
fieldbook are shown in brackets, known points are displayed in bold face).


.. figure:: images/t022.png
   :scale: 80 %
   :align: center

   *(21.) Resection of station 5001*

Select exactly three target points (the id in fieldbook is shown in brackets) 
and add them to the *Used Points* list, click on the *Calculate* button and 
coordinates will be calculated. Details of the calculation can be seen in the 
result widget.
Calculated coordinates are added to the coordinate list, too.

Please repeat the resection calculation for station 5003.

There are distance measurements from station 5001 to other known points (10001 and 10003). 
Free station calculation can be used to consider all observations (directions
and distances) from a station. Let\'s recalculate the coordinates of station 5001
using free station calculation.


.. figure:: images/t023.png
   :scale: 80 %
   :align: center

   *(22.) Preparing free station calculation*
   
For the free station calculation select station 5001 (the fieldbook name and the
id in fieldbook is shown in brackets, known points are displayed in bold face)
in the *Station (1)* list.


.. figure:: images/t024.png
   :scale: 80 %
   :align: center

   *(23.) Free station calculation for station 5001*

Select target points (the id in fieldbook is shown in brackets) and add them to the *Used Points* list, click on *Calculate* button and coordinates will be calculated. Details of the calculation can be seen in the result widget.
Free station calculation uses the least squares method. The calculation result
list contains all details about calculation, provided by GNU-Gama project.
Repeat the free station calculation using all possible observations.

Let\'s calculate the coordinates of some detail points.


.. figure:: images/t026.png
   :scale: 80 %
   :align: center

   *(24.) Preparing Radial Survey calculation*
   
Using the radial survey the position of several polar points can be calculated.
First select station point (the fieldbook name and the id in fieldbook is shown in brackets), only oriented known points can be selected.


.. figure:: images/t027.png
   :scale: 80 %
   :align: center

   *(25.) Radial Survey calculation*

Select target points 101-104 (the id in fieldbook is shown in brackets) and 
add them to the *Used Points* list, click on *Calculate* button and coordinates will be calculated. 
Results of the calculation can be seen in the result widget.

Traverse calculations
:::::::::::::::::::::

A link traverse will be calculated between points 5001 and 5002 in this section.
The orientations on the start and end point were 
calculated before. Let\'s repeat the orientation for points 5001 and 5002.


.. figure:: images/t029.png
   :scale: 80 %
   :align: center

   *(26.) Orientation on start point (5001)*

Be careful, point 5001 was occupied twice, the first was used for 
resection, the second is for traversing. Calculate orientation for line 370.


.. figure:: images/t030.png
   :scale: 80 %
   :align: center

   *(27.) Orientation on end point (5002)*


.. figure:: images/t031.png
   :scale: 80 %
   :align: center

   *(28.) Starting traverse calculation*

Click on the *Traverse calculations* icon in the SurveyingCalculation toolbar.


.. figure:: images/t032.png
   :scale: 80 %
   :align: center

   *(29.) Start point of traverse*

Select *Link Traverse* and the start point (the fieldbook name and 
the id in fieldbook is shown in brackets, only oriented known points can be 
selected).


.. figure:: images/t033.png
   :scale: 80 %
   :align: center

   *(30.) End point of traverse*

Select the end point (the fieldbook name and the id in fieldbook is shown in brackets, only known oriented points can be selected)


.. figure:: images/t034.png
   :scale: 80 %
   :align: center

   *(31.) Points in traverse*
   
Select the traverse points from target points and add them to the used points.
Change the order of points if necessary using the up and down button, the correct order is 1_tr, 2_tr, 3_tr. The 
fieldbook name and the id in fieldbook is shown in brackets, known points are 
displayed in bold face.


.. figure:: images/t035.png
   :scale: 80 %
   :align: center

   *(32.) Traverse calculation* 

Click on the *Calculate* button and the coordinates will be calculated. Results of the 
calculation can be seen in the result widget. The coordinates of traverse points
are updated in coordinate list, too.

Network adjustment
::::::::::::::::::

We have more observations than necessary for the coordinate calculation of 
points 5001-5004. If we would like to consider all observations, we have to use network 
adjustment (least squares estimation). Free station calculation also uses the 
least squares method, but the external directions are not considered in that case.


.. figure:: images/t051.png
   :scale: 80 %
   :align: center

   *(33.) Starting network adjustment*
   
Click on the *Network adjustment* icon on the SurveyingCalculation toolbar.


.. figure:: images/t052.png
   :scale: 80 %
   :align: center

   *(34.) Selecting the fix points*

Select fix points from the *List of Points* (the coordinates of these points
will not be changed during adjustment) and add them to the *Fix points* list. Only points in bold 
face can be added to the fix points list (those have coordinates in the coordinate list).


.. figure:: images/t053.png
   :scale: 80 %
   :align: center

   *(35.) Selecting points to adjust*

Select points to adjust from the *List of Points* and add them to the
*Adjusted Points* list.


.. figure:: images/t054.png
   :scale: 80 %
   :align: center

   *(36.) Adjustment parameters*
   
Set the parameters of the adjustment, horizontal network (2D), the standard 
deviation of observations. Click on the *Calculate* button and coordinates will be calculated. 
Results of the calculation can be seen in the result widget. In this long list,
generated by GNU Gama, several details of the adjustment calculation can be 
studied. For more details see the `GNU Gama <https://www.gnu.org/software/gama/>`_ documentation.

Coordinate transformation
:::::::::::::::::::::::::

Let\'s transform the points in *test1* data set to another coordinate system using common points, which are known in both coordinate systems.
A second coordinate list was prepared with the coordinates in the target system.


.. figure:: images/t64.png
   :scale: 80 %
   :align: center

   *(37.) Starting coordinate transformation*
   
Click on the *Coordinate transformation* icon in SurveyingCalculation toolbar to start 
the calculation.


.. figure:: images/t65.png
   :scale: 80 %
   :align: center

   *(38.) Selecting from coordinate list*
   
The *coord_test1* shape file is automatically selected to transform from, it is the only one loaded coordinate list.
Press the button with ellipses (...) to select the target shape file of the
transformation.


.. figure:: images/t66.png
   :scale: 80 %
   :align: center

   *(39.) Selecting points*
   
After specifying the source and the target of the transformation the *Common Points*
list is filled automatically. Add all points from the *Common Points* list to the *Used Points* list.


.. figure:: images/t67.png
   :scale: 80 %
   :align: center

   *(40.) Selecting the type of transformation*
   
Different transformation types require different numbers of point. Only those transformation types are available for which enough points were selected.


.. figure:: images/t68.png
   :scale: 80 %
   :align: center

   *(41.) Calculating transformation*
   
Click on the *Calculate* button and the transformation parameters and transformed 
coordinates will be calculated. Results of the calculation can be seen in the result widget.

Polygon division
::::::::::::::::

For demonstrating division of polygons, we need a vector layer containing polygons. Click on the *Add Vector Layer* button in the toolbar, 
in the file selection dialog navigate to the *sample* directory of the installed plugin and select the *parcels.shp* file.


.. figure:: images/t071.png
   :scale: 80 %
   :align: center

   *(42.) Selecting a polygon*

First a polygon has to be selected with *Select Features* QGIS tool.


.. figure:: images/t072.png
   :scale: 80 %
   :align: center

   *(43.) Starting Polygon division*

Click on *Polygon division* button, the mouse cursor is changed to a cross.
Draw a rubberband line crossing the selected parcel.


.. figure:: images/t073.png
   :scale: 80 %
   :align: center

   *(44.) Default parameters of division*

In the *Area Division* dialog the full area of selected polygon is displayed.
The area of wanted part-polygon can be given, which is on the right side of the given line. The default value for the area is calculated from the actual division line.
The method of division also has to be chosen. The polygon can be divided parallel to the given line, 
or by the rotation of the given line around first given point.


.. figure:: images/t074.png
   :scale: 80 %
   :align: center

   *(45.) Set the parameters of division*

We have set the area of wanted part-polygon to *5000* units and the method of division to *parallel division*.


.. figure:: images/t075.png
   :scale: 80 %
   :align: center

   *(46.) Measured area of the smaller new polygon.*

Click on the *Divide* button and division will be executed. The two new polygons are now visible in the attribute table, where attributes of new polygons can be given (e.g. *parcel_id*).

Plot by template
::::::::::::::::

Let\'s plot the actual view of the map window first.


.. figure:: images/t076.png
   :scale: 80 %
   :align: center

   *(47.) Starting Plot by template.*

Polygons can be labeled with *parcel_id* column in the map window using the 
standard QGIS labeling tools. We have given new *parcel_id* (101, 102) to the two new polygons.


.. figure:: images/t077.png
   :scale: 80 %
   :align: center

   *(48.) Set plot parameters*

In the plot window select a template file, set the scale of the plot and give it a name.


.. figure:: images/t078.png
   :scale: 80 %
   :align: center

   *(49.) Composer window of the map composition*

Click on the *Plot* button and a composer window will appear with the map composition.
The composition can be printed to a printer or exported to a PDF file.

Batch plotting
::::::::::::::

Selected polygons can be plotted by using *Batch plotting*.


.. figure:: images/t079.png
   :scale: 80 %
   :align: center

   *(50.) Add another layer to the map*

Any number of layers can be added to the map.


.. figure:: images/t080.png
   :scale: 80 %
   :align: center

   *(51.) Select the parcels and start Batch plotting*

Select one or more parcels to be plotted and click on the *Batch plotting* button.


.. figure:: images/t081.png
   :scale: 80 %
   :align: center

   *(52.) Set plot parameters*

In the plot window select a template file and set the scale of the plot. 
The compositions of the parcels with the given scale can be exported to *.pdf* files or 
printed or opened in a composer window.
Select *Single PDF file (multi-page) on the *To PDF* tab.

By clicking on the *Plot* button a file selection dialog appears and compositions will be exported to 
a multi-page *.pdf* file using the selected composer template.
