# Houdini Custom File Cache HDA

![filecache1](https://github.com/chandruvfx/Houdini_Custom_File_Cache/assets/45536998/5874d1fd-8879-4df0-acaf-7cccdb52eaa4)

## Overview

FA file caching HDA is a sop context multipurpose custom file caching in-house tool. These custom single HDA tools is a dual purpose and advanced version of the native houdini file caching tool. Which comprises few native file cache functionalities likewise loading, saving and also extended to includes below listed features.

- Self resolving sgtk template paths for saving
- Automatic versioning up, supporting multiple formats
- Steer to various caches at one time
- Chain of user action selections, reflects into the controllers of the hda
- Support deadline farm submission

## HDA Properties
### Load From Disk
 The Check Box make the HDA a dual purpose tool. If it is switched on it loads the cache from the given cache folder path and cache name.

Cache Folder Path
 The file path field automatically resolve sgtk template path 'houdini_file_cache' of the respective project. Users were allowed to break this if they want to enter own folder path. Note: Make sure the given path is the folder path not a file path

Cache Name
 In Default the cache name is the node name. Users allowed enter a valid custom name based upon the need. The Dropdown in the right-side corner automatically loads up all the available caches. User can select and change the cache, it dynamically updates the fields like comments text box by pulling respective cache comment text file and move the version slider to the latest available version, so on…

Version & Format
 The version slider works in dual mode, both in writing and reading. Scripted controlled to work dynamically!!

During writing, artist can slide the version field to the latest number. If suppose the user moved version number is breached the maximum number of available version of specified cache , then it automatically fall backed to a available version maximum number
During reading, Aka, if load_from_disk is enabled then moving the version slider dynamically pull the comments of the respective version cache and also update in the houdini viewport
FA File cache now supports bgeo, abc formates. This can be extended!!

Version Utility Buttons
 A minuscule util buttons to perform versioning operations.

Display & Cache
 LOD display utilities mirrored here from the houdini classic file cache system  Render frame range specifications

Comments
 A multi-line comment text field act like a dual purpose widget, both of reading and writing

On Writing, artist can include comments. It included with the respective version of the cache file format
On reading aka enabling 'load_on_disk', It pull the appropriate version comments of the cache format and update the text box, While the artist slide the version slider or version utility buttons.
Local Submission
 Mirrored houdini native local file caching options.
:point_down: [Youtube Link]
 
[![Houdini Dependency Cache Submitter](https://img.youtube.com/vi/SPw6o7h5O-M/0.jpg)](https://youtu.be/SPw6o7h5O-M)
