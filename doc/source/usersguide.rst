========================================
SurveyingCalculation plugin for QGIS 2.x
========================================
User's Guide
------------


Typographical conventions
:::::::::::::::::::::::::

**TODO**

Hardware and software requirements
::::::::::::::::::::::::::::::::::

The SurveyingCalculation plug-in can be used on any computer on which QGIS 
can run. It was tested on Windows 7 and Fedora Linux, but on any other Windows 
versions or Linux distros is should work.

SurveyingCalculation plugin install
:::::::::::::::::::::::::::::::::::

**Installing from GitHub**

If you have Git Client (Git Bash or other clients)

#. git clone from https://github.com/zsiki/ls to *~/.qgis2/python/plugins/SurveyingCalculation* (~ is your home directory on Linux, replace it on Windows)
#. Open QGIS Desktop.

If you don't have Git Clone

#. Download the ZIP file from https://github.com/zsiki/ls to your computer.
#. Unzip to *~/.qgis2/python/plugins/SurveyingCalculation*.
#. Open QGIS Desktop.

**Installing from QGIS Plug-in repo**

#. Start QGIS
#. In the the plug-in dialog enable experiental plugins
#. Look for SurveyingCalculation plug-in and press Install button

After installing the plug-in you must enable it in the *Manage and Install 
Plugins* dialog. After it the menu and the toolbar of the plug-in
will be visible.

.. figure:: images/u01.png
   :scale: 80 %
   :align: center

   *(1.) Manage and Install Plugins*


Is switched on SurveyingCalculation plugin?

.. figure:: images/u02.png
   :scale: 80 %
   :align: center

   *(2.) Installed SurveyingCalculation plug-in*


.. figure:: images/u03.png
   :scale: 80 %
   :align: center

   *(3.) SurveyingCalculation plugin in QGIS (menu and toolbar)*


**Gama project: gama-local**

Beside installing the plug-in you must also install gama-local (part of the GNU
Gama project) for adjustment calculation. See: https://www.gnu.org/software/gama



Settings before use
:::::::::::::::::::

Set to empty string the *Representation for NULL values* on the Data sources
tab in the Setting/Options menu. It makes the Attribute Table (Fieldbook) more
readable.

.. figure:: images/u04.png
   :scale: 80 %
   :align: center

   *(4.) Settings of Attribute Table*


.. figure:: images/u05.png
   :scale: 80 %
   :align: center

   *(5.) Settings of Attribute Table*

Open an existing QGIS project which contains a coordinate list (a point shape
file which name must stat with 'coord\_') or create a new project and add an
existing coordinate list to the project or create a new project and create 
a new coordinate list from the *Surveying Calculation* menu.

Check the coordinate reference system (CRS) of your coordinate list (layer
properties from the popup menu of the layer) and the map.

After loading an existing or creating a new Coordinate list shape file, you get
an empty table in your project with the following columns (column names and 
types are mandatory):
        :point_id:    point number
        :e:           East coordinate
        :n:           North coordinate
        :z:           Z coordinate (elevation)
        :pc:          point code
        :pt:          point type


.. figure:: images/u06.png
   :scale: 80 %
   :align: center

   *(6.) New coordinate list*


.. figure:: images/u07.png
   :scale: 80 %
   :align: center

   *(7.) Empty coordinate table*

Only one coordinate list should be open in a project.

Import fieldbook
::::::::::::::::

Any number of electric fieldbooks can be opened/loaded into a QGIS project.
You can even create a new empty fieldbook and fill it manually.

#. There must be az open coordinate list in your actual project (a point layer which name starts with coord\_). Otherwise coordinates read from the filedbook will be lost
#. Click on the Load fieldbook icon or select it from the menu
#. Choose the type of fieldbook (`Geodimeter JOB/ARE`_; `Leica GSI`_; `Sokkia CRD`_)

The loader adds an extra column to the observations, the id column, sorting the
table by this column gives the right order of observations.

You can create an empty fieldbook for manual input using the *Create fieldbook*
menu.

Geodimeter JOB/ARE
++++++++++++++++++

#. Select the JOB file
#. Select the output DBF file where your observations will be stored, the name will start with *fb_*, the program will add it to the name automatically you forget
#. After giving the path to the DBF file a new fieldbook is added to your QGIS project. The name of the fieldbook always starts with "fb\_". This database table stores measurements only, it has no graphical (map) data. Fields in the table:
        :id:          ordinal number of observation in fieldbook, sort by this field normally
        :point_id:    point number (max 20 characters)
        :station:     if record data belongs to a station it must be *station* otherwise empty
        :hz:          horizontal angle or orientation angle in station record
        :v:           vertical angle
        :sd:          slope distance
        :th:          target height or instrument height in station record
        :pc:          point code
#. After loading the .JOB, you can optionally load an .ARE file in the same way

.. figure:: images/u08.png
   :scale: 80 %
   :align: center

   *(8.) Import fieldbook*


.. figure:: images/u09.png
   :scale: 80 %
   :align: center

   *(9.) Fieldbook*


.. figure:: images/u10.png
   :scale: 80 %
   :align: center

   *(10.) Coordinate table*

TODO codes loaded from job/are
   
Leica GSI
+++++++++

Both the 8 byte and 16 byte GSI files are supported. As there is no standard
markers for station data in GSI files, you can use code block to mark a new
station in observations or you must have a record with station coordinates or
instrument height.

See Job loading.

TODO codes loaded from GSI

Sokkia CRD
++++++++++

See JOB loading.

TODO codes loaded from CRD

Using fieldbook data
::::::::::::::::::::

Angles are displayed in the fieldbook in Grads (Gon) unit with four decimals.
Distances, instrument and target heights are in meters.

Sort the fieldbook by the id column, to have the right order of observations.

(TODO: How to change, insert, delete, ...)

It is possible to change the fieldbook, insert and delete feature. Open the fieldbook Attribute Table,
turn on Toggle Editing Mode.

**Insert feature**: Click the Add feature button and fill in the gap.

**Delete feature**: Select to be delete feature(s) and click the Delete selected features.

After the action you have to save the changes, click the Save Edits or Toggle Editing Mode button.



.. figure:: images/u11.png
   :scale: 80 %
   :align: center

   *(11.) Add feature to Fieldbook*



Add new point to Coordinate list
::::::::::::::::::::::::::::::::

In the Add new point dialog you can manually add point with coordinates. Before start using, you have to
select Toggle Editing Mode at Layer.
Use the Add button if you would like to add more points. The Add button save the new point and clear the board.
The Close button save the new point and close the dialog window.


.. figure:: images/u12.png
   :scale: 80 %
   :align: center

   *(12.) Add new point with coordinates to Coordinate list*



Single Point Calculations
:::::::::::::::::::::::::

In the single calculation dialog you can calculate coordinates of single points
using trigonometric formulas.

Orientation
+++++++++++
#. Click the Single Point Calculations icon.
#. Select the Orientation from the type of Calculations.
#. Select the Station from the list. You can calculate only the orientation of one station at a time.
#. The Target Points list loads automatically.
#. Add to Used Points list one or more points which ypu would like to use for the orientation. If you would like to change the *Used Points* list, use the Remove button.
#. Click the Calculate button.
#. Result of Calculation displayed automatically in result window.
#. You can change settings in the dialog and press calculate to make another calculation, use the Reset button to reset the dialog to its original state.

.. figure:: images/u14.png
   :scale: 80 %
   :align: center    

   *(14.) Orientation*
       

.. figure:: images/u15.png
   :scale: 80 %
   :align: center

   *(15.) Result of Orientation*


Radial Survey (Polar Point)
+++++++++++++++++++++++++++

Elevation is calculated for polar points if the instrument height and the
station elevation are given.

#. Click the Single Point Calculations icon.
#. Select the Radial Survey from the type of Calculations.
#. Select the Station from the list. You can calculate several polar point from the same station at a time.
#. The Target Points list loads automatically.
#. Add to Used Points list one or more points which you would like to calculate coordinates for. If you would like to correct, use the Remove button.
#. Click the Calculate button.
#. Result of Calculation displayed automatically in result window.
#. You can change settings in the dialog and press calculate to make another calculation, use the Reset button to reset the dialog to its original state.

.. figure:: images/u16.png
   :scale: 80 %
   :align: center

   *(16.) Radial Survey*


Intersection
++++++++++++
#. Click the Single Point Calculations icon.
#. Select the Intersection from the type of Calculations.
#. Select two stations from the Station(1) and Station(2) lists
#. The Target Points list loads automatically. It contains the points, which were measured from both stations.
#. Add to Used Points list one or more points which would like to calculate coordinates. If you would like to correct, use the Remove button.
#. Click the Calculate button.
#. Result of Calculation prints automatically in result window.
#. You can change settings in the dialog and press calculate to make another calculation, use the Reset button to reset the dialog to its original state.

.. figure:: images/u17.png
   :scale: 80 %
   :align: center

   *(17.) Intersection*


Resection
+++++++++
#. Click the Single Point Calculations icon.
#. Select the Resection from the type of Calculations.
#. Select the station from Station (1) list.
#. The Target Points list loads automatically. The list contains the points, which were measured from the station. You can calculate only one station coordinates at a time.
#. Add three points to the Used Points list which will be used for resection. If you would like to correct, use the Remove button.
#. Click the Calculate button.
#. Result of Calculation prints automatically in result window.
#. You can change settings in the dialog and press calculate to make another calculation, use the Reset button to reset the dialog to its original state.

.. figure:: images/u18.png
   :scale: 80 %
   :align: center
       
   *(18.) Resection*

       
Free Station
++++++++++++
#. Click the Single Point Calculations icon.
#. Select the Free Station from the type of Calculations.
#. Select the station from Station (1) list.
#. The Target Points list loads automatically. The list contains the points, which were measured from the station. You can calculate only one station coordinates at a time.
#. Add two or more points to the Used Points list which will be used for calculate. If you would like to correct, use the Remove button.
#. Click the Calculate button.
#. Result of Calculation prints automatically in result window.
#. You can change settings in the dialog and press calculate to make another calculation, use the Reset button to reset the dialog to its original state.

.. figure:: images/u19.png
   :scale: 80 %
   :align: center
       
   *(19.) Free Station - Adjusted coordinates*



Traverse Calculations
:::::::::::::::::::::

It is possible to calculate three types of Traverse.

#. **Closed traverse**: Closed (polygonal or loop) traverse starts and finishes on the same known point.
#. **Link traverse**: A closed link traverse joins two known points.
#. **Open traverse**: An open (free) traverse starts on a known point and finishes on an unknown point.


How can I use?

#. Click the Traverse Calculations icon.
#. Select the type of Traverse Calculation from the list.
#. Select the Endpoint from Start Point list.
#. If necessary select the Endpoint from End Point list.
#. The Target Points list loads automatically. The list contains the points, which were measured from the station.
#. Add points of Traversing from Target Points list one by one to Order of Points list.
#. The Order can be changed with Up and Down button. If you would like to correct, use the Remove button.
#. Click the Calculate button.
#. Result of Calculation prints automatically in result window.
#. You can change settings in the dialog and press calculate to make another calculation, use the Reset button to reset the dialog to its original state.


.. figure:: images/u20.png
   :scale: 80 %
   :align: center
       
   *(20.) Traverse Calculation - Link traverse*



Network adjustment
::::::::::::::::::
#. Click the Network adjustment icon.
#. Select the fix points from List of Points and add to the Fix points list.
#. Select points to adjust from List of Points and add to the Adjusted points.
#. Check the parameters of the adjustment.
#. If you would like to correct, use the Remove button.
#. Click the Calculate button.
#. Result of Calculation prints automatically in result window. Parameters of the Adjustment can be checked in the result window.
#. You can change settings in the dialog and press calculate to make another calculation, use the Reset button to reset the dialog to its original state.


.. figure:: images/u21.png
   :scale: 80 %
   :align: center
       
   *(21.) Traverse Calculation - Link traverse*




Coordinate transformation
:::::::::::::::::::::::::
It is possible to calculate five types of Transformation. Each Transformations work, if you selected enough common points.

#. First add the coordinate file containing the points to transformate. Use the Add layer icon.
#. Click the Coordinate transformation icon.
#. The From Layer field automatically loaded.
#. Select the shape file where to transformate. The result points will be written in this shape file.
#. Add the used points from Common Points list to Used Points list.
#. Select the type of transformation.
#. If you would like to correct, use the Remove button.
#. Click the Calculate button.
#. Result of Calculation prints automatically in result window. Parameters of the Transformation can be checked in the result window.
#. You can change settings in the dialog and press calculate to make another calculation, use the Reset button to reset the dialog to its original state.


.. figure:: images/u22.png
   :scale: 80 %
   :align: center
       
   *(21.) Coordinate transformation - Affine transformation*




       
Polygon division
::::::::::::::::    





Plot
::::


Plot by Template
++++++++++++++++


Batch plotting       
++++++++++++++