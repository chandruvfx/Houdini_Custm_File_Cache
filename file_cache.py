# A custom file cache HDA having extended features including automatically version's up to a latest version
# support switching to different formats, allows to incorporating user comments and facilatates to
# submit the file caching to the deadline submitter.
#
# The HDA Work as two-in-one purpose. Supportd both of file caching and loading. 
# Writing(Local or Renderfarm submission):
#
# The fae file cache dump all the bgeo/abc cache versions into the user specified directory with a user comments file.
# Artist interactively navigate to any versions of the formate overwrite the comments or even the 
# exciting cache. If a user entered overflowed version number as latest version, 
# then HDA automatically rollbacked to the available latest version. 
#
# Loading:
#
# Utility Push buttons provide good control for artist to jump into versions. It interactively updates
# the comment section and current viewport respectively.
#
#
import os
import re
import hou
import sys
import subprocess


def version_up(cur_node: hou.Node) -> None:

    """ Increment one version up and pull the comments if exist any """
    
    current_version = cur_node.parm("version").eval()
    cur_node.parm("version").set(current_version+1)
    manip_comment_file(cur_node, w_verbose = False)

    
def version_down(cur_node: hou.Node) -> None:

     """ Decrement one version down and pull the comments if exist any """
    
    current_version = cur_node.parm("version").eval()
    cur_node.parm("version").set(current_version-1)
    manip_comment_file(cur_node, w_verbose = False)

def load_cache(cur_node: hou.Node) -> None:

    """Move The user loaded cache to latest version

    User selected cache from the drop down menu name updated
    into the cache_name parameter and the version is moved to the 
    latest number.
    """
    
    sel_cache_name = cur_node.parm("suggested_cache_name").evalAsString()
    cur_node.parm("cache_name").set(sel_cache_name)
    move_latest_version(cur_node)

def save_disk(cur_node: hou.Node, bg = False) -> None:

    """ Saving Cache in to Disk 

    Collect user entered formate type and version. check the version is 
    next recent available version. Example: if version 4 bgeo.sc is latest cache for 
    man1 charecter, then it move the version to 5. 
    Create the respective ROP nodes if it matches for bgeo or alembic, 
    Write comments and cache from the machine
    
    Args:
        bg (bool): If set false it switched to a background process mode
        else it do as normal
    """
        
    cache_folder_path = cur_node.parm("cache_folder_path").evalAsString().replace(os.sep, "/")
    formate_type = cur_node.parm("formate_type").rawValue()
    user_ver = cur_node.parm("version").eval()
    version_parm_manipulation(cur_node, formate_type, user_ver)
    job_name = cur_node.parm("dl_job_name").evalAsString()
    
    formate_type = cur_node.parm("formate_type").rawValue()
    manip_comment_file(cur_node, w_verbose = True)
    
    
    cache_node, _ = create_sop_cache(cur_node, cache_folder_path, job_name, formate_type)
    
    if not bg:
        cache_node.parm('execute').pressButton()
    else:
        cache_node.parm('executebackground').pressButton()
    
    
        
def move_latest_version(cur_node: hou.Node, 
                    abc_val_return = False,
                    bgeo_val_return = False) -> str, str, None:
    """Move Version Silder to latest version of the cache

    Traverse to cache folder and retrive files and determine the 
    maximum number of the cache file. also retrive the the comments 
    of the respective version of the cache file.
    """
    
    bgeo_cached_disk_versions = []
    abc_cached_disk_versions = []
    bgeo_version_no = 0
    abc_version_no = 0
    bge_ext = ''
    abc_ext = ''
    
    cache_folder_path = cur_node.parm("cache_folder_path").evalAsString()
    formate_type = cur_node.parm("formate_type").rawValue()
    cache_name = cur_node.parm("cache_name").eval()
   
    for folders in os.listdir(cache_folder_path):
        cache_folder_paths = os.path.join(cache_folder_path, folders)
        if os.path.isdir(cache_folder_paths):
            for file_path in os.listdir(cache_folder_paths):
            
                get_cache_name = re.split('v\d+', file_path)[0][:-1]

                if file_path.endswith('bgeo.sc') and get_cache_name == cache_name: 
                    bge_ext = '.bgeo.sc'
                    bgeo_version_no = int(re.findall('v\d+', file_path)[0].split('v')[-1])
                    bgeo_cached_disk_versions.append(bgeo_version_no)
                    
                elif file_path.endswith('abc') and get_cache_name == cache_name:
                    abc_ext = '.abc'
                    abc_version_no = int(re.findall('v\d+', file_path)[0].split('v')[-1])
                    abc_cached_disk_versions.append(abc_version_no)
    

    if bgeo_cached_disk_versions and formate_type == bge_ext and not bgeo_val_return and not abc_val_return:
        cur_node.parm("version").set(max(bgeo_cached_disk_versions)) 
        manip_comment_file(cur_node, w_verbose = False)

            
    elif abc_cached_disk_versions and formate_type == abc_ext and not abc_val_return and not bgeo_val_return:
        cur_node.parm("version").set(max(abc_cached_disk_versions))
        manip_comment_file(cur_node, w_verbose = False)
        
    elif bgeo_val_return:
        if bgeo_cached_disk_versions:
            # Returns the maximum number of the cached version
            return cache_name, bge_ext, max(bgeo_cached_disk_versions)
        else:
            # Return zero if no cached version found
            return cache_name, bge_ext, 0

    elif abc_val_return:
        if abc_cached_disk_versions:
            return cache_name, abc_ext, max(abc_cached_disk_versions)
        else:
            return cache_name, abc_ext, 0

        
def save_file():
    
    if hou.hipFile.isNewFile():
        hou.ui.displayMessage( "Please Save the File through Shotgrid before submitting the job", buttons=( "Ok", ), title="Submit Houdini To Deadline" )
        return False
    elif hou.hipFile.hasUnsavedChanges():
        hou.hipFile.save()
        return True

def trigger_parms(cur_node):

    auto_change_abc_chunksize(cur_node)
    move_latest_version(cur_node)        
    manip_comment_file(cur_node, w_verbose = False)
    pass
 
def auto_change_abc_chunksize(cur_node: hou.Node) -> None:
    
    if cur_node.parm("formate_type").rawValue() == ".abc":
        cur_node.parm('dl_chunksize').setExpression('ch("sei2")')
    else:
        cur_node.parm('dl_chunksize').deleteAllKeyframes()
        cur_node.parm('dl_chunksize').set(10)
        
def create_sop_cache(cur_node, cache_folder_path, job_name, formate_type):
    
    obj_geo_node_name = cur_node.parent().name()
    frame_range_type = cur_node.parm("trange").rawValue()
    
    
    def set_frame_range_params(cache_node):
    
        if frame_range_type == 'frame_range':
            cache_node.parm('trange').set(1)
            cache_node.parm('f1').setExpression('ch("/obj/%s/%s/sei1")' %(obj_geo_node_name, cur_node.name()))
            cache_node.parm('f2').setExpression('ch("/obj/%s/%s/sei2")' %(obj_geo_node_name, cur_node.name()))
            cache_node.parm('f3').setExpression('ch("/obj/%s/%s/sei3")' %(obj_geo_node_name, cur_node.name()))
            
        elif frame_range_type == 'single_range' and not cur_node.parm('useframeoverride').eval():
        
            cache_node.parm('trange').set(0)
        
        elif frame_range_type == 'single_frame' and cur_node.parm('useframeoverride').eval():
        
            cache_node.parm('trange').set(1)
            cache_node.parm('f1').setExpression('ch("/obj/%s/%s/frameoverride")' %(obj_geo_node_name, cur_node.name()))
            cache_node.parm('f2').setExpression('ch("/obj/%s/%s/frameoverride")' %(obj_geo_node_name, cur_node.name()))
            cache_node.parm('f3').set(1)
    
    
    if formate_type == '.bgeo.sc':
    
        bgeo_cache_nodes = []
        full_path = cache_folder_path + "/" + job_name + "/" + job_name + ".$F4" + str(formate_type)
        
        for outputnodes in cur_node.outputConnections():
            if "bgeo_cache_node" in outputnodes.outputNode().userDataDict():
                bgeo_cache_nodes.append(outputnodes.outputNode())
                
        if not bgeo_cache_nodes:
            bgeo_cache_node = hou.node('/obj/%s' %obj_geo_node_name).createNode("rop_geometry")
            bgeo_cache_node.setUserData("bgeo_cache_node", "1")
            bgeo_cache_node.parm('sopoutput').set(full_path)
            bgeo_cache_node.setInput(0, cur_node)
        else:
            bgeo_cache_node = bgeo_cache_nodes[0]
            bgeo_cache_node.parm('sopoutput').set(full_path)
            
        set_frame_range_params(bgeo_cache_node)
        return bgeo_cache_node, full_path
        
            
    elif formate_type == '.abc': 
        
        abc_cache_nodes = []
        full_path = cache_folder_path + "/" + job_name + "/" + job_name +  str(formate_type)
        
        for outputnodes in cur_node.outputConnections():
            if "abc_cache_node" in outputnodes.outputNode().userDataDict():
                abc_cache_nodes.append(outputnodes.outputNode())
        
        if not abc_cache_nodes:
            abc_cache_node = hou.node('/obj/%s' %obj_geo_node_name).createNode("rop_alembic")
            abc_cache_node.setUserData("abc_cache_node", "1")
            abc_cache_node.parm('filename').set(full_path)
            abc_cache_node.setInput(0, cur_node)
        else:
            abc_cache_node = abc_cache_nodes[0]
            abc_cache_node.parm('filename').set(full_path)
            
        set_frame_range_params(abc_cache_node)
        return abc_cache_node, full_path
        
    
def manip_comment_file(cur_node: hou.Node, w_verbose = False) -> None:   
    
    comments = cur_node.parm("comments").evalAsString()
    cache_folder_path = cur_node.parm("cache_folder_path").evalAsString().replace(os.sep, "/")
    cache_folder_name = cur_node.parm("dl_job_name").evalAsString()
    get_formate_type = cur_node.parm("formate_type").rawValue().split(".")[-1]+ ".txt"
    comment_file_name= f"{cache_folder_name}_{get_formate_type}"
    cache_path = os.path.join(cache_folder_path, cache_folder_name, comment_file_name)
    
    if not cur_node.parm("load_from_disk").eval() and w_verbose:
        if not os.path.exists(os.path.dirname(cache_path)):
            try:
                os.makedirs(os.path.dirname(cache_path))
            except (OSError): 
                pass
        try:
            with open(cache_path, "w") as write_comment_file:
               write_comment_file.writelines(comments)
        except FileNotFoundError:
            pass
    
    elif cur_node.parm("load_from_disk").eval() and not w_verbose:
        try:
            with open(cache_path, "r") as read_comment_file:
                read_comment = read_comment_file.read()
                cur_node.parm("comments").set(read_comment)
        except FileNotFoundError:
                pass
   
def version_parm_manipulation(cur_node: hou.Node, formate_type, user_ver):

    if formate_type == ".bgeo.sc":
        bgeo_max_infos = move_latest_version(cur_node, bgeo_val_return = True)
        # print(bgeo_max_infos)
        if bgeo_max_infos and bgeo_max_infos[-1] != 0:
            bgeo_max_ver = bgeo_max_infos[-1]
            if (bgeo_max_ver + 1) < user_ver:
                hou.ui.displayMessage("Bgeo Version Overflow. Fall Back to Available!", buttons=('Okay',))
                cur_node.parm("version").set(bgeo_max_ver+1) 
        else:
            cur_node.parm("version").set(1)
                
    elif formate_type == ".abc":
        abc_max_infos = move_latest_version(cur_node, abc_val_return = True)
        # print("abc", abc_max_infos)
        if abc_max_infos and abc_max_infos[-1] != 0: 
            abc_max_ver = abc_max_infos[-1]
            if (abc_max_ver + 1) < user_ver:
                hou.ui.displayMessage("Alembic Version Overflow. Fall Back to Available!", buttons=('Okay',))
                cur_node.parm("version").set(abc_max_ver+1)
        else:
            cur_node.parm("version").set(1)

    
def SubmitToDeadline(cur_node: hou.Node,
                     display_ui=False) -> None:

    cache_folder_path = cur_node.parm("cache_folder_path").evalAsString().replace(os.sep, "/")
    formate_type = cur_node.parm("formate_type").rawValue()
    user_ver = cur_node.parm("version").eval()
    cache_name = cur_node.parm("cache_name").eval()
    proceed = False
    
    if not cache_folder_path or not cache_name:
        hou.ui.displayMessage( "Please Fill Valid Cache Folder Path or Cache Name", 
                            buttons=( "Ok", ), 
                            title="FAE message" )
        proceed = False
    
    else: 
        proceed = True
        version_parm_manipulation(cur_node, formate_type, user_ver)
        

    job_name = cur_node.parm("dl_job_name").evalAsString()
    comment = cur_node.parm("dl_comment").evalAsString()
    pool = cur_node.parm("dl_pool").evalAsString()
    sec_pool = cur_node.parm("dl_secondary_pool").evalAsString()
    group = cur_node.parm("dl_group").evalAsString()
    priority = cur_node.parm("dl_priority").eval()
    chunksize = cur_node.parm("dl_chunksize").eval()
    
    start_frame =  int(cur_node.parm("sei1").eval())
    end_frame =  int(cur_node.parm("sei2").eval())
    steps =  int(cur_node.parm("sei3").eval())
    
    cache_node, full_path = create_sop_cache(cur_node, cache_folder_path, job_name, formate_type)
    
    OutputFilename_0 = ''
    if cache_node.type().name() == 'rop_geometry':
    
        OutputFilename_0 = "%s_####_%s" %(job_name, formate_type)
        
    elif cache_node.type().name() == 'rop_alembic':
    
        OutputFilename_0 = "%s%s" %(job_name, formate_type)
        
    
    deadline_files = []    
    
    def write_job_file(filename, data):
        
        dl_job_dir =  "Y:/pipeline/studio/temp/" + \
                      hou.userName() + \
                      "/houdini/deadline_job_files"
        dir_exist = os.path.exists(dl_job_dir)
        if not dir_exist:
            os.makedirs(dl_job_dir)
        
        job_file = os.path.join(dl_job_dir, filename)
            
        with open(job_file, "w") as write_file:
            for key, value in data.items():
                write_file.write(key +"=" + value + "\n") 
        deadline_files.append(job_file)
        return job_file
   
    def file_job_info():
    
        dl_job_info = {
            "BatchName": hou.hipFile.basename(),
            "Name": job_name + "_" + formate_type.split(".",1)[-1],
            "Comment" : comment,
            "ChunkSize" : str(chunksize),
            "Frames" : "%s-%severy%s" %(str(start_frame), str(end_frame), str(steps)),
            "Plugin" :"Houdini",
            "Pool": "houdini",
            "OutputDirectory0": cache_folder_path + "/" + job_name,
            "OutputFilename0" : OutputFilename_0,
            "EnvironmentKeyValue0" : "PYTHONPATH=Y:/pipeline/apps/houdini/19.5.534/deadline"
        }
        job_info_file = write_job_file("job_info_%s_%s.job" 
                                        %(cur_node.parent().name(), cur_node.name()), dl_job_info)
        return job_info_file
        
    def plugin_job_info():
    
        dl_plugin_job_info = {
            "Output": full_path,
            "OutputDriver": "%s" %cache_node.path(),
            "SceneFile" : hou.hipFile.path(),
            "Version" : "19.5",
            "CurrentNodeName": cur_node.path()
        }
        plugin_info_file = write_job_file("plugin_info_%s_%s.job" 
                                            %(cur_node.parent().name(), cur_node.name()), dl_plugin_job_info)
        return plugin_info_file
    
    if cur_node.parm("load_from_disk").eval():
        hou.ui.displayMessage("Switch Off 'Load_From_Disk' to proceed submission",
                              buttons=('OK',), 
                              severity=hou.severityType.Message,
                              title="FAE_Message")
        
        
    
    elif save_file() and not cur_node.parm("load_from_disk").eval() and proceed:  
    
        manip_comment_file(cur_node, w_verbose = True)
        job_file =file_job_info()
        plugin_file= plugin_job_info()
        
        if display_ui:
            dl_path = os.environ['DEADLINE_PATH'] 
            dl_path = dl_path.replace(r"/", "//") + "//deadlinecommand.exe"
            dl_path = '"%s"' %dl_path
            dl_command = '%s %s' %(dl_path, " ".join(deadline_files))
            result = subprocess.run(dl_command, 
                                    stdout=subprocess.PIPE, 
                                    shell=True,
                                    text=True)
            job_id = [id for id in result.stdout.split() if 'JobID' in id]
            
            
            hou.ui.displayMessage("Deadline \n\n%s\n\n Submitted" %job_id[0],
                                  buttons=('OK',), 
                                  severity=hou.severityType.Message,
                                  title="FAE_Message")
        else:
            return [job_file,
                    plugin_file]

        
