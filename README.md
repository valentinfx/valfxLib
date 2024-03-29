# valfxLib
A personal Houdini package containing mostly HDAs and shelf tools, feel free to steal what you like!

## Installation
- Create a folder named **packages** in your Houdini preferences.
- Copy **valfxLib.json** to the **packages** folder.
- Edit the json file so the **VALFX_LIB** variable points to the **valfxLib** folder, which can be placed wherever you choose.

## HDAs

### OBJ

* **hudInfo** : Displays context info (scene name, frame range, user name... etc) in specified camera that can be flipbooked and rendered

### SOP

* **arnoldPref** : Creates a Pref attribute for shading work with Arnold
* **colorFromVelocity** : Adds ramp color to points based on a velocity attribute
* **fastMovingPyroSource** : Creates a burn/temperature pyro source from fast moving surface geometry
* **insideUvs** : Deploys uv for fractured geometry inside faces based on a name attribute
* **mayaHoudiniScale** : Scales geometries, VDB grids and particle attributes for import and export from Houdini to other DCCs
* **raise** : Raises pieces with a piece attribute or particles with a pscale attribute to ground level
* **uuidAssign** : Assigns a unique ID (uuid) to primitives 
* **vdbFromAnimatedCam** : Generates a single VDB from the frustrums of camera animated over time
* **vdbNormalize** : Normalizes a VDB or volume grid from any values to a 0 to 1 range

### DOP

* **stopRollingPieces** : Helps with stopping rolling pieces in bullet simulations

