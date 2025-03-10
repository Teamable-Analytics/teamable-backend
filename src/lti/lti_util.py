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
    if (
        os.environ.get("LTI_CONF_JSON") is not None
        and os.environ.get("LTI_CONF_JSON_PRIVATE_KEYS") is not None
    ):
        conf_dict = json.loads(os.environ.get("LTI_CONF_JSON"))
        keys_dict = json.loads(os.environ.get("LTI_CONF_JSON_PRIVATE_KEYS"))
        tool_conf = ToolConfDict(conf_dict)

        for issuer, private_key in keys_dict.items():
            tool_conf.set_private_key(issuer, private_key)

    elif (
        os.environ.get("LTI_CONF_FOLDER") is not None
        and os.environ.get("LTI_CONF_FILE_NAME") is not None
    ):
        conf_file_location = os.path.join(
            os.environ.get("LTI_CONF_FOLDER"), os.environ.get("LTI_CONF_FILE_NAME")
        )
        tool_conf = ToolConfJsonFile(conf_file_location)

    return tool_conf
