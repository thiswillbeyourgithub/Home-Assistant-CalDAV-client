import time
from caldav_tasks_api.caldav_tasks_api import TasksAPI, TaskData

@service
def caldav_add(
    summary: str,
    list_uid: str,
    url: str,
    username: str,
    password: str,
    description: str = "",
    priority: int = 3,
    tags: list[str] = ["HAOS"],
    ssl_verify: bool = False,
    debug: bool = False,
) -> str:
    """yaml
description:
    Create a new CalDAV task.
    Documentation https://github.com/thiswillbeyourgithub/Home-Assistant-CalDAV-client

fields:
    summary:
        description: Task summary/title
        example: "Buy groceries"
        required: true
        selector:
            text:
    description:
        description: Task description
        example: "Important before the wedding"
        required: false
        default: ""
        selector:
            text:
    priority:
        description: Task priority on a 0 to 10 scale
        example: 5
        required: false
        default: 3
        selector:
            number:
                min: 0
                max: 10
    list_uid:
        description: Target task list UID
        example: "groceries"
        required: true
        default: "perso"
        selector:
            text:
    tags:
        description: Task tags. 'HAOS' will always be added automatically.
        example: ["tag1", "tag2"]
        required: false
        default:
            - "HAOS"
        selector:
            text:
                multiple: true
    url:
        description: CalDAV server URL
        example: "https://nextcloud.example.com/remote.php/dav"
        required: true
        selector:
            text:
    username:
        description: CalDAV username
        example: "user@example.com"
        required: true
        selector:
            text:
    password:
        description: CalDAV password
        required: true
        selector:
            text:
                type:
                    password
    ssl_verify:
        description: Crash for SSL errors. Can cause issues with the pyscript environment.
        default: false
        selector:
            bool:
    debug:
        description: Enable debug logging
        default: false
        selector:
            bool:
    """
    if not summary.strip():
        raise ValueError("caldav: missing argument 'summary'")
    if not list_uid.strip():
        raise ValueError("caldav: missing argument 'list_uid'")
    if not url.strip():
        raise ValueError("caldav: missing argument 'url'")
    if not password.strip():
        raise ValueError("caldav: missing argument 'password'")
    if not 0 <= priority <= 10:
        raise ValueError("caldav: invalid argument 'priority'")
    if tags:
        tags = [str(t) for t in tags]  # cast as str

    # make sure we have a haos tag
    if "haos" not in [t.lower() for t in tags]:
        tags.append("HAOS")

    if description:
        task_as_str = f"SUM={summary}' DESC='{description}' LIST_UID='{list_uid}' PRIO='{priority}' USER='{username}'"
    else:
        task_as_str = f"SUM={summary}' LIST_UID='{list_uid}' PRIO='{priority}' USER='{username}'"
    log.info(f"Will create task: '{task_as_str}'")

    # We have to use task.executor otherwise we run into errors because
    # urllib3's calls are blocked because of IO restrictions of HAOS.
    try:
        api = task.executor(
            TasksAPI,
            url=url,
            username=username,
            password=password,
            ssl_verify_cert=ssl_verify,
            debug=debug,
            read_only=False,
            target_lists=[],
        )
    except Exception as e:
        error_msg = f"Error creating TasksAPI instance: '{e}'\nTask was: '{task_as_str}'"
        service.call(
            "persistent_notification",
            "create",
            title="CalDAV Task Failed",
            message=error_msg,
            notification_id=f"caldav_error_{int(time.time())}",
        )
        raise RuntimeError(error_msg) from e

    try:
        task_data=task.executor(
            TaskData,
            summary=summary,
            list_uid=list_uid,
            priority=priority,
            description=description,
            tags=tags,
            x_properties={"CREATOR": "HAOS_CalDAV"},
        )
    except Exception as e:
        error_msg = f"Error creating TaskData object: '{e}'\nTask was: '{task_as_str}'"
        service.call(
            "persistent_notification",
            "create",
            title="CalDAV Task Failed",
            message=error_msg,
            notification_id=f"caldav_error_{int(time.time())}",
        )
        raise RuntimeError(error_msg) from e

    try:
        status = task.executor(
            api.add_task,
            task_data
        )
    except Exception as e:
        error_msg = f"Error TaskData object to the list: '{e}'\nTask was: '{task_as_str}'"
        service.call(
            "persistent_notification",
            "create",
            title="CalDAV Task Failed",
            message=error_msg,
            notification_id=f"caldav_error_{int(time.time())}",
        )
        raise RuntimeError(error_msg) from e

    log.info(f"Created task. Status: '{str(status)}'")
    return status
