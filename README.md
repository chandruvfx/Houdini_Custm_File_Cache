# Houdini Custom File Cache HDA

![filecache1](https://github.com/chandruvfx/Houdini_Custom_File_Cache/assets/45536998/5874d1fd-8879-4df0-acaf-7cccdb52eaa4)

## Demo Video 

:point_down: [Youtube Link]
 
[![Houdini Dependency Cache Submitter](https://img.youtube.com/vi/SPw6o7h5O-M/0.jpg)](https://youtu.be/SPw6o7h5O-M)

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

### Cache Folder Path

![filecache7](https://github.com/chandruvfx/Houdini_Custom_File_Cache/assets/45536998/07824aff-a202-4dcd-bc49-35039d4bbc36)

 The file path field automatically resolve sgtk template path 'houdini_file_cache' of the respective project. Users were allowed to break this if they want to enter own folder path. Note: Make sure the given path is the folder path not a file path

### Cache Name

![cachename](https://github.com/chandruvfx/Houdini_Custom_File_Cache/assets/45536998/3a7c38de-f578-49e7-bd42-52998326210f)

 In Default the cache name is the node name. Users allowed enter a valid custom name based upon the need. The Dropdown in the right-side corner automatically loads up all the available caches. User can select and change the cache, it dynamically updates the fields like comments text box by pulling respective cache comment text file and move the version slider to the latest available version, so on…

### Version & Format

![filecache_version_formatype](https://github.com/chandruvfx/Houdini_Custom_File_Cache/assets/45536998/f205cef5-1d11-43b9-8310-100d733a1dc4)

 The version slider works in dual mode, both in writing and reading. Scripted controlled to work dynamically!!

During writing, artist can slide the version field to the latest number. If suppose the user moved version number is breached the maximum number of available version of specified cache , then it automatically fall backed to a available version maximum number
During reading, Aka, if load_from_disk is enabled then moving the version slider dynamically pull the comments of the respective version cache and also update in the houdini viewport
FA File cache now supports bgeo, abc formates. This can be extended!!

### Version Utility Buttons

![filecache_version_buttons](https://github.com/chandruvfx/Houdini_Custom_File_Cache/assets/45536998/e8b08cd0-3f29-4c5c-94e5-538fe09a117b)

 A minuscule util buttons to perform versioning operations.

### Display & Cache

![filecache_cache](https://github.com/chandruvfx/Houdini_Custom_File_Cache/assets/45536998/9ff228cc-695b-4e82-a459-6e9ebe4d5037)

 LOD display utilities mirrored here from the houdini classic file cache system  Render frame range specifications

### Comments

![filecache_comments](https://github.com/chandruvfx/Houdini_Custom_File_Cache/assets/45536998/7cb19331-3fcc-4f1a-a8bd-a647b7af9540)

 A multi-line comment text field act like a dual purpose widget, both of reading and writing

On Writing, artist can include comments. It included with the respective version of the cache file format
On reading aka enabling 'load_on_disk', It pull the appropriate version comments of the cache format and update the text box, While the artist slide the version slider or version utility buttons.

### Local Submission

![filecache_localsubmission](https://github.com/chandruvfx/Houdini_Custom_File_Cache/assets/45536998/a84dea90-b234-4576-9a4e-c4c7b1824c40)

 Mirrored houdini native local file caching options.

### Deadline Submission

![filecache_deadline](https://github.com/chandruvfx/Houdini_Custom_File_Cache/assets/45536998/50b17643-4cc8-4146-b2e0-c3e6a44e3f68)

The Tab Contains all the necessary fields to shoot up the deadline job. Bgeo and abc(alembic) caches happen in the farm. For now, the alembic(abc) caches were limited to happen in only one machine in the farm, cause all the frames were gonna dumped into a single file..

- Job Name - Deadline job name. Default it is the cachename plus version name. Artist can enter his own prefered name
- Comment - Valid textual deadline comments
- Pool & Secondary pool - Drop-Down consist of deadline pools.
- Group - Deadline Groups
- Priority - Determine Deadline Priority
- Frames-Per-Task - Determine Chunk size aka the split of frame ranges into the machines
- Submit To Deadline - Push button collects all the deadline parameters values and submit into the deadline farm
- 
If the job is submitted sucessfully then the below message with deadline job id appears!!

![filecache_jobid](https://github.com/chandruvfx/Houdini_Custom_File_Cache/assets/45536998/c2050343-267a-4ede-95d3-10882e9274f8)
