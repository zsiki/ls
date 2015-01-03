========================================
SurveyingCalculation plugin for QGIS 2.x
========================================
Tutorial
--------

In this tutorial the functionality of the plugin is demonstrated through 
sample datasets, which can be found in the sample directory after the 
installation of the plugin. To use this tutorial you must have QGIS 2.x
installed on your machine. Linux or Windows operating system can be used.

Enable SurveyingCalculation plugin in QGIS
::::::::::::::::::::::::::::::::::::::::::

Befor using the installed SurveyingCalculation plugin, it has to be enabled in 
QGIS. The installation process of the plugin can be found in the User's Guide.

.. figure:: images/t001.png
   :scale: 80 %
   :align: center

   *(1.) From the Plugins menu select Manage and Install Plugins...*

.. figure:: images/t002.png
   :scale: 80 %
   :align: center

   *(2.) Search for SurveyingCalculation plugin and enable it*

After enabling the plugin a new pulldown menu (SurveyingCalculation) and a
toolbar are visible in the main window of QGIS.

Preparing the work
::::::::::::::::::

The SurveyingCalculation plugin is fully integrated into QGIS. We will use 
QGIS project to save our working environment. Some special data sets must be
added to the project to be able to use the different calculations (e.g.
traversing, network adjustment).

.. figure:: images/t003.png
   :scale: 80 %
   :align: center

   *(3.) From the SurveyingCalculation menu select New coordinate list ...*

A new empty 2D point shape file is created to store benchmarks (points with
known coordinates). The plugin adds *coord_* to the beginning of the
name to distinguish it from the other elements of the project.
Besides the point identifier, the coordinates (easting, 
northing, elevation), a point code and a point type can be stored in the 
attribute table of the shape file.

.. figure:: images/t005.png
   :scale: 80 %
   :align: center

   *(4.) The attribute table of the coordinate file is empty*

To demonstrate the calculations we need some benchmarks and observations.
During the next step an electric fieldbook is imported. Electric fieldbooks 
from total stations can contain observations (direction, distance) and
coordinates too.

For the transparency of the fieldbooks the representation of NULL values should
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
standard QGIS labelling tools.

.. figure:: images/t055.png
   :scale: 80 %
   :align: center

   *(14.) Points labelled with point id in the map window*

QGIS project can be saved by clicking on the save (floppy disk) icon.

Single Point Calculations
:::::::::::::::::::::::::

Now we are able to start the coordinate calculations from the observations.


.. figure:: images/t012.png
   :scale: 80 %
   :align: center

   *(15.) Click Single point calculations icon on SurveyingCalculation toolbar*

.. figure:: images/t013.png
   :scale: 80 %
   :align: center

   *(16.) First select the type of calculation*

Before starting the coordinate calculation the orientation angles must be set 
for known station.

.. figure:: images/t014.png
   :scale: 80 %
   :align: center

   *(17.) Selecting station 10001* 

Let\'s start with station 10001. Select the point from the *Station (1)* list.
In the *Station (1)* list the fieldbook name and the id in fieldbook are shown 
in brackets.

.. figure:: images/t015.png
   :scale: 80 %
   :align: center

   *(18.) Selecting target points for orientation*
   
Select one or more target points and add them to used points (the id in fieldbook is shown in bracket).

.. figure:: images/t016.png
   :scale: 80 %
   :align: center

   *(19.) Staring calculation*

Click Calculate button and the orientation angle will be calculated.
Results can be seen in the *Result of calculations* widget. 
The results are also written to the log file. The name and location of the 
log file can be set in *config.py*.
The orientation angle is stored in the fieldbook too, in the *hz* column of the 
station record.

.. figure:: images/t018.png
   :scale: 80 %
   :align: center

   *(21.) Orientation for station 10002*

Repeat the orientation calculation for all known stations (231, 10006).

There are observations to point 5002 and 5004 from station 10001 and 10002.
So coordinates can be calculated as an intersection for them.

.. figure:: images/t019.png
   :scale: 80 %
   :align: center

   *(22.) Starting intersection*

For the intersection two oriented stations must be selected in *Station (1)* and
*Station (2)* list.
The fieldbook name and the id in fieldbook is shown in brackets in the station 
list.

.. figure:: images/t020.png
   :scale: 80 %
   :align: center

   *(23.) Intersection of point 5004*

Select one or more target points and add them to used point, click calculate 
and coordinates will be calculated. Results of the calculation can be 
seen in the result widget. Calculated coordinates are added to the coordinate 
list too.

In the next step coordinates of point 5001 and 5003 will be calculated using
resection.

.. figure:: images/t021.png
   :scale: 80 %
   :align: center

   *(24.) Preparing resection*

By the resection select the station 5001 (the fieldbook name and the id in 
fieldbook is shown in brackets, known points are displayed in bold face).

.. figure:: images/t022.png
   :scale: 80 %
   :align: center

   *(25.) Resection of station 5001*

Select exactly three target points (the id in fieldbook is shown in brackets) 
and add them to the *Used Points* list, click on *Calculate* button and 
coordinates will be calculated. Details of the calculation can be seen in the 
result widget.
Calculated coordinates are added to the coordinate list too.

Please repeat the resection calculation for station 5003.

There are distance measurements from station 5001 to other known points (10001 and 10003). 
Free station calculation can be used to consider all observations (directions
and distances) from a station. Let's calculate the coordinates of station 5001
using free station calculation.

.. figure:: images/t023.png
   :scale: 80 %
   :align: center

   *(26.) Preparing free station calculation*
   
For the free station calculation select station 5001 (the fieldbook name and the
id in fieldbook is shown in brackets, known points are displayed in bold face)
in the *Station (1)* list.

.. figure:: images/t024.png
   :scale: 80 %
   :align: center

   *(27.) Free station calculation for station 5001*

Select two or more target points (the id in fieldbook is shown in brackets) and add to used points, click calculate and coordinates will be calculated. Details of the calculation can be seen in the result widget.
Free station calculation uses the least squares method. The calculation result
list contains all details about calculation, provided by GNU-Gama project.
Repeat the free station calculation using all possible observations!

.. figure:: images/t026.png
   :scale: 80 %
   :align: center

   *(28.) Preparing Radial Survey calculation*
   
By the radial survey the position of several polar points can be calculated.
First select station point (the fieldbook name and the id in fieldbook is shown in brackets), only oriented known points can be selected.

.. figure:: images/t027.png
   :scale: 80 %
   :align: center

   *(29.) Radial Survey calculation*

Select one or more target points (the id in fieldbook is shown in brackets) and 
add to used points, click calculate and coordinates will be calculated. 
Results of the calculation can be seen in the result widget.

**TODO**
*This example for point 5002 is not ideal. Why do not we add simple polar
points? There are observed detail points from 1_tr and 3_tr!*

Traverse calculations
:::::::::::::::::::::

A link traverse will be calculated between point 5001 and 5002 in this section.
If orientation is available on the start and/or end point, it should be 
calculated before starting the traversing calculation. 

.. figure:: images/t029.png
   :scale: 80 %
   :align: center

   *(30.) Orientation on start point (5001)*

Be careful, point 5001 was occupied twice, the first was used for 
resection, the second is for traversing. Calculate orientation for line 370.

.. figure:: images/t030.png
   :scale: 80 %
   :align: center

   *(31.) Orientation on end point (5002)*

.. figure:: images/t031.png
   :scale: 80 %
   :align: center

   *(32.) Starting traverse calculation*

Click Traverse calculations icon on SurveyingCalculation toolbar.

.. figure:: images/t032.png
   :scale: 80 %
   :align: center

   *(33.) Start point of traverse*

Select the *Link Traverse* and the start point (the fieldbook name and 
the id in fieldbook is shown in brackets, only oriented known points can be 
selected).

.. figure:: images/t033.png
   :scale: 80 %
   :align: center

   *(34.) End point of traverse*

Select the end point (the fieldbook name and the id in fieldbook is shown in brackets, only known oriented points can be selected except open traverse)

.. figure:: images/t034.png
   :scale: 80 %
   :align: center

   *(35.) Points in traverse*
   
Select the traverse point from target points and add them to the used points.
Change the order of points if necessary using the up and down button. The 
fieldbook name and the id in fieldbook is shown in brackets, known point are 
displayed in bold face.

.. figure:: images/t035.png
   :scale: 80 %
   :align: center

   *(36.) Traverse calculation* 

Click Calculate button and the coordinates will be calculated. Results of the 
calculation can be seen in the result window. The coordinates of traverse points
are updated in coordinate list too.

Network adjustment
::::::::::::::::::

We have more observations then necessary for the coordinate calculation of 
point 5001-5004. If we would like to consider all, we have to use network 
adjustment (least squares estimation). Free station calculation also uses the 
least squares method, but the external directions are not considered.

.. figure:: images/t051.png
   :scale: 80 %
   :align: center

   *(37.) Starting network adjustment*
   
Click Network adjustment icon on the SurveyingCalculation toolbar.

.. figure:: images/t052.png
   :scale: 80 %
   :align: center

   *(38.) Selecting the fix points*

Select fix points (the coordinates of these point will not be changed) from the
*List of Points* and add them to the *Fix points* list. Only points in bold 
face can be added to the fix points list (those have coordinates in the coordinate list).

.. figure:: images/t053.png
   :scale: 80 %
   :align: center

   *(39.) Selecting adjusted points*

Select points to adjust  from the *List of Points* and add them to the
*Adjusted Points* list.

.. figure:: images/t054.png
   :scale: 80 %
   :align: center

   *(40.) Adjustment parameters*
   
Set the parameters of the adjustment, horizontal network (2D), the standard 
deviation of observations. Click calculate and coordinates will be calculated. 
Results of the calculation can be seen in the result widget. In this long list,
generated by GNU Gama, several details of the adjustment calculation can be 
studied. For more details see the `GNU Gama <https://www.gnu.org/software/gama/>`_ documentation.

Coordinate transformation
:::::::::::::::::::::::::

**TODO**
*Why do we need new data set? We can use the coordinates calculate in the test1
data set! For the affine transformation we have enogh points!*

Let's transform the points in our data set to an other coordinate system using common points, which are known in both coordinate systems.
A second coordinate list was prepared with the coordinates in the target system.

**TODO**
*start of part to erase*

.. figure:: images/t61.png
   :scale: 80 %
   :align: center

   *(41.) Click Add vector layer icon, and select an existing file*

.. figure:: images/t62.png
   :scale: 80 %
   :align: center

   *(42.) Click Layer Labeling Options icon*

.. figure:: images/t63.png
   :scale: 80 %
   :align: center

   *(43.) Turn on labeling and select point_id*

**TODO**
*end of part to erase*

.. figure:: images/t64.png
   :scale: 80 %
   :align: center

   *(44.) Starting coorinate transformation*
   
Click Coordinate transformation icon on SurveyingCalculation toolbar to start 
the calculation.

.. figure:: images/t65.png
   :scale: 80 %
   :align: center

   *(45.) Selecting from coordinate list*
   
Select the shape file to transform from, only the loaded coordinate lists can be selected from the list.
Then press the button with ellipses (...) to select the target shape file of the
transformation.

.. figure:: images/t66.png
   :scale: 80 %
   :align: center

   *(46.) Selecting points*
   
After spacifying the source and the target of transformation the *Common Points*
list is filled automatically. Add points from the common points to the *Used Points* list.

.. figure:: images/t67.png
   :scale: 80 %
   :align: center

   *(47.) Selecting the type of transformation*
   
Different transformation types require different number of point. Only those transformation types are available for which enough points were selected.

.. figure:: images/t68.png
   :scale: 80 %
   :align: center

   *(48.) Calculating transformation*
   
Click calculate button and the transformation parameters and transformed 
coordinates will be calculated. Results of the calculation can be checked in the result widget.*

