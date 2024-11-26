# Map Debugging Prompt

## Current Issue
The map in DisasterConnect has a location selection issue where clicking on the map causes unwanted zooming instead of properly selecting the location.

## Project Context
- Application: DisasterConnect (Disaster Management System)
- Component: Location Selection Feature
- Files Involved:
  - `src/utils/map_client.py`
  - `src/utils/location_picker.py`
  - `src/incidents/incidents_widget.py`
  - `src/resources/resources_widget.py`

## Technical Details
- Framework: PyQt5
- Map Library: Leaflet.js
- Communication: QWebChannel (JavaScript ↔ Python)
- Map Provider: OpenStreetMap

## Specific Requirements
1. Fix map click behavior:
   - Prevent zooming when clicking to select a location
   - Maintain proper marker placement
   - Ensure coordinates are captured correctly

2. Debug the JavaScript-Python communication:
   - Verify QWebChannel initialization
   - Check event propagation
   - Validate location data transfer

3. Test the following scenarios:
   - Single click location selection
   - Double click behavior
   - Marker placement accuracy
   - Coordinate display updates

## Additional Context
- The location picker is used in both incident and resource forms
- The map should be in selection mode when opened from the location picker
- Coordinates should be displayed in the input fields above the map
- A green marker should indicate the selected location

## Expected Behavior
1. Click "Pick Location" button in form
2. Map opens in location picker dialog
3. Single click on map:
   - Places green marker
   - Updates coordinate displays
   - Does NOT zoom the map
4. Confirm button becomes enabled after selection
5. Selected coordinates are returned to the main form

## Current Behavior
- Map zooms in when clicked instead of just selecting location
- Marker placement may be inconsistent
- Possible issues with event handling

## Relevant Code Sections to Examine
1. Map click event handler in map_client.py
2. QWebChannel initialization
3. Event propagation in Leaflet.js
4. Location picker dialog implementation

## Previous Attempts
Document any previous attempts to fix the issue and why they didn't work completely.
