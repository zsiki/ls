.. role:: btn

.. role:: mnu

=======================================================
User's Guide for SurveyingCalculation plugin for QGIS 2
=======================================================

Version 0.2

DigiKom Ltd (c) 2015

http://www.digikom.hu

mail@digikom.hu

1 Introduction
~~~~~~~~~~~~~~~

The SurveyingCalculation plugin was created by the `DigiKom Ltd 
<http://www.digikom.hu>`_ (Hungary). It was supported by the SMOLE II for
Niras Finland Oy.
It was developed for the Land Parcel Cadastre of Zanzibar.

1.1 Hardware and software requirements
::::::::::::::::::::::::::::::::::::::

The SurveyingCalculation plugin can be used on any computer on which QGIS 2
can run. It was tested on Windows 7 and Fedora Linux, but it should work on 
other Windows versions or Linux distros. QGIS version 2.2, 2.4, 2.6 and 2.8
were used for testing the plugin.

The network adjustment and the free station calculation in the plugin is based 
on the GNU Gama open source project. `GNU Gama <https://www.gnu.org/software/gama/>`_ must be installed separately to use these calculations.

1.2 Installation of the SurveyingCalculation plugin
:::::::::::::::::::::::::::::::::::::::::::::::::::

There are different methods to install the plugin. The easiest way is to
install it from the QGIS Plugin repository. To use the latest development
version you can install it directly from GitHub, it is mainly for advanced
users.

1.2.1 Installing from QGIS Plugin repo
++++++++++++++++++++++++++++++++++++++

#. Start QGIS on your machine.
#. In the plugin dialog enable experimental plugins (after evaluating the plugin by the QGIS community it will be changed to standard - non experimental - plugin). To open the plugin dialog select :mnu:`Plugins/Manage and install plugins` from the menu then select *Settings* tab to see the checkbox of experimental plugins.
#. Look for SurveyingCalculation plugin in the list on the *All* or the *Not installed* tab, select the SurveyingCalculation plugin and press the :btn:`[Install]` button.

.. figure:: images/u01.png
   :scale: 75 %
   :align: center

   *(Figure 1) Manage and Install Plugins in the menu*

1.2.2 Installing from GitHub
++++++++++++++++++++++++++++

Before starting the installation exit QGIS.

If you have a *git* client on your machine (e.g. TortoiseGit):

#. git clone the plugin from https://github.com/zsiki/ls to *~/.qgis2/python/plugins/SurveyingCalculation* on your local machine (~ marks your home directory on Linux, replace it on Windows with your home directory).
#. Start QGIS on your machine.

If you don't have a *git* client:

#. Download the *ZIP* file from https://github.com/zsiki/ls/archive/master.zip to your computer.
#. Unzip it to *~/.qgis2/python/plugins/SurveyingCalculation* (~ marks your home directory on Linux, replace it on Windows with your home directory).
#. Start QGIS on your machine.

After installing the plugin you have to enable it in the *Manage and Install 
Plugins* dialog (Figure 1 and Figure 2). Then the menu and the toolbar of 
the plugin will be visible (Figure 3).

.. figure:: images/u02.png
   :scale: 75 %
   :align: center

   *(Figure 2) SurveyingCalculation plugin enabled*

.. figure:: images/u03.png
   :scale: 50 %
   :align: center

   *(Figure 3) SurveyingCalculation plugin in QGIS (menu and toolbar)*

1.2.3 GNU Gama project: gama-local
++++++++++++++++++++++++++++++++++

Beside installing the plugin you also have to install gama-local (part of the
GNU Gama project) to be able to calculate free station and adjustment
calculations. See: https://www.gnu.org/software/gama. You can download Windows 
binaries of GNU Gama from http://sourceforge.net/projects/gnu-gama-builds.

1.3 Settings before use
:::::::::::::::::::::::

There are some settings which the plugin can be customized with. These are in
the *config.py* file. Settings described in this section are optional.

Check and change the settings in the *config.py* file, this file is in the
installation directory of the SurveyingCalculation plugin. The following
variables can be set in the config:

    :fontname: monospace font used in the calculation results widgets
    :fontsize: font size used in the calculation results widget
    :homedir: starting directory used for loading fieldbooks from, you can select any other directory
    :log_path: full path to log file, the program must have write access right to the directory and the file
    :line_tolerance: snapping to vertex tolerance used by line tool in SRS units
    :area_tolerance: area tolerance for area division, if the difference between the actual area and the requested area is smaller than this value, the iteration is stopped
    :max_iteration: maximal number of iterations for area divisio
    :gama_path: full path to gama-local (used for network adjustment and free station)

Before changing any value in the config.py make a backup copy.
If you change any value in the *config.py* file, the QGIS plugin have to be
reloaded or QGIS have to be restarted to use the new value.

There are some QGIS settings which can make your work more confortable.

Set the default coordinate reference system (CRS) for new projects and
new layers on the *CRS* tab in the *Setting/Options* dialog (Figure 4) to the 
locally used CRS. 

Set the *Representation for NULL values* to empty string on the *Data sources*
tab in the :mnu:`Setting/Options` menu (Figure 5). It makes the Attribute Table
(Fieldbook) more readable.

.. figure:: images/u04.png
   :scale: 75 %
   :align: center

   *(Figure 4) Settings/Options... menu*

.. figure:: images/u05.png
   :scale: 75 %
   :align: center

   *(Figure 5) Setting NULL values*

1.4 Data sets used by the plugin
::::::::::::::::::::::::::::::::

The plugin uses standard QGIS data sets, only the name of them is plugin 
specific and there are obligatory columns in these data sets. QGIS project files
can also be used to save and reload your working environment.

1.4.1 Coordinate lists
++++++++++++++++++++++

Most of the cases you need an open coordinate list to have known points for the
calculations and to store calculated coordinates into. 
The coordinate list is a QGIS point vector layer with specific columns.
All point coordinates in a coordinate list have to be in the same Coordinate 
Refference System (CRS). The name of the 
coordinate lists must start with *coord\_* and have to contain some obligatory 
columns (column names and types are mandatory):

        :point_id:    point number (string 20)
        :e:           East coordinate (number 12.3)
        :n:           North coordinate (number 12.3)
        :z:           Z coordinate (elevation) (number 8.3)
        :pc:          point code (string 20)
        :pt:          point type (string 20)

You mustn't rename or erase the standard columns but you can add new columns to extend the attribute table.
The data in the first three columns (*point_id*, *e* and *n*) have to be filled for each point.

1.4.2 Fieldbooks
++++++++++++++++

Fieldbooks store observation data, angles, distances, etc. You can fill a
fieldbook manually or you can load electric fieldbooks downloaded from
totalstations.  Fieldbooks are standard QGIS table data without geometry.
The name of the fieldbook must start with "fb\_". Fields in the table are:

        :id:          ordinal number of observation in fieldbook, sort by this field normally
        :point_id:    point number (max 20 characters)
        :station:     if record data belongs to a station it must be *station* otherwise empty
        :hz:          horizontal angle or orientation angle in station record
        :v:           zenith angle
        :sd:          slope distance (horizontal distance if zenith angle is empty)
        :th:          target height or instrument height in station record
        :pc:          point code

You musn't change the name of columns or erase them, but you can add new
columns to the table. The first *id* column is used to define the order of the
observation records.

A fieldbook contains two different record types, station and observation 
records.  The station record marks the start of a new occupied station in the 
observations. These station records are marked by the **station** word in the
*station* column. In a station record only
the *id*, *point_id*, *station*, *th* columns are used.
The observation records contain empty (NULL) data in the *station* column.

2 Creating and loading data sets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before you can start the calculations some data sets have to be loaded into
your QGS project. Use one coordinate list and any number of fieldbooks.

2.1 Working with coordinate list
::::::::::::::::::::::::::::::::

Before you start your work open an existing QGIS project which contains a 
coordinate list (a point shape file whose name starts with *coord\_*) or create
a new project and add an existing coordinate list to the project by the
:btn:`[Add vector layer]` |addvec|  icon or create 
a new project and create a new coordinate list from the
:mnu:`SurveyingCalculation/New coordinate list ...` menu (Figure 6). The plugin
automatically adds the *coord\_* (if necessary) in front of the name you gave
and adds the new empty coordinate list to the project.

.. |addvec| image:: images/addvec.png

.. figure:: images/u06.png
   :scale: 75 %
   :align: center

   *(Figure 6) Creating new coordinate list from the menu*

Check the coordinate reference system (CRS) of your coordinate list
(:mnu:`Properties` from the popup menu of the layer) and the map (lower right 
part of the QGIS status line).

.. figure:: images/u07.png
   :scale: 50 %
   :align: center

   *(Figure 7) The new empty coordinate list/table*

.. note::
    Be careful!
    Do not edit the coordinates manually, because the point position won't change automatically. 
    Do not add new point by mouse click, because the coordinate columns in the table won't change automatically.

Use the *Add new point* dialog to update coordinates and location together.
Expert users can use the *Field calculator* to update the coordinates in the
attribute table from the geometry.

.. note::
   Only one coordinate list should be open in a project at a time.

2.1.1 Add new point to the Coordinate list
++++++++++++++++++++++++++++++++++++++++++

In the *Add new point* dialog you can manually add new points to the coordinate list. The *Add new point* dialog can be opened from the 
:btn:`SurveyingCalculation` menu.
The *Point ID*, *East*, *North* fields must be filled, the others are optional.
Use the :btn:`[Add]` button to add the point to the coordinate list. The 
:btn:`[Add]` button saves the new point and resets the form. You can add more 
points if you edit the fields and push the :btn:`[Add]` button.
The :btn:`[Close]` button closes the dialog window.

This dialog can be used to overwrite existing coordinates in the coordinate 
list, too. If you input an existing point number, a warning will be displayed 
and you can decide whether to overwrite the stored point.

.. figure:: images/u12.png
   :scale: 50 %
   :align: center

   *(Figure 12) Add new point to the Coordinate list*

You can use the standard QGIS :btn:`[Add Delimited Text Layer]` button to bulk
import coordinates from CSV or TXT files. The restrictions are

- the column names must be the same as discribed before (point_id, e, n, z, pc, pt)
- the column types must be the same as discribed before, a CSVT file can be created to define column types, the name of the CSVT file have to be the same as the CSV file
- the name of result shape file have to start with *coord_*

To define the data types for the columns of the CSV file, a CSVT definition
file can be created. It is a one line text file.
Sample CSVT file to load coordinate lists::

   String(20),Real(12.3),Real(12.3),Real(8.3),String(20),String(20)

2.2 Working with fieldbooks
:::::::::::::::::::::::::::

You can create an empty fieldbook for manual input using the
:mnu:`New fieldbook` from the SurveyingCalculation menu.
You can edit the fieldbook if you push :btn:`[Toggle Editing Mode]` |edit|
icon. The loader adds an extra column to the observation data, the id column,
sorting the table by this column gives the right order of the observations.

.. |edit| image:: images/edit.png

2.2.1 Importing fieldbooks
++++++++++++++++++++++++++

Observations made by total stations and GPS are stored in electric fieldbooks.
The files storing the fieldbook data have to be downloaded to the computer
before you can use them in the plugin. Different fieldbook types are supported:

- Leica GSI 8/16
- Geodimeter JOB/ARE
- Sokkia CRD
- SurvCE RW5
- STONEX DAT

Any number of electric fieldbooks can be opened/loaded into a QGIS project.
You can even create a new empty fieldbook and fill it manually.

#. There must be an open coordinate list in your actual project (a point layer whose name starts with *coord\_*). Otherwise coordinates read from the filedbook will be lost
#. Click on the Load fieldbook icon or select it from the :mnu:SurveyingCalculation` menu
#. Choose the type of the fieldbook (Geodimeter JOB/ARE, Leica GSI, Sokkia CRD, SurvCE RW5, STONEX DAT)
#. Select the output DBF file where your observations will be stored, the name will start with *fb_*, the program will add it to the name automatically if you forget it
#. After giving the path to the DBF file the new fieldbook will be added to your QGIS project.


.. figure:: images/u08.png
   :scale: 75 %
   :align: center

   *(Figure 8) Import fieldbook menu*


.. figure:: images/u09.png
   :scale: 50 %
   :align: center

   *(Figure 9) Fieldbook attribute window*


.. figure:: images/u10.png
   :scale: 50 %
   :align: center

   *(Figure 10) Coordinate list*

2.2.1.1 Leica GSI
-----------------

Both the 8 byte and 16 byte GSI files are supported. As there are no standard
markers for station start in GSI files, you can use code block to mark a new
station in observations or you have to have a record with station coordinates or
instrument height to mark the start of a new station.

Code block to mark the start of a station:

::

    410001+00000002 42....+12012502 43....+00001430

410001+00000002
    Code 2, start of a new station

42....+12012502
    Station id is 12012502

43....+00001430 
    Instument height 1.430 m (optional)

Data codes handled, loaded from GSI:

    :11: point id
    :21: horizontal angle (hz)
    :22: vertical angle (v)
    :31: slope distance (sd)
    :41: code block
    :42: station id
    :43: station height
    :71: point code (pc)
    :81: easting
    :82: northing
    :83: elevation
    :84: easting of station
    :85: northing of station
    :86: elevation of station
    :87: target height (th)
    :88: station height (overwrites 43 code)

The different units in the electric fieldbook are converted to GON and meters
during the import.

2.2.1.2 Geodimeter JOB/ARE
--------------------------

JOB and ARE are separate data files. Observations and optional coordinates are stored in JOB file. Only coordinates are stored in ARE file.
After loading a .JOB you can optionally load an .ARE file in the same way.

Data codes handled, loaded from JOB/ARE:

    :2: station id
    :3: instrument height
    :4: point code (pc)
    :5: point id
    :6: target height (th)
    :7: horizontal angle (hz)
    :8: zenith angle (v)
    :9: slope distance (sd)
    :23: units
    :37: northing
    :38: easting
    :39: elevation
    :62: orientation point id

The different units in the electric fieldbook are converted into GON and meters
during the import.

2.2.1.3 Sokkia CRD
------------------

Sokkia CRD loader can handle two softly different file format SDR33 and SDR20.

Data records handled, loaded from CRD:

    :00: header record
    :02: station record
    :03: target height
    :08: coordinates
    :09: observations

The different units in the electric fieldbook are converted into GON and meters
during the import.

2.2.1.4 SurvCE RW5
------------------

The SurvCE program RW5 format can store total station and GPS observations.
Both type of data can be loaded into QGIS.

Data records handled, loaded from CRD:

    :GPS: latitude, longitude from GPS receiver
    :--GS/SP: projected coordinates (overwrites latitude, longitude)
    :OC: station record
    :TR/SS/BD/BR/FD/FR: observation record
    :BK: orientation record
    :LS: instrument height and target height record
    :MO: units record

The different units in the electric fieldbook are converted into GON and meters
during the import.

2.2.1.5 STONEX DAT
------------------

Unfortunately we had no description for this fieldbook format, we reverse engineered information from the sample file we got.
GON angle units and meters are supposed for the data in the DAT file.

Data records handled, loaded from DAT:

    :K: station and orientation angle
    :E: observation record
    :B/C: coordinate record
    :L: orientation direction record

2.2.2 Using fieldbook data
++++++++++++++++++++++++++

Angles are displayed in the fieldbook in Grads (Gon) units with four decimals.
Distances, instrument and target heights are in meters.

Sort the fieldbook by the id column, to have the right order of observations.

Data in the loaded fieldbooks can be changed, records can be inserted, updated and deleted. You can use
the standard QGIS tools to change or extend fieldbook data. Open the 
fieldbook Attribute Table, turn on :btn:`[Toggle Editing Mode]` |edit|.

**Insert record**: Click on the :btn:`[Add feature]` button and fill in the record. Use the
right id (first column) for the row to get the right position in the fieldbook.

**Delete record**: Select the records to be deleted and click on the :btn:`[Delete selected features]` button.

**Update record**: Double click on the field you want to change and edit the data.

After editing the fieldbook data you have to save the changes, click the :btn:`[Save Edits]` or :btn:`[Toggle Editing Mode]` button.


.. figure:: images/u11.png
   :scale: 75 %
   :align: center

   *(Figure 11) Add feature to Fieldbook*

3 Surveying Calculations
~~~~~~~~~~~~~~~~~~~~~~~~

The calculation part of the plugin is divided into four parts. The *Single 
calculations* part contains all calculations for a single point (orientation, 
radial survey, intersection, reserction, free station). Traversing calculations
are in the second group, different types of traverse lines are supported
(closed, link and open traverse). Network adjustment is in the third group and 
coordinate transformations in the fourth group.

3.1 Single Point Calculations
:::::::::::::::::::::::::::::

During the calculations the plugin will use the data from the opened fieldbooks (*fb\_* tables) and from the opened coordinate list (*coord\_* layer).

In the single calculation dialog you can calculate coordinates of single points
using trigonometric formulas.

All calculations can be repeated, the last calculated values will be stored,
the previous values are lost. The results of the previous calculations are 
available in the log file.

A SurveyingCalculation plugin maintains a log file, a simple text file. The 
details of calculations are written to the log. The location of the log file 
can be set in the *config.py*.

In the different lists of the dialog you can see the fieldbook name and the id 
beside the point name. These are neccessary to distinguis stations if the same 
station was occupied more then once, or directions if the same direction was measured from the same station more than once.

3.1.1 Orientation
+++++++++++++++++

Orientation of stations is neccessary to solve intersection, radial survey and 
some type of traversing line. During the orientation no coordinates are calculated.

To calculate orientation angle on a station do the following:

#. Click on the Single Point Calculations icon to open the *Single Point Calculation* dialog.
#. Select the Orientation from the *Calculation* group.
#. Select the station id from the *Station (1)* list. You can calculate the orientation of one station at a time.
#. The *Target Points* list is filled automatically, with the directions to known points from the selected station.
#. Add to *Used Points* list one or more points which you would like to use for the orientation. If you would like to change the *Used Points* list, use the :btn:`[Remove]` button.
#. Click on the :btn:`[Calculate]` button.
#. Results of calculation are displayed automatically in result widget and sent to the log file.
#. You can change settings in the dialog and press *Calculate* to make another calculation, use the :btn:`[Reset]` button to reset the dialog to its original state.


.. figure:: images/u14.png
   :scale: 75 %
   :align: center    

   *(Figure 14) Orientation*
       

.. figure:: images/u15.png
   :scale: 75 %
   :align: center

   *(Figure 15) Result of Orientation*


3.1.2 Radial Survey (Polar Point)
+++++++++++++++++++++++++++++++++

Beside the horizontal coordinates the elevation is also calculated for polar 
points if the instrument height, the target height and the station elevation are given.

#. Click on the Single Point Calculations icon to open the *Single Point Calculations* dialog
#. Select *Radial Survey* from the *Calculation* group.
#. Select the Station id from the *Station (1)* list. The list contains only points with orientation angle. You can calculate several polar points from the same station at a time.
#. The *Target Points* list is filled automatically with the points observed from the selected station. The points in bold face have coordinates.
#. Add one or more points to the *Used Points* list, which you would like to calculate coordinates for. If you would like to change the *Used Points* list, use the :btn:`[Remove]` button.
#. Click on the :btn:`[Calculate]` button.
#. Results of calculation are displayed automatically in result widget and sent to the log file.
#. You can change settings in the dialog and press *Calculate* to make another calculation, use the :btn:`[Reset]` button to reset the dialog to its original state.


.. figure:: images/u16.png
   :scale: 75 %
   :align: center

   *(Figure 16) Radial Survey*


3.1.2 Intersection
++++++++++++++++++

You can calculate horizontal coordinates for one or more points, which directions were observed from two known stations.

Before the intersection calculation the used stations must be oriented.

To calculate intersection do the following:

#. Click on the Single Point Calculations icon in the toolbar to open the *Single Point Calculations* dialog.
#. Select Intersection from the *Calculation* group.
#. Select two known stations from the *Station(1)* and *Station(2)* lists. The lists contain only points with orientation angle.
#. The *Target Points* list is filled automatically. It contains the points measured from both stations. The points in bold face have coordinates.
#. Add one or more points to the *Used Points* list which you would like to calculate coordinates for. If you would like to change the *Used Points* list, use the :btn:`[Remove]` button.
#. Click on the :btn:`[Calculate]` button.
#. Results of Calculation are displayed automatically in result widget and sent to the log file.
#. You can change settings in the dialog and press *Calculate* to make another calculation, use the :btn:`[Reset]` button to reset the dialog to its original state.


.. figure:: images/u17.png
   :scale: 75 %
   :align: center

   *(Figure 17) Intersection*

3.1.4 Resection
+++++++++++++++

You can calculate horizontal coordinates of a station if at least three known points were observed from there.

To calculate resection do the followings

#. Click on the Single Point Calculations icon in the toolbar to open the *Single Point Calculations* dialog.
#. Select Resection from the *Calculation* group.
#. Select the station id from the *Station (1)* list. The list contains all stations. The stations in bold face have coordinates.
#. The *Target Points* list is filled automatically. The list contains the known points, which were measured from the station. You can calculate the coordinates of one station at a time.
#. Add exactly three points to the *Used Points* list which will be used for resection. If you would like to correct, use the :btn:`[Remove]` button.
#. Click on the :btn:`[Calculate]` button.
#. Results of calculation are displayed automatically in result widget and sent to the log file.
#. You can change settings in the dialog and press :btn:`[Calculate]` button to make another calculation, use the :btn:`[Reset]` button to reset the dialog to its original state.


.. figure:: images/u18.png
   :scale: 75 %
   :align: center
       
   *(Figure 18) Resection*
       
3.1.5 Free Station
++++++++++++++++++

You can calculate the horizontal coordinates of a station from directions and distances using the least squares method.

To calculate free station do the following:

#. Click on the Single Point Calculations icon in the toolbar to open the *Single Point Calculations* dialog.
#. Select Free Station from the *Calculation* group.
#. Select station id from the *Station (1)* list. The list contains all stations. The stations in bold face have coordinates.
#. The Target Points list is filled automatically. The list contains the known points, which were measured from the selected station. You can calculate the coordinates of one station at a time.
#. Add two or more points to the Used Points list which will be used for calculation. If you would like to correct, use the :btn:`[Remove]` button.
#. Click on the :btn:`[Calculate]` button.
#. Results of calculation are displayed automatically in the result widget and sent to the log file.
#. You can change settings in the dialog and press *Calculate* to make another calculation, use the :btn:`[Reset`] button to reset the dialog to its original state.


.. figure:: images/u19.png
   :scale: 75 %
   :align: center
       
   *(Figure 19) Free Station - Adjusted coordinates*

The result list of the adjustment is very long. Consult the GNU Gama documentation for further details.

Free station calculation uses the default standard deviations (3cc, 3mm+3ppm) for the adjustment.

3.2 Traverse Calculations
:::::::::::::::::::::::::

During the traverse calculations the plugin will use the data from the opened fieldbooks (*fb\_* tables) and from the opened coordinate list (*coord\_* layer).

It is possible to calculate three different types of traverse.

#. **Closed traverse**: Closed (polygonal or loop) traverse starts and finishes at the same known point. This point must be oriented.
#. **Link traverse**: A closed link traverse joins two different known points. None, one or both ends can be oriented.
#. **Open traverse**: An open (free) traverse starts at a known point with orientation and finishes at an unknown point.

To calculate traverse do the following:

#. Click on the Traverse Calculations icon in the toolbar to open the *Traverse Calculations* dialog.
#. Select the type of traverse from *Type* group.
#. Select the start point of traverse from the *Start Point* list.
#. Select the end point from the *End Point* list.

    - In case of closed traverse the *End Point* list is disabled and changes according to the *Start Point* list.
    - In case of link traverse the *End Point* list contains all known stations.
    - In case of open traverse the *End Point* list contains the points measured from the last point in the *Order of points* list. Therefore the end point should be selected after inserting and sorting all angle points in the *Order of points* list.

#. The Target Points list is filled automatically. The points in bold face have coordinates.
#. Add the traverse points from the *Target Points* list to the *Order of Points* list one by one.
#. The order of traverse points can be changed with :btn:`[Up]` and :btn:`[Down]` button. If you would like to correct, use the :btn:`[Remove]` button.
#. In case of open traverse select the end point now.
#. Click on the :btn:`[Calculate]` button.
#. Results of calculation are displayed automatically in result widget and sent to the log file.
#. You can change settings in the dialog and press :btn:`[Calculate]` button to make another calculation, use the :btn:`[Reset]` button to reset the dialog to its original state.


.. figure:: images/u20.png
   :scale: 75 %
   :align: center
       
   *(Figure 20) Traverse Calculation - Link traverse*

In the result of calculation you can find the angle and coordinate corrections, and the coordinates of the traversing points.

3.3 Network adjustment
::::::::::::::::::::::

During the network adjusment the plugin will use the data from the opened fieldbooks (*fb\_* tables) and from the opened coordinate list (*coord\_* layer).

Network adjustment is the best method to calculate the most probably position of observed points, when more observations were made than neccessary. By the help of GNU Gama adjustment the blunder errors can be detected, eliminated.

Free network can also be adjusted, when there are no fixed coordinates in the network. In this case some points have to have approximate coordinates.

To calculate network adjustment do the following:

#. Click on the Network adjustment icon to open the *Network Adjustment* dialog.
#. Select the fix points from the *List of Points* and add them to the *Fix points* list. During the adjustment the coordinates of fix points will not be changed. Points in bold face in the *List of Points* have coordinates in the actual coordinate list, so only those can be added to the *Fix Points* list. In the *List of points* you can find only those points which an observation was made to.
#. Select points to adjust from the *List of Points* and add them to the *Adjusted points* list. You can add any point to the *Adjusted Points*.
#. Set the parameters of the adjustment. Setting the correct standard deviations are very important from the view of adjustment calculation. Set these corresponding to the used total station.
#. If you would like to correct, use the :btn:`[Remove]` button.
#. Click on the :btn:`[Calculate]` button.
#. Results of calculation are displayed automatically in result widget and sent to the log file.
#. You can change settings in the dialog and press calculate to make another calculation, use the :btn:`[Reset]` button to reset the dialog to its original state.

.. figure:: images/u21.png
   :scale: 75 %
   :align: center
       
   *(Figure 21) Network adjustment*

The result list of the adjustment is very long. Consult the GNU Gama documentation for further details.

3.4 Coordinate transformation
:::::::::::::::::::::::::::::

Besides the on the fly reprojection service of QGIS, the SurveyingCalculation
plugin provides coordinate transformation based on common points having
coordinates in both coordinate systems. If you want to reproject coordinates to
another projection system which is known by QGIS, use QGIS :mnu:`Save As...` 
from the menu.

This coordinate transformation can be used if you know nothig about the SRS
(Spatial Reference System), but there must be points with known point in both
coordinate system. I can be more precise for smaller areas (10 km2 for 
orthogonal or affine transformation) than the reprojection with QGIS. 
Two separate coordinate lists have to be created with the coordinates in the 
two coordinate systems before starting the coordinate transformation. The point
id-s have to match in the two coordinate list.
During the coordinate transformation first the transformation parameters are
calculated based on common points and durint the second step the points whics
were not used to calculate the parameters are transformed using the parameters
calculated in the first step. The transformed coordinates of these points will
be added to the target coordinate list.

The plugin provides different types of transformation. The calculation of the transformation parameters uses the least squares estimation if you select more common points than the minimal neccessary.

    :Orthogonal transformation: at least two common points (4 parameters)
    :Affine transformation: at least three common points (6 parameters)
    :3rd order transformation: at least ten common points (20 parameters)
    :4th order transformation: at least fifteen common points (30 parameters)
    :5th order transformation: at least twenty-one common points (42 parameters)

The points in the two coordinate lists are groupped to three categories.

    :common points: point id and coordinates are given in both coordinate lists
    :points to transform: point id and coordinates are given in the source (from) list, these point will be transformed
    :other points: points which are present in the target coordinate list, these point are not used, not changed

#. The coordinate list you would like to transform from has to be opened in the actual QGIS project. **Do not open the coordinate list of the target system.**
#. Click on the Coordinate transformation icon in the toolbar to open the *Coordinate Transformation* dialog.
#. The *From Layer* field is filled automatically with the opened coordinate list.
#. Select *To Shape file* where to transform to, push the button with ellipses (:btn:`[...]`) to open the file selection dialog. The transformed points will be added to this shape file.
#. The list of *Common Points* is filled automatically.
#. Add points from the *Common Points* list to the *Used Points* list.
#. Select the type of transformation, only those types are enabled for which enough common points were selected.
#. If you would like to correct, use the :btn:`[Remove]` button.
#. Click on the :btn:`[Calculate]` button.
#. Results of calculation are displayed automatically in result widget and sent to the log file.
#. You can change settings in the dialog and press :btn:`[Calculate]` button to make another calculation, use the :btn:`[Rese]` button to reset the dialog to its original state.


.. figure:: images/u22.png
   :scale: 75 %
   :align: center
 
   *(Figure 22) Coordinate transformation - Affine transformation*

At the beginning of the result list you can find the used common points with the coordinates in both systems and the discrepancies between the target and transformed coordinates. If you find big discrepancies in the list, there are mistakes in the coordinates. At the end of the list you can find transformed points where the discrepancies are empty. These points are added to the target coordinate list.

The coordinates of those common points which were not selected for the transformation won't be changed in the target coordinate list.

4 Polygon division
~~~~~~~~~~~~~~~~~~

With the *Polygon Division* tool you can divide a parcel into two at a given area. There are two possible division types:

    :Paralel to a given line: the line will be shifted until the right side polygon of the division line will have the given area.
    :Through the first given point: the line will be rotated around the first point until the right side polygon of the division line will have the given area.

#. Select the polygon layer in the layer list in which you would like to divide a polygon.
#. Select the parcel with the *Select Single Feaure* tool, which you want to divide.
#. Click on the *Polygon Division* tool in the *SurveyingCalculation* toolbar.
#. Click at the start point of the division line and drag the rubberband line and release the mouse button at the end point. 
#. The *Area Division* dialog appears automatically.
#. Set the *Area* field and the select method. The full area field is not editable, it shows the total area of the selected polygon.
#. Set the type of division and click on the :btn:`[Divide]` button.


.. figure:: images/u23.png
   :scale: 50 %
   :align: center
       
   *(Figure 23) Polygon division - Selected polygon to divide*


.. figure:: images/u24.png
   :scale: 50 %
   :align: center
       
   *(Figure 24) Polygon division - Area Division*


.. figure:: images/u25.png
   :scale: 50 %
   :align: center
       
   *(Figure 25) Polygon division - Divided polygons*

If the given divider line does not intersect the polygon border, the plugin will extend the line.
You can give a divider line outside the selected polygon, in this case only parallel division is available in the *Area Division* dialog.

5 Plot
~~~~~~

This utility was added to the plugin for the ability to plot land parcels or other polygon type features automatically.
The plugin offers two ways to achieve this:

#. Firstly you can plot the actual map view by *Plot by Template* command using a precreated composer template file *(.qpt)*.
#. Secondly it is also possible to plot selected parcels (polygons) by *Batch plotting* command using a precreated composer template file *(.qpt)*.

Templates can be created by the print composer of QGIS (:mnu:`Save as template` from the menu). Look at the QGIS documentation for help.

5.1 Plot by Template
::::::::::::::::::::

With *Plot by template* command you can plot the actual map view at the given scale.

#. First zoom the map view to the required area and perhaps the required scale.
#. Click on the :btn:`[Plot by template]` button in the toolbar to open the *Plot by template* dialog.
#. In the dialog you can select a composer template and the scale.
#. Use the :btn:`[Change dir...]` button to select a template from another directory. The default directory for templates is the *template* subdirectory in the plugin installation directory.
#. In the scale list the previously set scale also appears beside some predefined scales. You can also give a new scale manually but it must be a positive integer value. The default scale is *<extent>* which means that the scale will be adjusted to the map view extent.
#. You can give a name to the composition optionally. If you leave blank QGIS will generate a name automatically.


.. figure:: images/u26.png
   :scale: 50 %
   :align: center
       
   *(Figure 26) Plot by Template*


In the end a composer window will appear with the map composition and it can be printed to a system printer or exported to PDF file.


5.2 Batch plotting
::::::::::::::::::

With the "Batch plotting" command you can plot selected polygons from one layer using a composer template file. *Batch plotting* creates a QGIS atlas composition, which is a multi-page composition. One polygon will be on one page. In the dialog you can choose the output of the plot.

#. This utility needs at least one polygon type layer open.
#. Select the polygons you want to plot, they must be on the same layer.
#. Click on the :btn:`[Batch plotting]` button in the toolbar to open the *Batch Plotting* dialog.
#. In the dialog select the layer which contains the selected polygons.
#. Select the composer template from the list. Use the :btn:`[Change dir...]` button to select a template from another directory. The default directory for templates is the *template* subdirectory in the plugin installation directory.
#. From the scale list you can choose from predefined scales or give a new scale manually. It has to be a positive integer value.

There are three possible outputs of batch plot:

- export to PDF
- plot to a system printer
- open in composer view 

Export to pdf
    You can export the composition to a single multi-page PDF file or to separate files (individual single page PDF file for each selected polygons). In the first case give the PDF file after pressing the :btn:`[Plot]` button. In the second case you have to fill the *Output filename pattern* field according to the *Output filename expression* of QGIS. After pressing the :btn:`[Plot]` button, select the directory where you want to save the PDF files to.


.. figure:: images/u27.png
   :scale: 50 %
   :align: center
       
   *(Figure 27) Batch plotting - Export to pdf*


Plot to the system printer
    It is possible to send the composition directly to the printer. After pushing the :btn:`[Plot]` button the Print settings dialog will be shown. At this point you can select the printer and the number of copies. You can't change the other settings, because the page order is not known. Push the :btn:`[Print]` button and the composition will be printed.  
    
Open in composer view
    The third option is to view the composition in composer view. This is very similar to the *Plot by template* function. Since it is an atlas composition, in the composer view you can look at each page separately. Use the arrows in the toolbar to move to the previous/next page. In the *Atlas generation* panel the settings of the atlas composition can be modified. From the composer view you can print either a single page or all pages or export them to a PDF file.  

    
.. figure:: images/u28.png
   :scale: 50 %
   :align: center
       
   *(Figure 28) Batch plotting - Open in composer view*

6 Localization
~~~~~~~~~~~~~~

The messages, the text labels of the dialog can be translated to your language.
You can use Qt Linguist program for translation. It is a free software, that 
you can download from here 
http://qt-apps.org/content/show.php/Qt+Linguist+Download?content=89360
The localized message files are stored in the *i18n* directory of the plugin.
The name of the file is the two character language code (e.g. en for English,
hu for Hungarian).
Files with .ts ans .qm extensions can be found there. The .ts files are the 
editable XML message files (edit it with Qt Linguist). The .qm files are binary
files used by QGIS.

The plugin will use the language set in QGIS or the English messages if the
language in not available for the plugin. You cannot change the language in the plugin, only in QGIS. The QGIS language can be changed from the menu 
:mnu:`Settings/Options`, select the *Locale* tab.

6.1 Add a new language to the plugin
::::::::::::::::::::::::::::::::::::

If you cannot find the message file of your language in the *i18n* directory,
then make a copy of the en.ts to a new file with a name of the new language 
code. For example for French use the following command in a Linux Bash
window (the actual directory have to be *i18n*)

::

    cp en.ts fr.ts

6.2 Translation
:::::::::::::::

Open the prepared new message file with Qt Linguist (Figure 29).
Select a group of messages from the left side list, Click on a message in the 
right side window and write your translation in the translation field.
If you finished the translation of the message click on the checkmark button 
in the toolbar. For further details read the Qt Linguist documentation
(http://doc.qt.io/qt-4.8/linguist-manual.html).

.. figure:: images/qt_linguist.png
   :scale: 50 %
   :align: center
       
   *(Figure 29) Translation in Qt Linguist* 

The .ts file have to be translated into a .qm file before you can test it in
QGIS. Use the :mnu:`File/Release` menu from the Qt Linguist or use the 
*lrelease* Qt command line utility.

::

    lrelease fr.ts
