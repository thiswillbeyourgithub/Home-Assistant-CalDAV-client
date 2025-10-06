from caldav_tasks_api.caldav_tasks_api import TasksAPI, TaskData

@service
def caldav_add(
    summary: str,
    list_uid: str,
    url: str,
    username: str,
    password: str,
    tags: list[str] = ["HAOS"],
    priority: int = 3,
    description: str = "",
    ssl_verify: bool = True,
    debug: bool = False,
):
    """yaml
description: Create a new CalDAV task.
fields:
    summary:
        description: Task summary/title
        example: "Buy groceries"
        required: true
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
    description:
        description: Task description
        example: "Important before the wedding"
        required: false
        default: ""
        selector:
            text:
    tags:
        description: Task tags
        example: ["tag1", "tag2"]
        required: false
        default: "HAOS"
        selector:
            text:
                multiple: true
    list_uid:
        description: Target task list UID
        example: "groceries"
        required: true
        default: "perso"
        selector:
            text:
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
    debug:
        description: Enable debug logging
        default: false
        selector:
            bool:
    ssl_verify:
        description: Crash for SSL errors
        default: true
        selector:
            bool:
    """
    log.info(f"CaldavTasksAPI: will create task '{summary}' in list '{list_uid}'")
    assert list_uid, "caldav list_uid not specified"

    # We have to use task.executor otherwise we run into errors because
    # urllib3's calls are blocked because of IO restrictions of HAOS.
    try:
        api = task.executor(
            TasksAPI,
            url=url,
            username=username,
            password=password,
            ssl_verify=ssl_verify,
            debug=debug,
            read_only=False,
            target_lists=[],
        )
    except Exception as e:
        log.error(f"Error creating TasksAPI instance: '{e}'")
        raise

    try:
        task_data=TaskData(
            summary=summary,
            list_uid=list_uid,
            priority=priority,
            description=description,
            tags=tags,
            x_properties={"CREATOR": "HAOS_CalDAV"},
        )
    except Exception as e:
        log.error(f"Error creating TaskData object: '{e}'")
        raise

    try:
        status = task.executor(
            api.add_task,
            task_data
        )
    except Exception as e:
        log.error(f"Error TaskData object to the list: '{e}'")
        raise

    log.info(f"Created task. Status: '{str(status)}'")
    return status
