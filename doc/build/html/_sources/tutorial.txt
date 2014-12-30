========================================
SurveyingCalculation plugin for QGIS 2.x
========================================
Tutorial
--------

Enable SurveyingCalculation plugin in QGIS
::::::::::::::::::::::::::::::::::::::::::

Befor use the installed SurveyingCalculation plugin has to be enabled in QGIS. The installation method of the plugin can be found in the Users's Guide.

.. figure:: images/t001.png
   :scale: 80 %
   :align: center

   *(1.) From the Plugins menu select Manage and Install Plugins...*

.. figure:: images/t002.png
   :scale: 80 %
   :align: center

   *(2.) Search for SurveyingCalculation plugin and enable it*

Now the menu and the toolbar of the plugin are visible.

Start a new project
:::::::::::::::::::

.. figure:: images/t003.png
   :scale: 80 %
   :align: center

   *(3.) From the SurveyingCalculation menu select New coordinate list ...*

A new empty shape file is created.

.. figure:: images/t005.png
   :scale: 80 %
   :align: center

   *(4.) The attribute table of the coordinate file is empty*

Next step is impoting an electric fieldbook.

.. figure:: images/t006.png
   :scale: 80 %
   :align: center

   *(5.) From the SurveyingCalculation menu select Import fieldbook ...*

For the transparency of the fieldbooks the representation of NULL values can be changed.

.. figure:: images/t008.png
   :scale: 80 %
   :align: center

   *(6.) From the Settings menu select Options...*

.. figure:: images/t009.png
   :scale: 80 %
   :align: center

   *(7.) Select Data Sources, and set the Representation for NULL values from "NULL" to empty*

.. figure:: images/t010.png
   :scale: 80 %
   :align: center

   *(8.) The attribute table of the fieldbook*

.. figure:: images/t011.png
   :scale: 80 %
   :align: center

   *(9.) The attribute table of the coordinate file*

.. figure:: images/t0111.png
   :scale: 80 %
   :align: center

   *(10.) To display the points in the map window, right click on the coordinate file and select Zoom to Layer*

Points can be labeled with point id.

v

.. figure:: images/t055.png
   :scale: 80 %
   :align: center

   *(14.) QGIS project can be saved by clicking on the save icon*

Single Point Calculations
:::::::::::::::::::::::::

.. figure:: images/t012.png
   :scale: 80 %
   :align: center

   *(15.) Click Single point calculations icon on SurveyingCalculation toolbar*

.. figure:: images/t013.png
   :scale: 80 %
   :align: center

   *(16.) First select the type of calculation*

.. figure:: images/t014.png
   :scale: 80 %
   :align: center

   *(17.) By the orientation select the station point (the fielbook name and the row id in fieldbook is shown in brackets)*

.. figure:: images/t015.png
   :scale: 80 %
   :align: center

   *(18.) Select one or more target points and add to used points (the row id in fieldbook is shown in brackets)*

.. figure:: images/t016.png
   :scale: 80 %
   :align: center

   *(19.) Click Calculate and orientation will be calculated. Parameters of the calculation can be checked in the result window.*

.. figure:: images/t017.png
   :scale: 80 %
   :align: center

   *(20.) Click reset to begin a new calculation*

.. figure:: images/t018.png
   :scale: 80 %
   :align: center

   *(21.) Orientation for a second station*

.. figure:: images/t019.png
   :scale: 80 %
   :align: center

   *(22.) By the intersection two stations must be selected with known orientation (the fielbook name and the row id in fieldbook is shown in brackets)*

.. figure:: images/t020.png
   :scale: 80 %
   :align: center

   *(23.) Select one or more target points and add to used point, click calculate and coordinates will be calculated. Parameters of the calculation can be checked in the result window.*

.. figure:: images/t021.png
   :scale: 80 %
   :align: center

   *(24.) By the resection select station point (the fielbook name and the row id in fieldbook is shown in brackets, known point are displayed bold type )*

.. figure:: images/t022.png
   :scale: 80 %
   :align: center

   *(25.) Select exactly three target points (the row id in fieldbook is shown in brackets) and add to used points, click calculate and coordinates will be calculated. Parameters of the calculation can be checked in the result window.*

.. figure:: images/t023.png
   :scale: 80 %
   :align: center

   *(26.) By the free station select station point (the fielbook name and the row id in fieldbook is shown in brackets, known point are displayed bold type )*

.. figure:: images/t024.png
   :scale: 80 %
   :align: center

   *(27.) Select two or more target points (the row id in fieldbook is shown in brackets) and add to used points, click calculate and coordinates will be calculated. Parameters of the calculation can be checked in the result window.*

.. figure:: images/t026.png
   :scale: 80 %
   :align: center

   *(28.) By the radial survey select station point (the fielbook name and the row id in fieldbook is shown in brackets, only known points can be selected)*

.. figure:: images/t027.png
   :scale: 80 %
   :align: center

   *(29.) Select one or more target points (the row id in fieldbook is shown in brackets) and add to used points, click calculate and coordinates will be calculated. Parameters of the calculation can be checked in the result window.*

Traverse calculations
:::::::::::::::::::::

If orientation can be calculated on start point or end point, it should be calculated first.

.. figure:: images/t029.png
   :scale: 80 %
   :align: center

   *(30.) Orientation on start point*

.. figure:: images/t030.png
   :scale: 80 %
   :align: center

   *(31.) Orientation on end point*

.. figure:: images/t031.png
   :scale: 80 %
   :align: center

   *(32.) Click Traverse calculations icon on SurveyingCalculation toolbar*

.. figure:: images/t032.png
   :scale: 80 %
   :align: center

   *(33.) Select the type of traverse and the start point (the fielbook name and the row id in fieldbook is shown in brackets, only known points can be selected)*

.. figure:: images/t033.png
   :scale: 80 %
   :align: center

   *(34.) Select the end point (the fielbook name and the row id in fieldbook is shown in brackets, only known points can be selected except open traverse)*

.. figure:: images/t034.png
   :scale: 80 %
   :align: center

   *(35.) Select target points and add to used points in the right order (the fielbook name and the row id in fieldbook is shown in brackets, known point are displayed bold type)*

.. figure:: images/t035.png
   :scale: 80 %
   :align: center

   *(36.) Click calculate and coordinates will be calculated. Parameters of the calculation can be checked in the result window.*

Network adjustment
::::::::::::::::::

.. figure:: images/t051.png
   :scale: 80 %
   :align: center

   *(37.) Click Network adjustment icon on SurveyingCalculation toolbar*

.. figure:: images/t052.png
   :scale: 80 %
   :align: center

   *(38.) Select the fix points and add to the fix points*

.. figure:: images/t053.png
   :scale: 80 %
   :align: center

   *(39.) Select points to adjust and add to the adjusted points*

.. figure:: images/t054.png
   :scale: 80 %
   :align: center

   *(40.) Check the parameters of the adjustment. Click calculate and coordinates will be calculated. Parameters of the calculation can be checked in the result window.*

Coordinate transformation
:::::::::::::::::::::::::

First add the coordinate file containing the points to transformate.

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

.. figure:: images/t64.png
   :scale: 80 %
   :align: center

   *(44.) Click Coordinate transformation icon on SurveyingCalculation toolbar*

.. figure:: images/t65.png
   :scale: 80 %
   :align: center

   *(45.) Select the shape file where to transformate. The result points will be written in this shape file.*

.. figure:: images/t66.png
   :scale: 80 %
   :align: center

   *(46.) From the common points add the needed points to used points*

.. figure:: images/t67.png
   :scale: 80 %
   :align: center

   *(47.) Select the type of transformation (each type can be selected only if enough common points)*

.. figure:: images/t68.png
   :scale: 80 %
   :align: center

   *(48.) Click calculate and coordinates will be calculated. Parameters of the calculation can be checked in the result window.*


