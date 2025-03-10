import os
import json
from pylti1p3.tool_config.dict import ToolConfDict
from pylti1p3.tool_config.json_file import ToolConfJsonFile


def is_lti_enabled():
    return (
        os.environ.get("LTI_CONF_JSON")
        and os.environ.get("LTI_CONF_JSON_PRIVATE_KEYS")
        or os.environ.get("LTI_CONF_FOLDER")
        and os.environ.get("LTI_CONF_FILE_NAME")
    )


def get_tool_conf():
    if not is_lti_enabled():
        return None

    tool_conf = None

    lti_conf_json = os.environ.get("LTI_CONF_JSON")
    lti_conf_json_private_keys = os.environ.get("LTI_CONF_JSON_PRIVATE_KEYS")

    lti_conf_folder = os.environ.get("LTI_CONF_FOLDER")
    lti_conf_file_name = os.environ.get("LTI_CONF_FILE_NAME")

    if lti_conf_json is not None and lti_conf_json_private_keys is not None:
        conf_dict = json.loads(lti_conf_json)
        keys_dict = json.loads(lti_conf_json_private_keys)
        tool_conf = ToolConfDict(conf_dict)

        for issuer, private_key in keys_dict.items():
            tool_conf.set_private_key(issuer, private_key)

    elif lti_conf_folder is not None and lti_conf_file_name is not None:
        conf_file_location = os.path.join(lti_conf_folder, lti_conf_file_name)
        tool_conf = ToolConfJsonFile(conf_file_location)

    return tool_conf
