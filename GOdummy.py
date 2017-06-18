import time
from datetime import datetime, timedelta
from globusonline.transfer.api_client import Transfer
from globusonline.transfer.api_client.goauth import get_access_token
from globusonline.transfer import api_client

# Jorge D. Morales 06/18/2017
# This package allows to set up globus transfers in a python script or notebook
# this is just a simplified wrapper
#
# Obviously, you need the globus online API, for a quick guide see: 
#    https://github.com/georgemm01/GOdummy
#
# For the globus api code you can just do: 
#     pip install globusonline-transfer-api-client
# see the code and guide here: 
#    https://github.com/globusonline/transfer-api-client-python
#
# 
# Most of these functions, as they are part of the globus online transfer api tutorial,
# are under:
#      Copyright 2010 University of Chicago
# Licensed under the Apache License, Version 2.0 (the "License");
#
# And this GOdummy wrapper so is: 
#      Copyright 2017 Jorge D. Morales
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



####################################################################
#########   Useful functions from the GO tutorial:
def display_activation(endpoint_name):
    print "=== Endpoint pre-activation ==="
    display_endpoint(endpoint_name)
    print
    code, reason, result = api.endpoint_autoactivate(endpoint_name,
                                                     if_expires_in=600)
    if result["code"].startswith("AutoActivationFailed"):
        print "Auto activation failed, ls and transfers will likely fail!"
    print "result: %s (%s)" % (result["code"], result["message"])
    print "=== Endpoint post-activation ==="
    display_endpoint(endpoint_name)
    print


def display_task_list(max_age=None):
    """
    @param max_age: only show tasks requested at or after now - max_age.
    @type max_age: timedelta
    """
    kwargs = {}
    if max_age:
        min_request_time = datetime.utcnow() - max_age
        # filter on request_time starting at min_request_time, with no
        # upper limit on request_time.
        kwargs["request_time"] = "%s," % min_request_time

    code, reason, task_list = api.task_list(**kwargs)
    print "task_list for %s:" % api.username
    for task in task_list["DATA"]:
        print "Task %s:" % task["task_id"]
        _print_task(task)


def _print_task(data, indent_level=0):
    indent = " " * indent_level
    indent += " " * 2
    for k, v in data.iteritems():
        if k in ("DATA_TYPE", "LINKS"):
            continue
        print indent + "%s: %s" % (k, v)


def display_task(task_id, show_successful_transfers=True):
    code, reason, data = api.task(task_id)
    print "Task %s:" % task_id
    _print_task(data, 0)

    if show_successful_transfers:
        code, reason, data = api.task_successful_transfers(task_id)
        transfer_list = data["DATA"]
        print "Successful Transfers (src -> dst)"
        for t in transfer_list:
            print " %s -> %s" % (t[u'source_path'],
                                 t[u'destination_path'])


def wait_for_task(task_id, timeout=120, poll_interval=30):
    """
    Wait for a task to complete within @timeout seconds, polling
    every @poll_interval seconds. If the task completed in the timeout,
    return the status ("SUCCEEDED" or "FAILED"). If it did not complete,
    returns None. Caller is responsible for cancelling incomplete task
    as appropriate.
    """
    assert timeout % poll_interval == 0, \
        "timeout must be multiple of poll_interval"
    timeout_left = timeout
    while timeout_left >= 0:
        code, reason, data = api.task(task_id, fields="status")
        status = data["status"]
        if status in ("SUCCEEDED", "FAILED"):
            return status
        if timeout_left > 0:
            time.sleep(poll_interval)
        timeout_left -= poll_interval

    return None


def display_endpoint_list():
    code, reason, endpoint_list = api.endpoint_list(limit=100)
    print "Found %d endpoints for user %s:" \
          % (endpoint_list["length"], api.username)
    for ep in endpoint_list["DATA"]:
        _print_endpoint(ep)


def display_endpoint(endpoint_name):
    code, reason, data = api.endpoint(endpoint_name)
    _print_endpoint(data)


def _print_endpoint(ep):
    name = ep["canonical_name"]
    print name
    if ep["activated"]:
        print "  activated (expires: %s)" % ep["expire_time"]
    else:
        print "  not activated"
    if ep["public"]:
        print "  public"
    else:
        print "  not public"
    if ep["myproxy_server"]:
        print "  default myproxy server: %s" % ep["myproxy_server"]
    else:
        print "  no default myproxy server"
    servers = ep.get("DATA", ())
    print "  servers:"
    for s in servers:
        uri = s["uri"]
        if not uri:
            uri = "GC endpoint, no uri available"
        print "    " + uri,
        if s["subject"]:
            print " (%s)" % s["subject"]
        else:
            print


def display_ls(endpoint_name, path=""):
    code, reason, data = api.endpoint_ls(endpoint_name, path)
    # The "path" field contains the canonical path from the GridFTP server. For
    # aboslute paths this will be the same as the requested path, but in some
    # cases it will be mapped. Also an empty path can be passed
    # and will be mapped to the user's default directory (typically
    # their home directory) by the Transfer API.
    path = data["path"]
    print "Contents of %s on %s:" % (path, endpoint_name)
    headers = "name, type, permissions, size, user, group, last_modified"
    headers_list = headers.split(", ")
    print headers
    for file_or_dir in data["DATA"]:
        print ", ".join([unicode(file_or_dir[field])
                         for field in headers_list])
    
    
#########   End of GO tutorial functions
####################################################################


## Class for your GO credential
class GOcredential:
    def __init__(self, username=None, success=False, goauth=None, ca_cert=None, keyfile=None, certfile=None):
        self.username=username
        self.success=success
        self.goauth=goauth
        self.ca_cert=ca_cert
        self.key=keyfile
        self.cert=certfile
               
        
## Now the relevant functions for transfers

# initialize credential
def GOinit(username, ca_cert=None, quiet=True):
    global api
    credential=GOcredential(username=username, ca_cert=ca_cert)
    try:
        if ca_cert:
            result=get_access_token(username=credential.username, ca_certs=credential.ca_cert)
        else:
            result=get_access_token(username=credential.username)
        credential.goauth=result.token
        credential.sucess=True
    except:
        print "GO autnetication failed!"
    
    if credential.success: print "GO authentication successful"
    
    api = api_client.TransferAPIClient(username=credential.username, goauth=credential.goauth)

    if not quiet: display_task_list()
  
    return credential 
        
# Autoactivate Endpoints
def GOendpoints(epoint1,epoint2):
    display_activation(epoint1)
    display_activation(epoint2)
    
# Now prepare a transfer
def GOpreTransfer(epoint1,epoint2,timeout=10):
    code, message, data = api.transfer_submission_id()
    submission_id = data["value"]
    deadline = datetime.utcnow() + timedelta(minutes=timeout)
    gotransf = Transfer(submission_id, epoint1, epoint2, deadline)
    return gotransf
#the user should 'add items' by doing:  gotransf.add_item("srcfile","destfile")
    
def GOTransfer( gotransf , quiet=True):
    code, reason, data = api.transfer(gotransf)
    task_id = data["task_id"]

    if not quiet: 
        # see the new transfer show up
        print "=== Transfer Submitted ==="
        display_task(task_id, False); print

    status = wait_for_task(task_id)

    if status is None:
        # Task didn't complete before the timeout.
        # Since the example transfers a single small file and the
        # timeout is 2 mintues, this shouldn't happen unless one of the
        # endpoints is having problems or the user already has a bunch
        # of other active tasks (there is a limit to the
        # number of concurrent active tasks a user can have).
        print "WARNING: task did not complete before timeout! ",
        print gotransf.deadline
    else:
        print "Task %s complete with status %s" % (task_id, status)
        if not quiet:
            print "=== After completion ==="
            display_task(task_id); print
            
